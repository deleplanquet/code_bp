# check the azimuth between each station and the hypocenter of the considered
# event (selected by the user through parametres.py). The station will be
# considered for back projection study only if the corresponding azimuth
# belongs to a specific range of azimuth given by user through parametres.py

import sys
import os
from obspy import read
from obspy import Trace
import math
import pickle

print('########################################',
    '\n###   python3 select_stat_angle.py   ###',
    '\n########################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
couronne = param['hypo_interv']
frq_bnd = param['frq_band']
cpnt = param['component']
hyp_bp = param['selected_waves']
azim = param['angle']
R_Earth = param['R_Earth']
azim_min = param['angle_min']
azim_max = param['angle_max']

# directories used in this script
# - path_data is the directory of the envelopes that passed previous selections
# - path_rslt is the directory of the envelopes that will pass the azimuth
# selection of the current script
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env_selection/'
             + frq_bnd + 'Hz_' + cpnt + '_smooth_' + couronne + 'km_' + hyp_bp)
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env_selection/'
             + frq_bnd + 'Hz_' + cpnt + '_smooth_' + couronne + 'km_' + hyp_bp
                + '_' + azim + 'deg')

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

# load location of the studied earthquake
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

lat_hyp = dict_seis[event]['lat']
lon_hyp = dict_seis[event]['lon']
dep_hyp = dict_seis[event]['dep']

# pick the envelopes from the directory path_data
lst_fch = os.listdir(path_data)

print('Checking azimuth between stations and hypocenter')
for s in lst_fch:
    os.chdir(path_data)
    # load the envelope
    st = read(s)
    # load the azimuth previously calculated through the run of
    # station_inf_100km.py
    azm = st[0].stats.sac.az
    print('The azimuth of {}'.format(s[:6]),
            'in relation to the hypocenter {}, {}'.format(lat_hyp, lon_hyp),
            'is equal to {:.2f} deg'.format(azm))
    # if the azimuth belongs to the range of azimuth specified by the user, the
    # station is selected and saved in path_rslt directory
    if ((azm > azim_min and azm < azim_max)
        or (azm > (azim_min + 180) and azm < (azim_max + 180))):
        #print('           ', 'ok')
        os.chdir(path_rslt)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s, format = 'SAC')
        print('   {:.2f} \u2208'.format(azm),
            '[{}, {}]\u222a[{}, {}]'.format(azim_min, azim_max,
                                            azim_min + 180, azim_max + 180),
            '--> station selected for back projection')
    # if the station does not fulfill the selection criteria, it will not be
    # considered for back projection study
    else:
        print('   {:.2f} \u2209'.format(azm),
            '[{}, {}]\u222a[{}, {}]'.format(azim_min, azim_max,
                                            azim_min + 180, azim_max + 180),
            '--> station NOT selected for back projection')
