from obspy import read
import pickle
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
from obspy.signal.util import smooth
import math

#constantes
R_Earth = 6400

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#distance entre deux points, coordonnees cartesiennes
def dist(la1, lo1, el1, la2, lo2, el2):
    x1, y1, z1 = geo2cart(R_Earth + el1, la1, lo1)
    x2, y2, z2 = geo2cart(R_Earth + el2, la2, lo2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#normalisation
def norm1(vect):
    return [5*a/vect.max() for a in vect]

name_dossier = sys.argv[1]

path = os.getcwd()[:-6]
path_data = path + '/Data/Kumamoto_env_selectS/' + name_dossier
path_results = path + '/Results/Kumamoto/' + name_dossier

os.chdir(path + '/Data')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

dict_doss = dict_seis[name_dossier]

list_station = os.listdir(path_data)
list_station = [a for a in list_station if 'UD' in a]

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance from the hypocenter (km)')

os.chdir(path_data)
for station in list_station:
    st = read(station)

    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate

    ordo = dist(st[0].stats.sac.stla, st[0].stats.sac.stlo, 0.001*st[0].stats.sac.stel, dict_doss['lat'], dict_doss['lon'], -dict_doss['dep'])
    #ax.plot(t, tr_brut, color='black')
    ax.plot(t, norm1(st[0].data) + ordo, linewidth=0.2, color='black')
    ax.axvline(5, linewidth = 0.2, color = 'steelblue')
    #ax.scatter(15 - st[0].stats.sac.t0 + st[0].stats.sac.a, ordo, 2, color = 'steelblue')
    ax.scatter(st[0].stats.sac.t0, ordo, 2, color = 'darkorange')

    #ax.text(0, 0, name_dossier)
    ax.text(40, ordo, st[0].stats.station)

os.chdir(path_results)
fig.savefig(name_dossier + '.pdf')
