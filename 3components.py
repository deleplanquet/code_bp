from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np
import pickle

print('')
print('      python3 3components.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km')

pth_dt = (path_data + '_'
          + frq + 'Hz/'
          + dossier
          + '_vel_'
          + couronne + 'km_'
          + frq + 'Hz')

pth_rslt = pth_dt + '_3comp'
pth_rslt_h = pth_dt + '_hori'
pth_rslt_v = pth_dt + '_vert'

if os.path.isdir(pth_rslt) == False:
    os.makedirs(pth_rslt)
if os.path.isdir(pth_rslt_h) == False:
    os.makedirs(pth_rslt_h)
if os.path.isdir(pth_rslt_v) == False:
    os.makedirs(pth_rslt_v)

lst_fch_x = []
lst_fch_y = []
lst_fch_z = []

lst_fch_x = [a for a in os.listdir(pth_dt) if ('EW' in a) == True]
lst_fch_y = [a for a in os.listdir(pth_dt) if ('NS' in a) == True]
lst_fch_z = [a for a in os.listdir(pth_dt) if ('UD' in a) == True]

lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

for station in lst_fch_x:
    os.chdir(pth_dt)
    stx = read(station)
    sty = read(lst_fch_y[lst_fch_x.index(station)])
    stz = read(lst_fch_z[lst_fch_x.index(station)])
    if stx[0].stats.station == sty[0].stats.station and stx[0].stats.station == stz[0].stats.station:
        stx.detrend(type = 'constant')
        sty.detrend(type = 'constant')
        stz.detrend(type = 'constant')
        tr_x = stx[0]
        tr_y = sty[0]
        tr_z = stz[0]
        trh = [math.sqrt(a**2 + b**2) for a,b in zip(tr_x, tr_y)]
        tr3 = [math.sqrt(a**2 + b**2 + c**2) for a,b,c in zip(tr_x, tr_y, tr_z)]
        os.chdir(pth_rslt_v)
        trv = Trace(np.asarray(tr_z), stz[0].stats)
        trv.write(station[:6]
                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_vert.sac', format = 'SAC')
        os.chdir(pth_rslt_h)
        trh = Trace(np.asarray(trh), stz[0].stats)
        trh.write(station[:6]
                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_hori.sac', format = 'SAC')
        os.chdir(pth_rslt)
        tr3 = Trace(np.asarray(tr3), stz[0].stats)
        tr3.write(station[:6]
                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz.sac', format = 'SAC')
    else:
        print('     ', stx[0].stats.station, sty[0].stats.station, stz[0].stats.station)

