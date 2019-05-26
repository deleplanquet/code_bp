# make a copie of the records in SAC format of the stations which hypocenter
# distance is between hypo_min and hypo_max
# hypo_min and hypo_max are user choosed through running parameters.py

import pickle
from obspy import read
import sys
import os
import math
from obspy import Trace

print('######################################',
    '\n###   python3 select_couronne.py   ###',
    '\n######################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
R_Earth = param['R_Earth']
event = param['event']
frq_bnd = param['frq_band']
cpnt = param['component']
couronne = param['hypo_interv']
dist_min = param['hypo_min']
dist_max = param['hypo_max']

# directories used in this script:
# - path_data is the directory where all the records with hypocenter distance
#   less than 100km are stored
# - path_results is the directory where a copy of the records with hypocenter
#   distance between hypo_min and hypo_max will be done (the values hypo_min
#   and hypo_max are given by the user through parametres.py)
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env/'
             + frq_bnd + 'Hz_' + cpnt + '_smooth')
path_results = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel_env_selection/'
                + frq_bnd + 'Hz_' + cpnt + '_smooth_' + couronne + 'km')

# create the directory path_results in case it does not exist
if not os.path.isdir(path_results):
    try:
        os.makedirs(path_results)
    except OSError:
        print('Creation of the directory {} failed'.format(path_results))
    else:
        print('Successfully created the directory {}'.format(path_results))
else:
    print('{} is already existing'.format(path_results))

# pick all the records from the directory path_data
list_stat = os.listdir(path_data)
list_stat = [a for a in list_stat if 'sac' in a]

print('Check if the hypocenter distance is between {}'.format(dist_min),
        'and {}'.format(dist_max), 'for each station')
for s in list_stat:
    os.chdir(path_data)
    st = read(s)
    dst = st[0].stats.sac.dist
    print('The station {}'.format(s[:6]),
          'with hypocenter distance equal to {:.1f} km'.format(dst),
          end = ' ')
    if dst > dist_min and dst < dist_max:
        os.chdir(path_results)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s, format='SAC')
        print('is selected ({} < {:.1f} < {})'.format(dist_min, dst, dist_max))
    elif dst < dist_min:
        print('is not selected ({:.1f} < {})'.format(dst, dist_min))
    else:
        print('is not seelcted ({} < {:.1f})'.format(dist_max, dst))
