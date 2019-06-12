#

import matplotlib.pyplot as plt
import pickle

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

# directories used in this script
#
#
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
             + couronne = 'km_' + hyp_bp + '_' + azim + 'deg/'
             + 'miscellaneous_plots')

# create the directory path_rslt in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path-rslt))
else:
    print('{} is already existing'.format(path_rslt))

lst_it = os.listdir(path_data)
lst_it = [a for a in lst_it if '_stack' in a]

fig, ax = plt.subplots(1, 1)
os.chdir(path_data)
for it in lst_it:
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it[10:] + '_stack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        stck = mdpk.load()
    stck_mx = stck[:, :, :].max()
    ax.scatter(int(it[10:]), stck_mx)

os.chdir(path_rslt)
fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'max_fct_it.pdf')
