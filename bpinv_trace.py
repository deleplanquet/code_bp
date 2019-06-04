#

import os
import pickle
from obspy import read
from obspy import Trace
from obspy.core import UTCDateTime
import numpy as np
import math

print('##################################',
    '\n###   python3 bpinv_trace.py   ###',
    '\n##################################')

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
bp_samp_rate = param['bp_samp_rate']

# directories used in this script
#
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'others')
path_sta = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'vel_env_selection/'
            + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
            + 'brut')
path_trvt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'general')
path_bpiv = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env_bpinv/'
             + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_bpiv_brut = (path_bpiv + '/'
                  + 'brut')
path_bpiv_smth = (path_bpiv + '/'
                  + 'smooth')

# in case they do not exist, the following directories are created:
# - path_bpiv_brut
# - path_bpiv_smth
for d in [path_bpiv_brut,
          path_bpiv_smth]:
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

if hyp_bp == 'P':
    dict_vel_used = dict_vel['delay_P']
elif hyp_bp == 'S':
    dict_vel_used = dict_vel['delay_S']
else:
    print('Issue with selected waves')

# load parameters of studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

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

# load the stack from which inverse back projection traces will be created
os.chdir(path_data)
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
          + cpnt + '_smooth_' + couronne + 'km_'
          + hyp_bp + '_' + azim + 'deg_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stack = mdpk.load()

# pick all the envelopes from the directory path_sta
lst_sta = os.listdir(path_sta)

# gaussienne
npts = 5001 # st[0].stats.npts
sampling_rate = 100.0 # st[0].stats.sampling_rate
vect = np.linspace(0,
                   npts/sampling_rate,
                   npts)
sigma = 1./bp_samp_rate
tr_gaus = [math.exp(- pow(a - 25, 2)/2/pow(sigma, 2)) for a in vect]

# load the travel time dictionnary
os.chdir(path_trvt)
with open(event + '_travel_time_dict', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    travt = mdpk.load()

# creation of traces of inverse back projection
for ista, s in enumerate(lst_sta):
    os.chdir(path_sta)
    st = read(s)
    sta_name = st[0].stats.station
    tstart = st[0].stats.starttime
    # first step, inversion of the back projection stack
    station = {}
    for it in range(len(stack[:, 0, 0])):
        tshift = (travt[sta_name]
                  - (tstart - t_origin_rupt)
                  + dict_vel_used[sta_name]
                  - 5
                  + it/bp_samp_rate)
        for x in range(len(tshift[:, 0])):
            for y in range(len(tshift[0, :])):
                station[tshift[x, y]] = stack[it, x, y]
    # second step, creation of the trace
    bpiv_tr = np.zeros(st[0].stats.npts)
    for k in station.keys():
        bpiv_tr[int(k*100)] += station[k]
    os.chdir(path_bpiv_brut)
    tr = Trace(bpiv_tr, st[0].stats)
    tr.write(sta_name, format = 'SAC')
    # third step, smoothing of the trace
    tr = np.convolve(tr, tr_gaus, mode = 'same')
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_bpiv_smth)
    tr.write(sta_name, format = 'SAC')
