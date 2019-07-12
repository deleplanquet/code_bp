# transform accelerograms into velocity waveforms through fft/ifft process

from obspy import read
from obspy import Trace
import pickle
import numpy as np
import sys
import os
import math
import matplotlib.pyplot as plt

print('##############################',
    '\n###   python3 acc2vel.py   ###',
    '\n##############################')

# open the file of the parameters given by the user through parameters.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
R_Earth = param['R_Earth']
event = param['event']

# directories used in this script
# - path_data is the directory with all the records that passed previous
#   conditions
# - path_results is the directory where the velocity associated to each record
#   will be stored in SAC format
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'acc/'
             + 'inf100km_copy')
path_results = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel/'
                + 'brut')

# create the directory path_results in case it does not exist
if not os.path.isdir(path_results):
    try:
        os.makedirs(path_results)
    except OSError:
        print('Creation of the directory {} failed'.format(path_results))
    else:
        print('Successfully created the directory {}'.format(path_results))
else:
    print('{} is already existing'.format(path_results))

# pick separately the stations depending on their component (EW, NS or UD)
lst_fch_x = [a for a in os.listdir(path_data) if 'EW' in a]
lst_fch_y = [a for a in os.listdir(path_data) if 'NS' in a]
lst_fch_z = [a for a in os.listdir(path_data) if 'UD' in a]

# sort the three lists so the n-element of each list is corresponding to the
# same station but for the three components
lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

print('Transformation of the accelerograms into velocity waveforms')
for sx, sy, sz in zip(lst_fch_x, lst_fch_y, lst_fch_z):
    os.chdir(path_data)
    # load the three components at the same time
    stx = read(sx)
    sty = read(sy)
    stz = read(sz)
    os.chdir(path_results)
    for st in [stx, sty, stz]:
        # remove the average mean value
        st.detrend(type = 'constant')
        # remove very low frequencies
        st[0].filter('highpass', freq = 1./20)
        # pick only 50 s of the original trace from 5 s before the picked
        # P-arrival time
        tstart = stz[0].stats.starttime + stz[0].stats.sac.a - 5
        tend = tstart + 50
        tr = st[0].trim(tstart, tend, pad = True, fill_value = 0)
        # to be sure the beginning and the end of the trace have 0 value, this
        # is necessary to prevent high frequency to appear with fft
        st[0].taper(0.05, type = 'hann', max_length = None, side = 'both')
        # allocate the time to another place for future user
        st[0].stats.sac.nzyear = st[0].stats.starttime.year
        st[0].stats.sac.nzjday = st[0].stats.starttime.julday
        st[0].stats.sac.nzhour = st[0].stats.starttime.hour
        st[0].stats.sac.nzmin = st[0].stats.starttime.minute
        st[0].stats.sac.nzsec = st[0].stats.starttime.second
        st[0].stats.sac.nzmsec = st[0].stats.starttime.microsecond
        # change the value for the picked P and S-arrival time. Before the
        # original value is defined from the beginning of the trace, and
        # because we redefined the beginning of the trace, we adjust here the
        # values. The phases are picked on UD component, this is the reason of
        # using especially "stz"
        st[0].stats.sac.t0 = stz[0].stats.sac.t0 - stz[0].stats.sac.a + 5
        st[0].stats.sac.a = 5
        # fft
        t = np.arange(tr.stats.npts)/tr.stats.sampling_rate
        freq = (np.arange(1, tr.stats.npts + 1)
                *tr.stats.sampling_rate/tr.stats.npts)
        tf = np.fft.fft(tr)
        # from acc to vel in Fourier space
        tf_vel = tf*(-1j)/2/math.pi/freq
        # ifft
        tr_vel = np.fft.ifft(tf_vel)
        # save to SAC format
        tr_vel = Trace(tr_vel, tr.stats)
        tr_vel.write(st[0].stats.station + '_'
                     + st[0].stats.channel[:2]
                     + '_vel.sac',
                     format = 'SAC')
    print('Accelerograms of the station {}'.format(stx[0].stats.station),
            'are now transformed into velocity waveforms')
