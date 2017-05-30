from obspy import read
import pickle
import os
import sys
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit

def fit_lineaire(x_data, a, b):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = a * x_data[i] + b

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

dossier = sys.argv[1]

path = '/Users/deleplanque/Documents'
#path = '/localstorage/deleplanque'
path_data = path + '/Data/Kumamoto_env/' + dossier
path_results = path + '/LaTeX/Poster_jpgu_2017'
path_vel = path + '/Results/Kumamoto/Velocity'

list_sta = os.listdir(path_data)
list_sta = [a for a in list_sta if ('UD' in a) == True and ('UD1' in a) == False]

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance from the hypocenter (km)')

list_tP = []
list_tS = []
list_dist = []
vP = {}
vS = {}
dist_hyp = {}

os.chdir(path_data)
for station in list_sta:
    st = read(station)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    tsec = st[0].stats.starttime.second
    tmicrosec = st[0].stats.starttime.microsecond
    t = [a + tsec + tmicrosec/1e6 for a in t]
#    t = [a + tsec - 40 + tmicrosec/1e6 if tsec > 10 else a + tsec + 20 + tmicrosec/1e6 for a in t]

    pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]
    pos_hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
    ordo = dist(pos_sta, pos_hypo)

    ax.plot(t, norm1(st[0].data) + ordo, linewidth = 0.2, color = 'black')
#    ax.text(50 + t[0], ordo, st[0].stats.station, fontsize = 3)

    list_tP.append(st[0].stats.sac.a + t[0])
    list_tS.append(st[0].stats.sac.t0 + t[0])
    list_dist.append(ordo)

    vP[st[0].stats.station] = st[0].stats.sac.a + t[0]
    vS[st[0].stats.station] = st[0].stats.sac.t0 + t[0]
    dist_hyp[st[0].stats.station] = ordo

poptP, pcovP = curve_fit(fit_lineaire, list_tP, list_dist)
poptS, pcovS = curve_fit(fit_lineaire, list_tS, list_dist)

vP['fit'] = poptP[0]
vS['fit'] = poptS[0]

for cles in vP.keys():
    if ('fit' in cles) == False:
    	vP[cles] = vP[cles] - (dist_hyp[cles] - poptP[1])/vP['fit']

for cles in vS.keys():
    if ('fit' in cles) == False:
    	vS[cles] = vS[cles] - (dist_hyp[cles] - poptS[1])/vS['fit']

to_register = [vP, vS]

print(poptP[0], poptS[0])

os.chdir(path_vel)
with open(dossier + '_vel', 'wb') as mon_fich:
    mon_pick = pickle.Pickler(mon_fich)
    mon_pick.dump(to_register)

tP = np.arange(9, 29)
tS = np.arange(10, 42)

ax.scatter(list_tP, list_dist, s=2)
ax.scatter(list_tS, list_dist, s=2)

ax.text(65, 30, str(int(1000*poptP[0])) + 'm/s', color='steelblue')
ax.text(65, 20, str(int(1000*poptS[0])) + 'm/s', color='darkorange')
ax.text(5, 115, '2016/04/16 08:02', color = 'black')

ax.plot(tP, poptP[0]*tP + poptP[1], linewidth=0.2)
ax.plot(tS, poptS[0]*tS + poptS[1], linewidth=0.2)
os.chdir(path_results)
fig.savefig('env_fct_dist_' + dossier + '.pdf')
