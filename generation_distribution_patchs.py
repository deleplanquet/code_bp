import matplotlib.pyplot as plt
import math

def d2r(angle):
    return(angle*math.pi/180)

def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

def rotation(u, theta, OM):
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    radian = d2r(theta)
    mat = array([[a*a + (1 - a*a)*math.cos(radion),
                  a*b*(1 - math.cos(radian)) - c*math.sin(radian),
                  a*c*(1 - math.cos(radian)) + b*math.sin(radian)],
                 [a*b*(1 - math.cos(radian)) + c*math.sin(radian),
                  b*b + (1 - b*b)*math.cos(radian),
                  b*c*(1 - math.cos(radian)) - a*math.sin(radian)],
                 [a*c*(1 - math.cos(radian)) - b*math.sin(radian),
                  b*c*(1 - math.cos(radian)) + a*math.sin(radian),
                  c*c + (1 - c*c)*math.cos(radian)]])
    vect = array([[u[0]],
                  [u[1]],
                  [u[2]]])
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])

def fault(cen_fault, length, width, u_strike, u_dip, pasx, pasy):
    x_cf, y_cf, z_cf = geo2cart(cen_fault[0], cen_fault[1], cen_fault[2])
    x_fault = np.arange(-length/2/pasx, length/2/pasx)
    y_fault = np.arange(-width/2/pasy, length/2/pasy)
    grill_fault = np.zeros((len(x_fault), len(y_fault), 3))
    for a in x_fault:
        for b in y_fault:
            grill_fault[np.where(x_fault == a), np.where(y_fault == b), 0] = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
            grill_fault[np.where(y_fault == a), np.where(y_fault == b), 1] = y_cf + b*pasx*u_strike[1] + b*pasy*u_dip[1]
            grill_fault[np.where(z_fault == a), np.where(y_fault == b), 2] = z_cf + c*pasx*u_strike[2] + b*pasy*u_dip[2]

dir_cen_fault = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)),
                 math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)),
                 math.sin(d2r(lat_hyp))]

vect_nord = rotation(dir_cen_fault,
                     90,
                     [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])

vect_strike = rotation(vect_nord,
                       - strike,
                       dir_cen_fault)

vect_perp_strike = rotation(vect_nord,
                            - strike - 90,
                            dir_cen_fault)

vect_dip = rotation(vect_perp_strike,
                    dip,
                    vect_strike)

coord_fault = fault([R_Earth - dep_hyp, lat_hyp, lon_hyp],
                    l_fault,
                    w_fault,
                    norm(vect_strike),
                    norm(vect_dip),
                    pas_l,
                    pas_w)


