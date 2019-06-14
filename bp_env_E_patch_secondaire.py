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
it_nb_i = None
while not isinstance(it_nb_i, int):
    try:
        it_nb_i = int(input('Pick a number corresponding to the iteration you'
                            + ' want to use as input (interger): '))
    except ValueError:
        print('No valid number, try again')
it_nb_o = str(it_nb_i + 1)
it_nb_i = str(it_nb_i)
m_or_c = None
while m_or_c != 'M' and m_or_c != 'C':
    m_or_c = input('Choose if you want to apply the mask or its'
                    + 'complementary (M or C): ')

# in the case the complementary is choosen, intead of using the last iteration
# modified traces, the original traces are used
# we remove the selected patch to the original stack
path_data_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_modified/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
if m_or_c == 'M':
    path_data_tr = path_data_tr + '/iteration-' + it_nb_i
elif m_or_c == 'C':
    path_data_tr = path_data_tr + '/iteration-0'
else:
    print('Issue with m_or_c')
# however the used mask is always the one selected
path_data_mask = (root_folder + '/'
                  + 'Kumamoto/'
                  + event + '/'
                  + 'vel_env_bpinv/'
                  + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                        + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                  + 'iteration-' + it_nb_o + '/'
                  + 'smooth')
path_rslt_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_modified/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                + 'iteration-' + it_nb_o)
if m_or_c == 'M':
    path_rslt_tr = path_rslt_tr + '/iteration-' + it_nb_o
elif m_or_c == 'C':
    path_rslt_tr = path_rslt_tr + '/iteration-' + it_nb_o + '_patch_2'
else:
    print('Issue with m_or_c')

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
    msk = read(sta_name + '_inv_smooth_it-' + it_nb_o + '.sac')
    if m_or_c == 'M':
        tr = np.multiply(st[0].data, norm1(msk[0].data))
    elif m_or_c == 'C':
        tr = np.multiply(st[0].data, 1 - np.asarray(norm1(msk[0].data)))
    else:
        print('Issue between mask and complementary')
    tr[-1] = (st[0].data).max()
    os.chdir(path_rslt_tr)
    tr = Trace(np.asarray(tr), st[0].stats)
    if m_or_c == 'M':
        tr.write(sta_name + '_it-' + it_nb_o + '.sac', format = 'SAC')
        st = read(sta_name + '_it-' + it_nb_o + '.sac')
    elif m_or_c == 'C':
        tr.write(sta_name + '_it-' + it_nb_o + '_patch_2.sac', format = 'SAC')
        st = read(sta_name + '_it-' + it_nb_o + '_patch_2.sac', format = 'SAC')
    else:
        print('Issue between mask and complementary')
    # the maximum of the envelope is set to 1
    env_norm = norm1(st[0].data)
    # x-axis corresponding to the trace
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    # interpolate the trace so we can assess a value even between two bins
    f = interpolate.interp1d(t, env_norm)
    # vectorize the interpolated function to be able to apply it over a
    # np.array
    npf = np.vectorize(f)
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
    prestack[sta_name] = npf(bp1sta)
    print('done')

os.chdir(path_stck)
if m_or_c == 'M':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_o + '_prestack', 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(prestack)
elif m_or_c == 'C':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_o + '_patch_2_prestack', 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(prestack)
else:
    print('Issue between mask and complementary')
