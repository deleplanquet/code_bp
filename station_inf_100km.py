#

import pickle
from obspy import read
import sys
import os
import math
from obspy import Trace

# few functions used in this script
# a library may be done

# conversion angle degre -> radian
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

root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
# load parameters given by the user through parametres.py
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used, only the following ones
R_Earth = param['R_Earth']
event = param['event']

# directories used in this script
# 
path = (root_folder + '/'
        + 'Kumamoto/'
        + event)
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + acc + '/'
             + 'brut')
path_results = (path + '/'
                + event + '_sac_inf100km')

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

lat_hyp = dict_seis[event]['lat']
lon_hyp = dict_seis[event]['lon']
dep_hyp = dict_seis[event]['dep']

os.chdir(path_data)

list_stat = os.listdir(path_data)
list_stat_UD = [a for a in list_stat if ('UD' in a) and ('UD1' not in a)]
list_stat_NS = [a for a in list_stat if ('NS' in a) and ('NS1' not in a)]
list_stat_EW = [a for a in list_stat if ('EW' in a) and ('EW1' not in a)]
list_stat = list_stat_UD + list_stat_NS + list_stat_EW

hypo = [R_Earth - dep_hyp, lat_hyp, lon_hyp]

for station in list_stat:
    os.chdir(path_data)
    print(station)
    st = read(station)
    pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel,
               st[0].stats.sac.stla,
               st[0].stats.sac.stlo]
    print(dist(hypo, pos_sta), st[0].stats.sac.dist)
    if dist(hypo, pos_sta) < 100:
        os.chdir(path_results)
        print('selection')
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format='SAC')
