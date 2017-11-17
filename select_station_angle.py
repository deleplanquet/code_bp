import sys
import os
from obspy import read
from obspy import Trace
import math
import pickle

def d2r(angle):
    return angle*math.pi/180

def r2d(angle):
    return angle*180/math.pi

def dist_azim(ptA, ptB, R):
    '''distance et azimuth de B par rapport a A -> dist_azim(A, B)'''
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))/(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R*dist_rad, r2d(angle_brut)
    else:
        return R*dist_rad, 360 - r2d(angle_brut)

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']
R_Earth = param['R_Earth']
azim_min = param['angle_min']
azim_max = param['angle_max']

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp
path_results = path_data + '_' + azim + 'deg'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = []

lst_fch = os.listdir(path_data)

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']

for station in lst_fch:
    print('     ', station)
    os.chdir(path_data)
    st = read(station)
    d_btw_st, az_btw_st = dist_azim([lat_hyp, lon_hyp], [st[0].stats.sac.stla, st[0].stats.sac.stlo], R_Earth)
    print('        ', d_btw_st, az_btw_st)
    if az_btw_st > azim_min and az_btw_st < azim_max:
        print('           ', 'ok')
        os.chdir(path_results)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format = 'SAC')
    elif az_btw_st > (azim_min + 180) and az_btw_st < (azim_max + 180):
        print('           ', 'ok')
        os.chdir(path_results)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format = 'SAC')



