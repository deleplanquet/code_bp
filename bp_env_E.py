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

# conversion geographical coordinated -> cartesian coordinates
# vect := (R, lat, lon)
def geo2cart(vect):
    r = vect[0]
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
    x_cf, y_cf, z_cf = geo2cart(cen_fault)
    x_fault = np.arange(-length/2/pasx, length/2/pasx)
    #y_fault = np.arange(0, width/pasy)
    y_fault = np.arange(-width/2/pasy, width/2/pasy)
    grill_fault = np.zeros((len(x_fault), len(y_fault), 3))
    for a in x_fault:
        for b in y_fault:
            grill_fault[np.where(x_fault==a),
                        np.where(y_fault==b),
                        0] = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
            grill_fault[np.where(x_fault==a),
                        np.where(y_fault==b),
                        1] = y_cf + a*pasx*u_strike[1] + b*pasy*u_dip[1]
            grill_fault[np.where(x_fault==a),
                        np.where(y_fault==b),
                        2] = z_cf + a*pasx*u_strike[2] + b*pasy*u_dip[2]
    return grill_fault

#calcul de la matrice des tps de trajet pour une station
def trav_time(station, fault, velocity):
    x_sta, y_sta, z_sta = geo2cart([R_Earth + station[0]/1000,
                                    station[1],
                                    station[2]])
    mat_time = np.zeros((len(fault[:, 0, 0]), len(fault[0, :, 0])))
    for a in range(len(fault[:, 0, 0])):
        for b in range(len(fault[0, :, 0])):
            mat_time[a, b] = math.sqrt(pow(x_sta - fault[a, b, 0], 2)
                                    + pow(y_sta - fault[a, b, 1], 2)
                                    + pow(z_sta - fault[a, b, 2], 2))/velocity
    return mat_time

#normalisation avec max = 1
def norm1(vect):
    return [a/vect.max() for a in vect]

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
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
cpnt = param['component']
frq_bnd = param['frq_band']
hyp_bp = param['selected_waves']
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
             + frq_bnd + 'Hz_' + cpnt + '_smooth')
path_rslt_gnrl = (root_folder + '/'
                  + 'Kumamoto/'
                  + event + '/'
                  + 'results/'
                  + 'general')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + 'others')

# in case they do not exist, the following directories are created:
# - path_rslt
for d in [path_rslt]:
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print('Creation of the directory {} failed'.format(d))
        else:
            print('Successfully created the directory {}'.format(d))
    else:
        print('{} is already existing'.format(d))

# load picking delay dictionnary
os.chdir(path_rslt_gnrl)
with open(event + '_picking_delays', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_vel = mdpk.load()

# pick the correct sub dictionnary depending on the choice of the user through
# the run of parametres.py
if hyp_bp == 'P':
    vel_used = param['vP']
    dict_vel_used = dict_vel['delay_P']
elif hyp_bp == 'S':
    vel_used = param['vS']
    dict_vel_used = dict_vel['delay_S']
else:
    print('Issue with selected waves')

# pick all the envelopes from the directory path_data and sort them
lst_sta = os.listdir(path_data)
lst_sta.sort()

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

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

# identification of the station which started to record the first, it will
# be used as reference station (technically, any station can be reference
# station but this one is picked to deal with positive value only)
tstart_ref = None
os.chdir(path_data)
for s in lst_sta:
    st = read(s)
    if tstart_ref == None or tstart_ref - st[0].stats.starttime > 0:
        tstart_ref = st[0].stats.starttime

travt = {}
os.chdir(path_data)
for s in lst_sta:
    st = read(s)
    travt[st[0].stats.station] = (trav_time([st[0].stats.sac.stel,
                                             st[0].stats.sac.stla,
                                             st[0].stats.sac.stlo],
                                            coord_grid,
                                            vel_used))

# save the travel time dictionnary
os.chdir(path_rslt_gnrl)
with open(event + '_travel_time_dict', 'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(travt)

length_t = int(bp_len_t*bp_samp_rate)
stack = {}

print('Back projection method applied to the envelopes',
        'from {}'.format(path_data))
for ista, s in enumerate(lst_sta):
    os.chdir(path_data)
    # load the envelope
    st = read(s)
    # few parameters are stored because they will be used more than once
    tstart = st[0].stats.starttime
    sta_name = st[0].stats.station
    # the maximum of the envelope is set to 1
    env_norm = norm1(st[0].data)
    # x-axis corresponding to the trace
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    # interpolate the trace so we can assess a value even between two bins
    f = interpolate.interp1d(t, env_norm)
    # vectorize the interpolated function to be able to apply it over a
    # np.array
    npf = np.vectorize(f)
    # initialise 3D np.array which will contain back projection values for one
    # station
    bp1sta = []
    print('Processing of the station {}'.format(sta_name),
            '({}/{})'.format(ista + 1, len(lst_sta)),
            end = ' ')
    # loop over the time
    for it in range(length_t):
        # calculation of the real delay for a specific time
        # (specific time := t_origin_rupt - 5 + it/samp_rate
        #  which is different from previous travt that had calculated a
        #  relative delay between subgrids without knowing the absolute delay)
        # for one station, the following parameters are constant all over the
        # grid:
        # - tstart := st[0].stats.starttime, the starting time of the trace 
        # - t_origin_rupt which is the same among all stations because it is
        #   one of the event properties
        # - 5 is obviously a constant, it is introduced to start the back
        #   projection 5 sec before the start of the rupture
        # - samp_rate which is the frequency of back projection pictures and is
        #   also the same among all stations
        # however the variable "it" is changing on every time step but it still
        # the same among every single subgrid
        tshift = (travt[sta_name]
                  - (tstart - t_origin_rupt)
                  + dict_vel_used[sta_name]
                  - 5
                  + it/bp_samp_rate)
        tshift = np.where(tshift > 0, tshift, 0)
        tshift = np.where(tshift < t[-1], tshift, 0)
        # make a bigger np.array containing every time step of the back
        # projection of one station
        bp1sta.append(tshift)
    # store inside a dictionnary the back projection values of every station
    # at every time step on every subgrid
    stack[sta_name] = npf(bp1sta)
    print('done')

# save the back projection 4D cube in the path_rslt directory (4D because 2
# spatial dimensions (the grid), 1 temporal dimension (the time) and 1 network
# dimension (the stations))
# on purpose, the energy from every station is not directly summed up to allow
# different selection of stations without running the current code (the most
# time consuming) many times
os.chdir(path_rslt)
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
          + cpnt + '_smooth_' + hyp_bp + '_prestack',
          'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(stack)
