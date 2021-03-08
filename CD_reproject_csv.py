########################################################
######REPROYECCION DE COORDENADAS DESDE UN FICHERO######
######CSV Y EXPORTACION#################################
########################################################

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from fiona.crs import from_epsg

#Lectura del csv y conversion en df
#El fichero tiene que estar en la carpeta de python para que
# funcione. Es donde estan los modulos importados arriba
# CAMBIAR EL NOMBRE DEL FICHERO EN CUESTION ANTES DE EJECUTAR

fp = gpd.read_file("C:\python\Taintrux_210301_testpython.csv")

geo_data = gpd.GeoDataFrame (fp, geometry = "geometry")
geo_data[["latitude","longitude"]] = geo_data[["latitude","longitude"]].astype("float")
geo_data.crs = 'EPSG:4326'

# Bucle a traves de todos los elementos del df
i=0
for lat,lon in zip(geo_data['latitude'], geo_data['longitude']):
    p = [lat,lon]
    geo_data.loc[i,"geometry"] = Point(p)
    i = i+1
    #Generamos el punto en formato shapely y con la funcion .loc lo
    #asignamos a la casilla de la columna geometry que corresponde

# Anadimos las columnas north y east al df para anadir las coordenadas reproyectadas
geo_data["north"] = ""
geo_data["east"] = ""

# Reproyeccion al RGF93 (comprobacion de la reproyeccion)
geo_data = geo_data.to_crs("EPSG:2154")

# Rellenamos los nuevos campos con los x y reproyectados
for index1, rows1 in geo_data.iterrows():
    p1 = [rows1.geometry.x, rows1.geometry.y]
    geo_data.loc[index1, "north"] = p1[0]
    geo_data.loc[index1, "east"] = p1[1]

print (geo_data)
print (geo_data.crs)

# Creacion del camino de exportacion
outFP = r"C:\python\tests\Tai_testpython"

####################################################################
############EXPORTACION DE FICHERO CSV##############################
####################################################################
geo_data.to_csv(outFP)

####################################################################
###################### O SHAPEFILE #################################
####################################################################

#geo_data.to_file(outFP)
print ("Done!")

#FUNCIONA!