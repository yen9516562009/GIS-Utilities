# Convert .e00 to Shapefile
ESRI ArcInfo interchange file (E00) is a proprietary ESRI file format intended to support the transfer between ESRI systems of different types of geospatial data used in ESRI software. 
However, ESRI ArcGIS Pro doesn't provide a conversion tool transforming traditional e00 to Shapefile, although ArcGIS Desktop does (checkout this [page](https://gis.ubc.ca/2018/02/how-to-create-a-shapefile-from-an-e00)).

As ESRI promotes ArcGIS Pro and stops providing upgrades for ArcGIS Desktop, a need to develop a tool to convert traditional e00 files to Shapefile can favor those users who have geospatial datasets stored in e00.

This utility was developed using open-source geospatial packages such as GDAL and geopandas. Users do not need to have ESRI ArcGIS license to run the e00 conversion.
