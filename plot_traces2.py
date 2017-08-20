from obspy import read
import matplotlib.pyplot as plt
import pickle
import os
import sys
import numpy as np
import math

def norm1(vect):
    return [10*a/vect.max() for a in vect]

def translate(vect, a):
    return [b + a for b in vect]

def d2r(angle):
    return angle*math.pi/180

def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

def dist(v1, v2):
    x1, y1, z1 = geo2cart(v1)
    x2, y2, z2 = geo2cart(v2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

R_Earth = 6400

dossier = sys.argv[1]
freq = sys.argv[2]
dt_type = sys.argv[3]

if len(dossier) != 14:
    print('ERROR TYPO dossier', len(dossier))
    sys.exit(0)
if freq != '02_05' and freq != '05_1' and freq != '1_2' and freq != '2_4' and freq != '4_10':
    print('ERROR TYPO freq')
    sys.exit(0)
if dt_type != '3comp' and dt_type != 'hori' and dt_type != 'vert':
    print('ERROR TYPE dt_type')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env'
path_results = path_data + '_results'

list_fich = os.listdir(path_data)

os.chdir(path)
with open(dossier + '_veldata', 'rb') as myfch:
    mydp = pickle.Unpickler(myfch)
    dict_vel = mydp.load()

dict_vel_used = dict_vel[1]

os.chdir(path_data)

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time')

stt = read(list_fich[0])
tarrival = stt[0].stats.starttime

t_start_ref = None
for cles in dict_vel[2].keys():
    if t_start_ref == None or t_start_ref > dict_vel[2][cles]:
    	t_start_ref = dict_vel[2][cles]

for fich in list_fich:
    st = read(fich)
    #xh, yh, zh = geo2cart([R_Earth - 11.97, 32.8408, 130.8845])
    xh, yh, zh = -3514.73166817, 4053.15977919, 3467.78299218
    xs, ys, zs = geo2cart([R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo])
    print(xh, yh, zh, xs, ys, zs)
    tshift = t_start_ref - dict_vel[2][st[0].stats.station] + math.sqrt(pow(xh - xs, 2) + pow(yh - ys, 2) + pow(zh - zs, 2))/3.4 + dict_vel_used[st[0].stats.station]
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    delaistart = st[0].stats.starttime - tarrival
    t = [a + tshift for a in t]
    ordo = dist([R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo])
    #print(t_start_ref, dict_vel[2][st[0].stats.station], math.sqrt(pow(xh - xs, 2) + pow(yh - ys, 2) + pow(zh - zs, 2))/3.4, dict_vel_used[st[0].stats.station], tshift)
    ax.plot(t, translate(norm1(st[0].data), ordo), lw = 0.2)
    #ax.scatter(ordo/3.4 - 0.2 + dict_vel_used[st[0].stats.station], ordo, s = 2)

os.chdir(path_results)
fig.savefig('tttraces_' + dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env.pdf')




























