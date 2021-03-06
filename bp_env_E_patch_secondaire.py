#

import numpy as np
import pickle
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
import sys
from scipy import interpolate
from scipy.signal import hilbert
from obspy import read
from obspy.signal.util import smooth
from scipy import ndimage
from obspy import Trace
from obspy.core import UTCDateTime
#from mpl_toolkits.basemap import Basemap

#normalisation avec max = 1
def norm1(vect):
    return [a/vect.max() for a in vect]

print('################################################',
    '\n###   python3 bp_env_E_patch_secondaire.py   ###',
    '\n################################################')

#recuperation position stations
print('     recuperation position stations')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
frq_bnd = param['frq_band']
cpnt = param['component']
couronne = param['hypo_interv']
hyp_bp = param['selected_waves']
azim = param['angle']
R_Earth = param['R_Earth']
l_grid = param['l_grid']
w_grid = param['w_grid']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']
bp_samp_rate = param['bp_samp_rate']
bp_len_t = param['bp_length_time']
#selected_patch = 'patch_85'
l_smooth = param['l_smooth']

# directories used in this script
#
#
#
path_trvt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'general')

path_tr = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'vel_env_modified/'
            + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')

lst_mdf_env = os.listdir(path_tr)
lst_mdf_env = [a for a in lst_mdf_env if 'it' in a]
lst_mdf_env.sort()
print('Here is a list of the modified envelopes that has already been built: ')
for f in lst_mdf_env:
    print(f)
mdf_env_name_i = None
while mdf_env_name_i not in lst_mdf_env:
    mdf_env_name_i = input('Name of the modified envelope you want to use to'
                            + ' create the next prestack (copy/paste from the'
                            + ' above list): ')
path_data_tr = path_tr + '/' + mdf_env_name_i

path_data_mask = (root_folder + '/'
                  + 'Kumamoto/'
                  + event + '/'
                  + 'vel_env_bpinv/'
                  + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                        + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
lst_msk = os.listdir(path_data_mask)
lst_msk = [a for a in lst_msk if 'it' in a]
lst_msk.sort()
print('Here is a list of the inverse back projection traces that have already',
        'been done: ')
for f in lst_msk:
    print(f)
msk_name = None
while msk_name not in lst_msk:
    msk_name = input('Name of the mask you want to use to create the next'
                        + ' prestack (copy/paste from the above list): ')
path_data_mask = path_data_mask + '/' + msk_name + '/smooth'

mdf_env_name_o = None
while mdf_env_name_o in lst_mdf_env or mdf_env_name_o == None:
    mdf_env_name_o = input('Name of the modified envelope this code will'
                            + ' create (input: {}): '.format(mdf_env_name_i))
path_rslt_tr = path_tr + '/' + mdf_env_name_o

path_stck = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'others')
lst_iter = os.listdir(path_stck)
lst_iter = [a for a in lst_iter if '_it-' in a and '_stack' in a]
lst_iter.sort()
print('Here is a list of the iterations of back projection that has already',
        'been done:')
for f in lst_iter:
    print(f)
stck_name_o = None
while stck_name_o in lst_iter or stck_name_o == None:
    stck_name_o = input('Name of the stack that will be create with the'
                        + ' current code: ')

m_or_c = None
while m_or_c != 'M' and m_or_c != 'C':
    m_or_c = input('Choose if you want to apply the mask or its'
                    + 'complementary (M or C): ')

# in the case they do not exist, the following directories are created:
# - path_rslt_tr
for d in [path_rslt_tr]:
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print('Creation of the directory {} failed'.format(d))
        else:
            print('Successfully created the directory {}'.format(d))
    else:
        print('{} is already existing'.format(d))

# pick all the envelopes from the directory path_data_tr and sort them
lst_sta = os.listdir(path_data_tr)
lst_sta = [a for a in lst_sta if '.sac' in a]
lst_sta.sort()

print(path_data_mask)
lst_msk = os.listdir(path_data_mask)
lst_msk = [a for a in lst_msk if '.sac' in a]
lst_msk.sort()

print(len(lst_sta), len(lst_msk))

length_t = int(bp_len_t*bp_samp_rate)
prestack = {}

print('Back projection method applied to the modified envelopes',
        'from {}'.format(path_data_tr))
for ista, s in enumerate(lst_sta):
    # load the envelope
    os.chdir(path_data_tr)
    st = read(s)
    # few parameters are stored because they will be used more than once
    sta_name = st[0].stats.station
    # load the mask
    os.chdir(path_data_mask)
    msk = read(lst_msk[ista])
    if m_or_c == 'M':
        tr = np.multiply(st[0].data, norm1(msk[0].data))
    elif m_or_c == 'C':
        tr = np.multiply(st[0].data, 1 - np.asarray(norm1(msk[0].data)))
    else:
        print('Issue between mask and complementary')
    tr[-1] = (st[0].data).max()
    os.chdir(path_rslt_tr)
    tr = Trace(np.asarray(tr), st[0].stats)
    tr.write(sta_name + '.sac', format = 'SAC')
    st = read(sta_name + '.sac')
    # the maximum of the envelope is set to 1
    env_norm = norm1(st[0].data)
    # x-axis corresponding to the trace
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    # interpolate the trace so we can assess a value even between two bins
    f = interpolate.interp1d(t, env_norm)
    # initialise 3D np.array which will contain back projection values for
    # one station
    bp1sta = []
    print('Processing of the station {}'.format(sta_name),
            '{} / {}'.format(ista + 1, len(lst_sta)),
            end = ' ')
    os.chdir(path_trvt)
    with open(event + '_' + sta_name + '_absolute_delays', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        bp1sta = mdpk.load()
    prestack[sta_name] = f(bp1sta)
    print('done')

os.chdir(path_stck)
with open(stck_name_o, 'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(prestack)
