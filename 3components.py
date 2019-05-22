# combine in different ways the three components (EW, NS and UD) to create
# the following velocity waveforms:
# - 3cpn with EW, NS and UD to have the full velocity waveform
# - hori with EW and NS to have the horizontal velocity waveform
# - vert with UD to have the vertical velocity waveform
# the combination is the root sum squared: sqrt(sum(xi*xi))
# because of that the produced velocity waveforms are always positive but it is
# not problematic for the bp study since we are using envelopes (square of the
# velocity waveforms) so the sign of the velocity waveforms is not relevant

from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np
import pickle

print('##################################',
    '\n###   python3 3components.py   ###',
    '\n##################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
frq_bnd = param['frq_band']

# directories used in this script:
# - path_data is the directory with all the velocity waveforms that passed
# previous conditions
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + frq_bnd + 'Hz')
# - path_rslt is the list of directories where different combinations of the
# three original components (EW, NS and UD) will be stored
# -- 3 cpn is a combination of the 3 components (EW, NS and UD)
# -- hori is a combination of the 2 horizontal components (EW and NS)
# -- vert is the vertical component only (UD)
cpnt = ['3cpn', 'hori', 'vert']
path_r = (root_folder + '/'
          + 'Kumamoto/'
          + event + '/'
          + 'vel')
path_rslt = []
for cpn in cpnt:
    path_rslt.append(path_r + '/'
                     + frq_bnd + 'Hz_' + cpn)

# create the directories from the list path_rslt in case they do not exist
for pth in path_rslt:
    if not os.path.isdir(pth):
        try:
            os.makedirs(pth)
        except OSError:
            print('Creation of the directory {} failed'.format(pth))
        else:
            print('Successfully created the directory {}'.format(pth))
    else:
        print('{} is already existing'.format(pth))

# pick separately the stations depending on their component (EW, NS or UD)
lst_fch_x = [a for a in os.listdir(path_data) if 'EW' in a]
lst_fch_y = [a for a in os.listdir(path_data) if 'NS' in a]
lst_fch_z = [a for a in os.listdir(path_data) if 'UD' in a]

# sort the three lists so the n-element of each list is corresponding to the
# same station but for the three components
lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

print('Combination of the velocity waveforms')
for sx, sy, sz in zip(lst_fch_x, lst_fch_y, lst_fch_z):
    os.chdir(path_data)
    # load the three components at same time
    stx = read(sx)
    sty = read(sy)
    stz = read(sz)
    if (stx[0].stats.station == sty[0].stats.station
        and stx[0].stats.station == stz[0].stats.station):
        # remove the average mean value
        stx.detrend(type = 'constant')
        sty.detrend(type = 'constant')
        stz.detrend(type = 'constant')
        # tapering
        tr_x = stx[0]
        tr_y = sty[0]
        tr_z = stz[0]
        # creation of the different velocity waveforms (3cpn, hori and vert)
        tr3 = [math.sqrt(a**2 + b**2 + c**2)
               for a, b, c in zip(tr_x, tr_y, tr_z)]
        trh = [math.sqrt(a**2 + b**2) for a, b in zip(tr_x, tr_y)]
        trv = [math.sqrt(a**2) for a in tr_z]
        # preparation for SAC format
        tr3 = Trace(np.asarray(tr3), stz[0].stats)
        trh = Trace(np.asarray(trh), stz[0].stats)
        trv = Trace(np.asarray(trv), stz[0].stats)
        # save the files
        os.chdir(path_rslt[0])
        tr3.write(sx[:7] + cpnt[0] + sx[9:], format = 'SAC')
        os.chdir(path_rslt[1])
        trh.write(sx[:7] + cpnt[1] + sx[9:], format = 'SAC')
        os.chdir(path_rslt[2])
        trv.write(sx[:7] + cpnt[2] + sx[9:], format = 'SAC')
        print('The different component combinations',
                'of the station {}'.format(sx[:6]),
                'have been successfully done')
    else:
        print('The three velocity waveforms',
                '{}, {} and {}'.format(sx[:6], sy[:6], sz[:6]),
                'are not corresponding and combination can not be done')
