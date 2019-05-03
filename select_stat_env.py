#

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

# open the filde of the parameters given by the user through parametres.py and
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
# - path_data
# - path_rslt
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/'
             + 'env_smooth')

path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz_' + cpnt + '/')
path_rslt_P = (path_rslt
               + 'env_smooth_P')
path_rslt_S = (path_rslt
               + 'env_smooth_S')

#path = (path_origin
#        + '/Kumamoto/'
#        + dossier)
#
#path_data = (path + '/'
#             + dossier
#             + '_vel_'
#             + couronne + 'km_'
#             + frq + 'Hz/'
#             + dossier
#             + '_vel_'
#             + couronne + 'km_'
#             + frq + 'Hz_'
#             + dt_type
#             + '_env_smooth')
#
#path_results_P = path_data + '_P'
#path_results_S = path_data + '_S'

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
    # 
    arrival_P = stP[0].stats.starttime + stP[0].stats.sac.a
    arrival_S = stS[0].stats.starttime + stS[0].stats.sac.t0

    stP[0].trim(arrival_P, arrival_S - 0.1)
    stS[0].trim(arrival_S, stS[0].stats.endtime)
    trP = stP[0]
    trS = stS[0]
    # ratio between max value of S energy and max value of P energy
    rapport_PS = math.log10(trS.max()/trP.max())
    #print(trS.max()/trP.max())
    if rapport_PS > math.log10(rSP):
        #print('   S')
        st = read(s)
        os.chdir(path_rslt_S)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s[:6], format = 'SAC')
    if rapport_PS < math.log10(1./rSP):
        #print('   P')
        st = read(s)
        os.chdir(path_rslt_P)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(s[:6], format = 'SAC')
