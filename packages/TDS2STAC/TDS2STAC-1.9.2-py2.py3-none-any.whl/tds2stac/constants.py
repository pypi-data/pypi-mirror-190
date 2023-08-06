unidata = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
w3 = "http://www.w3.org/1999/xlink"
iso_gmd = "http://www.isotc211.org/2005/gmd"
iso_gco = "http://www.isotc211.org/2005/gco"
iso_gml = "http://www.opengis.net/gml/3.2"
global_bounding_box = [-360, -90, 0, 90]
No_inf = "No information"
ncml = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"
# a list of parameters to be not used in 'aName' parameter in iso webservice and 'dimension' and 'variable' parameters in ncML webservice
avoided_list = ["time_bnds", "bnds", "ens"]
# a list of parameters to be used in 'keyword' parameter in iso webservice
allowed_list = [
    "time",
    "lat",
    "latitude",
    "lon",
    "longitude",
    "long",
    "time_bnds",
    "bnds",
]
# a list of parameters to avoid use of them in final item
avoided_formats = [
    "float",
    "double",
    "int",
    "time_bnds",
    "bnds",
    "ens",
    "String",
]
epilon = 0.000001
