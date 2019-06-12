#

import matplotlib.pyplot as plt
import os
import pickle
import numpy as np
from obspy import read
#from scipy.integrate import trapz

print('##########################################',
    '\n###   python3 plot_station_fct_it.py   ###',
    '\n##########################################')

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

# directories used in this script
#
#
path_data = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_modified/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_rslt = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'results/'
                + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                + 'miscellaneous_plots/'
                + 'stations_fct_iterations')

# create the directory path_rslt in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path_rslt))
else:
    print('{} is already created'.format(path_rslt))

lst_it = os.listdir(path_data)
lst_it = [a for a in lst_it if 'iteration' in a]
itx = np.linspace(0, len(lst_it) - 1, len(lst_it))

lst_sta = os.listdir(path_data + '/iteration-0')
lst_sta = [a for a in lst_sta if '.sac' in a]

for s in lst_sta:
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Number of iterations')
    ax.set_ylabel('')
    ax.set_xlim([0, 1.1*len(lst_it)])
    ax.set_ylim([0, 1.1])
    tr_mx = np.zeros(len(lst_it))
    integ = np.zeros(len(lst_it))
    for it in lst_it:
        os.chdir(path_data + '/' + it)
        st = read(s[:6] + '_it-' + it[10:] + '.sac')
        tr = st[0]
        tr_mx[int(it[10:])] = tr[:int(30*st[0].stats.sampling_rate)].max()
        integ[int(it[10:])] = np.trapz(tr, dx = st[0].stats.sampling_rate)
    tr_mx = [a/tr_mx.max() for a in tr_mx]
    integ = [a/integ.max() for a in integ]
    ax.scatter(itx, tr_mx, s = 10, color = 'red', label = 'maximum value')
    ax.scatter(itx, integ, s = 10, color = 'blue', label = 'integration')
    ax.legend(fontsize = 10, loc = 1)
    os.chdir(path_rslt)
    fig.savefig(s[:6] + '_max_and_integ_eveloution.pdf')
