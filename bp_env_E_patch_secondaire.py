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
#from mpl_toolkits.basemap import Basemap

#fonctions

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion angle radian -> degre
def r2d(angle):
    return angle*180/math.pi

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#normalisation
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

#rotation 3d d'angle theta et d'axe passant par l'origine porte par le vecteur
#(a, b, c) de norme 1, repere orthonormal direct
def rotation(u, theta, OM):
    """ attention OM unitaire """
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    radian = d2r(theta)
    #coefficients de la matrice de rotation
    mat = array([[a*a + (1 - a*a)*math.cos(radian),
                  a*b*(1 - math.cos(radian)) - c*math.sin(radian),
                  a*c*(1 - math.cos(radian)) + b*math.sin(radian)],
                 [a*b*(1 - math.cos(radian)) + c*math.sin(radian),
                  b*b + (1 - b*b)*math.cos(radian),
                  b*c*(1 - math.cos(radian)) - a*math.sin(radian)],
                 [a*c*(1 - math.cos(radian)) - b*math.sin(radian),
                  b*c*(1 - math.cos(radian)) + a*math.sin(radian),
                  c*c + (1 - c*c)*math.cos(radian)]])
    #rearrangement du vecteur auquel on applique la rotation
    vect = array([[u[0]],
                  [u[1]],
                  [u[2]]])
    #rotation du vecteur u de theta autour de OM
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])

#bissectrice en 3d
def milieu(lat1, long1, lat2, long2):
    x1, y1, z1 = geo2cart(1, lat1, long1)
    x2, y2, z2 = geo2cart(1, lat2, long2)
    x_m = x1 + x2
    y_m = y1 + y2
    z_m = z1 + z2
    return [r2d(math.asin(z_m/math.sqrt(x_m*x_m + y_m*y_m + z_m*z_m))),
            r2d(math.acos(x_m/math.sqrt(x_m*x_m + y_m*y_m)))]

#calcul de la matrice des tps de trajet pour une station
def fault(cen_fault, length, width, u_strike, u_dip, pasx, pasy):
    x_cf, y_cf, z_cf = geo2cart(cen_fault[0], cen_fault[1], cen_fault[2])
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
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000, station[1], station[2])
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
        y_data[i] = 1./(sigma*math.sqrt(2))*math.exp(-(x_data[i] - mu)*(x_data[i] - mu)
                                                        /(2*sigma*sigma))
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

#union d'intervalles
def interv_uni(list_inter):
    list_debut = [ a[0] for a in list_inter]
    list_fin = [ a[1] for a in list_inter]
    list_debut.sort()
    list_fin.sort()
    list_inter_final = []
    nb_superp = 0
    debut_inter_courant = 0
    while list_debut:
        if list_debut[0] < list_fin[0]:
            pos_debut = list_debut.pop(0)
            if nb_superp == 0:
                debut_inter_courant = pos_debut
            nb_superp += 1
        elif list_debut[0] > list_fin[0]:
            pos_fin = list_fin.pop(0)
            nb_superp -= 1
            if nb_superp == 0:
                list_inter_final.append([debut_inter_courant, pos_fin])
        else:
            list_debut.pop(0)
            list_fin.pop(0)
    if list_fin:
        pos_fin = list_fin[-1]
        list_inter_final.append([debut_inter_courant, pos_fin])
    return list_inter_final

print('################################################',
    '\n###   python3 bp_env_E_patch_secondaire.py   ###',
    '\n################################################')

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
frq_bnd = param['frq_band']
cpnt = param['component']
couronne = param['hypo_interv']
hyp_bp = param['selected_waves']
azim = param['angle']
R_Earth = param['R_Earth']
l_grid = param['l_grid']
w_grid = param['w_grid']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']
bp_samp_rate = param['bp_samp_rate']
bp_len_t = param['bp_length_time']
#selected_patch = 'patch_85'
l_smooth = param['smooth']

###########################
###########################
past = ''
#past = 'patch_85' # ce qui va avant slected_patch
pastpast = '' # a garder vide pour modifier a chaque fois la trace originelle
#pastpast = 'patch_85' # le dossier des fichiers utilises
###########################
###########################

if past != '':
    past = '_' + past
if pastpast != '':
    pastpast = '_' + pastpast

# directories used in this script
#
#
#
path_trvt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'general')
path_stck = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'others')
path_data_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_selection/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                    + 'brut')
path_rslt_mask = (root_folder + '/'
                  + 'Kumamoto/'
                  + event + '/'
                  + 'vel_env_selection/'
                  + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                        + couronne + 'km_' + hyp_bp + '_' azim + 'deg/'
                  + 'mask')
path_rslt_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_selection/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                + 'modified')

# in the case they do not exist, the following directories are created:
# - path_rslt_mask
# - path_rslt_tr
for d in [path_rslt_mask,
          path_rslt_tr]:
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
os.chdir(path_trvt)
with open(event + '_picking_delays', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_vel = mdpk.load()

# pick the correct sub dictionnary depending on the choice of the user through
# the run of parametres.py
if hyp_bp =='P':
    vel_used = param['vP']
    dict_vel_used = dict_vel['delay_P']
elif hyp_bp == 'S':
    vel_used = param['vS']
    dict_vel_used = dict_vel['delay_S']
else:
    print('Issue with selected waves')

# pick all the envelopes from the directory path_data_tr and sort them
lst_sta = os.listdir(path_data_tr)
lst_sta.sort()

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']
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

# load the travel time dictionnary
os.chdir(path_trvt)
with open(event + '_travel_time_dict', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    travt = mdpk.load()

length_t = int(length_time*samp_rate)
stack = {}

print('Back projection method applied to the modified envelopes',
        'from {}'.format(path_tr))
for ista, s in enumerate(lst_sta):
    # load the envelope
    os.chdir(path_data_tr)
    st = read(s)
    # few parameters are stored because they will be used more than once
    tstart = st[0].stats.starttime
    sta_name = st[0].stats.station
    # load the mask
    os.chdir(path_rslt_mask)
    msk = read(sta_name)
    if:
        tr = np.multiply(st[0].data, norm1(msk[0].data))
    else:
        tr = np.multiply(st[0].data, 1 - norm1(msk[0].data)
    tr[-1] = (st[0].data).max()
    os.chdir(path_rslt_tr)
    tr = Trace(np.asarray(tr), st[0].stats)
    tr.write(s + '_modified.sac', format = 'SAC')
    st = read(s + '_modified.sac')
    #st = read(station[:-4] + '_' + selected_patch + scis + '.sac')
    #tstart = st[0].stats.starttime
    # the maximum of the envelope is set to 1
    env_norm = norm1(st[0].data)
    # x-axis corresponding to the trace
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    # interpolate the trace so we can assess a value even between two bins
    f = interpolate.interp1d(t, env_norm)
    # vectorize the interpolated function to be able to apply it over a
    # np.array
    npf = np.vectorize(f)
    # initialise 3D np.array which will contain back projection values for
    # one station
    bp1sta = []
    print('Processing of the station {}'.format(sta_name),
            '{} / {}'.format(ista + 1, len(lst_sta)),
            end = ' ')
    for it in range(length_t):
        tshift = (travt[sta_name]
                  - tstart - t_origin_rupt
                  + dict_vel_used[sta_name]
                  - 5
                  + it/bp_samp_rate)
        tshift = np.where(tshift > 0, tshift, 0)
        tshift = np.where(tshift < t[-1], tshift, 0)
        # make a bigger np.array containing every time step of the back
        # projection of one station
        bp1sta.append(npf(tshift))
    stack[sta_name] = bp1sta
    print('done')

os.chdir(path_stck)
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
                + cpnt + '_smooth_' + hyp_bp + '_prestack',
          'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(stack)

###############################
# bp inverse
###############################

'''
stckmx = stack[0][:, :, :].max()
thresh = int(selected_patch[-2:]) *0.01

for sta in lst_fch:
    os.chdir(path_data_1)
    st = read(sta)
    #print(sta, st[0].stats.starttime, dict_vel_used[st[0].stats.station], t_origin_rupt)
    ista = lst_fch.index(sta)
    station = {}
    for i in range(len(stack[1][:, 0, 0])):
        for j in range(len(stack[1][0, :, 0])):
            for k in range(len(stack[1][0, 0, :])):
                tshift = (travt[ista][i,j]
                          - (st[0].stats.starttime - t_origin_rupt)
                          + dict_vel_used[st[0].stats.station]
                          - 5
                          + k/samp_rate)
                station[tshift] = stack[0][i, j, k]
    os.chdir(path_bpinv)
    with open(st[0].stats.station, 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(station)

lst_bpinv = os.listdir(path_bpinv)

for sta in lst_fch:
    os.chdir(path_data_1)
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

vect = np.linspace(0, st[0].stats.npts/st[0].stats.sampling_rate, st[0].stats.npts)
sigma = 1./samp_rate

for sta in lst_fch:
    os.chdir(path_bpinvtr)
    st = read(sta[:6])
    dst, azm = dist_azim([st[0].stats.sac.stla, st[0].stats.sac.stlo], [lat_hyp, lon_hyp])
    trg = [math.exp(-(pow(a - 25, 2))/(2*pow(sigma, 2))) for a in vect]
    tr = np.convolve(st[0].data, trg, mode = 'same')
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_bpinvsm)
    tr.write(sta[:6], format = 'SAC')
'''
