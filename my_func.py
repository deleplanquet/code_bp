


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
    normalisation: sum(vi*vi) = 1
    """
    Norm = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return [v[0]/Norm, v[1]/Norm, v[2]/Norm]

def rotation(u, theta, OM):
    """
    rotation of a vector in 3D, return a vector

    u: should have 3 components
    theta: should be in degree
    OM: should have 3 components
    """
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    rth = d2r(theta)
    mat = array([[a*a + (1 - a*a)*math.cos(rth),
    	    	  a*b*(1 - math.cos(rth)) - c*math.sin(rth),
    	    	  a*c*(1 - math.cos(rth)) + b*math.sin(rth)],
    	    	 [a*b*(1 - math.cos(rth)) + c*math.sin(rth),
    	    	  b*b + (1 - b*b)*math.cos(rth),
    	    	  b*c*(1 - math.cos(rth)) - a*math.sin(rth)],
    	    	 [a*c*(1 - math.cos(rth)) - b*math.sin(rth),
    	    	  b*c*(1 - math.cos(rth)) + a*math.sin(rth),
    	    	  c*c + (1 - c*c)*math.cos(rth)]])
    v = array([[u[0]],
    	       [u[1]],
    	       [u[2]]])
    v_rot = dot(mat, v)
    return (v_rot[0][0], v_rot[1][0], v_rot[2][0])
