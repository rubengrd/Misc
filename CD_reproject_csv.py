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

# We loop over latitude and longitude values
for index, rows in geo_data.iterrows():
    p = [rows.longitude, rows.latitude]
    geo_data.loc[index, "geometry"] = Point(p)
    #We generate the shapely point and insert it into the dataframe
    #This loop may not be the most performing one and you'll see that
    #Iterrows is a deprecated method, but it does its job!!!! 

# Add two new columns, northing and easting of the projected coordinates
geo_data["north"] = ""
geo_data["east"] = ""

# Reprojection to RGF93. Choose the CRS you need!
geo_data = geo_data.to_crs("EPSG:2154")

# Loop to insert the coordinates into the new columns
for index1, rows1 in geo_data.iterrows():
    p1 = [rows1.geometry.x, rows1.geometry.y]
    geo_data.loc[index1, "north"] = p1[0]
    geo_data.loc[index1, "east"] = p1[1]

print (geo_data)
print (geo_data.crs) # Data check

# Choose the export path
outFP = r"C:\python\tests\Tai_testpython"

####################################################################
########################EXPORT TO CSV ##############################
####################################################################
#Please note that you should choose only one of the two export methods#
geo_data.to_csv(outFP)

####################################################################
###################OR TO SHAPEFILE #################################
####################################################################

#geo_data.to_file(outFP)
print ("Done!")
