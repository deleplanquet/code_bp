#

import numpy as np
import pickle
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
import sys
from scipy import interpolate
from scipy.signal import hilbert
from obspy import read
from obspy.signal.util import smooth
from scipy import ndimage
from obspy import Trace
from obspy.core import UTCDateTime

# few functions used in this script
# a library may be done

# conversion angle degree -> radian
def d2r(angle):
    return angle*math.pi/180

# conversion angle radian -> degree
def r2d(angle):
    return angle*180/math.pi

# conversion geographical coordinated -> cartesian coordinates
# vect := (R, lat, lon)
def geo2cart(vect):
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

# normalisation with norm = 1
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

# 3d axial rotation of angle theta
# axis defined by (a, b, c) with norm(a, b, c) = 1 and going through the origin
# direct orthogonal coordinate system
def rotation(u, theta, OM):
    """ attention OM unitaire """
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    radian = d2r(theta)
    # coefficients of the rotation matrix
    mat = array([[a*a + (1 - a*a)*math.cos(radian),
                  a*b*(1 - math.cos(radian)) - c*math.sin(radian),
                  a*c*(1 - math.cos(radian)) + b*math.sin(radian)],
                 [a*b*(1 - math.cos(radian)) + c*math.sin(radian),
                  b*b + (1 - b*b)*math.cos(radian),
                  b*c*(1 - math.cos(radian)) - a*math.sin(radian)],
                 [a*c*(1 - math.cos(radian)) - b*math.sin(radian),
                  b*c*(1 - math.cos(radian)) + a*math.sin(radian),
                  c*c + (1 - c*c)*math.cos(radian)]])
    # reshape the vector to apply the rotation matrix
    vect = array([[u[0]],
                  [u[1]],
                  [u[2]]])
    # the vector u is rotated with the angle theta and the rotation axis OM
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])

# travel time matrix between one station and each subfault
def fault(cen_fault, length, width, u_strike, u_dip, pasx, pasy):
    x_cf, y_cf, z_cf = geo2cart(cen_fault[0], cen_fault[1], cen_fault[2])
    x_fault = np.arange(-length/2/pasx, length/2/pasx)
    #y_fault = np.arange(0, width/pasy)
    y_fault = np.arange(-width/2/pasy, width/2/pasy)
    grill_fault = np.zeros((len(x_fault), len(y_fault), 3))
    for a in x_fault:
        for b in y_fault:
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 0]
                    = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 1]
                    = y_cf + a*pasx*u_strike[1] + b*pasy*u_dip[1]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 2]
                    = z_cf + a*pasx*u_strike[2] + b*pasy*u_dip[2]
    return grill_fault

#calcul de la matrice des tps de trajet pour une station
def trav_time(station, fault, velocity):
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000,
                                   station[1],
                                   station[2])
    mat_time = np.zeros((len(fault[:, 0, 0]), len(fault[0, :, 0])))
    for a in range(len(fault[:, 0, 0])):
        for b in range(len(fault[0, :, 0])):
            mat_time[a, b] = math.sqrt(pow(x_sta - fault[a, b, 0], 2)
                                    + pow(y_sta - fault[a, b, 1], 2)
                                    + pow(z_sta - fault[a, b, 2], 2))/velocity
    return mat_time

#distance entre deux points, coordonnees cartesiennes
def dist(la1, lo1, el1, la2, lo2, el2):
    x1, y1, z1 = geo2cart(R_Earth + el1, la1, lo1)
    x2, y2, z2 = geo2cart(R_Earth + el2, la2, lo2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#normalisation avec max = 1
def norm1(vect):
    return [a/vect.max() for a in vect]

#fonction gaussienne
def gauss(x_data, H, mu):
    sigma = H/2.3548
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = (1./(sigma*math.sqrt(2))
                *math.exp(-(x_data[i] - mu)*(x_data[i] - mu)/(2*sigma*sigma)))
    return y_data

#calcul distance et azimuth d'un point par rapport a un autre
''' distance et azimuth de B par rapport a A -> dist_azim(A, B) '''
def dist_azim(ptA, ptB):
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB)
                        + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))
                            /(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R_Earth*dist_rad, r2d(angle_brut)
    else:
        return R_Earth*dist_rad, 360 - r2d(angle_brut)

#nombre de lignes d'un fichier
def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

print('###############################',
    '\n###   python3 bp_env_E.py   ###',
    '\n###############################')

print('Ne pas oublier de changer la valeur de thresh si on souhaite autre',
        'chose qu\'un threshold a 85 %')

#recuperation position stations
print('     recuperation position stations')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
cpnt = param['component']
hyp_bp = param['selected_waves']
couronne = param['hypo_interv']
azim = param['angle']
frq_bnd = param['frq_band']
R_Earth = param['R_Earth']
strike = param['strike']
dip = param['dip']
l_grid = param['l_grid']
w_grid = param['w_grid']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']
bp_samp_rate = param['bp_samp_rate']
bp_len_t = param['bp_length_time']
l_smooth = param['l_smooth']

# directories used in this script
#
#
#
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt
                    + '_smooth_' + hyp_bp + '_' + azim + 'deg')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt
                    + '_smooth_' + hyp_bp + '/'
             + azim + 'deg')
# to prevent repetition path_bpinv is created and used for the directories:
# - path_bpinv_brut
# - path_bpinv_trace
# - path_bpinv_smooth
path_bpinv = (root_folder + '/'
              + 'Kumamoto/'
              + event + '/'
              + 'vel_env_bpinv/'
              + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt
                    + '_smooth_' + hyp_bp + '_' + azim + 'deg')
path_bpinv_brut = (path_bpinv + '/'
                   + 'brut')
path_bpinv_trace = (path_bpinv + '/'
                    + 'trace')
path_bpinv_smooth = (path_bpinv + '/'
                     + 'trace_smooth')

# in case they do not exist, the following directories are created:
# - path_rslt
# - path_bpinv_brut
# - path_bpinv_trace
# - path_bpinv_smooth
for d in [path_rslt, path_bpinv_brut, path_bpinv_trace, path_bpinv_smooth]:
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print('Creation of the directory {} failed'.format(d))
        else:
            print('Successfully created the directory {}'.format(d))
    else:
        print('{} is already existing'.format(d))

#os.chdir(path_results)
#with open(dossier + '_veldata', 'rb') as mon_fich:
#    mon_depick = pickle.Unpickler(mon_fich)
#    dict_vel = mon_depick.load()

#if hyp_bp == 'P':
#    vel_used = param['vP']
#    dict_vel_used = dict_vel[0]
#elif hyp_bp == 'S':
#    vel_used = param['vS']
#    dict_vel_used = dict_vel[1]

# pick all the envelopes from the directory path_data and sort them
lst_sta = os.listdir(path_data)
lst_sta.sort()

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

lat_hyp = dict_seis[event]['lat']
lon_hyp = dict_seis[event]['lon']
dep_hyp = dict_seis[event]['dep']
hypo = [R_Earth - dep_hyp, lat_hyp, lon_hyp]

# define the origin time of the rupture
yea_seis = int(dict_seis[event]['nFnet'][0:4])
mon_seis = int(dict_seis[event]['nFnet'][4:6])
day_seis = int(dict_seis[event]['nFnet'][6:8])
hou_seis = int(dict_seis[event]['nFnet'][8:10])
min_seis = int(dict_seis[event]['nFnet'][10:12])
sec_seis = int(dict_seis[event]['nFnet'][12:14])
mse_seis = int(dict_seis[event]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis,
                            mon_seis,
                            day_seis,
                            hou_seis,
                            min_seis,
                            sec_seis,
                            mse_seis)

print('Creation of the grid where the envelopes will be back projected')
# direction of the center of the grid, that is CH vector:
# CH := Earth center -> event hypocenter
# defined easily from couple (lat, lon))
dir_cen_grid = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)),
                math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)),
                math.sin(d2r(lat_hyp))]
# direction of the North at hypocenter location, that is N vector:
# N := event hypocenter -> North pole
# the vertor is still tangential to the surface of the EARTH, it is not
# pointing towards the North pole strictly speeking
# defined by rotation of CH vector around the EW local axis with an angle
# equal to 90 degrees
vect_nord = rotation(dir_cen_grid,
                     90,
                     [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])
# direction of the strike of the grid, that is S vector:
# S := event hypocenter -> strike
# defined by rotation of N vector around CH vector with an angle equal to
# "strike" degrees (because strike is counted clockwise, angle should be
# negative in the formula)
vect_strike = rotation(vect_nord,
                       - strike,
                       dir_cen_grid)
# direction of the vector PS perpendicular to vector S, that is:
# PS := event hypocenter -> strike + 90
# defined by rotation of N vector around CH vector with an angle equal to
# "strike" + 90 degrees (here again negative value for angle)
vect_perp_strike = rotation(vect_nord,
                            - strike - 90,
                            dir_cen_grid)
# direction of the dip of the grid, that is D vector:
# D := event hypocenter -> dip
# defined by rotation of PS vector around S vector with an angle equal to
# "dip" degrees
vect_dip = rotation(vect_perp_strike,
                    dip,
                    vect_strike)

# coordinates of each sub grid
# the whole grid is centered in both strike and dip directions on the
# hypocenter of the event
coord_grid = fault(hypo,
                   l_grid,
                   w_grid,
                   norm(vect_strike),
                   norm(vect_dip),
                   l_grid_step,
                   w_grid_step)

#print(coord_fault)
#x1, y1, z1 = (-3526.0445, 4052.5618, 3477.1154)
#x2, y2, z2 = (-3506.0853, 4040.5830, 3471.2726)
#x3, y3, z3 = (-3509.9947, 4096.7141, 3441.4227)
#x4, y4, z4 = (-3490.0355, 4084.7354, 3435.5798)
#x5, y5, z5 = (-3531.4623, 4041.4161, 3485.4628)
#x6, y6, z6 = (-3531.0461, 4041.1676, 3485.3404)
#x7, y7, z7 = (-3531.3274, 4041.7909, 3485.1606)
#print(x1, y1, z1)
#print(x2, y2, z2)
#print(x3, y3, z3)
#print(x4, y4, z4)
#print(x5, y5, z5)
#print(x6, y6, z6)
#print(x7, y7, x7)
#print(r2d(math.acos(x1/pow(x1*x1 + y1*y1, 0.5))),
#      r2d(math.acos(pow((x1*x1 + y1*y1)/(x1*x1 + y1*y1 + z1*z1), 0.5))))
#print(r2d(math.acos(x2/pow(x2*x2 + y2*y2, 0.5))),
#      r2d(math.acos(pow((x2*x2 + y2*y2)/(x2*x2 + y2*y2 + z2*z2), 0.5))))
#print(r2d(math.acos(x3/pow(x3*x3 + y3*y3, 0.5))),
#      r2d(math.acos(pow((x3*x3 + y3*y3)/(x3*x3 + y3*y3 + z3*z3), 0.5))))
#print(r2d(math.acos(x4/pow(x4*x4 + y4*y4, 0.5))),
#      r2d(math.acos(pow((x4*x4 + y4*y4)/(x4*x4 + y4*y4 + z4*z4), 0.5))))
#print(r2d(math.acos(x5/pow(x5*x5 + y5*y5, 0.5))),
#      r2d(math.acos(pow((x5*x5 + y5*y5)/(x5*x5 + y5*y5 + z5*z5), 0.5))))
#print(r2d(math.acos(x6/pow(x6*x6 + y6*y6, 0.5))),
#      r2d(math.acos(pow((x6*x6 + y6*y6)/(x6*x6 + y6*y6 + z6*z6), 0.5))))
#print(r2d(math.acos(x7/pow(x7*x7 + y7*y7, 0.5))),
#      r2d(math.acos(pow((x7*x7 + y7*y7)/(x7*x7 + y7*y7 + z7*z7), 0.5))))

# identification of the station which started to record the first, it will
# be used as reference station (technically, any station can be reference
# station but this one is picked to deal with positive value only)
tstart_ref = None
os.chdir(path_data)
for s in lst_sta:
    st = read(s)
    if tstart_ref == None or tstart_ref - st[0].stats.starttime > 0:
        tstart_ref = st[0].stats.starttime

travt = []
tmin = None
dmin = None
os.chdir(path_data)
for fichier in lst_fch:
    st = read(fichier)
    travt.append(trav_time([st[0].stats.sac.stel,
                            st[0].stats.sac.stla,
                            st[0].stats.sac.stlo],
                           coord_fault,
                           vel_used))
    if dmin == None or dmin > st[0].stats.sac.dist:
        dmin = st[0].stats.sac.dist
    if tmin == None or tmin > st[0].stats.sac.t0:#   calcule les temps de trajet
        tmin = st[0].stats.sac.t0               #   entre chaque station
print(tmin)                                 #   et chaque subfault

length_t = int(length_time*samp_rate)
stack = np.zeros((len(coord_fault[:, 0, 0]),
                  len(coord_fault[0, :, 0]),
                  length_t))            #   initialisation

for station in lst_fch: #   boucle sur les stations
    os.chdir(path_data)
    st = read(station)  #   va chercher une station
    tstart = st[0].stats.starttime#   norm avec max = 1
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    #   interpole: serie de points -> fonction
    f = interpolate.interp1d(t, env_norm)

    ista = lst_fch.index(station)
    print('     ', station, st[0].stats.sampling_rate, str(ista + 1), '/', len(lst_fch))

    for ix in range(len(coord_fault[:, 0, 0])): #   boucle sur le strike
        for iy in range(len(coord_fault[0, :, 0])): #   boucle sur le dip
            for it in range(length_t):      #   boucle sur le tps
                tshift = (travt[ista][ix, iy]#   tps de traj station/subfault
                          - (st[0].stats.starttime - t_origin_rupt)
                          #   correction debut enregistrement
                          + dict_vel_used[st[0].stats.station]
                          #   correction station
                          - 5#   5 sec avant la rupture #   calcul du shift
                          + it/samp_rate)#   pas de tps #   pour la back p
                if tshift > 0 and tshift < t[-1]:#   si le shift ne sort pas de la trace
                    stack[ix, iy, it] = (stack[ix, iy, it]#   on stocke en normalisant
                                         + 1./len(lst_fch)*f(tshift))
                    #   par le nombre de stations

# save the back projection 4D cube in the path_rslt directory (4D because 2
# spatial dimensions (the grid), 1 temporal dimension (the time) and 1 network
# dimension (the stations))
# on purpose, the energy from every station is not directly summed up to allow
# different selection of stations without running the current code (the most
# time consuming) many times
os.chdir(path_rslt)
with open(event + '_vel_'
          + couronne + 'km_'
          + frq_bnd + 'Hz_'
          + cpnt
          + '_smooth_'
          + hyp_bp + '_'
          + azim + 'deg_stack2D', 'wb') as my_fch:
    my_pck = pickle.Pickler(my_fch)
    my_pck.dump(stack)

################################
# bp inverse
################################

stckmx = stack[:, :, :].max()
thresh = 85 *0.01

for sta in lst_fch:# pour chaque station
    os.chdir(path_data)
    st = read(sta)
    ista = lst_fch.index(sta)
    station = {}
    for i in range(len(stack[:, 0, 0])):
        for j in range(len(stack[0, :, 0])):
            for k in range(len(stack[0, 0, :])):# pour chaque element du cube de bp
                tshift = (travt[ista][i, j]
                          - (st[0].stats.starttime - t_origin_rupt)
                          + dict_vel_used[st[0].stats.station]
                          - 5
                          + k/samp_rate)
                station[tshift] = stack[i, j, k]
    os.chdir(path_bpinv)
    with open(st[0].stats.station, 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(station)

lst_bpinv = os.listdir(path_bpinv)

for sta in lst_fch:
    os.chdir(path_data)
    st = read(sta)
    os.chdir(path_bpinv)
    bpinv = np.zeros(st[0].stats.npts)
    with open(sta[:6], 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        station = mdpk.load()
    for key in station.keys():
        bpinv[int(key*100)] = bpinv[int(key*100)] + station[key]
        #print(bpinv[int(key*100)])
    os.chdir(path_bpinvtr)
    tr = Trace(bpinv, st[0].stats)
    tr.write(sta[:6], format = 'SAC')

vect = np.linspace(0,
                   st[0].stats.npts/st[0].stats.sampling_rate,
                   st[0].stats.npts)
sigma = 1./samp_rate

for sta in lst_fch:
    os.chdir(path_bpinvtr)
    st = read(sta[:6])
    dst, azm = dist_azim([st[0].stats.sac.stla,
                          st[0].stats.sac.stlo],
                          [lat_hyp, lon_hyp])
    trg = [math.exp(-(pow(a - 25, 2))/(2*pow(sigma, 2))) for a in vect]
    tr = np.convolve(st[0].data, trg, mode = "same")
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_bpinvsm)
    tr.write(sta[:6], format = 'SAC')
