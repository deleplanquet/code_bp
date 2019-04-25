#

from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle

print('##############################',
    '\n###   python3 vel2env.py   ###',
    '\n##############################')

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

#
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'brut')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env')

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

# pick the velocity waveforms from the directory path_data
lst_fch = os.listdir(path_data)

print('Creation of envelopes')
for s in lst_fch:
    os.chdir(path_data)
    st = read(s)
    tr = [a**2 for a in st[0].data]
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_rslt)
    tr.write(s[:-4] + '_env.sac', format = 'SAC')
    print('The envelope of the station {}'.format(s[:6]),
            'has been successfully done')
