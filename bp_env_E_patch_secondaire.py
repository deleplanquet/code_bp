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

#rotation 3d d'angle theta et d'axe passant par l'origine porte par le vecteur (a, b, c) de norme 1, repere orthonormal direct
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
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 0] = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 1] = y_cf + a*pasx*u_strike[1] + b*pasy*u_dip[1]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 2] = z_cf + a*pasx*u_strike[2] + b*pasy*u_dip[2]
    return grill_fault

#calcul de la matrice des tps de trajet pour une station
def trav_time(station, fault, velocity):
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000, station[1], station[2])
    mat_time = np.zeros((len(fault[:, 0])))
    for a in range(len(fault[:, 0])):
        mat_time[a] = math.sqrt(pow(x_sta - fault[a, 0], 2)
                                        + pow(y_sta - fault[a, 1], 2)
                                        + pow(z_sta - fault[a, 2], 2))/velocity
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
        y_data[i] = 1./(sigma*math.sqrt(2))*math.exp(-(x_data[i] - mu)*(x_data[i] - mu)/(2*sigma*sigma))
    return y_data

#calcul distance et azimuth d'un point par rapport a un autre
''' distance et azimuth de B par rapport a A -> dist_azim(A, B) '''
def dist_azim(ptA, ptB):
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))/(math.cos(latA)*math.sin(dist_rad)))
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

#recuperation position stations
print('     recuperation position stations')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

#dossier = param['dossier']
dossier = '20160414212600'

path = path_origin + '/Kumamoto/' + dossier

os.chdir(path)
with open(dossier + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

dt_type = param['composante']
hyp_bp = param['ondes_select']
couronne = param['couronne']
azim = param['angle']
frq = param['band_freq']
R_Earth = param['R_Earth']
if hyp_bp == 'P':
    vel_used = param['vP']
    dict_vel_used = dict_vel[0]
elif hyp_bp == 'S':
    vel_used = param['vS']
    dict_vel_used = dict_vel[1]
#if param['fault'] == 0:
#    strike = param['strike']
#    dip = param['dip']
#    l_fault = param['l_fault']
#    w_fault = param['w_fault']
#    pas_l = param['pas_l']
#    pas_w = param['pas_w']
samp_rate = param['samp_rate']
length_time = param['length_t']

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_data_2 = path_data + '_patch09_1'
path_results = path + '/' + dossier + '_results/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz'
path_results_2 = path_results + '/Traces_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'

if os.path.isdir(path_data_2) == False:
    os.makedirs(path_data_2)

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

if os.path.isdir(path_results_2) == False:
    os.makedirs(path_results_2)

lst_fch = []

lst_fch = os.listdir(path_data)
lst_fch.sort()

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

yea_seis = int(dict_seis[dossier]['nFnet'][0:4])
mon_seis = int(dict_seis[dossier]['nFnet'][4:6])
day_seis = int(dict_seis[dossier]['nFnet'][6:8])
hou_seis = int(dict_seis[dossier]['nFnet'][8:10])
min_seis = int(dict_seis[dossier]['nFnet'][10:12])
sec_seis = int(dict_seis[dossier]['nFnet'][12:14])
mse_seis = int(dict_seis[dossier]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis, mon_seis, day_seis, hou_seis, min_seis, sec_seis, mse_seis)

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']

os.chdir(path)
nbr_sfaults = file_length(dossier + '_subfault_positions.txt')
coord_fault = np.zeros((nbr_sfaults, 3))
cf_tmp = None
cpt = 0

with open(dossier + '_subfault_positions.txt', 'r') as myf:
    for line in myf:
        spliit = line.split(' ')
        spliit = [i for i in spliit if i != '']
        cf_tmp = geo2cart(R_Earth - float(spliit[2]), float(spliit[0]), float(spliit[1]))
        coord_fault[cpt, 0] = cf_tmp[0]
        coord_fault[cpt, 1] = cf_tmp[1]
        coord_fault[cpt, 2] = cf_tmp[2]
        cpt = cpt + 1

#if param['fault'] == 0:
#    dir_cen_fault = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)), math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)), math.sin(d2r(lat_hyp))]
#    vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])
#    vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
#    vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
#    vect_dip = rotation(vect_perp_strike, dip, vect_strike)

#    coord_fault = fault([R_Earth - dep_hyp, lat_hyp, lon_hyp], l_fault, w_fault, norm(vect_strike), norm(vect_dip), pas_l, pas_w)
#else:
#    coord_fault = np.zeros((10, 16, 3))
#    ttmppp = 0
#    tmmp = 0
#    cf_tmp = None

#    with open(param['fault'], 'r') as myf:
#        myf.readline()
#        for line in myf:
#            spliit = line.split(' ')
#            spliit = [i for i in spliit if i != '']
#            if ttmppp >= 16:
#                ttmppp = 0
#                tmmp = tmmp + 1
#            cf_tmp = geo2cart(R_Earth - float(spliit[2]), float(spliit[0]), float(spliit[1]))
#            coord_fault[tmmp, ttmppp, 0] = cf_tmp[0]
#            coord_fault[tmmp, ttmppp, 1] = cf_tmp[1]
#            coord_fault[tmmp, ttmppp, 2] = cf_tmp[2]
#            ttmppp = ttmppp + 1
#    coord_fault[0, 0, 0] = 0
#    coord_fault[0, 1, 0] = 0
#    coord_fault[0, 10, 0] = 0
#    coord_fault[0, 13, 0] = 0
    #cf_tmp = None
    #cf_tmp = coord_fault
    #for i in range(10):
    #    for j in range(6):
    #        for k in range(3):
    #            coord_fault[i, 10+j, k] = cf_tmp[9-i, 15-j, 0]
    #print(coord_fault)
    
length_t = int(length_time*samp_rate)

tstart_ref = None

os.chdir(path_data)
for fichier in lst_fch:
    st = read(fichier)
    if tstart_ref == None or tstart_ref - st[0].stats.starttime > 0:
        tstart_ref = st[0].stats.starttime
        
os.chdir(path_data)
travt = []
tmin = None
dmin = None
for fichier in lst_fch:
    st = read(fichier)
    travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], coord_fault, vel_used))
    if dmin == None or dmin > st[0].stats.sac.dist:
        dmin = st[0].stats.sac.dist
    if tmin == None or tmin > st[0].stats.sac.t0:
        tmin = st[0].stats.sac.t0
print(tmin)

identified_patch = {}

os.chdir(path)
with open(dossier + '_premier_patch_09', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_ok = my_dpck.load()

os.chdir(path_data)
for station in lst_fch:
    list_inter = []
    st = read(station)
    ista = lst_fch.index(station)
    for ix in dict_ok.keys():
        for it in dict_ok[ix]:
            ix = int(ix)
            tshift = travt[ista][ix] - (st[0].stats.starttime - t_origin_rupt) + dict_vel_used[st[0].stats.station] - 5 + it/samp_rate
            list_inter.append([tshift, tshift + 1.01/samp_rate])
    identified_patch[st[0].stats.station] = interv_uni(list_inter)

for station in identified_patch.keys():
    print(station, identified_patch[station][0][0], identified_patch[station][0][1])

for station in lst_fch:
    os.chdir(path_data)
    st = read(station)
    tr = st[0].data
    cpt = 0
    for dat in tr:
        cpt = cpt + 1
        time = cpt/st[0].stats.sampling_rate
        if time >= identified_patch[st[0].stats.station][0][0] and time <= identified_patch[st[0].stats.station][0][1]:
            #tr[cpt] = 0.2*tr[cpt]
            tr[cpt] = math.pi/4*math.cos(math.pi*(time - identified_patch[st[0].stats.station][0][0])/(identified_patch[st[0].stats.station][0][1] - identified_patch[st[0].stats.station][0][0]))*tr[cpt]
    os.chdir(path_data_2)
    st[0].stats.sac.user6 = identified_patch[st[0].stats.station][0][0]
    st[0].stats.sac.user7 = identified_patch[st[0].stats.station][0][1]
    tr_reg = Trace(np.asarray(tr), st[0].stats)
    tr_reg.write(station[:-4] + '_1er_patch09.sac', format = 'SAC')

stack = np.zeros((nbr_sfaults, len(lst_fch), length_t))
for station in lst_fch:
    os.chdir(path_data)
    st = read(station)
    tstart = st[0].stats.starttime
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    f = interpolate.interp1d(t, env_norm)

    ista = lst_fch.index(station)
    print('     ', station, st[0].stats.sampling_rate, str(ista + 1), '/', len(lst_fch))

    for ix in range(nbr_sfaults):
        for it in range(length_t):
            tshift = travt[ista][ix] - (st[0].stats.starttime - t_origin_rupt) + dict_vel_used[st[0].stats.station] - 5 + it/samp_rate
            if tshift > 0 and tshift < t[-1]:
                if tshift >= identified_patch[st[0].stats.station][0][0] and tshift <= identified_patch[st[0].stats.station][0][1]:
                    stack[ix, ista, it] = math.pi/4*math.cos(math.pi*(tshift - identified_patch[st[0].stats.station][0][0])/(identified_patch[st[0].stats.station][0][1] - identified_patch[st[0].stats.station][0][0]))*f(tshift)
                    #stack[ix, ista, it] = 0.2*f(tshift)
                else:
                    stack[ix, ista, it] = f(tshift)

#if param['fault'] == 0:
#    stack = np.zeros((int(l_fault/pas_l), int(w_fault/pas_w), length_t))
#    for station in lst_fch:
#        os.chdir(path_data)
#        st = read(station)
#        tstart = st[0].stats.starttime
#        env_norm = norm1(st[0].data)
#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        f = interpolate.interp1d(t, env_norm)

#        ista = lst_fch.index(station)
#        print('     ', station, st[0].stats.sampling_rate, str(ista + 1), '/', len(lst_fch))

#        for ix in range(int(l_fault/pas_l)):
#    	    for iy in range(int(w_fault/pas_w)):
#    	        for it in range(length_t):
#                    tshift = travt[ista][ix, iy] - (st[0].stats.starttime - t_origin_rupt) + dict_vel_used[st[0].stats.station] - 5 + it/samp_rate
#                    if ix == 0 and iy == 0 and it == 0:
#                        st[0].stats.sac.user1 = 0
#                        st[0].stats.sac.user2 = 0
#                        st[0].stats.sac.user3 = 0
#                    if tshift > 0 and tshift < t[-1]:
#                        stack[ix, iy, it] = stack[ix, iy, it] + 1./len(lst_fch)*f(tshift)
#                        if ix == 24 and iy == 9 and it == 60:
#                            st[0].stats.sac.user1 = tshift
#                        if ix == 26 and iy == 9 and it == 80:
#                            st[0].stats.sac.user2 = tshift
#                        if ix == 22 and iy == 9 and it == 97:
#                            st[0].stats.sac.user3 = tshift

#else:
#    stack = np.zeros((len(coord_fault[:, 0, 0]), len(coord_fault[0, :, 0]), length_t))
#    for station in lst_fch:
#        os.chdir(path_data)
#        st = read(station)
#        tstart = st[0].stats.starttime
#        env_norm = norm1(st[0].data)
#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        f = interpolate.interp1d(t, env_norm)

#        ista = lst_fch.index(station)
#        print('     ', station, st[0].stats.sampling_rate, str(ista + 1), '/', len(lst_fch))

#        for ix in range(len(coord_fault[:, 0, 0])):
#    	    for iy in range(len(coord_fault[0, :, 0])):
#    	        for it in range(length_t):
#                    tshift = travt[ista][ix, iy] - (st[0].stats.starttime - t_origin_rupt) + dict_vel_used[st[0].stats.station] - 5 + it/samp_rate
#                    if ix == 0 and iy == 0 and it == 0:
#                        st[0].stats.sac.user1 = 0
#                        st[0].stats.sac.user2 = 0
#                        st[0].stats.sac.user3 = 0
#                    if tshift > 0 and tshift < t[-1]:
#                        stack[ix, iy, it] = stack[ix, iy, it] + 1./len(lst_fch)*f(tshift)
#                        if ix == 24 and iy == 9 and it == 60:
#                            st[0].stats.sac.user1 = tshift
#                        if ix == 26 and iy == 9 and it == 80:
#                            st[0].stats.sac.user2 = tshift
#                        if ix == 22 and iy == 9 and it == 97:
#                            st[0].stats.sac.user3 = tshift


#    tr = Trace(st[0].data, st[0].stats)
#    os.chdir(path_results_2)
#    tr.write(station, format = 'SAC')

os.chdir(path_results)
with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack3D_patch_09', 'wb') as my_fch:
    my_pck = pickle.Pickler(my_fch)
    my_pck.dump(stack)









#lat_fault = [32.6477, 32.9858]
#long_fault = [130.7071, 131.1216]

#lat_cen_fault, long_cen_fault = milieu(lat_fault[0], long_fault[0], lat_fault[1], long_fault[1])
