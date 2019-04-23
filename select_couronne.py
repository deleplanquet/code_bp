# make a copie of the records in SAC format of the stations which hypocenter
# distance is between hypo_min and hypo_max
# hypo_min and hypo_max are user choosed through running parameters.py

import pickle
from obspy import read
import sys
import os
import math
from obspy import Trace

# few functions used in this script
# a library may be done

# conversion angle degree -> radian
def d2r(angle):
    return angle*math.pi/180

# conversion geographic coordinates -> cartesian coordinates
# outputs xx, yy and zz have same units than r and should be kilometer
def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

# distance between two points whose coordinates are cartesians
def dist(vect1, vect2):
    x1, y1, z1 = geo2cart(vect1)
    x2, y2, z2 = geo2cart(vect2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

print('######################################',
    '\n###   python3 select_couronne.py   ###',
    '\n######################################')

# open the file of the parameters given by the user
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
# load parameters given by the user through parametres.py
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
R_Earth = param['R_Earth']
event = param['event']
couronne = param['hypo_interv']
dist_min = param['hypo_min']
dist_max = param['hypo_max']

# directories used in this script:
# - path_data is the directory where all the records with hypocenter distance
# less than 100km are stored
# - path_results is the directory where a copy of the records with hypocenter
# distance between hypo_min and hypo_max will be done (the values hypo_min and
# hypo_max are given by the user through parametres.py)
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'acc/'
             + 'inf100km_copie')
path_results = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'acc/'
                + couronne + 'km')

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

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

lat_hyp = dict_seis[event]['lat']
lon_hyp = dict_seis[event]['lon']
dep_hyp = dict_seis[event]['dep']
hypo = [R_Earth - dep_hyp, lat_hyp, lon_hyp]

# pick all the records from the directory path_data
os.chdir(path_data)
list_stat = os.listdir(path_data)

print('Check if the hypocenter distance is between {}'.format(dist_min),
        'and {}'.format(dist_max), 'for each station')
for s in list_stat:
    os.chdir(path_data)
    st = read(s)
    pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel,
               st[0].stats.sac.stla,
               st[0].stats.sac.stlo]
    dst = dist(hypo, pos_sta)
    print('The station {}'.format(s[:6]),
          'with hypocenter distance equal to {:.1f} km'.format(dst),
          end = ' ')
    if dst > dist_min and dst < dist_max:
        os.chdir(path_results)
        st[0].stats.sac.dist = dst
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s, format='SAC')
        print('is selected ({} < {:.1f} < {})'.format(dist_min, dst, dist_max))
    elif dst < dist_min:
        print('is not selected ({:.1f} < {})'.format(dst, dist_min))
    else:
        print('is not seelcted ({} < {:.1f})'.format(dist_max, dst))
