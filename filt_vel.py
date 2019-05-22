# filtering of the velocity waveforms

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
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
frq_min = param['frq_min']
frq_max = param['frq_max']
frq_bnd = param['frq_band']

# directories used in this script:
# - path_data is the directory with all the velocity waveforms that passed
# previous conditions
# - path_rslt is the directory where the filtered velocity waveforms will be
# stored
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + 'brut')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + frq_bnd + 'Hz')

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

# pick separately the stations depending on their component (EW, NS or UD)
lst_fch_x = [a for a in os.listdir(path_data) if 'EW' in a]
lst_fch_y = [a for a in os.listdir(path_data) if 'NS' in a]
lst_fch_z = [a for a in os.listdir(path_data) if 'UD' in a]

# sort the three lists so the n-element of each list is corresponding to the
# same station but for the three components
lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

print('Filtering of the velocity waveforms between {}'.format(frq_min),
        'and {} Hz'.format(frq_max))
for sx, sy, sz in zip(lst_fch_x, lst_fch_y, lst_fch_z):
    os.chdir(path_data)
    # load the three components at same time
    stx = read(sx)
    sty = read(sy)
    stz = read(sz)
    os.chdir(path_rslt)
    for s, st in zip([sx, sy, sz], [stx, sty, stz]):
        # remove the average mean value
        st.detrend(type = 'constant')
        # to be sure the beginning and the ned of the trace have 0 value, not
        # sure it is really necessary because we don't use fft here but it does
        # not have significant effect since the beginning and the end of the
        # velocity waveforms are not relevants (the beginning is before the
        # beginning of the rupture, -5 s before P-arrival time, and the end
        # is 50 s later, too late for our study)
        st[0].taper(0.05,
                    type = 'hann',
                    max_length = None,
                    side = 'both')
        # filter the velocity waveform in the frequency band given by user
        # through parametres.py
        tr = st[0].filter('bandpass',
                          freqmin = frq_min,
                          freqmax = frq_max,
                          corners = 4,
                          zerophase = False)
        # save to SAC format
        tr = Trace(np.asarray(tr), st[0].stats)
        tr.write(s[:-4] + '_' + frq_bnd + 'Hz.sac', 
                 format = 'SAC')
    print('Velocity waveforms of the station {}'.format(stx[0].stats.station),
            'have been filtered between {}'.format(frq_min),
            'and {} Hz'.format(frq_max))
