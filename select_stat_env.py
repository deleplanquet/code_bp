import math
from obspy import read
import os
import sys
from obspy import Trace
import numpy as np
import pickle

print('')
print('      python3 select_stat_env.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
rSP = param['ratioSP']

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth'
path_results_P = path_data + '_P'
path_results_S = path_data + '_S'

if os.path.isdir(path_results_P) == False:
    os.makedirs(path_results_P)
if os.path.isdir(path_results_S) == False:
    os.makedirs(path_results_S)

lst_fch = []

lst_fch = os.listdir(path_data)

for station in lst_fch:
    os.chdir(path_data)
    stP = read(station)
    stS = read(station)
    arrival_P = stP[0].stats.starttime + stP[0].stats.sac.a
    arrival_S = stS[0].stats.starttime + stS[0].stats.sac.t0
    delai_PS = arrival_S - arrival_P
    if delai_PS < 5:
        stP[0].trim(arrival_P, arrival_P + delai_PS + 0.1)
    else:
        stP[0].trim(arrival_P, arrival_P + 5)
    stS[0].trim(arrival_S, stS[0].stats.endtime)
    trP = stP[0]
    trS = stS[0]
    rapport_PS = math.log10(trS.max()/trP.max())
    #print(trS.max()/trP.max())
    if rapport_PS > math.log10(rSP):
        #print('   S')
        st = read(station)
        os.chdir(path_results_S)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format = 'SAC')
    if rapport_PS < math.log10(1./rSP):
        #print('   P')
        st = read(station)
        os.chdir(path_results_P)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format = 'SAC')














