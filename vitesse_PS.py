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

#constantes
R_Earth = 6400

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#distance entre deux points, coordonnees cartesiennes
def dist(vect1, vect2):
    x1, y1, z1 = geo2cart(vect1)
    x2, y2, z2 = geo2cart(vect2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#normalisation avec max = 1
def norm1(vect):
    norm_v = 0
    for a in vect:
        norm_v = norm_v + a*a
    return [50*a/pow(norm_v, 0.5) for a in vect]

print('')
print('      python3 vitesse_PS.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
velP = param['vP']
velS = param['vS']

yea_seis = int(dict_seis[dossier]['nFnet'][0:4])
mon_seis = int(dict_seis[dossier]['nFnet'][4:6])
day_seis = int(dict_seis[dossier]['nFnet'][6:8])
hou_seis = int(dict_seis[dossier]['nFnet'][8:10])
min_seis = int(dict_seis[dossier]['nFnet'][10:12])
sec_seis = int(dict_seis[dossier]['nFnet'][12:14])
mse_seis = int(dict_seis[dossier]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis, mon_seis, day_seis, hou_seis, min_seis, sec_seis, mse_seis)

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz_'
             + dt_type
             + '_env_smooth')

path_results = (path + '/'
                + dossier
                + '_results/'
                + dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz')

list_sta = os.listdir(path_data)

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Source time (s)')
ax.set_ylabel('Hypocenter distance (km)')

vP = {}
vS = {}

os.chdir(path_data)

vct_dst = np.zeros(50)

for i, station in enumerate(list_sta):
    st = read(station)
    dst = st[0].stats.sac.dist

    delai_rec = st[0].stats.starttime - t_origin_rupt

    vP[st[0].stats.station] = st[0].stats.sac.a + delai_rec - st[0].stats.sac.dist/velP
    vS[st[0].stats.station] = st[0].stats.sac.t0 + delai_rec - st[0].stats.sac.dist/velS

    if vct_dst[int(dst//2)] == 0:
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        t = [a + delai_rec for a in t]

        #ax.plot(t, norm1(st[0].data) + st[0].stats.sac.dist, linewidth = 0.5, color = 'black')
        ax.fill_between(t, st[0].stats.sac.dist, norm1(st[0].data) + st[0].stats.sac.dist, linewidth = 0.3, color = 'black', alpha = 0.2)
        ax.text(50 + t[0], st[0].stats.sac.dist, st[0].stats.station, fontsize = 3)
        #ax.scatter(st[0].stats.sac.a + delai_rec, st[0].stats.sac.dist, s = 30, color = 'steelblue')
        #ax.scatter(st[0].stats.sac.t0 + delai_rec, st[0].stats.sac.dist, s = 30, color = 'darkorange')
        ax.vlines(st[0].stats.sac.a + delai_rec, st[0].stats.sac.dist - 1, st[0].stats.sac.dist + 1, linewidth = 1, color = 'steelblue')
        ax.vlines(st[0].stats.sac.t0 + delai_rec, st[0].stats.sac.dist - 1, st[0].stats.sac.dist + 1, linewidth = 1, color = 'darkorange')

        if (st[0].stats.sac.t0 + delai_rec) > 30:
            print(st[0].stats.station, st[0].stats.sac.dist, st[0].stats.sac.t0 + delai_rec)

        vct_dst[int(dst//2)] = 1

to_register = [vP, vS]#, tdeb]

os.chdir(path_results)
with open(dossier + '_veldata', 'wb') as mon_fich:
    mon_pick = pickle.Pickler(mon_fich)
    mon_pick.dump(to_register)

#ax.text(10, 115, str(t_origin_rupt), color = 'black')
ax.plot([0, 100./velP], [0, 100], linewidth = 2, color = 'steelblue')
ax.plot([0, 100./velS], [0, 100], linewidth = 2, color = 'darkorange')
ax.set_xlim([0, 40])
ax.set_ylim([0, 110])
#ax.xaxis.set_visible(False)
#ax.yaxis.set_visible(False)
fig.savefig('env_fct_dist_'
            + dossier
            + '_env_'
            + couronne + 'km_'
            + frq + 'Hz_'
            + dt_type
            + '_env_smooth'
            + '.pdf')
