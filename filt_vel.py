from obspy import read
import numpy as np
from obspy import Trace
import os
import sys
import pickle

print('')
print('      python3 filt_vel.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
fqmi = param['freq_min']
fqma = param['freq_max']
bdfrq = param['band_freq']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km')

pth_rslt = (path_data + '_'
            + bdfrq + 'Hz/'
            + dossier
            + '_vel_'
            + couronne + 'km_'
            + bdfrq + 'Hz')

if os.path.isdir(pth_rslt) == False:
    os.makedirs(pth_rslt)

lst_fch_x = [a for a in os.listdir(path_data) if ('EW' in a) == True]
lst_fch_y = [a for a in os.listdir(path_data) if ('NS' in a) == True]
lst_fch_z = [a for a in os.listdir(path_data) if ('UD' in a) == True]

lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

for station in lst_fch_x:
    os.chdir(path_data)

    stx = read(station)
    sty = read(lst_fch_y[lst_fch_x.index(station)])
    stz = read(lst_fch_z[lst_fch_x.index(station)])

    stx.detrend(type = 'constant')
    sty.detrend(type = 'constant')
    stz.detrend(type = 'constant')

    stx[0].taper(0.05,
                 type = 'hann',
                 max_length = None,
                 side = 'both')
    sty[0].taper(0.05,
                 type = 'hann',
                 max_length = None,
                 side = 'both')
    stz[0].taper(0.05,
                 type = 'hann',
                 max_length = None,
                 side = 'both')

    tr_x = stx[0].filter('bandpass',
                         freqmin = fqmi,
                         freqmax = fqma,
                         corners = 4,
                         zerophase = False)
    tr_y = sty[0].filter('bandpass',
                         freqmin = fqmi,
                         freqmax = fqma,
                         corners = 4,
                         zerophase = False)
    tr_z = stz[0].filter('bandpass',
                         freqmin = fqmi,
                         freqmax = fqma,
                         corners = 4,
                         zerophase = False)

    stx[0].stats.sac.a = stz[0].stats.sac.a
    stx[0].stats.sac.t0 = stz[0].stats.sac.t0
    sty[0].stats.sac.a = stz[0].stats.sac.a
    sty[0].stats.sac.t0 = stz[0].stats.sac.t0

    tr_x = Trace(np.asarray(tr_x),
                 stx[0].stats)
    tr_y = Trace(np.asarray(tr_y),
                 sty[0].stats)
    tr_z = Trace(np.asarray(tr_z),
                 stz[0].stats)

    os.chdir(pth_rslt)
    tr_x.write(station[:-4] + '_' + bdfrq + 'Hz.sac', format = 'SAC')
    tr_y.write(lst_fch_y[lst_fch_x.index(station)][:-4] + '-' + bdfrq + 'Hz.sac', format = 'SAC')
    tr_z.write(lst_fch_z[lst_fch_x.index(station)][:-4] + '-' + bdfrq + 'Hz.sac', format = 'SAC')


























