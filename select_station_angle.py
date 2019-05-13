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

# few functions used in this script
# a library may be done

# conversion angle degree -> radian
def d2r(angle):
    return angle*math.pi/180

# conversion angle radian -> degree
def r2d(angle):
    return angle*180/math.pi

# distance and azimuth between two points
# the reference point is the first given and the azimuth of the second point is
# calculated with respect to the first one
def dist_azim(ptA, ptB, R):
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB)
                         + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB)
                            - math.sin(latA)*math.cos(dist_rad))
                           /(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R*dist_rad, r2d(angle_brut)
    else:
        return R*dist_rad, 360 - r2d(angle_brut)

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
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env_smooth_' + hyp_bp)
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env_smooth_' + hyp_bp + '_' + azim + 'deg')

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
    # calculate the distance and the azimuth between the station and the
    # hypocenter
    d_hp_st, az_hp_st = dist_azim([lat_hyp, lon_hyp],
                                  [st[0].stats.sac.stla, st[0].stats.sac.stlo],
                                  R_Earth)
    print('The azimuth between the station {}'.format(s[:6]),
            'and the hypocenter {}, {}'.format(lat_hyp, lon_hyp),
            'is equal to {:.2f} deg'.format(az_hp_st),
            end = ' ')
    # if the calculated azimuth belongs to the range of azimuth specified by
    # the user, the station is selected and saved in path_rslt directory
    if ((az_hp_st > azim_min and az_hp_st < azim_max)
        or (az_hp_st > (azim_min + 180) and az_hp_st < (azim_max + 180))):
        #print('           ', 'ok')
        os.chdir(path_rslt)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s[:6], format = 'SAC')
        print('which belongs to',
            '[{}, {}]\u222a[{}, {}]'.format(azim_min, azim_max,
                                            azim_min + 180, azim_max + 180),
            '\n   --> station selected for back projection')
    # if the station does not fulfill the selection criteria, it will not be
    # considered for back projection study
    else:
        print('which does NOT belong to',
            '[{}, {}]\u222a[{}, {}]'.format(azim_min, azim_max,
                                            azim_min + 180, azim_max + 180),
            '\n   --> station NOT selected for back projection')
