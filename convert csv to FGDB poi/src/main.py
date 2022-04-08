# -*- coding: utf-8 -*-
"""
Merge multiple csv files to a master csv file
and convert the lat/lon to a Point Features dataset 
and stored in a ESRI File Geodatabase

@Jeff Yen
"""

import os
import glob
import arcpy
import pandas as pd

# TODO: configure output variables
out_csv_name = r'test' #output csv name
csv_in = os.path.dirname(os.getcwd()) + r'..\output\{}.csv'.format(out_csv)
fc_out = "XY_point" #output feature point name
x = "lng" #longitude column 
y = "Lat" #latitude column 
z = ""
inSpatialRef = arcpy.SpatialReference(4326)
outSpatialRef = 2230

# Iterate all csv files in subdirectories
path = r'..\data'
dataList = []
for root, dirs, files in os.walk(path):
    for d in dirs:
        path_sub = os.path.join(root,d)
        for filename in glob.glob(os.path.join(path_sub, '*.csv')):
            name = os.path.split(filename)[1]
            dataList.append(filename)

# Merge csv files and export to local drive
df = pd.concat([pd.read_csv(f) for f in dataList])
df.to_csv(r"..\output\{}.csv".format(out_csv_name))

# Create a FGDB if it is not exist
FGDB_path = output_path + r'..\output\data.gdb'
if os.path.exists(FGDB_path) == False:
    print("Creating a GeoDatabase...")
    arcpy.CreateFileGDB_management(output_path, "data")
else:
    msg = "data.gdb exists. Please delete it and try again..."
    raise ValueError(msg)

# Convert XY csv files to feature points
arcpy.env.workspace = FGDB_path # set arcpy workspace to FGDB path

# Convert lat/lon to feature points
arcpy.management.XYTableToPoint(csv_in, fc_out, x, y, z, SpatialRef)
print('Total number of feature points: {}'.format(arcpy.GetCount_management(fc_out)))

# Re-project to user-specified projection
arcpy.Project_management(fc_out, "XY_point_reprj", arcpy.SpatialReference(outSpatialRef))
