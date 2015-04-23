import os, sys, gdal, math, time
from gdalconst import *

path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILENAME = path+'/data/Mercator.tif'
NULL_VALUE = -9999

# register all of the drivers
gdal.AllRegister()
gdal.UseExceptions()
def opentiff():
    try:
        # open the image
        ds = gdal.Open(FILENAME, GA_ReadOnly)
    except RuntimeError, e:
        print 'Unable to open '+FILENAME
        print e
        sys.exit(1)
    return ds

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

def ToWebMercator(mercatorX_lon, mercatorY_lat):
    if ((math.fabs(mercatorX_lon) > 180 or math.fabs(mercatorY_lat) > 90)):
        return
    num = mercatorX_lon * 0.017453292519943295
    x = 6378137.0 * num
    a = mercatorY_lat * 0.017453292519943295;
    mercatorX_lon = x
    mercatorY_lat = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
    return [mercatorX_lon,mercatorY_lat]



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
        data = band.ReadAsArray(0, 0, cols, rows)#Building the narray to the total width and total height
	if data[yOffset,xOffset]<0:
		return -9999
	else:
        	return data[yOffset,xOffset]


def retrieveHighPoint(lon,lat,r):
    if -180.0>lon>180.0 or -90>lat>90:
	return NULL_VALUE
    else:
        ds=opentiff()
        a= b =r
        merc = ToWebMercator(lon, lat)
        x = int(merc[0]-r)
        y = int(merc[1]-r)
        m=0
        xy=[]
        xa= [x for x in range(x,x+(r*2),30)]
        ya= [y for y in range(y,y+(r*2),30)]
        transform = ds.GetGeoTransform()
        # get georeference info from rasterfile
        band= ds.GetRasterBand(1)
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        data = band.ReadAsArray(0, 0, cols, rows) #Building the narray to the total width and total height
        map_ = [[NULL_VALUE for x in range(len(xa))] for y in range(len(ya))] #this is used for visualisation
        for y in range(len(xa)):
            for x in range(len(ya)):
                xOffset = int((xa[x] - transform[0]) / transform[1]) #(X-Coor - Xorigin) / Pixel Width
                yOffset = int((ya[y] - transform[3]) / transform[5]) #(Y-Coor - Yorigin) / Pixel Height
                point= [xOffset, yOffset]
                if (x-(a/30))**2 + (y-(b/30))**2 < (r/30)**2:
                    if xOffset > 0 or yOffset > 0 or xOffset < cols or yOffset < rows:
                        map_[y][x] = int(data[yOffset,xOffset]) #this is used for visualisation
			#print m
                        if m < int(data[yOffset,xOffset]):
                            xy = []
                            m = int(data[yOffset,xOffset])
                            xy.append((xa[x], ya[y], m))
                        elif m == int(data[yOffset,xOffset]):
                            xy.append((xa[x], ya[y], m))
        return findClosest(xy,merc)
    
def findClosest(list, origin):
    newlist = []
    for x in range(len(list)):
        distance = calculateDistance(list[x][0],list[x][1],origin[0],origin[1])
        latlon=ToGeographic(list[x][0],list[x][1])
        newlist.append([latlon[0], latlon[1], list[x][2], distance])
    maxlist = newlist[0]
    for i in range(len(newlist)):
        if maxlist[3]< newlist[i][3]:
            maxlist=newlist[i]
    return  maxlist

def calculateDistance(x1, y1, x2, y2):
    return math.sqrt(abs((y1-y2)*(y1-y2))+abs((x1-x2)*(x1-x2)))

