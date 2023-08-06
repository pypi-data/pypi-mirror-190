import json
import os
from datetime import datetime
from urllib.parse import quote_plus

import pystac
import pytz
import requests
from dateutil.parser import parse
from lxml import etree
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

# from pypgstac.migrate import Migrate
from pystac.extensions.datacube import (
    DatacubeExtension,
    DimensionType,
    HorizontalSpatialDimension,
    Variable,
)
from shapely import geometry
from tqdm import tqdm

from . import config_pgstac, constants, funcs

# config_pgstac.run_all()


def xml_processing(catalog):
    """A function for getting out XML details of a catalog URL"""
    catalog_xml = funcs.html2xml(catalog)
    catalog_id = funcs.replacement_func(catalog_xml)
    xml_final = funcs.get_xml(catalog_xml)
    return catalog_xml, catalog_id, xml_final


class Converter(object):
    def __init__(
        self,
        main_url,  # TDS Catalog url for harvesting
        stac=None,  # Permitting creation of STAC catalogs
        stac_dir=None,  # Directory saving of created STAC catalogs
        stac_id=None,  # STAC catalog ID
        stac_description=None,  # STAC catalog description
        web_service="iso",  # Choosing the web service between 'iso' and 'ncml' to begin harvesting
        datetime_filter=None,  # Filter harvesting dataset according to modified date in TDS
        stac_catalog_dynamic=None,  # Choosing STAC catalog type between Static and Dynamic
    ):
        self.scanned = []  # to skip scanned data in main function
        self.scanned_summary = (
            []
        )  # to skip scanned data in 'datasets_summary' function
        self.catalog = dict()  # Main STAC catalog for
        self.datetime_after = None
        self.datetime_before = None
        self.data_num_all = 0  # A counter of data in the whole catalog url
        self.branch_num_all = (
            0  # A counter of datasets in the whole catalog url
        )
        self.data_num = 0  # A counter of data in a dataset
        self.branch_num = 0  # A counter of data in a dataset
        self.final_msg = "STAC Catalog has been created!"

        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of catalog.

        xml_url, id, xml = xml_processing(main_url)

        print("Start Scanning datasets of %s" % xml_url)

        # This function displays a summary of datasets that are going to harvest
        Scanning = list(self.datasets_summary(xml_url, xml))

        # Writing description in the first step of scanning
        print(str(self.data_num_all), "data are going to be set as items")
        print(
            str(self.branch_num_all),
            "datasets are going to be set as collction",
        )

        if datetime_filter is not None:
            """Skip TDS datasets out of 'datetime_filter' according
            to 'modified' parameter in TDS"""

            if datetime_filter[0] is not None:
                datetime_after = datetime.strptime(
                    datetime_filter[0], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if not isinstance(datetime_after, datetime):
                    raise ValueError(
                        "'datetime_after' parameter have to be a datatime object"
                    )
                else:
                    if datetime_after.tzinfo:
                        datetime_after = datetime_after.astimezone(pytz.utc)
                    else:
                        datetime_after = datetime_after.replace(
                            tzinfo=pytz.utc
                        )
                self.datetime_after = datetime_after

            if datetime_filter[1] is not None:
                datetime_before = datetime.strptime(
                    datetime_filter[1], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if not isinstance(datetime_before, datetime):
                    raise ValueError(
                        "'datetime_before' parameter have to be a datatime object"
                    )
                else:
                    if datetime_before.tzinfo:
                        datetime_before = datetime_before.astimezone(pytz.utc)
                    else:
                        datetime_before = datetime_before.replace(
                            tzinfo=pytz.utc
                        )
                self.datetime_before = datetime_before

        if stac is not False:
            """In this part STAC catalogs will be created"""

            # Main STAC catalog for linking other items and collections
            self.catalog[id] = pystac.Catalog(
                id=id,
                description="[Link to TDS](" + funcs.xml2html(xml_url) + ")",
            )

            urls = list(self.datasets_harvester(xml_url, web_service, xml))
            if len(urls) != 0:
                self.catalog[id].normalize_hrefs(
                    os.path.join(stac_dir, "stac")
                )
                self.catalog[id].save(
                    catalog_type=pystac.CatalogType.SELF_CONTAINED
                )
                print(self.final_msg)
            else:
                print(
                    "tag_elemrning: "
                    + web_service
                    + " is not in the list of sevices of dataset"
                )

        if stac_catalog_dynamic is not False:
            """With enabling 'stac_catalog_dynamic' STAC catalogs
            , collections and items ingest into the 'pgSTAC'"""

            config_pgstac.run_all()  # This enables the confiduration of pgSTAC
            # First of all catalog should be opened
            f = open(os.path.join(stac_dir, "stac/catalog.json"))
            catalog_json = json.load(f)
            # pgSTAC database will be loaded here
            loader = Loader(db=PgstacDB(dsn=""))
            # Each collection and item that are linked to the catalog through 'links' is extracted.
            for dc in catalog_json["links"]:
                if dc["rel"] == "item":
                    try:
                        loader.load_items(
                            str(
                                os.path.join(
                                    stac_dir,
                                    "stac/" + dc["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                    except:
                        continue
                    print("|____", dc["href"])
                # 'child' means Collection in Catalog json file
                if dc["rel"] == "child":
                    self.dynamic_ingester(
                        loader,
                        dc["href"],
                        stac_dir,
                        "stac/" + dc["href"].replace("./", ""),
                    )

    def dynamic_ingester(self, loaderx, param, stac_dirx, address_coll):
        """This is a function for ingesting collections
        into pgSTAC specifically for nested datasets"""

        f = open(os.path.join(stac_dirx, address_coll))
        collection_josn_path = os.path.join(stac_dirx, address_coll)
        collection_josn_data = json.load(f)

        item_collection_list = [
            ci["rel"] for ci in collection_josn_data["links"]
        ]

        if (
            "child" in item_collection_list
        ):  # To ensure collection exists in 'links'
            item_collection_list = []  # Considered empty to prevent recursion

            for ci in collection_josn_data["links"]:
                if ci["rel"] == "child":
                    try:
                        self.dynamic_ingester(
                            loaderx,
                            ci["href"],
                            stac_dirx,
                            collection_josn_path.replace(
                                "collection.json", "/"
                            )
                            + ci["href"].replace("./", ""),
                        )
                    except:
                        continue
        else:
            item_collection_list = []  # Considered empty to prevent recursion
            loaderx.load_collections(
                str(os.path.join(stac_dirx, collection_josn_path)),
                Methods.insert,
            )
            print(param)
            for ci in collection_josn_data["links"]:
                if ci["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_josn_path.replace(
                                        "collection.json", "/"
                                    )
                                    + ci["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                        print("|____", ci["href"])
                    except:
                        continue

    def datasets_harvester(self, url, web_service, xml_content):
        """This is the main function to create the STAC catalog, collections,
        and items and also is for linking them to each other"""

        footprint_temp = None  # Define initial bounding box
        footprint_temp_point = None  # Define initial point
        collection_interval_time = (
            []
        )  # An array for collecting all items datetime

        if url in self.scanned:
            print("Already Scanned %s " % url)
            return
        self.scanned.append(url)

        url, catalog_colleciton_id, xml = xml_processing(url)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return
        # Finding datasets and consider each of them as a collection
        branches_main = []
        for br in tree.findall(".//{%s}catalogRef" % constants.unidata):
            branches_main.append(
                funcs.references_urls(url, br.get("{%s}href" % constants.w3))
            )
            collection_id = funcs.replacement_func(
                funcs.references_urls(url, br.get("{%s}href" % constants.w3))
            )
            # creation of collection
            self.catalog[collection_id] = pystac.Collection(
                id=collection_id,
                extent=pystac.Extent(spatial=None, temporal=None),
                description="[Link to TDS](" + funcs.xml2html(url) + ")",
            )
            # self.catalog_all.add_child(self.catalog[convert_xml_x])
            self.catalog[catalog_colleciton_id].add_child(
                self.catalog[collection_id]
            )
        # Finding all data in datasets to create item
        data_main = []
        for e in branches_main:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")
            except BaseException:
                continue
            data_main.append(content)
        # This condition displays a summary of dataset that is harvesting
        if branches_main == []:
            self.data_num = self.data_num + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            self.branch_num = self.branch_num + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )
        # A loop through the nested datasets
        for i, d in enumerate(data_main):
            for dataset in self.datasets_harvester(
                branches_main[i], web_service, d
            ):
                yield dataset

        # This displays status of harvesting datasets and data
        print("Start processing: ", url)
        print(
            self.branch_num,
            "/",
            self.branch_num_all,
            "STAC catalogs are created",
        )
        print(
            self.data_num,
            "/",
            self.data_num_all,
            "STAC items are connected to the related catalog",
        )

        # A loop through data in a dataset to create items
        for elem in tqdm(
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata),
            colour="red",
        ):
            # Defining variables in TDS catalog and webservices as an empty parameter
            self.services = []
            self.id = None
            self.name = None
            self.catalog_url = None
            self.extracted_date = None
            variables = {}
            dimensions = {}
            var = []
            dim = []
            keyword = []
            aName = []
            descriptor = []
            dimensionName = []
            resolution = []

            data_get = requests.get(
                str(url) + "?dataset=" + str(elem.get("ID")),
                None,
                verify=False,
            )
            try:
                tree_data = etree.XML(data_get.text.encode("utf-8"))
            except etree.XMLSyntaxError:
                continue
            else:
                try:
                    # It serves as a function to skip data based on datetime
                    extracted_date = elem.find(
                        './/{%s}date[@type="modified"]' % constants.unidata
                    )
                    if extracted_date is not None:
                        try:
                            self.extracted_date = extracted_date.text
                            dt = parse(extracted_date.text)
                            comp_dt = dt.replace(tzinfo=pytz.utc)
                        except ValueError:
                            continue
                        else:
                            dt = dt.replace(tzinfo=pytz.utc)
                            if (
                                self.datetime_after
                                and dt < self.datetime_after
                            ):
                                continue
                            if (
                                self.datetime_before
                                and dt > self.datetime_before
                            ):
                                continue

                    dataset = tree_data.find("{%s}dataset" % constants.unidata)
                    self.id = dataset.get("ID")
                    self.name = dataset.get("name")
                    metadata = dataset.find("{%s}metadata" % constants.unidata)
                    self.catalog_url = url.split("?")[0]

                    # Services
                    service_tag = dataset.find(
                        "{%s}serviceName" % constants.unidata
                    )
                    if service_tag is None:
                        if metadata is not None:
                            service_tag = metadata.find(
                                "{%s}serviceName" % constants.unidata
                            )

                    if service_tag is None:
                        # Use services found in the file. FMRC aggs do this.
                        services = tree_data.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                    else:
                        # Use specific named services
                        services = tree_data.findall(
                            ".//{%s}service[@name='%s']"
                            % (constants.unidata, service_tag.text)
                        )

                    for i, service in enumerate(services):
                        # In TDS version 4 and 5 'Compound' is different
                        if (
                            service.get("serviceType") == "Compound"
                            or service.get("serviceType") == "compound"
                        ):
                            for s in service.findall(
                                "{%s}service" % constants.unidata
                            ):
                                service_url = funcs.references_urls(
                                    url, s.get("base")
                                ) + dataset.get("urlPath")
                                if s.get("suffix") is not None:
                                    service_url += s.get("suffix")
                                if s.get("name") in ["iso", "ncml", "uddc"]:
                                    service_url += (
                                        "?dataset=%s&&catalog=%s"
                                        % (
                                            self.id,
                                            quote_plus(self.catalog_url),
                                        )
                                    )
                                if web_service in service_url:
                                    service_url_html = (
                                        funcs.xml2html(url)
                                        + "?dataset="
                                        + dataset.get("ID")
                                    )
                                    root = etree.parse(service_url).getroot()
                                    # It just harvests 'iso' webservice of data
                                    if web_service == "iso":
                                        for tags in root.iter():
                                            # Getting geogrophical information of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}westBoundLongitude"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    westBoundLongitude = (
                                                        tag_elem.text
                                                    )
                                            if (
                                                tags.tag
                                                == "{%s}eastBoundLongitude"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    eastBoundLongitude = (
                                                        tag_elem.text
                                                    )
                                            if (
                                                tags.tag
                                                == "{%s}southBoundLatitude"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    southBoundLatitude = (
                                                        tag_elem.text
                                                    )
                                            if (
                                                tags.tag
                                                == "{%s}northBoundLatitude"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    northBoundLatitude = (
                                                        tag_elem.text
                                                    )
                                            # Getting 'keywords' gmd parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}keyword"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    if (
                                                        tag_elem.text
                                                        in constants.allowed_list
                                                    ):
                                                        keyword.append(
                                                            tag_elem.text
                                                        )
                                            # Getting 'aName' gco parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}aName"
                                                % constants.iso_gco
                                            ):
                                                for tag_elem in tags:
                                                    if (
                                                        tag_elem.text
                                                        not in constants.avoided_formats
                                                    ):
                                                        aName.append(
                                                            tag_elem.text
                                                        )
                                            # Getting 'descriptor' gmd parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}descriptor"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    descriptor.append(
                                                        tag_elem.text
                                                    )
                                            # Getting 'dimensionName' gmd parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}dimensionName"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    dimensionName.append(
                                                        tag_elem.text
                                                    )
                                            # Getting 'resolution' gmd parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}resolution"
                                                % constants.iso_gmd
                                            ):
                                                for tag_elem in tags:
                                                    resolution.append(
                                                        tag_elem.text
                                                    )
                                            # Getting 'beginPosition' gml parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}beginPosition"
                                                % constants.iso_gml
                                            ):
                                                beginPosition = tags.text
                                            # Getting 'endPosition' gml parameters of iso webservice
                                            if (
                                                tags.tag
                                                == "{%s}endPosition"
                                                % constants.iso_gml
                                            ):
                                                endPosition = tags.text
                                    # It just harvests 'ncml' webservice of data
                                    elif web_service == "ncml":
                                        for tags in root.iter():
                                            # Getting geogrophical information of ncml webservice
                                            if (
                                                tags.attrib.get("name")
                                                == "geospatial_lon_min"
                                            ):
                                                westBoundLongitude = (
                                                    tags.attrib.get("value")
                                                )
                                            if (
                                                tags.attrib.get("name")
                                                == "geospatial_lon_max"
                                            ):
                                                eastBoundLongitude = (
                                                    tags.attrib.get("value")
                                                )
                                            if (
                                                tags.attrib.get("name")
                                                == "geospatial_lat_min"
                                            ):
                                                southBoundLatitude = (
                                                    tags.attrib.get("value")
                                                )
                                            if (
                                                tags.attrib.get("name")
                                                == "geospatial_lat_max"
                                            ):
                                                northBoundLatitude = (
                                                    tags.attrib.get("value")
                                                )
                                            # Getting 'time_coverage_start' parameter from ncml webservice
                                            if (
                                                tags.attrib.get("name")
                                                == "time_coverage_start"
                                            ):
                                                beginPosition = (
                                                    tags.attrib.get("value")
                                                )
                                            # Getting 'time_coverage_end' parameter from ncml webservice
                                            if (
                                                tags.attrib.get("name")
                                                == "time_coverage_end"
                                            ):
                                                endPosition = tags.attrib.get(
                                                    "value"
                                                )
                                        # Getting 'dimension' parameter from ncml webservice
                                        for r in root:
                                            if (
                                                r.tag
                                                == "{%s}dimension"
                                                % constants.ncml
                                            ):
                                                if (
                                                    r.get("name")
                                                    not in constants.avoided_list
                                                ):
                                                    dimensionName.append(
                                                        r.get("name")
                                                    )
                                        # Getting 'variable' parameter from ncml webservice
                                        for r in root:
                                            if (
                                                r.tag
                                                == "{%s}variable"
                                                % constants.ncml
                                            ):
                                                if (
                                                    r.get("name")
                                                    not in constants.avoided_list
                                                ):
                                                    aName.append(r.get("name"))
                                        # Getting 'standard_name' parameter from ncml webservice
                                        for r in root:
                                            if (
                                                r.tag
                                                == "{%s}variable"
                                                % constants.ncml
                                            ):
                                                array = [
                                                    w.get("name") for w in r
                                                ]
                                                for w in r:
                                                    if (
                                                        w.get("name")
                                                        == "standard_name"
                                                    ):
                                                        descriptor.append(
                                                            w.get("value")
                                                        )
                                                    elif (
                                                        w.get("name")
                                                        == "long_name"
                                                        and "standard_name"
                                                        not in array
                                                    ):
                                                        descriptor.append(
                                                            w.get("value")
                                                        )
                                        # Cause both of dimensionName and keyword are same in ncml webservice
                                        keyword = dimensionName

                                    else:
                                        self.final_msg = (
                                            "Activate "
                                            + web_service
                                            + " service in the requested catalog"
                                        )
                                        continue
                        # A condition for longitudes more than 180 e.g. 360 degree. Cause STAC doesn't support longs
                        # more than 180
                        if (
                            float(westBoundLongitude) > 180
                            or float(eastBoundLongitude) > 180
                        ):
                            westBoundLongitude = str(
                                float(westBoundLongitude) - 180
                            )
                            eastBoundLongitude = str(
                                float(eastBoundLongitude) - 180
                            )
                        # A criterion for point or bounding box geogrophical coordination in item creation
                        if (
                            westBoundLongitude == eastBoundLongitude
                            or northBoundLatitude == southBoundLatitude
                        ):
                            boundingBox = [
                                westBoundLongitude,
                                northBoundLatitude,
                            ]
                            bbox_x = list(map(float, boundingBox))
                            footprint = geometry.Point(
                                float(westBoundLongitude),
                                float(northBoundLatitude),
                            )

                            if footprint_temp_point is None:
                                footprint_temp_point = footprint
                            footprint_temp_point = geometry.shape(
                                footprint
                            ).union(geometry.shape(footprint_temp_point))

                            collection_bbox = list(footprint_temp_point.bounds)

                        else:
                            boundingBox = [
                                westBoundLongitude,
                                southBoundLatitude,
                                eastBoundLongitude,
                                northBoundLatitude,
                            ]
                            bbox_x = list(map(float, boundingBox))
                            footprint = geometry.Polygon(
                                [
                                    [bbox_x[0], bbox_x[1]],
                                    [bbox_x[0], bbox_x[3]],
                                    [bbox_x[2], bbox_x[3]],
                                    [bbox_x[2], bbox_x[1]],
                                ]
                            )
                            if footprint_temp is None:
                                footprint_temp = footprint
                            footprint_temp = geometry.shape(footprint).union(
                                geometry.shape(footprint_temp)
                            )
                            collection_bbox = list(footprint_temp.bounds)

                        # Append date of items to an array to create Temporalextend for collections
                        collection_interval_time.append(
                            datetime.strptime(
                                beginPosition, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
                        collection_interval_time.append(
                            datetime.strptime(
                                endPosition, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
                        collection_interval_time = sorted(
                            collection_interval_time
                        )
                        collection_interval_final_time = [
                            collection_interval_time[0],
                            collection_interval_time[-1],
                        ]
                        # Item creation
                        item = pystac.Item(
                            id=funcs.replacement_func(elem.get("ID")),
                            geometry=geometry.mapping(footprint),
                            bbox=bbox_x,
                            datetime=comp_dt,
                            properties={},
                        )
                        # Add auxiliary information to items
                        item.common_metadata.start_datetime = (
                            datetime.strptime(
                                beginPosition, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
                        item.common_metadata.end_datetime = datetime.strptime(
                            endPosition, "%Y-%m-%dT%H:%M:%SZ"
                        ).replace(tzinfo=pytz.utc)
                        item.common_metadata.description = (
                            "[Link to the data in TDS]("
                            + service_url_html
                            + ")"
                        )

                        # Adding web services as assets into items
                        for service in services:
                            if (
                                service.get("serviceType") == "Compound"
                                or service.get("serviceType") == "compound"
                            ):
                                for s in service.findall(
                                    "{%s}service" % constants.unidata
                                ):
                                    service_url = funcs.references_urls(
                                        url, s.get("base")
                                    ) + dataset.get("urlPath")
                                    if s.get("suffix") is not None:
                                        service_url += s.get("suffix")
                                    if s.get("name") in [
                                        "iso",
                                        "ncml",
                                        "uddc",
                                    ]:
                                        service_url += (
                                            "?dataset=%s&&catalog=%s"
                                            % (
                                                self.id,
                                                quote_plus(self.catalog_url),
                                            )
                                        )
                                    if s.get("name") in ["odap"]:
                                        service_url += ".html"
                                    # Determinatio of Media Type
                                    if s.get("name") in [
                                        "iso",
                                        "ncml",
                                        "wms",
                                        "wcs",
                                        "wfs",
                                        "sos",
                                    ]:
                                        media_type_ = pystac.MediaType.XML
                                    elif s.get("name") in ["http"]:
                                        media_type_ = "application/netcdf"
                                    elif s.get("name") in [
                                        "dap4",
                                        "odap",
                                        "uddc",
                                    ]:
                                        media_type_ = pystac.MediaType.HTML
                                    else:
                                        media_type_ = pystac.MediaType.TEXT

                                    item.add_asset(
                                        key=s.get("name"),
                                        asset=pystac.Asset(
                                            href=service_url,
                                            # title=without_slash,
                                            media_type=media_type_,
                                        ),
                                    )
                        # applying datacube extension to items
                        cube = DatacubeExtension.ext(item, add_if_missing=True)
                        # Creating dimension and varibles to datacube extension
                        for i, v in enumerate(aName):
                            var.append(
                                Variable(
                                    dict(
                                        type="data",
                                        description=descriptor[i],
                                        dimensions=keyword,
                                    )
                                )
                            )

                        for i, v in enumerate(aName):
                            if aName[i] not in constants.allowed_list:
                                variables[v] = var[i]

                        for i, v in enumerate(dimensionName):
                            if (
                                dimensionName[i] == "row"
                                or dimensionName[i] == "lon"
                            ):
                                extend_ = [
                                    westBoundLongitude,
                                    eastBoundLongitude,
                                ]
                                type_ = DimensionType.SPATIAL.value
                                description_ = "longitude"
                                axis_ = "x"
                            elif (
                                dimensionName[i] == "column"
                                or dimensionName[i] == "lat"
                            ):
                                extend_ = [
                                    southBoundLatitude,
                                    northBoundLatitude,
                                ]
                                type_ = DimensionType.SPATIAL.value
                                description_ = "latitude"
                                axis_ = "y"
                            elif (
                                dimensionName[i] == "temporal"
                                or dimensionName[i] == "time"
                            ):
                                extend_ = [beginPosition, endPosition]
                                type_ = DimensionType.TEMPORAL.value
                                description_ = "time"
                                axis_ = "time"

                            dim.append(
                                HorizontalSpatialDimension(
                                    properties=dict(
                                        axis=axis_,
                                        extent=extend_,
                                        description=description_,
                                        reference_system="epsg:4326",
                                        type=type_,
                                    )
                                )
                            )
                        for i, v in enumerate(dimensionName):
                            dimensions[v] = dim[i]
                        cube.apply(dimensions=dimensions, variables=variables)
                        # Because Collection does not provide point coordination, this condition was applied.
                        if (
                            collection_bbox[0] == collection_bbox[2]
                            or collection_bbox[1] == collection_bbox[3]
                        ):
                            collection_bbox = [
                                collection_bbox[0] - constants.epilon,
                                collection_bbox[1] - constants.epilon,
                                collection_bbox[2] + constants.epilon,
                                collection_bbox[3] + constants.epilon,
                            ]

                        spatial_extent = pystac.SpatialExtent(
                            bboxes=[collection_bbox]
                        )
                        temporal_extent = pystac.TemporalExtent(
                            intervals=[collection_interval_final_time]
                        )
                        # An empty condition for either Temporal or Spatial extent
                        if (
                            collection_bbox is None
                            or collection_interval_final_time is None
                        ):
                            spatial_extent = pystac.SpatialExtent(
                                bboxes=[(0, 0)]
                            )
                            temporal_extent = pystac.TemporalExtent(
                                intervals=[
                                    [datetime.utcnow(), datetime.utcnow()]
                                ]
                            )
                        collection_item_id = funcs.replacement_func(url)
                        self.catalog[
                            collection_item_id
                        ].extent = pystac.Extent(
                            spatial=spatial_extent, temporal=temporal_extent
                        )
                        self.catalog[collection_item_id].add_item(item)
                except BaseException as e:
                    print(e)
                    continue

            yield str(url) + "?dataset=" + str(elem.get("ID"))
        # When a collection doesn't have Spatial or Temporal extent
        if (
            type(self.catalog[catalog_colleciton_id])
            is pystac.collection.Collection
            and self.catalog[catalog_colleciton_id].extent.spatial is None
        ):
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for elements in list(
                self.catalog[catalog_colleciton_id].get_children()
            ):
                if elements.extent.spatial is not None:
                    self.catalog[
                        catalog_colleciton_id
                    ].extent = elements.extent
                else:
                    self.catalog[catalog_colleciton_id].extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )
            if (
                len(list(self.catalog[catalog_colleciton_id].get_children()))
                == 0
            ):
                self.catalog[catalog_colleciton_id].extent = pystac.Extent(
                    spatial=spatial_extent, temporal=temporal_extent
                )
        if type(self.catalog[catalog_colleciton_id]) is pystac.catalog.Catalog:
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for i in list(self.catalog[catalog_colleciton_id].get_children()):
                if (
                    type(i) is pystac.collection.Collection
                    and i.extent.spatial is None
                ):
                    i.extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )

    def datasets_summary(self, url, xml_content):
        if url in self.scanned_summary:
            print("Already Scanned %s " % url)
            return
        self.scanned_summary.append(url)

        url = funcs.html2xml(url)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return

        branches = []

        for br in tree.findall(".//{%s}catalogRef" % constants.unidata):
            branches.append(
                funcs.references_urls(url, br.get("{%s}href" % constants.w3))
            )

        data = []
        for e in branches:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")
            except BaseException:
                print("INFO: Skipping %s (error parsing the XML)" % url)
            data.append(content)

        if branches == []:
            print(
                "|_______",
                url,
                "|  Number of data: ",
                len(
                    tree.findall(
                        ".//{%s}dataset[@urlPath]" % constants.unidata
                    )
                ),
            )
            self.data_num_all = self.data_num_all + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            print(
                "|__",
                url,
                "|  Number of branches: ",
                len(tree.findall(".//{%s}catalogRef" % constants.unidata)),
            )
            self.branch_num_all = self.branch_num_all + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )

        for i, d in enumerate(data):
            for dataset in self.datasets_summary(branches[i], d):
                yield dataset

        for elem in tree.findall(
            ".//{%s}dataset[@urlPath]" % constants.unidata
        ):
            yield str(url) + "?dataset=" + str(elem.get("ID"))
