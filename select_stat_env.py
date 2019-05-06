# sort the stations into three sub group:
# - stations S: stations with high energy of S-waves compared to P-waves, those
# stations will be used for back projection with S velocity hypothesis
# - stations P: stations with high energy of P-waves compared to S-waves, those
# stations will be used for back projection with P velocity hypothesis
# - other stations: stations with comparable energy of P and S-waves, those
# stations will not be used for any back projection analysis
# the criteria to sort the stations is the parameter ratioSP given by the user
# through the script parametres.py

import math
from obspy import read
import os
import sys
from obspy import Trace
import numpy as np
import pickle

print('######################################',
    '\n###   python3 select_stat_env.py   ###',
    '\n######################################')

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
rSP = param['ratioSP']

# directories used in this script
# - path_data is the directory of the envelopes that passed previous conditions
# - path_rslt_P is the directory of the envelopes selected for back projection
# with P velocity hypothesis
# - path_rslt_S is the directory of the envelopes selected for back projection
# with S velocity hypothesis
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env_smooth')
# path_rslt is created to prevent repetition, the two real directories to be
# considered are path_rslt_P and path_rslt_S
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/')
path_rslt_P = (path_rslt
               + 'env_smooth_P')
path_rslt_S = (path_rslt
               + 'env_smooth_S')

# create the directories path_rslt_P and path_rslt_S in case they do not exist
if not os.path.isdir(path_rslt_P):
    try:
        os.makedirs(path_rslt_P)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt_P))
    else:
        print('Successfully created the directory {}'.format(path_rslt_P))
else:
    print('{} is already existing'.format(path_rslt_P))
if not os.path.isdir(path_rslt_S):
    try:
        os.makedirs(path_rslt_S)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt_S))
    else:
        print('Successfully created the directory {}'.format(path_rslt_S))
else:
    print('{} is already existing'.format(path_rslt_S))

# pick the envelopes from the directory path_data
lst_fch = os.listdir(path_data)

print('Checking ratio of energy S/P')
for s in lst_fch:
    os.chdir(path_data)
    # load the envelope twice to prevent confusion
    stP = read(s)
    stS = read(s)
    # define picked arrival time of both P ans S waves
    arrival_P = stP[0].stats.starttime + stP[0].stats.sac.a
    arrival_S = stS[0].stats.starttime + stS[0].stats.sac.t0
    # trim differently the two traces to isolate the energies of P and S waves
    stP[0].trim(arrival_P, arrival_S - 0.1)
    stS[0].trim(arrival_S, stS[0].stats.endtime)
    # consider the trace
    trP = stP[0]
    trS = stS[0]
    # ratio between max value of S energy and max value of P energy
    rapport_SP = trS.max()/trP.max()
    print('The ratio between the energy of S-waves and the energy of P-waves',
            'of the station {}'.format(s[:6]),
            'is equal to {:.1f}'.format(rapport_SP),
            end = ' ')
    # for stations with 'high' S energy
    if rapport_SP > rSP:
        st = read(s)
        os.chdir(path_rslt_S)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s[:6], format = 'SAC')
        print('which is higher than {}'.format(rSP),
                '\n   --> station selected for back projection of S-waves')
    # for stations wilh 'high' P energy
    elif rapport_SP < 1./rSP:
        st = read(s)
        os.chdir(path_rslt_P)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s[:6], format = 'SAC')
        print('which is lower than {:.2f}'.format(1./rsP),
                '\n   --> station selected for back projection of P-waves')
    # for remaining stations
    else:
        print('which is between {:.2f} and {}'.format(1./rSP, rSP),
                '\n   --> station NOT selected for back projection')
