#

from obspy import read
import numpy as np
from obspy import Trace
import os
import sys
import pickle

print('###############################',
    '\n###   python3 filt_vel,py   ###',
    '\n###############################')

# open the file of the parameters given by the user through parameters.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
couronne = param['hypo_interv']
frq_min = param['frq_min']
frq_max = param['frq_max']
frq_bnd = param['frq_band']

path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz')

# create the directory path_rslt in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path_rslt))
else:
    print('{} is already existing'.format(path_rslt))

lst_fch_x = [a for a in os.listdir(path_data) if 'EW' in a]
lst_fch_y = [a for a in os.listdir(path_data) if 'NS' in a]
lst_fch_z = [a for a in os.listdir(path_data) if 'UD' in a]

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
    tr_y.write(lst_fch_y[lst_fch_x.index(station)][:-4] + '_' + bdfrq + 'Hz.sac', format = 'SAC')
    tr_z.write(lst_fch_z[lst_fch_x.index(station)][:-4] + '_' + bdfrq + 'Hz.sac', format = 'SAC')


























