from obspy import read
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
def norm(vect):
    norm_v = 0
    for a in vect:
    	norm_v = norm_v + a*a
    return [30*a/pow(norm_v, 0.5) for a in vect]

name_dossier = '20160415015900'
#name_dossier = '20160417054100'
#name_dossier = '20160416074900'
#name_dossier = '20160416131700'
#name_dossier = '20160415124600'
#name_dossier = '20160416220600'

#path = '/localstorage/deleplanque'
path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/' + name_dossier
path_results = path + '/Results'

os.chdir(path_data)

list_station = ['KMMH161604150159.UD2.sac', 'KMMH031604150159.UD2.sac', 'FKOH101604150159.UD2.sac']
#list_station = ['KMM0111604170541.UD.sac', 'MYZ0201604170541.UD.sac', 'MYZH081604170541.UD2.sac']
#list_station = ['KMMH031604160749.UD2.sac', 'KMM0021604160749.UD.sac', 'FKO0161604160749.UD.sac']
#list_station = ['KMMH161604161317.UD2.sac', 'KMM0091604161317.UD.sac', 'MYZ0011604161317.UD.sac']
#list_station = ['KMM0091604151246.UD.sac', 'MYZ0201604151246.UD.sac', 'MYZH051604151246.UD2.sac']
#list_station = ['KMM0061604162206.UD.sac', 'KMMH141604162206.UD2.sac', 'KMMH121604162206.UD2.sac']

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance from the hypocenter (km)')

for station in list_station:
    st = read(station)
    st = st.detrend(type='constant')
    tstart = st[0].stats.starttime + st[0].stats.sac.t0 - 15
    print(st[0].stats.sac.b)
    tend = tstart + 50
    st[0].trim(tstart, tend, pad=True, fill_value=0)
    tr_brut = st[0]
    tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
    envelop = abs(hilbert(tr_filt))
    env_smoothed2 = smooth(envelop, 20)
    squared_tr = [a**2 for a in tr_filt]
    env_smoothed = smooth(squared_tr, 20)

    t = np.arange(tr_brut.stats.npts)/tr_brut.stats.sampling_rate

    ordo = dist(st[0].stats.sac.stla, st[0].stats.sac.stlo, 0.001*st[0].stats.sac.stel, st[0].stats.sac.evla, st[0].stats.sac.evlo, -st[0].stats.sac.evdp)

    #ax.plot(t, tr_brut, color='black')
    ax.plot(t, norm(env_smoothed) + ordo, linewidth=0.2, color='blue')
    ax.plot(t, norm(env_smoothed2) + ordo, linewidth=0.2, color='red')
    ax.axvline(15)

    #ax.text(0, 0, name_dossier)
    ax.text(40, ordo, st[0].stats.station)

os.chdir(path_results)
fig.savefig(name_dossier + '.pdf')
