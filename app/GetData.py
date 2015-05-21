"""
Created on 160315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
import os
import sys
import gdal
import math
from gdalconst import GA_ReadOnly
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILENAME = PATH + '/data/world.vrt'
NULL_VALUE = -9999
gdal.AllRegister()
gdal.UseExceptions()


def open_raster():
    """
    This functions opens the raster file for processing
    """
    try:
        raster = gdal.Open(FILENAME, GA_ReadOnly)
    except RuntimeError, exception:
        print 'Unable to open '+FILENAME
        print exception
        sys.exit(1)
    return raster


def to_geographic(mercator_x_lon, mercator_y_lat):
    """
    This function will change the given Pseudo/Mercator coordinates and convert
    to WGS 84 lat/lon coordinate

    mercator_x_lon - coordinates for the x axis or the longitude
    mercator_y_lat - coordinates for the y axis or the latitude
    """
    if math.fabs(mercator_x_lon) < 180 and math.fabs(mercator_y_lat) < 90:
        return
    if (math.fabs(mercator_x_lon) > 20037508.3427892) or \
            (math.fabs(mercator_y_lat) > 20037508.3427892):
        return
    x_value = mercator_x_lon
    y_value = mercator_y_lat
    num3 = x_value / 6378137.0
    num4 = num3 * 57.295779513082323
    num5 = math.floor(((num4 + 180.0) / 360.0))
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - \
           (2.0 * math.atan(math.exp((-1.0 * y_value) / 6378137.0)))
    mercator_x_lon = num6
    mercator_y_lat = num7 * 57.295779513082323
    return [mercator_x_lon, mercator_y_lat]


def to_mercator(mercator_x_lon, mercator_y_lat):
    """
    This function will change the given WGS 84 lat/lon coordinate and convert
    to Pseudo/Mercator coordinates

    mercator_x_lon - coordinates for the x axis or the longitude
    mercator_y_lat - coordinates for the y axis or the latitude
    """
    if math.fabs(mercator_x_lon) > 180 or math.fabs(mercator_y_lat) > 90:
        return
    num = mercator_x_lon * 0.017453292519943295
    x_value = 6378137.0 * num
    additional = mercator_y_lat * 0.017453292519943295
    mercator_x_lon = x_value
    mercator_y_lat = 3189068.5 * \
                     math.log((1.0 + math.sin(additional)) /
                              (1.0 - math.sin(additional)))
    return [mercator_x_lon, mercator_y_lat]


def find_closest(height, origin):
    """
    This function will read the list of values and call the calculate_distance()
    to return the information regarding the nearest point.

    height - the 3D array of all the possible height within the radius
    origin - the original coordinate  which defines the center of a circle
    """
    new_list = []
    for i in range(len(height)):
        distance = calculate_distance(int(height[i][0]), int(height[i][1]),
                                      int(origin[0]), int(origin[1]))
        azimuth = calculate_azimuth(int(height[i][0]), int(height[i][1]),
                                    int(origin[0]), int(origin[1]))
        geographic = to_geographic(height[i][0], height[i][1])
        new_list.append([geographic[0], geographic[1],
                         height[i][2], int(distance), azimuth])
    max_list = new_list[0]
    for j in range(1, len(new_list)):
        if max_list[3] > new_list[j][3]:
            max_list = new_list[j]
    return max_list


def calculate_distance(give_x, give_y, origin_x, origin_y):
    """
    This is to find distance of all of possible height within the radius

    give_x - the longitude of the possible height
    give_y - the latitude of the possible height
    origin_x - the point of origin defined by user
    origin_y - the point of origin defined by user
    """
    return math.sqrt(abs((give_y-origin_y)**2) +
                     abs((give_x-origin_x)**2))


def calculate_azimuth(give_x, give_y, origin_x, origin_y):
    """
    This is to find the azimuth from the original location to the
    highest point

    give_x - the longitude of the possible height
    give_y - the latitude of the possible height
    origin_x - the point of origin defined by user
    origin_y - the point of origin defined by user
    """
    opposite = (give_y-origin_y)
    adjacent = (give_x-origin_x)
    azimuth = math.degrees(math.atan((abs(opposite)*1.0/abs(adjacent))))
    if opposite < 0 < adjacent:
        return azimuth + 90
    elif adjacent < 0 and opposite < 0:
        return azimuth + 180
    elif opposite > 0 > adjacent:
        return azimuth + 270
    else:
        return azimuth


def retrieve_band(longitude, latitude):
    """
    This function will take in the given coordinates and return the
    elevation(band) NOTE: this only takes in Mercator value does not
    work with WGS84

    x - coordinates for the x axis or the longitude that users defined
    y - coordinates for the y axis or the latitude that user defined
    """
    if -180.0 > longitude > 180.0 or -90 > latitude > 90:
        return NULL_VALUE
    else:
        raster = open_raster()
        transform = raster.GetGeoTransform()
        mercator = to_mercator(longitude, latitude)
        x_offset = int((mercator[0] - transform[0]) / transform[1])
        y_offset = int((mercator[1] - transform[3]) / transform[5])
        band = raster.GetRasterBand(1)
        data = band.ReadAsArray(x_offset, y_offset, 1, 1)
        return data[0]


def retrieve_highest_point(lon, lat, rad):
    """
    This function will take in the given coordinates and return
    the highest elevation(band) within the radius from the original
    point(a circle). Where multiple similar height the function will
    return the value of the nearest highest peak

    lon - coordinates for the x axis or the longitude that users defined
    lat - coordinates for the y axis or the latitude that user defined
    r - this is the radius to define the possible area
    """
    raster = gdal.Open(FILENAME, GA_ReadOnly)
    highest = 0
    mercator = to_mercator(lon, lat)
    transform = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    x_coordinate = [x_value for x_value in
                    range(int(mercator[0]-rad),
                          int(mercator[0]-rad)+(rad*2), 30)]
    y_coordinate = [y_value for y_value in
                    range(int(mercator[1]-rad),
                          int(mercator[1]-rad)+(rad*2), 30)]
    for y_value in range(len(x_coordinate)):
        for x_value in range(len(y_coordinate)):
            x_offset = int((x_coordinate[x_value] -
                            transform[0]) / transform[1])
            y_offset = int((y_coordinate[y_value] -
                            transform[3]) / transform[5])
            data = band.ReadAsArray(x_offset, y_offset, 1, 1)
            if (x_value-(rad/30))**2 + (y_value-(rad/30))**2 < \
                            (rad/30)**2:
                if highest < int(data[0]):
                    height_list = []
                    highest = int(data[0])
                    height_list.append((x_coordinate[x_value],
                                        y_coordinate[y_value], highest))
                elif highest == int(data[0]):
                    height_list.append((x_coordinate[x_value],
                                        y_coordinate[y_value], highest))
    return find_closest(height_list, mercator)

