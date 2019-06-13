#

from obspy import read
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

print('###########################################',
    '\n###   python3 plot_it_traces_bpinv.py   ###',
    '\n###########################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb')as mfch:
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
path_tr_modf = (root_folder +'/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_modified/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_tr_bpiv = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_bpinv/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_rslt = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'results/'
                + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
                + couronne + 'km_' + hyp_bp + '_' +azim + 'deg/'
                + 'miscellaneous_plots/'
                + 'modif_plots_and_bpinv_traces_iteration')

# create the directory path_rslt in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} faided'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path_rslt))
else:
    print('{} is already existing'.format(path_rslt))

lst_it = os.listdir(path_tr_bpiv)
lst_it = [a for a in lst_it if 'iteration' in a]

lst_sta = os.listdir(path_tr_bpiv + '/iteration-1/smooth')
lst_sta = [a for a in lst_sta if '.sac' in a]

for s in lst_sta:
    fig, ax = plt.subplots(2, 1)
    ax[1].set_xlabel('Time (s)')
    ax[0].set_ylabel('Normalized envelope')
    ax[1].set_ylabel('Back projection inverse trace')
    ax[0].set_xlim([0, 30])
    ax[1].set_xlim([0, 30])
    ax[0].set_ylim([0, 1.1])
    ax[1].set_ylim([0, 1.1])
    for it in lst_it:
        os.chdir(path_tr_modf + '/' + it)
        st = read(s[:6] + '_it-' + it[10:] + '.sac')
        tr = st[0]
        tr.normalize()
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[0].plot(t, tr, lw = 0.1, color = 'black')
        ax[0].fill_between(t, 0, tr, lw = 0, color = 'black', alpha = 0.1)
        os.chdir(path_tr_bpiv + '/' + it + '/smooth')
        st = read(s[:6] + '_inv_smooth_it-' + it[10:] + '.sac')
        tr = st[0]
        tr.normalize()
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[1].plot(t, tr, lw = 0.1, color = 'black')
        ax[1].fill_between(t, 0, tr, lw = 0, color = 'black', alpha = 0.1)
    os.chdir(path_rslt)
    fig.savefig(s[:6] + '.pdf')