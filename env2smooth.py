# smoothing of the envelopes

from obspy import read
from obspy.signal.util import smooth
from obspy import Trace
import sys
import os
import numpy as np
import pickle

print('#################################',
    '\n###   python3 env2smooth.py   ###',
    '\n#################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
couronne = param['hypo_interv']
frq_bnd = param['frq_band']
cpnt = param['component']
l_smooth = param['l_smooth']

# directories used in this script
# - path_data is the directory of the envelopes that passed previous conditions
# - path_rslt is the directory where the smoothed envelopes will be stored
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env_smooth')

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

# pick the envelopes from the directory path_data
lst_fch = os.listdir(path_data)

print('Smoothing of the envelopes')
for s in lst_fch:
    os.chdir(path_data)
    # load the envelope
    st = read(s)
    # smooth the envelope
    tr = smooth(st[0].data, int(l_smooth/st[0].stats.delta))
    # preparation for SAC format
    tr = Trace(tr, st[0].stats)
    # save the file
    os.chdir(path_rslt)
    tr.write(s[:-4] + '_smooth.sac', format = 'SAC')
    print('The envelope of the station {}'.format(s[:6]),
            'has been successfully smoothed')
