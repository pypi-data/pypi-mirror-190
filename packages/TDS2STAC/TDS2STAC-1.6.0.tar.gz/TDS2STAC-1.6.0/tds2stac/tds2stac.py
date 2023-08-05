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
from pypgstac.load import Loader, Methods, Tables
from pypgstac.migrate import Migrate
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


class Converter(object):
    def __init__(
        self,
        main_url,
        stac=None,
        stac_dir=None,
        stac_id=None,
        stac_description=None,
        web_service="iso",
        datetime_filter=None,
        stac_catalog_type="static",
    ):
        self.scanned = []
        self.catalog = dict()
        self.catalog_names = []
        self.catalog_id = []
        self.data_num = 0
        self.branch_num = 0

        self.final_msg = "STAC Catalog has been created!"

        if (
            datetime_filter[0] is not None
        ):  # 2020-02-20T00:00:00.000Z datetime.strptime(datetime_filter[0], '%Y-%m-%dT%H:%M:%S.%f')
            datetime_after = datetime.strptime(
                datetime_filter[0], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if not isinstance(datetime_after, datetime):
                raise ValueError(
                    "'after' parameter should be a datetime object"
                )
            else:
                if datetime_after.tzinfo:
                    datetime_after = datetime_after.astimezone(pytz.utc)
                else:
                    datetime_after = datetime_after.replace(tzinfo=pytz.utc)
            self.after = datetime_after

        # Only return datasets with a modified date greater or equal to this
        if datetime_filter[1] is not None:
            datetime_before = datetime.strptime(
                datetime_filter[1], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if not isinstance(datetime_before, datetime):
                raise ValueError(
                    "'before' parameter should be a datetime object"
                )
            else:
                if datetime_before.tzinfo:
                    datetime_before = datetime_before.astimezone(pytz.utc)
                else:
                    datetime_before = datetime_before.replace(tzinfo=pytz.utc)
            self.before = datetime_before

        url_cat = funcs.html2xml(main_url)
        convert_xml_o = funcs.replacement_func(url_cat)
        xml = funcs.get_xml(url_cat)

        print("Start Scanning datasets of %s" % url_cat)
        Scanning = list(self.dataset_status(url_cat, xml))

        self.catalog[convert_xml_o] = pystac.Catalog(
            id=convert_xml_o,
            description="[Link to TDS](" + funcs.xml2html(url_cat) + ")",
        )
        self.catalog_id.append(self.catalog[convert_xml_o].id)
        # print(self.catalog_id)
        self.catalog_all = pystac.Collection(
            id="all",
            extent=pystac.Extent(spatial=None, temporal=None),
            description="all",
        )
        self.catalog_all.add_child(self.catalog[convert_xml_o])

        print(str(self.data_num), "data are going to be set as items")
        print(
            str(self.branch_num), "datasets are going to be set as collction"
        )
        self.scanned = []

        self.data_num1 = 0
        self.branch_num1 = 0
        if stac is not False:
            self.catalog_main = pystac.Catalog(
                id=stac_id, description=stac_description
            )
            urls = list(self.dataset_url_finder(url_cat, web_service, xml))
            # print(urls)
            if len(urls) != 0:
                children = list(self.catalog[convert_xml_o].get_children())
                # print(list(self.catalog[convert_xml_o].get_items()))
                print(children)
                self.catalog[convert_xml_o].normalize_hrefs(
                    os.path.join(stac_dir, "stac")
                )
                self.catalog[convert_xml_o].save(
                    catalog_type=pystac.CatalogType.SELF_CONTAINED
                )
                print(self.final_msg)
            else:
                print(
                    "Warning: "
                    + web_service
                    + " is not in the list of sevices of dataset"
                )

        if stac_catalog_type != "static":
            f = open(os.path.join(stac_dir, "stac/catalog.json"))
            data_collection_1 = json.load(f)
            # print(data["links"])
            loader = Loader(db=PgstacDB(dsn=""))
            for dc in data_collection_1["links"]:
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
                if dc["rel"] == "child":
                    aaaa = self.nested_fun(
                        loader,
                        dc["href"],
                        stac_dir,
                        "stac/" + dc["href"].replace("./", ""),
                    )
                    # print(dc["href"])
                    # f = open(os.path.join(stac_dir, "stac/" + dc["href"].replace("./", "")))

                    # collection_address_1 = os.path.join(stac_dir, "stac/" + dc["href"].replace("./", ""))
                    # loader.load_collections(str(os.path.join(stac_dir, "stac/" + dc["href"].replace("./", ""))), Methods.insert)

                    # data_collection_item_1 = json.load(f)
                    # for dci1 in data_collection_item_1["links"]:
                    #     if dci1["rel"] == "child":
                    #         print(dci1["href"])
                    #         f = open(os.path.join(stac_dir, collection_address_1.replace("collection.json", "/")) + dci1["href"].replace("./", ""))
                    #         try:
                    #             collection_address_2 = os.path.join(stac_dir, collection_address_1.replace("collection.json", "/") + dci1["href"].replace("./", ""))
                    #             loader.load_collections(str(os.path.join(stac_dir, collection_address_1.replace("collection.json", "/") + dci1["href"].replace("./", ""))), Methods.insert)
                    #         except:
                    #             pass
                    #         data_collection_item_2 = json.load(f)
                    #         for dci2 in data_collection_item_2["links"]:
                    #             if dci2["rel"] == "item":
                    #                 try:

                    #                     loader.load_items(str(os.path.join(stac_dir, collection_address_2.replace("collection.json", "/") + dci2["href"].replace("./", ""))), Methods.insert)
                    #                 except:
                    #                     continue
                    #                 print("|____", dci2["href"])
                    #     if dci1["rel"] == "item":
                    #         try:

                    #             loader.load_items(str(os.path.join(stac_dir, collection_address_1.replace("collection.json", "/") + dci1["href"].replace("./", ""))), Methods.insert)
                    #         except:
                    #             continue
                    #         print("|____", dc["href"])

            # Loader.load_collections(str(TEST_COLLECTIONS_JSON),insert_mode=Methods.insert,)

    def nested_fun(self, loaderx, param, stac_dirx, address_coll):
        f = open(os.path.join(stac_dirx, address_coll))

        collection_address_1 = os.path.join(stac_dirx, address_coll)

        data_collection_item_1 = json.load(f)

        l = [dci1["rel"] for dci1 in data_collection_item_1["links"]]
        if "child" in l:
            l = []

            for dci1 in data_collection_item_1["links"]:
                if dci1["rel"] == "child":
                    try:
                        self.nested_fun(
                            loaderx,
                            dci1["href"],
                            stac_dirx,
                            collection_address_1.replace(
                                "collection.json", "/"
                            )
                            + dci1["href"].replace("./", ""),
                        )
                    except:
                        continue
        else:
            l = []

            loaderx.load_collections(
                str(os.path.join(stac_dirx, collection_address_1)),
                Methods.insert,
            )
            print(param)
            for dci1 in data_collection_item_1["links"]:
                if dci1["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_address_1.replace(
                                        "collection.json", "/"
                                    )
                                    + dci1["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                        print("|____", dci1["href"])
                    except:
                        continue
                        # print("|____", dc["href"])

    def dataset_url_finder(self, url, web_service, xml_content):
        if url in self.scanned:
            print("Already Scanned %s " % url)
            return
        self.scanned.append(url)

        convert_xml = funcs.replacement_func(url)

        for el in list(self.catalog_all.get_children()):
            self.catalog_id.append(el.id)
        if convert_xml not in self.catalog_id:
            self.catalog[convert_xml] = pystac.Collection(
                id=convert_xml,
                extent=pystac.Extent(spatial=None, temporal=None),
                description="[Link to TDS](" + funcs.xml2html(url) + ")",
            )
        self.catalog_all.add_child(self.catalog[convert_xml])
        self.catalog_names.append(convert_xml)

        url = funcs.html2xml(url)

        try:
            tree = etree.XML(xml_content)
        except BaseException:
            return

        branches_main = []
        for br in tree.findall(".//{%s}catalogRef" % constants.unidata):
            branches_main.append(
                funcs.references_urls(url, br.get("{%s}href" % constants.w3))
            )
            convert_xml_x = funcs.replacement_func(
                funcs.references_urls(url, br.get("{%s}href" % constants.w3))
            )

            self.catalog[convert_xml_x] = pystac.Collection(
                id=convert_xml_x,
                extent=pystac.Extent(spatial=None, temporal=None),
                description="[Link to TDS](" + funcs.xml2html(url) + ")",
            )
            self.catalog_all.add_child(self.catalog[convert_xml_x])
            self.catalog[convert_xml].add_child(self.catalog[convert_xml_x])

        data_main = []
        for e in branches_main:
            try:
                url_stat = requests.get(e, None, verify=False)
                content = url_stat.text.encode("utf-8")
            except BaseException:
                continue
            data_main.append(content)

        if branches_main == []:
            self.data_num1 = self.data_num1 + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            self.branch_num1 = self.branch_num1 + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )

        for i, d in enumerate(data_main):
            # print(i)
            for dataset in self.dataset_url_finder(
                branches_main[i], web_service, d
            ):
                yield dataset

        print("Start processing: ", url)
        print(
            self.branch_num1, "/", self.branch_num, "STAC catalogs are created"
        )
        print(
            self.data_num1,
            "/",
            self.data_num,
            "STAC items are connected to the related catalog",
        )
        # footprint_temp = geometry.Polygon(
        #     [
        #         [0, 0],
        #         [0, 0],
        #         [0, 0],
        #         [0, 0],
        #     ]
        # )
        # footprint_temp_point = geometry.Point(0,0)
        footprint_temp = None
        footprint_temp_point = None
        collection_interval = []

        if (
            len(tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata))
            == 0
        ):
            # print(convert_xml_x)
            # print(list(self.catalog[convert_xml_x].get_children()))
            for elements in list(self.catalog[convert_xml].get_children()):
                self.catalog[convert_xml].extent = elements.extent

                # print(elements.extent)

        # if url == "http://172.27.80.119:8088/thredds/catalog/regclim/raster/global/chirps/climatology/catalog.xml":
        #     print(tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata))
        #     print(convert_xml_x)
        #     print(convert_xml)
        #     print(list(self.catalog_all.get_children()))
        #     print(list(self.catalog[convert_xml_x].get_children()))
        #     print(list(self.catalog[convert_xml].get_children()))
        for elem in tqdm(
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata),
            colour="red",
        ):
            gid = elem.get("ID")
            self.services = []
            self.id = None
            self.name = None
            self.catalog_url = None
            self.date_ = None
            variables = {}
            dimensions = {}
            var = []
            dim = []
            keyword = []
            aName = []
            descriptor = []
            dimensionName = []
            resolution = []

            const_list = [
                "time",
                "lat",
                "latitude",
                "lon",
                "longitude",
                "long",
                "time_bnds",
                "bnds",
            ]
            const_list2 = ["time_bnds", "bnds", "ens"]
            data_format = [
                "float",
                "double",
                "int",
                "time_bnds",
                "bnds",
                "ens",
                "String",
            ]
            r = requests.get(
                str(url) + "?dataset=" + str(gid), None, verify=False
            )
            try:
                tree_x = etree.XML(r.text.encode("utf-8"))

            except etree.XMLSyntaxError:
                continue
            else:
                try:
                    date_tag = elem.find(
                        './/{%s}date[@type="modified"]' % constants.unidata
                    )
                    if date_tag is not None:
                        try:
                            dt = parse(date_tag.text)
                        except ValueError:
                            continue
                        else:
                            dt = dt.replace(tzinfo=pytz.utc)
                        if self.after and dt < self.after:
                            continue
                        if self.before and dt > self.before:
                            continue

                    dataset = tree_x.find("{%s}dataset" % constants.unidata)
                    self.id = dataset.get("ID")
                    self.name = dataset.get("name")
                    metadata = dataset.find("{%s}metadata" % constants.unidata)
                    self.catalog_url = url.split("?")[0]

                    date_ = dataset.find(
                        './/{%s}date[@type="modified"]' % constants.unidata
                    )
                    if date_ is not None:
                        try:
                            dt = date_.text
                            comp_dt = parse(date_.text)
                            comp_dt = comp_dt.replace(tzinfo=pytz.utc)
                            self.date_ = dt

                        except ValueError:
                            continue
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
                        services = tree_x.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                    else:
                        # Use specific named services
                        services = tree_x.findall(
                            ".//{%s}service[@name='%s']"
                            % (constants.unidata, service_tag.text)
                        )

                    for i, service in enumerate(services):
                        if (
                            service.get("serviceType") == "Compound"
                            or service.get("serviceType") == "compound"
                        ):
                            # web_services_arr = []
                            for s in service.findall(
                                "{%s}service" % constants.unidata
                            ):
                                # web_services_arr.append(s.get("name"))

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
                                    if web_service == "iso":
                                        for watt in root.iter():
                                            if (
                                                watt.tag
                                                == "{%s}westBoundLongitude"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    westBoundLongitude = (
                                                        wa.text
                                                    )
                                            if (
                                                watt.tag
                                                == "{%s}eastBoundLongitude"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    eastBoundLongitude = (
                                                        wa.text
                                                    )
                                            if (
                                                watt.tag
                                                == "{%s}southBoundLatitude"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    southBoundLatitude = (
                                                        wa.text
                                                    )
                                            if (
                                                watt.tag
                                                == "{%s}northBoundLatitude"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    northBoundLatitude = (
                                                        wa.text
                                                    )
                                            # if watt.tag == "{%s}title" % constants.iso_gmd:
                                            #     for wa in watt:
                                            #         title_ = wa.text
                                            if (
                                                watt.tag
                                                == "{%s}keyword"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    if wa.text in const_list:
                                                        keyword.append(wa.text)
                                            if (
                                                watt.tag
                                                == "{%s}aName"
                                                % constants.iso_gco
                                            ):
                                                for wa in watt:
                                                    if (
                                                        wa.text
                                                        not in data_format
                                                    ):
                                                        aName.append(wa.text)
                                            if (
                                                watt.tag
                                                == "{%s}descriptor"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    descriptor.append(wa.text)
                                            if (
                                                watt.tag
                                                == "{%s}dimensionName"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    dimensionName.append(
                                                        wa.text
                                                    )
                                            # if watt.tag == "{%s}Measure" % constants.iso_gco:
                                            #     for wa in watt:
                                            #         Measure.append(wa.text)
                                            if (
                                                watt.tag
                                                == "{%s}resolution"
                                                % constants.iso_gmd
                                            ):
                                                for wa in watt:
                                                    resolution.append(wa.text)

                                            if (
                                                watt.tag
                                                == "{%s}beginPosition"
                                                % constants.iso_gml
                                            ):
                                                beginPosition = watt.text

                                            if (
                                                watt.tag
                                                == "{%s}endPosition"
                                                % constants.iso_gml
                                            ):
                                                endPosition = watt.text
                                    elif web_service == "ncml":
                                        for watt in root.iter():
                                            if (
                                                watt.attrib.get("name")
                                                == "geospatial_lon_min"
                                            ):
                                                westBoundLongitude = (
                                                    watt.attrib.get("value")
                                                )
                                            if (
                                                watt.attrib.get("name")
                                                == "geospatial_lon_max"
                                            ):
                                                eastBoundLongitude = (
                                                    watt.attrib.get("value")
                                                )
                                            if (
                                                watt.attrib.get("name")
                                                == "geospatial_lat_min"
                                            ):
                                                southBoundLatitude = (
                                                    watt.attrib.get("value")
                                                )
                                            if (
                                                watt.attrib.get("name")
                                                == "geospatial_lat_max"
                                            ):
                                                northBoundLatitude = (
                                                    watt.attrib.get("value")
                                                )
                                            if (
                                                watt.attrib.get("name")
                                                == "time_coverage_start"
                                            ):
                                                beginPosition = (
                                                    watt.attrib.get("value")
                                                )
                                            if (
                                                watt.attrib.get("name")
                                                == "time_coverage_end"
                                            ):
                                                endPosition = watt.attrib.get(
                                                    "value"
                                                )
                                        for i in root:
                                            if (
                                                i.tag
                                                == "{%s}dimension"
                                                % constants.ncml
                                            ):
                                                if (
                                                    i.get("name")
                                                    not in const_list2
                                                ):
                                                    dimensionName.append(
                                                        i.get("name")
                                                    )

                                        for i in root:
                                            if (
                                                i.tag
                                                == "{%s}variable"
                                                % constants.ncml
                                            ):
                                                if (
                                                    i.get("name")
                                                    not in const_list2
                                                ):
                                                    aName.append(i.get("name"))
                                        for i in root:
                                            if (
                                                i.tag
                                                == "{%s}variable"
                                                % constants.ncml
                                            ):
                                                array = [
                                                    j.get("name") for j in i
                                                ]
                                                for j in i:
                                                    if (
                                                        j.get("name")
                                                        == "standard_name"
                                                    ):
                                                        descriptor.append(
                                                            j.get("value")
                                                        )
                                                    elif (
                                                        j.get("name")
                                                        == "long_name"
                                                        and "standard_name"
                                                        not in array
                                                    ):
                                                        descriptor.append(
                                                            j.get("value")
                                                        )

                                        # descriptor = set({v.casefold(): v for v in descriptor}.values())
                                        # descriptor = list(set(descriptor))

                                        keyword = dimensionName

                                        # if watt.tag == "{%s}Measure" % constants.iso_gco:
                                        #     for wa in watt:
                                        #         Measure.append(wa.text)

                                    else:
                                        self.final_msg = (
                                            "Activate "
                                            + web_service
                                            + " service in the requested catalog"
                                        )
                                        continue
                            # if web_service not in web_services_arr:
                            #     print(web_service + " is not in the list of sevices of dataset")
                            #     break

                        # print("beginPosition", beginPosition)
                        # print("endPosition", endPosition)
                        # print("westBoundLongitude", westBoundLongitude)
                        # print("eastBoundLongitude", eastBoundLongitude)
                        # print("southBoundLatitude", southBoundLatitude)
                        # print("northBoundLatitude", northBoundLatitude)
                        # print("descriptor", descriptor)
                        # print("aName", aName)
                        # print("dimensionName", dimensionName)
                        # print("keyword", keyword)
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

                        # collection_interval.append(comp_dt)
                        collection_interval.append(
                            datetime.strptime(
                                beginPosition, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
                        collection_interval.append(
                            datetime.strptime(
                                endPosition, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )

                        collection_interval = sorted(collection_interval)
                        collection_interval_final_time = [
                            collection_interval[0],
                            collection_interval[-1],
                        ]
                        # print(collection_interval_final_time)
                        # print(funcs.replacement_func(elem.get("ID")))
                        item = pystac.Item(
                            id=funcs.replacement_func(elem.get("ID")),
                            geometry=geometry.mapping(footprint),
                            bbox=bbox_x,
                            datetime=comp_dt,
                            properties={},
                        )
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

                        cube = DatacubeExtension.ext(item, add_if_missing=True)

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
                            if aName[i] not in const_list:
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
                        # print(url)

                        convert_xml_m = funcs.replacement_func(url)

                        if (
                            collection_bbox[0] == collection_bbox[2]
                            or collection_bbox[1] == collection_bbox[3]
                        ):
                            collection_bbox = [
                                collection_bbox[0] - 0.000001,
                                collection_bbox[1] - 0.000001,
                                collection_bbox[2] + 0.000001,
                                collection_bbox[3] + 0.000001,
                            ]
                        spatial_extent = pystac.SpatialExtent(
                            bboxes=[collection_bbox]
                        )
                        temporal_extent = pystac.TemporalExtent(
                            intervals=[collection_interval_final_time]
                        )

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
                        self.catalog[convert_xml_m].extent = pystac.Extent(
                            spatial=spatial_extent, temporal=temporal_extent
                        )
                        # print(collection_bbox)
                        # print(collection_interval_final_time)
                        self.catalog[convert_xml_m].add_item(item)
                        # print(convert_xml_m)
                        # print(self.catalog[convert_xml_m].extent)
                        # print(list(list(self.catalog[convert_xml_m].get_children())[0].get_children()))
                        # print(list(self.catalog[convert_xml_m].get_children()))
                except BaseException as e:
                    print(e)
                    continue

            yield str(url) + "?dataset=" + str(gid)

        # if type(self.catalog[convert_xml]) is pystac.catalog.Catalog:
        #     print((self.catalog[convert_xml]))
        # print(type(self.catalog[convert_xml]))
        # type(self.catalog[convert_xml]) is "pystac.catalog.Collection"
        print("convert_xml", convert_xml)
        print("type(self.catalog[convert_xml])", self.catalog[convert_xml])
        print(
            "type(self.catalog[convert_xml])", type(self.catalog[convert_xml])
        )
        if (
            type(self.catalog[convert_xml]) is pystac.collection.Collection
            and self.catalog[convert_xml].extent.spatial is None
        ):
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for elements in list(self.catalog[convert_xml].get_children()):
                if elements.extent.spatial is not None:
                    self.catalog[convert_xml].extent = elements.extent
                else:
                    self.catalog[convert_xml].extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )
            if len(list(self.catalog[convert_xml].get_children())) == 0:
                self.catalog[convert_xml].extent = pystac.Extent(
                    spatial=spatial_extent, temporal=temporal_extent
                )
        if type(self.catalog[convert_xml]) is pystac.catalog.Catalog:
            spatial_extent = pystac.SpatialExtent(bboxes=[[0, 0, 0, 0]])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )
            for i in list(self.catalog[convert_xml].get_children()):
                if (
                    type(i) is pystac.collection.Collection
                    and i.extent.spatial is None
                ):
                    i.extent = pystac.Extent(
                        spatial=spatial_extent, temporal=temporal_extent
                    )

    def dataset_status(self, url, xml_content):
        if url in self.scanned:
            print("Already Scanned %s " % url)
            return
        self.scanned.append(url)

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
            self.data_num = self.data_num + len(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
            )
        else:
            print(
                "|__",
                url,
                "|  Number of branches: ",
                len(tree.findall(".//{%s}catalogRef" % constants.unidata)),
            )
            self.branch_num = self.branch_num + len(
                tree.findall(".//{%s}catalogRef" % constants.unidata)
            )

        for i, d in enumerate(data):
            for dataset in self.dataset_status(branches[i], d):
                yield dataset

        for elem in tree.findall(
            ".//{%s}dataset[@urlPath]" % constants.unidata
        ):
            gid = elem.get("ID")
            yield str(url) + "?dataset=" + str(gid)
