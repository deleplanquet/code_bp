import numpy as np
from pylab import *
import math
import pickle
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
        norm_v = max([norm_v, a])
    return [a/norm_v for a in vect]

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

def dist_azim(ptA, ptB, R):
    '''distance et azimuth de B par rapport a A -> dist_azim(A, B)'''
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))/(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R*dist_rad, r2d(angle_brut)
    else:
        return R*dist_rad, 360 - r2d(angle_brut)

path_origin = os.getcwd()[:-6]

os.chdir(path_origin + '/Kumamoto')         #
with open('parametres_bin', 'rb') as mfch:  #
    mdpck = pickle.Unpickler(mfch)          #
    param = mdpck.load()                    #   load parametres

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']

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
             + '_env_smooth_'
             + hyp_bp + '_'
             + azim + 'deg')

path_results = (path + '/'
                + dossier
                + '_results/'
                + dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz')

path_pdf = (path_results + '/'
            + 'Traces_azimuth_pdf')

path_png = (path_results + '/'
            + 'Traces_azimuth_png')

if os.path.isdir(path_pdf) == False:
    os.makedirs(path_pdf)

if os.path.isdir(path_png) == False:
    os.makedirs(path_png)

lst_fch = os.listdir(path_data)






fig1, ax1 = plt.subplots(1, 1)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Azimuth (deg)')
ax1.set_title('0 < Hyp. Dist. < 50 km')
ax1.set_xlim([-10, 40])
ax1.set_ylim([0, 380])

fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Azimuth (deg)')
ax2.set_title('50 < Hyp. Dist. < 80 km')
ax2.set_xlim([-15, 35])
ax2.set_ylim([0, 380])

fig3, ax3 = plt.subplots(1, 1)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Azimuth (deg)')
ax3.set_title('80 < Hyp. Dist. < 100 km')
ax3.set_xlim([-20, 30])
ax3.set_ylim([0, 380])

os.chdir(path_data)
for fichier in lst_fch:
    print(fichier)
    st = read(fichier)
    hypo = [R_Earth - st[0].stats.sac.evdp,
            st[0].stats.sac.evla,
            st[0].stats.sac.evlo]
    pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel,
            st[0].stats.sac.stla,
            st[0].stats.sac.stlo]

    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    dst, azm = dist_azim(hypo[1:], pos_sta[1:], R_Earth)
    print(dst, azm)

    if dst > 50 and dst < 80:
        clr = 'red'
    elif dst < 80:
        clr = 'white'
    else:
        clr = 'white'

    if dst <= 50:
        #ax.plot([a - st[0].stats.sac.t0 for a in t], [5*a + azim for a in norm1(st[0].data)], linewidth = 0.2, color = clr)
        ax1.fill_between([a - st[0].stats.sac.t0 for a in t], azm, [10*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = 'black', alpha = 0.2)
    #ax2.fill_between([a - dst/3.4 + dst/5.8 - 5 for a in t], azm, [2*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = 'black', alpha = 0.2)
        ax1.scatter(0, azm, 3, color = 'darkorange')
        ax1.scatter(st[0].stats.sac.a - st[0].stats.sac.t0, azm, 3, color = 'steelblue')
        ax1.text(38, azm + 1, st[0].stats.station, fontsize = 6, ha = 'right')
    #ax2.text(-5, azm + 1, st[0].stats.station, fontsize = 3)
        #ax1.scatter(st[0].stats.sac.user1 - dst/3.4 + dst/5.8 - 5, azm, 3, color = 'red')
    elif dst <= 80:
        ax2.fill_between([a - st[0].stats.sac.t0 for a in t], azm, [10*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = 'black', alpha = 0.2)
        ax2.scatter(0, azm, 3, color = 'darkorange')
        ax2.scatter(st[0].stats.sac.a - st[0].stats.sac.t0, azm, 3, color = 'steelblue')
        ax2.text(33, azm + 1, st[0].stats.station, fontsize = 6, ha = 'right')
        #ax2.scatter(st[0].stats.sac.user1 - dst/3.4 + dst/5.8 - 5, azm, 3, color = 'red')
    else:
        ax3.fill_between([a - st[0].stats.sac.t0 for a in t], azm, [10*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = 'black', alpha = 0.2)
        ax3.scatter(0, azm, 3, color = 'darkorange')
        ax3.scatter(st[0].stats.sac.a - st[0].stats.sac.t0, azm, 3, color = 'steelblue')
        ax3.text(28, azm + 1, st[0].stats.station, fontsize = 6, ha = 'right')
        #ax3.scatter(st[0].stats.sac.user1 - dst/3.4 + dst/5.8 - 5, azm, 3, color = 'red')

os.chdir(path_results)
fig1.savefig(dossier
             + 'envelopes_0-50km_fct_azimuth.pdf')
fig1.savefig(dossier
             + 'envelopes_0-50km_fct_azimuth.png')
fig2.savefig(dossier
             + 'envelopes_50-80km_fct_azimuth.pdf')
fig2.savefig(dossier
             + 'envelopes_50-80km_fct_azimuth.png')
fig3.savefig(dossier
             + 'envelopes_80-100km_fct_azimuth.pdf')
fig3.savefig(dossier
             + 'envelopes_80-100km_fct_azimuth.png')

        #if dist(hypo, pos_sta) > 20 and dist(hypo, pos_sta) < 80:
        #    st = st.detrend(type = 'constant')
        #    tstart = st[0].stats.starttime + st[0].stats.sac.t0 - 15
        #    tend = tstart + 50
        #    st[0].trim(tstart, tend, pad=True, fill_value=0)
        ##    tr_brut = st[0]
        ##    tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
        ##envelop = abs(hilbert(tr_filt))
        ##env_smoothed = smooth(envelop, 20)
        ##    squared_tr = [a**2 for a in tr_filt]
        ##    env_smoothed = smooth(squared_tr, 20)

        #    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate

        #    lath = st[0].stats.sac.evla
        #    lonh = st[0].stats.sac.evlo
        #    dir_hypo = [math.cos(d2r(lath))*math.cos(d2r(lonh)), math.cos(d2r(lath))*math.sin(d2r(lonh)), math.sin(d2r(lath))]
        #    vect_nord = rotation(dir_hypo, 90, [math.sin(d2r(lonh)), - math.cos(d2r(lonh)), 0])

        #    alpha = angle(geo2cart([R_Earth, lath, lonh]), geo2cart([R_Earth, st[0].stats.sac.stla, st[0].stats.sac.stlo]))
        #    vect_dir_sta = pt2vect([R_Earth, lath, lonh], [R_Earth/math.cos(d2r(alpha)), st[0].stats.sac.stla, st[0].stats.sac.stlo])
        #    if st[0].stats.sac.stlo - lonh > 0:
        #        azimuth = angle(vect_nord, vect_dir_sta)
        #    else:
        #        azimuth = -angle(vect_nord, vect_dir_sta)
        #    ordo = azimuth# % 180

        #    env_norm_shift = [a + ordo for a in st[0].data]
        #    print('    ', fichier, lath, lonh, st[0].stats.sac.stla, st[0].stats.sac.stlo, azimuth, ordo)

        #    ax.plot(t, [a + ordo for a in norm1(st[0].data)], linewidth = 0.2, color = 'black')
#            ax.text(30, ordo, st[0].stats.station, fontsize=3)

        #    ax2.plot(t, [a + ordo for a in norm1(st[0].data)], linewidth = 0.2, color = 'black')
#            ax2.text(30, ordo, st[0].stats.station + ' ' + str(azimuth), fontsize=3)

        #    ax2.scatter(15 - st[0].stats.sac.t0 + st[0].stats.sac.a, ordo, s = 2, color = 'steelblue')

 #   os.chdir(path_data_5)
#    list_fichier = os.listdir(path_data_5)

#    for fichier in list_fichier:
#        st = read(fichier)
#        hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
#        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]

#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        dst, azm = dist_azim(hypo[1:], pos_sta[1:], R_Earth)

#        if dst > 50 and dst < 80:
#            clr = 'black'

#            ax.fill_between([a - dst/3.4 + dst/5.8 - 5 for a in t], azm, [2*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = clr, alpha = 0.2)
            #ax.fill_between([a - dst/3.4 + dst/5.8 - 5 for a in t], azm, [5*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = clr, alpha = 0.2)

    #os.chdir(path_data_2)
    #list_fichier = os.listdir(path_data_2)

#    for fichier in list_fichier:
#        st = read(fichier)
#        hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
#        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]

#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        dst, azm = dist_azim(hypo[1:], pos_sta[1:], R_Earth)

#        if dst > 80 and dst < 100:
#            clr = 'red'

#            ax.fill_between([a - dst/3.4 for a in t], azm, [5*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = clr, alpha = 0.2)
            
    #os.chdir(path_data_3)
    #list_fichier = os.listdir(path_data_3)

#    for fichier in list_fichier:
#        st = read(fichier)
#        hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
#        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]

#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        dst, azm = dist_azim(hypo[1:], pos_sta[1:], R_Earth)

#        if dst > 80 and dst < 100:
#            clr = 'blue'

#            ax.fill_between([a - dst/3.4 for a in t], azm, [5*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = clr, alpha = 0.2)

    #os.chdir(path_data_4)
    #list_fichier = os.listdir(path_data_4)

#    for fichier in list_fichier:
#        st = read(fichier)
#        hypo = [R_Earth - st[0].stats.sac.evdp, st[0].stats.sac.evla, st[0].stats.sac.evlo]
#        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]

#        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#        dst, azm = dist_azim(hypo[1:], pos_sta[1:], R_Earth)

#        if dst > 80 and dst < 100:
#            clr = 'red'

#            ax.fill_between([a - dst/3.4 + dst/5.8 - 5 for a in t], azm, [5*a + azm for a in norm1(st[0].data)], linewidth = 0.2, color = clr, alpha = 0.2)

#    os.chdir(path_results)
#    ax2.axvline(0, linewidth = 0.5, color = 'darkorange')
    #ax2.text(30, 185, '2016/04/16 08:02', color = 'black')
#    fig2.savefig('tt_sta_angle' + dossier + 'inf80th.pdf')

#ax.axvline(0, linewidth = 0.5, color = 'darkorange')
#fig.savefig('tt_sta_angle_tt_seisme_inf80th' + dossier + '.pdf')
