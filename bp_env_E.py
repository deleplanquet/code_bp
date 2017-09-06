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
    y_fault = np.arange(0, width/pasy)
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
    return [10*a/vect.max() for a in vect]

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

#recuperation position stations
print('     recuperation position stations')

dossier_seisme = sys.argv[1]
dt_type = sys.argv[2]
select_station = sys.argv[3]

#dossier_seisme = dossier_seisme[0:-1]
print('     ', dossier_seisme, dt_type, select_station)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier_seisme

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []

for freq in lst_frq:
    pth_dt = path + '/' + dossier_seisme + '_vel_' + freq + 'Hz/' + dossier_seisme + '_vel_' + freq + 'Hz'
    lst_pth_dt.append(pth_dt + '_' + dt_type + '_env_' + select_station)

path_results = path + '/' + dossier_seisme + '_results'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_pth_fch = []

for freq in lst_frq:
    lst_pth_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

os.chdir(path)
with open(dossier_seisme + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

#constantes
R_Earth = 6400
v_P = 5.8
v_S = 3.4

vel_used = v_S
dict_vel_used = dict_vel[1]

dict_delai = dict_vel[2]

print(vel_used)
print('vP', v_P, 'vS',  v_S)

#recuperation position faille
strike = 224
dip = 65
l_fault = 56
w_fault = 24
lat_fault = [32.6477, 32.9858]
long_fault = [130.7071, 131.1216]
pas_l = 2
pas_w = 2

#placement de la faille
print('     localisation de la faille en volume')

lat_cen_fault, long_cen_fault = milieu(lat_fault[0], long_fault[0], lat_fault[1], long_fault[1])
dir_cen_fault = [math.cos(d2r(lat_cen_fault))*math.cos(d2r(long_cen_fault)), math.cos(d2r(lat_cen_fault))*math.sin(d2r(long_cen_fault)), math.sin(d2r(lat_cen_fault))]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(long_cen_fault)), -math.cos(d2r(long_cen_fault)), 0])
vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
vect_dip = rotation(vect_perp_strike, dip, vect_strike)

coord_fault = fault([6400, lat_cen_fault, long_cen_fault], l_fault, w_fault, norm(vect_strike), norm(vect_dip), pas_l, pas_w)

#stacks
print('     stacks envelop')

os.chdir(lst_pth_dt[0])
st = read(lst_pth_fch[0][0])
#pas_t = st[0].stats.sampling_rate
pas_t = 10
length_t = int(30*pas_t)

tstart_ref = None
for cles in dict_delai.keys():
    if tstart_ref == None or tstart_ref > dict_delai[cles]:
    	tstart_ref = dict_delai[cles]

for freq in lst_frq:
    os.chdir(lst_pth_dt[lst_frq.index(freq)])

    travt = []
    for fichier in lst_pth_fch[lst_frq.index(freq)]:
    	st = read(fichier)
    	travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], coord_fault, vel_used))

    stack = np.zeros((int(l_fault/pas_l), int(w_fault/pas_w), length_t))

    for station in lst_pth_fch[lst_frq.index(freq)]:
    	st = read(station)
    	tstart = st[0].stats.starttime
    	env_norm = norm1(st[0].data)
    	t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    	f = interpolate.interp1d(t, env_norm)

    	ista = lst_pth_fch[lst_frq.index(freq)].index(station)
    	print('     ', station, str(ista + 1), '/', len(lst_pth_fch[lst_frq.index(freq)]))

    	for ix in range(int(l_fault/pas_l)):
    	    for iy in range(int(w_fault/pas_w)):
    	    	for it in range(length_t):
    	    	    tshift = tstart_ref + dict_delai[st[0].stats.station] + travt[ista][ix, iy] + dict_vel_used[st[0].stats.station] + it/pas_t
    	    	    if tshift > 0 and tshift < t[-1] - pas_t/st[0].stats.sampling_rate:
    	    	    	for itt in range(int(st[0].stats.sampling_rate/pas_t)):
    	    	    	    stack[ix, iy, it] = stack[ix, iy, it] + 1./len(lst_pth_fch[lst_frq.index(freq)])*f(tshift + itt/st[0].stats.sampling_rate)

    os.chdir(path_results)
    with open(dossier_seisme + '_vel_' + freq + 'Hz_' + dt_type + '_env_' + select_station + '_stack2D', 'wb') as my_fch:
    	my_pck = pickle.Pickler(my_fch)
    	my_pck.dump(stack)
