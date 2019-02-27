from obspy import read
import matplotlib.pyplot as plt
import os
import numpy as np
import math

def d2r(angle):
    return angle*math.pi/180

def r2d(angle):
    return angle*180/math.pi

#normalisation
def norm1(vect):
    return[5*a/vect.max() for a in vect]

def translate(vect, a):
    return [b + a for b in vect]

def dist_azim(pt1, pt2, r):
    lat1 = d2r(pt1[0])
    lon1 = d2r(pt1[1])
    lat2 = d2r(pt2[0])
    lon2 = d2r(pt2[1])
    dist_rad = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2 - lon1))
    angle_brut = math.acos((math.sin(lat2) - math.sin(lat1)*math.cos(dist_rad))/(math.cos(lat1)*math.sin(dist_rad)))
    if math.sin(lon2 - lon1) > 0:
        return r*dist_rad, r2d(angle_brut)
    else:
        return r*dist_rad, 360 - r2d(angle_brut)

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')

dossier = '20160415173900'
lat_hyp, lon_hyp = (32.8408, 130.8845)

path = (path_origin + '/'
        + 'Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier + '_vel_0-100km_2.0-8.0Hz/'
             + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env_smooth_S')

path_results = (path + '/'
                + dossier + '_results')

lst_fch = os.listdir(path_data)
lst_fch.sort()

fig, ax = plt.subplots(1, 1)

os.chdir(path_data)
for fich in lst_fch:
    st = read(fich)
    dt, az = dist_azim([lat_hyp, lon_hyp], [st[0].stats.sac.stla, st[0].stats.sac.stlo], 6400)
    if (az > 90 and az < 180) or (az > 270):
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax.fill_between(translate(t, 1 - st[0].stats.sac.t0),
                        st[0].stats.sac.dist,
                        norm1(st[0].data) + st[0].stats.sac.dist,
                        lw = 0.5, color = 'black', alpha = 0.2)

        if hasattr(st[0].stats.sac, 't1'):
            ax.vlines(st[0].stats.sac.t1 + 1 - st[0].stats.sac.t0, st[0].stats.sac.dist, st[0].stats.sac.dist + 1, lw = 0.5)
        if hasattr(st[0].stats.sac, 't2'):
            ax.vlines(st[0].stats.sac.t2 + 1 - st[0].stats.sac.t0, st[0].stats.sac.dist, st[0].stats.sac.dist + 1, lw = 0.5)
        if hasattr(st[0].stats.sac, 't3'):
            ax.vlines(st[0].stats.sac.t3 + 1 - st[0].stats.sac.t0, st[0].stats.sac.dist, st[0].stats.sac.dist + 1, lw = 0.5)

ax.set_xlim([0, 10])
ax.set_xlabel('Source time (s)')
ax.set_ylabel('Hypocenter distance (km)')
os.chdir(path_results)
fig.savefig('shape_fct_dist.pdf')
