#

import matplotlib.pyplot as plt
import pickle
import os
import numpy as np

print('##########################################',
    '\n###   python3 plot_maxstck_fct_it.py   ###',
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
l_grid = param['l_grid']
w_grid = param['w_grid']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']

# directories used in this script
#
#
path_nb_it = (root_folder + '/'
              + 'Kumamoto/'
              + event + '/'
              + 'results/'
              + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
              + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'others')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'miscellaneous_plots')

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

# load the original back projection stack to get the maximum
os.chdir(path_data)
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'it-0_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stck_orgn = mdpk.load()

stck_or_mx = stck_orgn[:, :, :].max()

lst_it = os.listdir(path_nb_it)
lst_it = [a for a in lst_it if 'iteration-' in a]

fig1, ax1 = plt.subplots(1, 1)
ax1.set_xlabel('Number of iterations')
ax1.set_ylabel('Global maximum of the stack\n'
                + '(normalized by iteration 0 value)')
ax1.set_xlim([0, 1.1*len(lst_it)])
ax1.set_ylim([0, 1.1])
fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel('Along strike (km)')
ax2.set_ylabel('Down dip (km)')
ax2.set_xlim([-l_grid*l_grid_step/2, l_grid*l_grid_step/2])
ax2.set_ylim([-w_grid*w_grid_step/2, w_grid*w_grid_step/2])
os.chdir(path_data)
for it in lst_it:
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it[10:] + '_stack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        stck = mdpk.load()
    stck_mx = stck[:, :, :].max()
    ax1.scatter(int(it[10:]), stck_mx/stck_or_mx, s = 10, color = 'black')
    # red star with white border for the hypocenter
    ax2.scatter(0, 0, 250, marker = '*', color = 'white', lw = 0.2, zorder = 0)
    ax2.scatter(0, 0, 150, marker = '*', color = 'red', lw = 0.2, zorder = 1)
    ax2.scatter(np.where(stck == stck_mx)[1] - l_grid/2 + int(it[10:])/10,
                np.where(stck == stck_mx)[2] - w_grid/2,
                s = 3,
                color = 'black',
                zorder = 2)

os.chdir(path_rslt)
fig1.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'max_fct_it.pdf')
fig2.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'posmax_fct_it.pdf')
