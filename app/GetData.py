'''
Created on 28 March 2015
Created by Eugene Phua
'''

import os, sys, gdal, math, time
from gdalconst import *

path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILENAME = path+'/data/world.vrt'
NULL_VALUE = -9999

# register all of the drivers
gdal.AllRegister()
gdal.UseExceptions()


'''
This functions opens the raster file for processing
'''
def opentiff():
    try:
        ds = gdal.Open(FILENAME, GA_ReadOnly)
    except RuntimeError, e:
        print 'Unable to open '+FILENAME
        print e
        sys.exit(1)
    return ds


'''
This function will change the given Pseudo/Mercator coordinates and convert
to WGS 84 lat/lon coordinate
'''
def ToGeographic(mercatorX_lon, mercatorY_lat):
    if (math.fabs(mercatorX_lon) < 180 and math.fabs(mercatorY_lat) < 90):
        return
    if ((math.fabs(mercatorX_lon) > 20037508.3427892) or (math.fabs(mercatorY_lat) > 20037508.3427892)):
        return
    x = mercatorX_lon
    y = mercatorY_lat
    num3 = x / 6378137.0
    num4 = num3 * 57.295779513082323
    num5 = math.floor(((num4 + 180.0) / 360.0))
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * y) / 6378137.0)))
    mercatorX_lon = num6
    mercatorY_lat = num7 * 57.295779513082323
    return [mercatorX_lon,mercatorY_lat]


'''
This function will change the given WGS 84 lat/lon coordinate and convert
to Pseudo/Mercator coordinates
'''
def ToWebMercator(mercatorX_lon, mercatorY_lat):
    if ((math.fabs(mercatorX_lon) > 180 or math.fabs(mercatorY_lat) > 90)):
        return
    num = mercatorX_lon * 0.017453292519943295
    x = 6378137.0 * num
    a = mercatorY_lat * 0.017453292519943295;
    mercatorX_lon = x
    mercatorY_lat = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
    return [mercatorX_lon,mercatorY_lat]


'''
This function will read the list of values and call the calculateDistance() 
to return the information regarding the nearest point.
'''
def findClosest(list, origin):
    newlist = []
    for x in range(len(list)):
        distance = calculateDistance(int(list[x][0]),int(list[x][1]),int(origin[0]),int(origin[1]))
        latlon=ToGeographic(list[x][0],list[x][1])
        newlist.append([latlon[0], latlon[1], list[x][2], int(distance)])
    maxlist = newlist[0]
    for i in range(1, len(newlist)):
        if maxlist[3]> newlist[i][3]:
            maxlist=newlist[i]
    return  maxlist


'''
This is to find the nearest point to the original point
'''
def calculateDistance(x1, y1, x2, y2):
    return math.sqrt(abs((y1-y2)*(y1-y2))+abs((x1-x2)*(x1-x2)))

'''
This function will take in the given coordinates and return the elevation(band)
'''
def retrieveband(x,y):
    if -180.0>x>180.0 or -90>y>90:
	return NULL_VALUE
    else:
        ds=opentiff()
        transform = ds.GetGeoTransform()
        # get georeference info from rasterfile
        merc = ToWebMercator(x, y)
        xOffset = int((merc[0] - transform[0]) / transform[1]) #(X-Coor - Xorigin) / Pixel Width
        yOffset = int((merc[1] - transform[3]) / transform[5]) #(Y-Coor - Yorigin) / Pixel Height
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        band= ds.GetRasterBand(1)
        data = band.ReadAsArray(xOffset,yOffset,1,1)#Building the narray to the total width and total height
        return data[0]

'''
This function will take in the given coordinates and return the highest elevation(band)
and nearest elevation to the original point
'''
def retrieveHighPoint(lon,lat,r):
    if -180.0>lon>180.0 or -90>lat>90:
	return NULL_VALUE
    else:
	ds = gdal.Open(FILENAME, GA_ReadOnly)
	a = b = r
	m=0
	xy=[]
	merc = ToWebMercator(lon, lat)
	x = int(merc[0]-r)
	y = int(merc[1]-r)
	transform = ds.GetGeoTransform()
	band= ds.GetRasterBand(1)
	xa= [x for x in range(x,x+(r*2),30)]
	ya= [y for y in range(y,y+(r*2),30)]
	# get georeference info from rasterfile
	#map_ = [[NULL_VALUE for x in range(len(xa))] for y in range(len(ya))]
	for y in range(len(xa)):
	    for x in range(len(ya)):
		xOffset = int((xa[x] - transform[0]) / transform[1]) #(X-Coor - Xorigin) / Pixel Width
		yOffset = int((ya[y] - transform[3]) / transform[5]) #(Y-Coor - Yorigin) / Pixel Height
		data = band.ReadAsArray(xOffset,yOffset,1,1)
		if (x-(a/30))**2 + (y-(b/30))**2 < (r/30)**2:
		    #map_[y][x] =int(data[0])
		    if m < int(data[0]):
		        xy = []
		        m = int(data[0])
		        xy.append((xa[x], ya[y], m))
		    elif m == int(data[0]):
		        xy.append((xa[x], ya[y], m))
        return findClosest(xy,merc)
    


