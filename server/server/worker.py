import sys
from math import radians, cos, sin, asin, sqrt
import uuid

def validateLongi (lo):
    value = None
    try:
        value = float (lo)
    except ValueError:
        return None
    valueStr = "%.6f" % value
    value = float(valueStr)
    
    if value < -180.0 or value > 180.0:
        return None
    else:
        return value

def validateLati (la):
    value = None
    try:
        value = float (la)
    except ValueError:
        return None
    valueStr = "%.6f" % value

    value = float (valueStr)
    
    if value < -90.0 or value > 90.0:
        return None
    else:
        return value

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367.0 * c
    return km

def is_dist_km_far (src_x, src_y, dest_x, dest_y, dist = 5.0):
        actual_dist = haversine( src_y, src_x, dest_y, dest_x)
        print ("actual dist: " + str(actual_dist))
        if actual_dist < dist:
            # return dest x,y coordinate
            return (dest_x, dest_y)
        else:
            return (None, None)

def uuidGen ():

