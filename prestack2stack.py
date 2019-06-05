#

import os
import pickle
import numpy as np

print('#####################################',
    '\n###   python3 prestack2stack.py   ###',
    '\n#####################################')

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
angle = param['angle']
l_grid = param['l_grid']
w_grid = param['w_grid']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']
bp_len_t = param['bp_length_time']
bp_samp_rate = param['bp_samp_rate']

# directories used in this script
#
#
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + 'others')
path_sta = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'vel_env_selection/'
            + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + couronne + 'km_' + hyp_bp + '_' + angle + 'deg/'
             + 'others')

# create path_rslt directory in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path_rslt))
else:
    print('{} is already existing'.format(path_rslt))

# load the 4D back projection cube
os.chdir(path_data)
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt
          + '_smooth_' + hyp_bp + '_prestack',
          'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    prestack = mdpk.load()

lst_sta = os.listdir(path_sta)
lst_sta = [a for a in lst_sta if '.sac' in a]
stack = np.zeros((int(bp_len_t*bp_samp_rate),
                  int(l_grid/l_grid_step),
                  int(w_grid/w_grid_step)))

for s in lst_sta:
    stack = stack + prestack[s[:6]]

os.chdir(path_rslt)
with open(event + '_vel_env_' + frq_bnd + 'Hz_'
          + cpnt + '_smooth_' + couronne + 'km_'
          + hyp_bp + '_' + angle + 'deg_it-0_stack', 'wb') as mfch:
    mpck = pickle.Pickler(mfch)
    mpck.dump(stack)
