from obspy import read
from obspy.signal.util import smooth
from obspy import Trace
import sys
import os
import numpy as np
import pickle

print('')
print('      python3 env2smooth.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
l_smooth = param['smooth']

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env'
path_results = path_data + '_smooth'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = []

lst_fch = os.listdir(path_data)

for station in lst_fch:
    os.chdir(path_data)
    st = read(station)
    tr = Trace(smooth(st[0].data, int(l_smooth/st[0].stats.delta)), st[0].stats)
    os.chdir(path_results)
    tr.write(station[:-4] + '_smooth.sac', format = 'SAC')




