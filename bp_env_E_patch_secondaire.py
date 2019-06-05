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
l_smooth = param['smooth']

###########################
###########################
past = ''
#past = 'patch_85' # ce qui va avant slected_patch
pastpast = '' # a garder vide pour modifier a chaque fois la trace originelle
#pastpast = 'patch_85' # le dossier des fichiers utilises
###########################
###########################

if past != '':
    past = '_' + past
if pastpast != '':
    pastpast = '_' + pastpast

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
path_data_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_selection/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                    + 'brut')
path_rslt_mask = (root_folder + '/'
                  + 'Kumamoto/'
                  + event + '/'
                  + 'vel_env_selection/'
                  + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                        + couronne + 'km_' + hyp_bp + '_' azim + 'deg/'
                  + 'mask')
path_rslt_tr = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_selection/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                + 'modified')

# in the case they do not exist, the following directories are created:
# - path_rslt_mask
# - path_rslt_tr
for d in [path_rslt_mask,
          path_rslt_tr]:
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print('Creation of the directory {} failed'.format(d))
        else:
            print('Successfully created the directory {}'.format(d))
    else:
        print('{} is already existing'.format(d))

# load picking delay dictionnary
os.chdir(path_trvt)
with open(event + '_picking_delays', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_vel = mdpk.load()

# pick the correct sub dictionnary depending on the choice of the user through
# the run of parametres.py
if hyp_bp =='P':
    vel_used = param['vP']
    dict_vel_used = dict_vel['delay_P']
elif hyp_bp == 'S':
    vel_used = param['vS']
    dict_vel_used = dict_vel['delay_S']
else:
    print('Issue with selected waves')

# pick all the envelopes from the directory path_data_tr and sort them
lst_sta = os.listdir(path_data_tr)
lst_sta.sort()

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']
hypo = [R_Earth - dep_hyp, lat_hyp, lon_hyp]

# define the origin time of the rupture
yea_seis = int(dict_seis[event]['nFnet'][0:4])
mon_seis = int(dict_seis[event]['nFnet'][4:6])
day_seis = int(dict_seis[event]['nFnet'][6:8])
hou_seis = int(dict_seis[event]['nFnet'][8:10])
min_seis = int(dict_seis[event]['nFnet'][10:12])
sec_seis = int(dict_seis[event]['nFnet'][12:14])
mse_seis = int(dict_seis[event]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis,
                            mon_seis,
                            day_seis,
                            hou_seis,
                            min_seis,
                            sec_seis,
                            mse_seis)

# load the travel time dictionnary
os.chdir(path_trvt)
with open(event + '_travel_time_dict', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    travt = mdpk.load()

length_t = int(length_time*samp_rate)
prestack = {}

print('Back projection method applied to the modified envelopes',
        'from {}'.format(path_tr))
for ista, s in enumerate(lst_sta):
    # load the envelope
    os.chdir(path_data_tr)
    st = read(s)
    # few parameters are stored because they will be used more than once
    tstart = st[0].stats.starttime
    sta_name = st[0].stats.station
    # load the mask
    os.chdir(path_rslt_mask)
    msk = read(sta_name)
    if:
        tr = np.multiply(st[0].data, norm1(msk[0].data))
    else:
        tr = np.multiply(st[0].data, 1 - norm1(msk[0].data)
    tr[-1] = (st[0].data).max()
    os.chdir(path_rslt_tr)
    tr = Trace(np.asarray(tr), st[0].stats)
    tr.write(s + '_modified.sac', format = 'SAC')
    st = read(s + '_modified.sac')
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
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
                + cpnt + '_smooth_' + hyp_bp + '_prestack',
          'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(prestack)
