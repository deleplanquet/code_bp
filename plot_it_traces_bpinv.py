#

from obspy import read
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from cycler import cycler

print('###########################################',
    '\n###   python3 plot_it_traces_bpinv.py   ###',
    '\n###########################################')

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
lst_it = [a for a in lst_it if 'it-' in a if 'ptch' not in a]
#lst_it = [a for a in lst_it if 'it-' in a if 'ptch' in a]
lst_it.sort()

lst_sta = os.listdir(path_tr_bpiv + '/it-1/smooth')
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
    os.chdir(path_tr_modf + '/iteration-0')
    st = read(s[:6] + '_it-0.sac')
    tr = st[0]
    tr.normalize()
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[0].plot(t, tr, lw = 0.3, color = 'black', label = 'it-0')
    ax[0].fill_between(t, 0, tr, lw = 0, color = 'black', alpha = 0.1)
    ax[0].set_prop_cycle(cycler('color',
                                ['b', 'c', 'yellowgreen', 'y', 'r']))
    ax[1].set_prop_cycle(cycler('color',
                                ['b', 'c', 'yellowgreen', 'y', 'r']))
    for it in lst_it:
        lst_pth = [path_tr_modf + '/' + it,
                   path_tr_bpiv + '/' + it + '/smooth']
        lst_sta_fil = [s[:6] + '.sac',
                       s[:6] + '_inv_smooth.sac']
        for axnb, (path, sta_file) in enumerate(zip(lst_pth, lst_sta_fil)):
            os.chdir(path)
            st = read(sta_file)
            tr = st[0]
            tr.normalize()
            t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
            ax[axnb].plot(t, tr, lw = 0.3, label = it)
            ax[axnb].fill_between(t, 0, tr,
                                  lw = 0,
                                  color = 'black',
                                  alpha = 0.1)
    ax[0].legend(fontsize = 10, loc = 1)
    ax[1].legend(fontsize = 10, loc = 1)
    os.chdir(path_rslt)
    fig.savefig(s[:6] + '.pdf')
