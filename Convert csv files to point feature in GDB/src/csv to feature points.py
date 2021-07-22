# -*- coding: utf-8 -*-
"""
This script converts multiple csv files to a Point Feature dataset 
with user-specified projection and store in a ESRI File Geodatabase

Jeff Yen
"""

import os
import glob
import arcpy
import pandas as pd

# Set workspace to the script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Iterate all csv files in subdirectories
path = r'' #TODO: specify the data directory contains all csv files
dataList = []
for root,dirs,_ in os.walk(path):
    for d in dirs:
        path_sub = os.path.join(root,d)
        for filename in glob.glob(os.path.join(path_sub, '*.csv')):
            name = os.path.split(filename)[1]
            dataList.append(filename)

# Merge csv files and export to local drive
df = pd.concat([pd.read_csv(f) for f in dataList])
out_csv = r'' #TODO: specify output csv name
df.to_csv(r"..\output\{}.csv".format(out_csv))

# Create a FGDB if it is not exist
output_path = os.path.dirname(os.getcwd()) + r'\output'
FGDB_path = output_path + r'\data.gdb'

#delete existing FGDB
if os.path.exists(FGDB_path):
    print("Deleting existing GeoDatabase...")
    arcpy.Delete_management(FGDB_path)

#create a new FGDB
print("Creating a GeoDatabase...")
arcpy.CreateFileGDB_management(output_path, "data")

# Convert XY csv files to feature points
arcpy.env.workspace = FGDB_path # set arcpy workspace to FGDB path

#set the local variables
csv_in = os.path.dirname(os.getcwd()) + r'\output\{}.csv'.format(out_csv)
fc_out = "XY_point" #TODO: specify output feature point name
x = "Longitude" #TODO: specify longitude column 
y = "Latitude" #TODO: specify latitude column 
z = ""
SpatialRef = arcpy.SpatialReference(4326) #WGS84

#convert lat/lon to feature points
arcpy.management.XYTableToPoint(csv_in, fc_out, x, y, z, SpatialRef)
print('Total number of feature points: {}'.format(arcpy.GetCount_management(fc_out)))

#re-project to user-specified projection
arcpy.Project_management(fc_out, "XY_point_reprj", arcpy.SpatialReference(2230)) #TODO: specify output projection (e.g., EPSG 2230)
arcpy.Delete_management(fc_out) # delete the initial feature point w/ GCS WGS84
