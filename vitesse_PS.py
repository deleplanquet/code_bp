#

from obspy import read
import pickle
import os
import sys
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit
from obspy.core import UTCDateTime

#fit par une droite lineaire
def fit_lineaire(x_data, a, b):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = a * x_data[i] + b
    return y_data

def fit_lineaire_S(x_data, b):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = 3.4 * x_data[i] + b
    return y_data

def fit_lineaire_P(x_data, b):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = 5.8 * x_data[i] + b
    return y_data

# conversion angle degree -> radian
def d2r(angle):
    return angle*math.pi/180

# conversion geographic coordinates - > cartesian coordinates
def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

# normalisation with max = 1
def norm1(vect):
    norm_v = 0
    for a in vect:
        norm_v = norm_v + a*a
    return [50*a/pow(norm_v, 0.5) for a in vect]

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
frq_bnd = param['frq_band']
cpnt = param['component']
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
# - path_data
# - path_rslt
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel_env/'
             + frq_bnd + 'Hz_' + cpnt + '_smooth')
path_rslt = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'results/'
             + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
             + 'others')

# pick the envelopes from the directory path_data
list_sta = os.listdir(path_data)

#fig, ax = plt.subplots(1, 1)
#ax.set_xlabel('Source time (s)')
#ax.set_ylabel('Hypocenter distance (km)')

delay_P = {}
delay_S = {}

os.chdir(path_data)
for i, s in enumerate(list_sta):
    # load the envelope
    st = read(s)
    # few parameters are stored because they will be used more than once
    dst = st[0].stats.sac.dist
    sta_name = st[0].stats.station
    starttime = st[0].stats.starttime
    #
    delay_P[sta_name] = (starttime + st[0].stats.sac.a
                         - t_origin_rupt - dst/velP)
    delay_S[sta_name] = (starttime + st[0].stats.sac.t0
                         - t_origin_rupt - dst/velS)

#    if vct_dst[int(dst//2)] == 0:
#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        t = [a + delai_rec for a in t]
#        #ax.plot(t, norm1(st[0].data) + st[0].stats.sac.dist, linewidth = 0.5, color = 'black')
#        ax.fill_between(t,
#                        st[0].stats.sac.dist,
#                        norm1(st[0].data) + st[0].stats.sac.dist,
#                        linewidth = 0.3,
#                        color = 'black',
#                        alpha = 0.2)
#        ax.text(50 + t[0],
#                st[0].stats.sac.dist,
#                st[0].stats.station,
#                fontsize = 3)
#        ax.vlines(st[0].stats.sac.a + delai_rec,
#                  st[0].stats.sac.dist - 1,
#                  st[0].stats.sac.dist + 1,
#                  linewidth = 1,
#                  color = 'steelblue')
#        ax.vlines(st[0].stats.sac.t0 + delai_rec,
#                  st[0].stats.sac.dist - 1,
#                  st[0].stats.sac.dist + 1,
#                  linewidth = 1,
#                  color = 'darkorange')
#        if (st[0].stats.sac.t0 + delai_rec) > 30:
#            print(st[0].stats.station,
#                  st[0].stats.sac.dist,
#                  st[0].stats.sac.t0 + delai_rec)
#        vct_dst[int(dst//2)] = 1

to_register = {'delay_P':delay_P, 'delay_S':delay_S}

os.chdir(path_rslt)
with open(dossier + '_picking_delays', 'wb') as mon_fich:
    mon_pick = pickle.Pickler(mon_fich)
    mon_pick.dump(to_register)

##ax.text(10, 115, str(t_origin_rupt), color = 'black')
#ax.plot([0, 100./velP], [0, 100], linewidth = 2, color = 'steelblue')
#ax.plot([0, 100./velS], [0, 100], linewidth = 2, color = 'darkorange')
#ax.set_xlim([0, 40])
#ax.set_ylim([0, 110])
##ax.xaxis.set_visible(False)
##ax.yaxis.set_visible(False)
#fig.savefig('env_fct_dist_'
#            + dossier
#            + '_env_'
#            + couronne + 'km_'
#            + frq + 'Hz_'
#            + dt_type
#            + '_env_smooth'
#            + '.pdf')
