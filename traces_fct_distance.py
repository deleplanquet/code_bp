from obspy import read
import math
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
from obspy.signal.util import smooth

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

list_dossier = ['20160417054100', '20160415015900', '20160416074900', '20160416131700', '20160415124600', '20160416220600']

path = '/localstorage/deleplanque'
path_data = path + '/Data/Kumamoto_sac'
path_results = path + '/Results'

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')

for dossier in list_dossier:
    print(dossier)
    os.chdir(path_data + '/' + dossier)
    list_fichier = os.listdir(path_data + '/' + dossier)
    list_fichier = [a for a in list_fichier if (('UD' in a) == True and ('UD1' in a) == False)]

    fig2, ax2 = plt.subplots(1, 1)
    ax2.set_xlabel('Time (s)')

    for fichier in list_fichier:
    	st = read(fichier)
    	st = st.detrend(type = 'constant')
    	tstart = st[0].stats.starttime + st[0].stats.sac.t0 - 15
    	tend = tstart + 50
    	st[0].trim(tstart, tend, pad=True, fill_value=0)
    	tr_brut = st[0]
    	tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
    	#envelop = abs(hilbert(tr_filt))
    	#env_smoothed = smooth(envelop, 20)
    	squared_tr = [a**2 for a in tr_filt]
    	env_smoothed = smooth(squared_tr, 20)

    	t = np.arange(tr_brut.stats.npts)/tr_brut.stats.sampling_rate

    	ordo = dist(st[0].stats.sac.stla, st[0].stats.sac.stlo, 0.001*st[0].stats.sac.stel, st[0].stats.sac.evla, st[0].stats.sac.evlo, -st[0].stats.sac.evdp)

    	ax.plot(t, norm(env_smoothed) + ordo, linewidth = 0.2)
    	ax.text(40, ordo, st[0].stats.station)

    	ax2.plot(t, norm(env_smoothed) + ordo, linewidth = 0.2)
    	ax2.text(40, ordo, st[0].stats.station)

    os.chdir(path_results)
    ax2.axvline(15)
    fig2.savefig('tt_sta_' + dossier + '.pdf')

ax.axvline(15)
fig.savefig('tt_sta_tt_seisme.pdf')
