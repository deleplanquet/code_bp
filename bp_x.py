from obspy import read
import math
import pickle
from scipy import interpolate
import numpy as np
import os
import sys

def d2r(angle):
    return angle*math.pi/180

def r2d(angle):
    return angle*180/math.pi

def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

def milieu(lat1, lon1, lat2, lon2):
    x1, y1, z1 = geo2cart(1, lat1, lon1)
    x2, y2, z2 = geo2cart(1, lat2, lon2)
    xm = x1 + x2
    ym = y1 + y2
    zm = z1 + z2
    return [r2d(math.asin(zm/math.sqrt(xm*xm + ym*ym +zm*zm))),
    	    r2d(math.acos(xm/math.sqrt(xm*xm + ym*ym)))]

def fault(cen_fault, length, u_strike, pas):
    x_cf, y_cf, z_cf = geo2cart(cen_fault[0], cen_fault[1], cen_fault[2])
    x_fault = np.arange(-length/2/pas, length/2/pas)
    grill_fault = np.zeros((len(x_fault), 1, 3))
    for a in x_fault:
    	grill_fault[np.where(x_fault==a), 0, 0] = x_cf + a*pas*u_strike[0]
    	grill_fault[np.where(x_fault==a), 0, 1] = y_cf + a*pas*u_strike[1]
    	grill_fault[np.where(x_fault==a), 0, 2] = z_cf + a*pas*u_strike[2]
    return grill_fault

def trav_time(station, fault, velocity):
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000, station[1], station[2])
    mat_time = np.zeros((len(fault[:, 0, 0])))
    for a in range(len(fault[:, 0, 0])):
    	mat_time[a] = math.sqrt(pow(x_sta - fault[a, 0, 0], 2)
    	    	    	    	+ pow(y_sta - fault[a, 0, 1], 2)
    	    	    	    	+ pow(z_sta - fault[a, 0, 2], 2))/velocity
    return mat_time

def norm1(vect):
    return [10*a/vect.max() for a in vect]

R_Earth = 6400
vel_used = 3.4

dossier = sys.argv[1]
dt_type = sys.argv[2]

if dt_type != '3comp' and dt_type != 'hori' and dt_type != 'vert':
    print('ERROR TYPO')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_2_4Hz_' + dt_type + '_env'
path_results = path_data + '_results'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = os.listdir(path_data)

os.chdir(path)
with open(dossier + '_veldata', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_vel = my_dpck.load()

dict_vel_used = dict_vel[1]

dict_delai = dict_vel[2]

strike = 224 
dip = 65 
L_fault = 60

lat_fault = [32.6477, 32.9858]
lon_fault = [130.7071, 131.1216]
dep_fault = [9, 9]

pas = 2

lat_cen_fault, lon_cen_fault = milieu(lat_fault[0], lon_fault[0], lat_fault[1], lon_fault[1])
x1_flt, y1_flt, z1_flt = geo2cart(R_Earth - dep_fault[0], lat_fault[0], lon_fault[0])
x2_flt, y2_flt, z2_flt = geo2cart(R_Earth - dep_fault[1], lat_fault[1], lon_fault[1])
vect_strike = [x2_flt - x1_flt, y2_flt - y1_flt, z2_flt - z1_flt]

coord_fault = fault([R_Earth, lat_cen_fault, lon_cen_fault], L_fault, norm(vect_strike), pas)

travt = []

os.chdir(path_data)
for fich in lst_fch:
    st = read(fich)
    travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], coord_fault, vel_used))

#ARF?

length_t = int(30*st[0].stats.sampling_rate)
stack = np.zeros((int(L_fault/pas), length_t))

t_start_ref = None
for cles in dict_delai.keys():
    if t_start_ref == None or t_start_ref > dict_delai[cles]:
    	t_start_ref = dict_delai[cles]

for fich in lst_fch:
    print('     ', fich)
    st = read(fich)
    tstart = st[0].stats.starttime
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    f = interpolate.interp1d(t, env_norm)

    for ix in range(int(L_fault/pas)):
    	for it in range(length_t):
    	    tshift = t_start_ref - dict_delai[st[0].stats.station] + travt[lst_fch.index(fich)][ix] + dict_vel_used[st[0].stats.station] + it/st[0].stats.sampling_rate
    	    if tshift > 0 and tshift < t[-1]:
    	    	stack[ix, it] = stack[ix, it] + 1./len(lst_fch)*f(tshift)

os.chdir(path_results)
with open('stack_vel_2_4Hz_' + dt_type + '_env', 'wb') as my_fch_stk:
    my_pck_stk = pickle.Pickler(my_fch_stk)
    my_pck_stk.dump(stack)





























