


import math

def d2r(angle):
    """
    convert angle from degree to radian

    angle: should be in degree
    """
    return angle*math.pi/180

def geo2cart(r, lat, lon):
    """
    convert geographic coordinates to Cartesian coordinates

    r: should be in km
    lat: should be in degree
    lon: should be in degree
    """
    rlat = d2r(lat)
    rlon = d2r(lon)
    x = r*math.cos(rlat)*math.cos(rlon)
    y = r*math.cos(rlat)*math.sin(rlon)
    z = r*math.sin(rlat)
    return[x, y, z]

def norm1(v):
    """
    return a list whose maximum is equal to 1 (take care of negative value)
    """
    return[a/v.max() for a in v]

def r2d(angle):
    """
    convert angle from radian to degree

    angle: should be in degree
    """
    return angle*180/math.pi

def norm(v):
    """
    """
    Norm = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return []
