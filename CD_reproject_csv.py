########################################################
######GEOGRAPHIC COORDINATES REPROJECTION###############
##############FROM A CSV FILE###########################

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from fiona.crs import from_epsg

#Read the shapefile from the selected path
fp = gpd.read_file("C:\python\Taintrux_210301_testpython.csv") # Here you put your path

# Set up of the GeoDataFrame and its coordinate system
geo_data = gpd.GeoDataFrame (fp, geometry = "geometry")
geo_data[["latitude","longitude"]] = geo_data[["latitude","longitude"]].astype("float")
geo_data.crs = 'EPSG:4326' 

# Loop over latitude and longitude values in the dataframe
#We generate the shapely point and insert it into the dataframe
i = 0
for xy in zip (geo_data["longitude"], geo_data["latitude"]):
    coor = [xy[0],xy[1]]
    geo_data.loc[i, "geometry"] = Point(coor)
    i = i+1

# Add two new columns, northing and easting of the projected coordinates
geo_data["north"] = ""
geo_data["east"] = ""

# Reprojection to RGF93. Here you select the coordinate system of your choice
geo_data = geo_data.to_crs("EPSG:2154") 

# Loop to insert the coordinates into the new columns
j =0
for p in geo_data["geometry"]:
    geo_data.loc[j,"north"] = p.y
    geo_data.loc[j,"east"] = p.x
    j = j+1

print (geo_data)
print (geo_data.crs) # Data check

# Choose the export path
outFP = r"C:\python\tests\Tai_testpython"

####################################################################
########################EXPORT TO CSV ##############################
####################################################################
######Please choose only one of the two export methods below########
geo_data.to_csv(outFP)

####################################################################
###################OR TO SHAPEFILE #################################
####################################################################

#geo_data.to_file(outFP)
print ("Done!")
