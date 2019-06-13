#

from obspy import read
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

print('####################################',
    '\n###   python3 plot_it_bpinv.py   ###',
    '\n####################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickler.Unpickler(mfch)
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
path_data_common = (root_folder + '/'
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
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
                + 'miscellaneous_plots/'
                + 'bpinv_traces_iteration')

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

lst_it = os.listdir(path_data_common)
lst_it = [a for a in lst_it if 'iteration' in a]

lst_sta = os.listdir(path_data_common + '/iteration-0')
lst_sta = [a for a in lst_sta if '.sac' in a]

for s in lst_sta:
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Normalized envelope')
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 1.1])
    for it in lst_it:
        os.chdir(path_data_common + '/' + it + '/smooth')
        st = read(s[:6] + '_inv_smooth_it-' + it[10:] + '.sac')
        tr = st[0]
        tr.normalize()
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax.plot(t, tr, lw = 0.1, color = 'black')
        ax.fill_betweent(t, 0, tr, lw = 0, color = 'black', alpha = 0.1)
    os.chdir(path_rslt)
    fig.savefig(s[:6] + '.pdf')
