# calculation of the delays between the hand picking arrival times and the
# expected calculated arrival times for both P and S waves

from obspy import read
import pickle
import os
import sys
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit
from obspy.core import UTCDateTime

print('#################################',
    '\n###   python3 vitesse_PS.py   ###',
    '\n#################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# load location of the studied earthquake
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
vP = param['vP']
vS = param['vS']

# define the origin of the rupture
yea_seis = int(dict_seis[event]['nFnet'][0:4])
mon_seis = int(dict_seis[event]['nFnet'][4:6])
day_seis = int(dict_seis[event]['nFnet'][6:8])
hou_seis = int(dict_seis[event]['nFnet'][8:10])
min_seis = int(dict_seis[event]['nFnet'][10:12])
sec_seis = int(dict_seis[event]['nFnet'][12:14])
mse_seis = int(dict_seis[event]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis,
                            mon_seis,
                            day_seis,
                            hou_seis,
                            min_seis,
                            sec_seis,
                            mse_seis)

# directories used in this script:
# - path_data is the directory where all the records with picking values and
#   hypocenter distance less than 100km are stored
# - path_rslt is the directory where the dictionnary of the delays will be
#   saved
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + 'brut')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'general')

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

# pick the envelopes from the directory path_data
list_sta = os.listdir(path_data)

# initialisation of the delays dictionnaries
delay_P = {}
delay_S = {}

os.chdir(path_data)
print('Calculation of the delays between the picked values of P and S',
        'arrival times and the expected calculated values between the',
        'stations and the hypocenter of the following event: {}'.format(event))
for i, s in enumerate(list_sta):
    # load the envelope
    st = read(s)
    # few parameters are stored because they will be used more than once
    dst = st[0].stats.sac.dist
    sta_name = st[0].stats.station
    starttime = st[0].stats.starttime
    # delay for P and S arrival time defined by the difference between the time
    # of the picking and the expected calculated arrival time depending only on
    # the distance and the velocity of the considered wave
    delay_P[sta_name] = (starttime + st[0].stats.sac.a
                         - t_origin_rupt - dst/vP)
    delay_S[sta_name] = (starttime + st[0].stats.sac.t0
                         - t_origin_rupt - dst/vS)

# creation of a dictionnary containing the two delay dictionnaries
to_register = {'delay_P':delay_P, 'delay_S':delay_S}

# save to bin file
os.chdir(path_rslt)
with open(event + '_picking_delays', 'wb') as mon_fich:
    mon_pick = pickle.Pickler(mon_fich)
    mon_pick.dump(to_register)
