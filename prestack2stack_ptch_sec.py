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
             + couronne + 'km_' + hyp_bp + '_' + angle + 'deg/'
             + 'others')
path_sta = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'vel_env_selection/'
            + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg')

list_iter = os.listdir(path_data)
list_iter = [ a for a in list_iter if '_it-' in a and 'prestack' in a]
list_iter.sort()
print('Here is a list of the iterations of back projection prestack that has',
        'already been done:')
for f in list_iter:
    print(f)
it_nb_i = None
while not isinstance(it_nb_i, int):
    try:
        it_nb_i = int(input('Pick a number corresponding to the iteration you'
                            + ' want to use as input (interger): '))
    except ValueError:
        print('No valid number, try again')
it_nb_i = str(it_nb_i)
m_or_c = None
while m_or_c != 'M' and m_or_c != 'C':
    m_or_c = input('Choose if you want to get the mask or its complementary'
                    + ' (M or C): ')

# load the 4D back projection cube
os.chdir(path_data)
if m_or_c == 'M':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg_'
                + 'it-' + it_nb_i + '_prestack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        prestack = mdpk.load()
elif m_or_c == 'C':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg_'
                + 'it-' + it_nb_i + '_patch_2_prestack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        prestack = mdpk.load()
else:
    print('Issue between mask and complementary')

lst_sta = os.listdir(path_sta)
lst_sta = [a for a in lst_sta if '.sac' in a]
stack = np.zeros((int(bp_len_t*bp_samp_rate),
                  int(l_grid/l_grid_step),
                  int(w_grid/w_grid_step)))

for s in lst_sta:
    stack = stack + prestack[s[:6]]

os.chdir(path_data)
if m_or_c == 'M':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg_'
                + 'it-' + it_nb_i + '_stack', 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(stack)
elif m_or_c == 'C':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + angle + 'deg_'
                + 'it-' + it_nb_i + '_patch_2_stack', 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(stack)
