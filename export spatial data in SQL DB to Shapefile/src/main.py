# -*- coding: utf-8 -*-
"""
Convert Geospatial Data to TopoJSON
- query data from SQL Server

@author: Jeff Yen
"""
import pyodbc
import pandas as pd
import geopandas as gpd
from shapely import wkt


# Functions
def get_gis_layer(sql):
    """
    Query a GIS layer from SQL Server
    """
    #establish SQL connection
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=;" # TODO
                          "Database=;" # TODO
                          "Trusted_Connection=yes;")
    #run query
    resultDF = pd.read_sql_query(sql, conn)
    
    #convert to GeoDF
    resultDF["geometry"] = [wkt.loads(x) for x in resultDF["geometry"]]
    resultDF = gpd.GeoDataFrame(resultDF,
                                crs="EPSG:", #TODO: layer projection
                                geometry="geometry")
    
    #drop columns encoded with bytes
    resultDF = resultDF.drop(['Shape'], axis=1)
    
    return resultDF


# Initialize spatial query
lyr_name = '[database].[schema].[table name]'
sql = ("SELECT *"
       ", [Shape].ToString() AS [geometry]"
       "FROM {}".format(lyr_name)
       )

# Get GIS layer
gisLYR = get_gis_layer(sql)

# Convert GIS layer to Shapefile
out_lyr_name = lyr_name.split(".")[-1].strip("[]")
gisLYR.to_file(r"..\output\{}.shp".format(out_lyr_name))