"""
Module to identify WRS path and rows from Lat and Long

@author - pmeyyappan

"""

import io
import ogr
import osgeo
import shapely.wkt
import shapely.geometry

import urllib.request

import zipfile

#from osgeo import ogr


# GDAL - for manipulating geospatial raster data
# OGR - for manipulating geospatial vector data


url = "https://prd-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip"

#from urllib import urlopen
#r = urlopen(url)

r = urllib.request.urlopen(url)

zip_file = zipfile.ZipFile(io.BytesIO(r.read()))
zip_file.extractall("landsat-path-row")
zip_file.close()


#import shapefile
#shape = shapefile.Reader(shapefile_directory)
#feature = shape.shapeRecords()[0]

#import fiona
#shape = fiona.open(shapefile)
#print shape.schema
#layer =fiona.open(shapefile_directory, layer=0)


#wrs = ogr.Open(shapefile)
#layer = wrs.GetLayer(0)


shapefile_directory = 'landsat-path-row/WRS2_descending.shp'
wrs = ogr.Open(shapefile_directory)
layer = wrs.GetLayer(0)

lon = - 74.0060
lat = 40.7128
point = shapely.geometry.Point(lon, lat)
mode = 'D'


def checkPoint(feature, point, mode):
    """
    Returns True if the point is within the shape. Else, returns False.

    :param feature:
    :param point:
    :param mode:['D', 'A']; D - Descending; day-time images; A - Ascending; night-time images
    :return:
    """

    geom = feature.GetGeometryRef()  # Get geometry from feature

    shape = shapely.wkt.loads(geom.ExportToWkt())  # Import geometry into shapely to easily work with our point

    if point.within(shape) and feature['MODE'] == mode:
        return True
    else:
        return False


i = 0

while not checkPoint(layer.GetFeature(i), point, mode):
    i += 1

feature = layer.GetFeature(i)
path = feature['PATH']
row = feature['ROW']


print('Path: ', path, 'Row: ', row)