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
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_abs_trvt = (root_folder + '/'
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

if not os.path.isdir(path_bpiv):
    try:
        os.makedirs(path_bpiv)
    except OSError:
        print('Creation of the directory {} failed'.format(path_bpiv))
    else:
        print('Successfully created the directory {}'.format(path_bpiv))
else:
    print('{} is already existing'.format(path_bpiv))

lst_iter = os.listdir(path_bpiv)
lst_iter = [a for a in lst_iter if 'iteration' in a]
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
                    + ' complementary (M or C): ')

path_bpiv_brut = (path_bpiv + '/'
                  + 'iteration-' + it_nb_o + '/'
                  + 'brut')
path_bpiv_smth = (path_bpiv + '/'
                  + 'iteration-' + it_nb_o + '/'
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

# load the stack from which inverse back projection traces will be created
os.chdir(path_data)
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
          + cpnt + '_smooth_' + couronne + 'km_'
          + hyp_bp + '_' + azim + 'deg_'
          + 'it-' + it_nb_i + '_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stack = mdpk.load()

# pick all the envelopes from the directory path_sta
lst_sta = os.listdir(path_sta)
lst_sta = [a for a in lst_sta if '.sac' in a]

# gaussienne
npts = 5001 # st[0].stats.npts
sampling_rate = 100.0 # st[0].stats.sampling_rate
vect = np.linspace(0,
                   npts/sampling_rate,
                   npts)
sigma = 1./bp_samp_rate
tr_gaus = [math.exp(- pow(a - 25, 2)/2/pow(sigma, 2)) for a in vect]

# creation of traces of inverse back projection
print('Creation of the back projection inverse traces')
for ista, s in enumerate(lst_sta):
    os.chdir(path_sta)
    st = read(s)
    sta_name = st[0].stats.station
    print('Processing of the station {}'.format(sta_name),
            '({} / {})'.format(ista + 1, len(lst_sta)),
            end = ' ')
    # first step, inversion of the back projection stack
    station = {}
    os.chdir(path_abs_trvt)
    with open(event + '_' + sta_name + '_absolute_delays', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        bp1sta = mdpk.load()
    for it in range(len(bp1sta)):
        for x in range(len(bp1sta[0][:, 0])):
            for y in range(len(bp1sta[0][0, :])):
                station[bp1sta[it][x, y]] = stack[it, x, y]
    # second step, creation of the trace
    bpiv_tr = np.zeros(st[0].stats.npts)
    for k in station.keys():
        bpiv_tr[int(k*100)] += station[k]
    os.chdir(path_bpiv_brut)
    tr = Trace(bpiv_tr, st[0].stats)
    tr.write(sta_name + '_inv_it-' + it_nb_o + '.sac', format = 'SAC')
    # third step, smoothing of the trace
    tr = np.convolve(tr, tr_gaus, mode = 'same')
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_bpiv_smth)
    tr.write(sta_name + '_inv_smooth_it-' + it_nb_o + '.sac', format = 'SAC')
    print('done')
