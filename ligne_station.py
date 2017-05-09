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

name_dossier = '20160415015900'
#name_dossier = '20160417054100'

path = '/localstorage/deleplanque'
#path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/' + name_dossier
path_results = path + '/Results'

os.chdir(path_data)

st1 = read('KMMH161604150159.UD2.sac')
st2 = read('KMMH031604150159.UD2.sac')
st3 = read('FKOH101604150159.UD2.sac')
#st1 = read('KMM0111604170541.UD.sac')
#st2 = read('MYZ0201604170541.UD.sac')
#st3 = read('MYZH081604170541.UD2.sac')
t1start = st1[0].stats.starttime + st1[0].stats.sac.t0 - 15
t2start = st2[0].stats.starttime + st2[0].stats.sac.t0 - 15
t3start = st3[0].stats.starttime + st3[0].stats.sac.t0 - 15
t1end = t1start + 50
t2end = t1start + 50
t3end = t3start + 50
st1[0].trim(t1start, t1end)
st2[0].trim(t2start, t2end)
st3[0].trim(t3start, t3end)
st1 = st1.detrend(type='constant')
st2 = st2.detrend(type='constant')
st3 = st3.detrend(type='constant')
st1.normalize()
st2.normalize()
st3.normalize()
tr1_brut = st1[0]
tr2_brut = st2[0]
tr3_brut = st3[0]
tr1_filt = tr1_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
tr2_filt = tr2_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
tr3_filt = tr3_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
envelop1 = abs(hilbert(tr1_filt))
envelop2 = abs(hilbert(tr2_filt))
envelop3 = abs(hilbert(tr3_filt))
env1_smoothed = smooth(envelop1, 20)
env2_smoothed = smooth(envelop2, 20)
env3_smoothed = smooth(envelop3, 20)

t1 = np.arange(tr1_brut.stats.npts)/tr1_brut.stats.sampling_rate
t2 = np.arange(tr2_brut.stats.npts)/tr2_brut.stats.sampling_rate
t3 = np.arange(tr3_brut.stats.npts)/tr3_brut.stats.sampling_rate

ord1 = dist(st1[0].stats.sac.stla, st1[0].stats.sac.stlo, 0.001*st1[0].stats.sac.stel, st1[0].stats.sac.evla, st1[0].stats.sac.evlo, -st1[0].stats.sac.evdp)
ord2 = dist(st2[0].stats.sac.stla, st2[0].stats.sac.stlo, 0.001*st2[0].stats.sac.stel, st2[0].stats.sac.evla, st2[0].stats.sac.evlo, -st2[0].stats.sac.evdp)
ord3 = dist(st3[0].stats.sac.stla, st3[0].stats.sac.stlo, 0.001*st3[0].stats.sac.stel, st3[0].stats.sac.evla, st3[0].stats.sac.evlo, -st3[0].stats.sac.evdp)

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.plot(t1, 20*env1_smoothed + ord1, linewidth=0.2)
ax.plot(t2, 20*env2_smoothed + ord2, linewidth=0.2)
ax.plot(t3, 20*env3_smoothed + ord3, linewidth=0.2)
ax.axvline(15)

#ax.text(0, 0, name_dossier)
ax.text(40, ord1, st1[0].stats.station)
ax.text(40, ord2, st2[0].stats.station)
ax.text(40, ord3, st3[0].stats.station)

os.chdir(path_results)
fig.savefig(name_dossier + '.pdf')
