import numpy as np
from pylab import *
import math
import matplotlib.pyplot as plt
import os
from obspy import read
from obspy.signal.util import smooth

#constantes
R_Earth = 6400

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion angle radian -> degre
def r2d(angle):
    return angle*180/math.pi

#conversion coordonnees geographiques -> cartesien
def geo2cart(pt):
    r = pt[0]
    rlat = d2r(pt[1])
    rlon = d2r(pt[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#normalisation
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

#normalisation avec max = 1
def norm1(vect):
    norm_v = 0
    for a in vect:
        norm_v = norm_v + a*a
    return [90*a/pow(norm_v, 0.5) for a in vect]

#rotation 3d d'angle theta et d'axe passant par l'origine porte par le vecteur (a, b, c) de norme 1, repere orthonormal direct
def rotation(u, theta, OM):
    """ attention OM unitaire """
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    radian = d2r(theta)
    #coefficients de la matrice de rotation
    mat = array([[a*a + (1 - a*a)*math.cos(radian),
                  a*b*(1 - math.cos(radian)) - c*math.sin(radian),
                  a*c*(1 - math.cos(radian)) + b*math.sin(radian)],
                 [a*b*(1 - math.cos(radian)) + c*math.sin(radian),
                  b*b + (1 - b*b)*math.cos(radian),
                  b*c*(1 - math.cos(radian)) - a*math.sin(radian)],
                 [a*c*(1 - math.cos(radian)) - b*math.sin(radian),
                  b*c*(1 - math.cos(radian)) + a*math.sin(radian),
                  c*c + (1 - c*c)*math.cos(radian)]])
    #rearrangement du vecteur auquel on applique la rotation
    vect = array([[u[0]],
                  [u[1]],
                  [u[2]]])
    #rotation du vecteur u de theta autour de OM
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])

#angle entre deux vecteurs, return en deg
def angle(vect1, vect2):
    x1, y1, z1 = norm(vect1)
    x2, y2, z2 = norm(vect2)
    #x1, y1, z1 = norm(geo2cart(vect1[0], vect1[1], vect1[2]))
    #x2, y2, z2 = norm(geo2cart(vect2[0], vect2[1], vect2[2]))
    return r2d(math.acos(x1*x2 + y1*y2 + z1*z2))

#vecteur a partir de deux points
def pt2vect(pt1, pt2):
    #x1, y1, z1 = pt1
    #x2, y2, z2 = pt2
    x1, y1, z1 = geo2cart(pt1)
    x2, y2, z2 = geo2cart(pt2)
    return norm([x2-x1, y2-y1, z2-z1])

#distance entre deux points, coordonnees cartesiennes
def dist(pt1, pt2):
    x1, y1, z1 = geo2cart(pt1)
    x2, y2, z2 = geo2cart(pt2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#list_dossier = ['20160416080200']#, '20160415072000']#, '20160414230200']
list_dossier = ['20160415072000']

#path = '/localstorage/deleplanque'
path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_env'
path_results = path + '/Results'

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Azimuth (deg)')

for dossier in list_dossier:
    print(dossier)
    os.chdir(path_data + '/' + dossier)
    list_fichier = os.listdir(path_data + '/' + dossier)
    list_fichier = [a for a in list_fichier if (('UD' in a) == True and ('UD1' in a) == False)]

    fig2, ax2 = plt.subplots(1, 1)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Azimuth (deg)')

    for fichier in list_fichier:
        st = read(fichier)
        hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]
        if dist(hypo, pos_sta) > 20 and dist(hypo, pos_sta) < 80:
            st = st.detrend(type = 'constant')
            tstart = st[0].stats.starttime + st[0].stats.sac.t0 - 15
            tend = tstart + 50
            st[0].trim(tstart, tend, pad=True, fill_value=0)
        #    tr_brut = st[0]
        #    tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
        #envelop = abs(hilbert(tr_filt))
        #env_smoothed = smooth(envelop, 20)
        #    squared_tr = [a**2 for a in tr_filt]
        #    env_smoothed = smooth(squared_tr, 20)

            t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate

            lath = st[0].stats.sac.evla
            lonh = st[0].stats.sac.evlo
            dir_hypo = [math.cos(d2r(lath))*math.cos(d2r(lonh)), math.cos(d2r(lath))*math.sin(d2r(lonh)), math.sin(d2r(lath))]
            vect_nord = rotation(dir_hypo, 90, [math.sin(d2r(lonh)), - math.cos(d2r(lonh)), 0])

            alpha = angle(geo2cart([R_Earth, lath, lonh]), geo2cart([R_Earth, st[0].stats.sac.stla, st[0].stats.sac.stlo]))
            vect_dir_sta = pt2vect([R_Earth, lath, lonh], [R_Earth/math.cos(d2r(alpha)), st[0].stats.sac.stla, st[0].stats.sac.stlo])
            if st[0].stats.sac.stlo - lonh > 0:
                azimuth = angle(vect_nord, vect_dir_sta)
            else:
                azimuth = -angle(vect_nord, vect_dir_sta)
            ordo = azimuth# % 180

            env_norm_shift = [a + ordo for a in st[0].data]
            print('    ', fichier, lath, lonh, st[0].stats.sac.stla, st[0].stats.sac.stlo, azimuth, ordo)

            ax.plot(t, [a + ordo for a in norm1(st[0].data)], linewidth = 0.2, color = 'black')
#            ax.text(30, ordo, st[0].stats.station, fontsize=3)

            ax2.plot(t, [a + ordo for a in norm1(st[0].data)], linewidth = 0.2, color = 'black')
#            ax2.text(30, ordo, st[0].stats.station + ' ' + str(azimuth), fontsize=3)

            ax2.scatter(15 - st[0].stats.sac.t0 + st[0].stats.sac.a, ordo, s = 2, color = 'steelblue')

    os.chdir(path_results)
    ax2.axvline(15, linewidth = 0.5, color = 'darkorange')
    fig2.savefig('tt_sta_angle' + dossier + '.pdf')

ax.axvline(15, linewidth = 0.5, color = 'darkorange')
fig.savefig('tt_sta_angle_tt_seisme.pdf')
