# -*- coding: utf-8 -*-
"""
Convert Geospatial Data to TopoJSON
- query data from SQL Server

@author: Jeff Yen
"""


import os
import pyodbc
import pandas as pd
import geopandas as gpd
from shapely import wkt
import topojson as tp #topojson: https://mattijn.github.io/topojson/

# Set workspace to the script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Functions
def get_gis_layer(sql):
    """
    Query a GIS layer from SQL Server
    """
    #establish SQL connection
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=;" # TODO: specify server
                          "Database=;" # TODO: specify database
                          "Trusted_Connection=yes;")
    #run query
    resultDF = pd.read_sql_query(sql, conn)
    
    #convert to GeoDF
    resultDF["geometry"] = [wkt.loads(x) for x in resultDF["geometry"]]
    resultDF = gpd.GeoDataFrame(resultDF,
                                crs="EPSG:", #TODO: specify layer projection
                                geometry="geometry")
    
    #drop columns with bytes encoding
    resultDF = resultDF.drop(['Shape'], axis=1)
    
    return resultDF

def convert_to_TopoJSON(input_data, outname):
    """
    Convert a GIS layer to TopoJSON and export attribute table
    """
    #if input projection is not WGS84
    #then do re-projection
    if input_data.crs != "EPSG:4326":
        input_data = input_data.to_crs("EPSG:4326")
    
    #export geomtery to topojson
    resultTP = tp.Topology(input_data, prequantize=False).to_json()
    Output_object = open(r"..\output\{}.json".format(outname),"w")
    Output_object.write(resultTP)

    #export attribute table as csv (exclude geometry)
    input_data.iloc[:,:-1].to_csv(r'..\output\{}.csv'.format(outname), index = False)
    
    return resultTP


# Initialize spatial query
lyr_name = '[database].[schema].[table name]' #TODO: specify table name
sql = ("SELECT *"
       ", [Shape].ToString() AS [geometry]"
       "FROM {}".format(lyr_name)
       )

# Get GIS layer
gisLYR = get_gis_layer(sql)

# Convert GIS layer to TopoJSON and export attribute table
topoJSON = convert_to_TopoJSON(gisLYR, lyr_name)