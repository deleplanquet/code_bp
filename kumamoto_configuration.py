import numpy as np
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
import sys
from mpl_toolkits.basemap import Basemap
from scipy import interpolate
from scipy.signal import hilbert
from obspy import read
from obspy.signal.util import smooth
from scipy import ndimage

#constantes
R_Earth = 6400
v_s = 6./math.sqrt(3)

#fonctions

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion angle radian -> degre
def r2d(angle):
    return angle*180/math.pi

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#normalisation
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

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

#bissectrice en 3d
def milieu(lat1, long1, lat2, long2):
    x1, y1, z1 = geo2cart(1, lat1, long1)
    x2, y2, z2 = geo2cart(1, lat2, long2)
    x_m = x1 + x2
    y_m = y1 + y2
    z_m = z1 + z2
    return [r2d(math.asin(z_m/math.sqrt(x_m*x_m + y_m*y_m + z_m*z_m))),
	    r2d(math.acos(x_m/math.sqrt(x_m*x_m + y_m*y_m)))]

#calcul de la matrice des tps de trajet pour une station
def fault(cen_fault, length, width, u_strike, u_dip, pasx, pasy):
    x_cf, y_cf, z_cf = geo2cart(cen_fault[0], cen_fault[1], cen_fault[2])
    x_fault = np.arange(-length/2/pasx, length/2/pasx)
    y_fault = np.arange(0, width/pasy)
    grill_fault = np.zeros((len(x_fault), len(y_fault), 3))
    for a in range(len(x_fault)):
    	for b in range(len(y_fault)):
    	    grill_fault[a, b, 0] = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
    	    grill_fault[a, b, 1] = y_cf + a*pasx*u_strike[1] + b*pasy*u_dip[1]
    	    grill_fault[a, b, 2] = z_cf + a*pasx*u_strike[2] + b*pasy*u_dip[2]
    return grill_fault

#calcul de la matrice des tps de trajet pour une station
def trav_time(station, fault):
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000, station[1], station[2])
    mat_time = np.zeros((len(fault[:, 0, 0]), len(fault[0, :, 0])))
    for a in range(len(fault[:, 0, 0])):
    	for b in range(len(fault[0, :, 0])):
    	    mat_time[a, b] = math.sqrt(pow(x_sta - fault[a, b, 0], 2)
					+ pow(y_sta - fault[a, b, 1], 2)
					+ pow(z_sta - fault[a, b, 2], 2))/v_s
    return mat_time

#recuperation position stations
print('     recuperation position stations')

dossier_seisme = sys.argv[1]
#dossier_seisme = dossier_seisme[0:-1]
print('     ', dossier_seisme)

path = '/localstorage/deleplanque'
path_data = path + '/Data/Kumamoto_sac/' + dossier_seisme
#path1 = path_data + '/' + dossier_seisme + '.kik'
#path2 = path_data + '/' + dossier_seisme + '.knt'
path_results = path + '/Results/Kumamoto/' + dossier_seisme
if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

path_map = path_results + '/map'
path_env = path_results + '/envelop'
path_ARF = path_results + '/ARF'
path_bp_syn = path_results + '/bp_synthetique'
path_bp_cos = path_results + '/bp_stationnaire'

if os.path.isdir(path_map) == False:
    os.makedirs(path_map)
if os.path.isdir(path_env) == False:
    os.makedirs(path_env)
if os.path.isdir(path_ARF) == False:
    os.makedirs(path_ARF)
if os.path.isdir(path_bp_syn) == False:
    os.makedirs(path_bp_syn)
if os.path.isdir(path_bp_cos) == False:
    os.makedirs(path_bp_cos)

list_fichier = os.listdir(path_data)
list_fichier = [a for a in list_fichier if (('UD' in a) or ('UD2' in a)) == True]

list_file_used = list_fichier

#recuperation position faille

strike = 234
dip = 64
#dip = 90
l_fault = 40
w_fault = 15
lat_fault = [32.65, 32.86]
long_fault = [130.72, 131.07]

#map avec les stations et la faille
print('     map avec stations et faille')

fig_pos_sta, ax_pos_sta = plt.subplots(1, 1)
m = Basemap(projection='merc',
    	    llcrnrlon=128,
    	    llcrnrlat=30,
    	    urcrnrlon=140,
    	    urcrnrlat=37,
    	    resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(30, 38, 2), labels=[1, 0, 0, 0], linewidth=0)
m.drawmeridians(np.arange(128, 141, 2), labels=[0, 0, 0, 1], linewidth=0)
ax_pos_sta.plot(x_fault,
                y_fault,
                color='green',
                linewidth = 0.3,
                zorder=1)

os.chdir(path_data)
for fichier in list_file_used:
    st = read(fichier)
    x_sta, y_sta = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    if st[0].stats.channel == 'UD2':
    	couleur = 'red'
    else:
    	couleur = 'blue'
    ax_pos_sta.scatter(x_sta,
    	    	       y_sta,
    	    	       2,
    	    	       marker='^',
    	    	       color=couleur,
    	    	       zorder=2)
    ax_pos_sta.text(x_sta,
    	    	    y_sta,
    	    	    st[0].stats.station,
    	    	    fontsize=2,
    	    	    ha='center',
    	    	    va='bottom',
    	    	    zorder=3)

x_epi, y_epi = m(st[0].stats.sac.evlo, st[0].stats.sac.evla)
ax_pos_sta.scatter(x_epi,
    	    	   y_epi,
    	    	   5,
    	    	   marker='*',
    	    	   color='green',
    	    	   zorder=4)

os.chdir(path_map)
fig_pos_sta.savefig('map_stations.pdf')

#envelope
print('     envelopes')

fig_env_all, ax_env_all = plt.subplots(1, 1)
ax_env_all.set_xlabel('time (s)')

cpt = 0

for fichier in list_file_used:
    os.chdir(path_data)
    st = read(fichier)
    st = st.detrend(type='constant') #retirer la moyenne
    tr_brut = st[0]
    tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
    envelop = abs(hilbert(tr_filt))
    env_smoothed = smooth(envelop, 20)

    t = np.arange(tr_brut.stats.npts)/tr_brut.stats.sampling_rate

    os.chdir(path_env)

    fig_env, ax_env = plt.subplots(1, 1)
    ax_env.set_xlabel('time (s)')
    ax_env.plot(t, tr_brut, linewidth=0.2, color='black')
    ax_env.plot(t, env_smoothed, linewidth=1, color='red')
    fig_env.savefig('envelope_' + str(st[0].stats.station) + '.pdf')

    ax_env_all.plot(t, env_smoothed + cpt, linewidth=0.5)

    cpt = cpt + 2000

fig_env_all.savefig('envelope_all.pdf')

#placement de la faille
print('     localisation de la faille en volume')

lat_cen_fault, long_cen_fault = milieu(lat_fault[0], long_fault[0], lat_fault[1], long_fault[1])
dir_cen_fault = [math.cos(d2r(lat_cen_fault))*math.cos(d2r(long_cen_fault)), math.cos(d2r(lat_cen_fault))*math.sin(d2r(long_cen_fault)), math.sin(d2r(lat_cen_fault))]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(long_cen_fault)), -math.cos(d2r(long_cen_fault)), 0])
vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
vect_dip = rotation(vect_perp_strike, dip, vect_strike)

coord_fault = fault([6400, lat_cen_fault, long_cen_fault], l_fault, w_fault, norm(vect_strike), norm(vect_dip), 1., 1.)

#calcul matrice tps de trajet
print('     matrice tps de trajet')

travt = []

os.chdir(path_data)
for fichier in list_file_used:
    st = read(fichier)
    travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], coord_fault))

#ARF figures
print('     figures ARF')

frq_lst = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ARF_complex = np.zeros((len(coord_fault[:, 0, 0]), len(coord_fault[0, :, 0]), len(frq_lst)), dtype=complex)
ARF = np.zeros((len(coord_fault[:, 0, 0]), len(coord_fault[0, :, 0]), len(frq_lst)))

for ixf in range(l_fault):
    for iyf in range(w_fault):
    	for freq in range(len(frq_lst)):
    	    for ista in range(len(list_file_used)):
    	    	ARF_complex[ixf, iyf, freq] = ARF_complex[ixf, iyf, freq] + cmath.exp(2*math.pi*1j*frq_lst[freq]*(travt[ista][ixf, iyf] - travt[ista][20, 7]))
    	    ARF[ixf, iyf, freq] = pow(abs(ARF_complex[ixf, iyf, freq]/len(list_file_used)), 2)

os.chdir(path_ARF)

fig_ARF, ax_ARF = plt.subplots(2, 5)
for freq in range(len(frq_lst)):
    ax_ARF[freq//5, freq%5].set_title(str(frq_lst[freq]) + 'Hz')
    ax_ARF[freq//5, freq%5].set_xlabel('k')
    ax_ARF[freq//5, freq%5].set_ylabel('l')
    ax_ARF[freq//5, freq%5].imshow(ndimage.rotate(ARF[:, :, freq], strike), cmap='jet', interpolation='none', origin = 'lower')

    fig_ARF_unique, ax_ARF_unique = plt.subplots(1, 1)
    ax_ARF_unique.set_xlabel('k')
    ax_ARF_unique.set_ylabel('l')
    ax_ARF_unique.imshow(ndimage.rotate(ARF[:, :, freq], strike), cmap='jet', interpolation='none', origin='lower')
    fig_ARF_unique.savefig('ARF_' + str(frq_lst[freq]) + 'Hz.pdf')

fig_ARF.savefig('ARF.pdf')

#signal stationnaire
print('     stacks stationnaire')

f_ech = 50
f_cos = 2
ph_cos = 0 #phase du cos en degre

x_source = 20
y_source = 7

stack_cos = np.zeros((l_fault, w_fault, int(2*f_ech/f_cos)))

for ista in range(len(list_file_used)):
    print('     ', list_file_used[ista], str(ista + 1) + '/' + str(len(list_file_used)))
    for ixf in range(l_fault):
    	for iyf in range(w_fault):
    	    for it in range(int(2*f_ech/f_cos)):
    	    	stack_cos[ixf, iyf, it] = stack_cos[ixf, iyf, it] + 1./len(list_file_used)*math.cos(d2r(ph_cos) + 2*math.pi*f_cos*(travt[ista][ixf, iyf] - travt[ista][x_source, y_source] + it/f_ech))

#stacks
print('     stacks synthetique')

time = np.arange(0, 10, 1./f_ech)
signal = np.zeros((len(time)))
for i in range(f_ech):
    signal[int(4*f_ech) + i] = 1 - i/f_ech #signal de 10 sec echantillone a f_ech avec un triangle d'amplitude 1 de largeur 1 sec

f = interpolate.interp1d(time, signal)

stack = np.zeros((l_fault, w_fault, 20000))

for ista in range(len(list_file_used)):
#for ista in range(10):
    print('     ', list_file_used[ista], str(ista + 1) + '/' + str(len(list_file_used)))
    for ixf in range(l_fault):
    	for iyf in range(w_fault):
    	    for it in range(len(time)):
    	    	if travt[ista][ixf, iyf] - travt[ista][x_source, y_source] + it/f_ech > 0 and travt[ista][ixf, iyf] - travt[ista][x_source, y_source] + it/f_ech < 9.8:
    	    	    stack[ixf, iyf, it] = stack[ixf, iyf, it] + 1./len(list_file_used)*f(travt[ista][ixf, iyf] - travt[ista][x_source, y_source] + it/f_ech)

#plots
print('     figures bp synthetique')

os.chdir(path_bp_syn)

for ij in range(100):
    m = 5*ij
    fig_bp, ax_bp = plt.subplots(1, 1)
    ax_bp.set_xlabel('x')
    ax_bp.set_ylabel('y')
    cax_bp = ax_bp.imshow(ndimage.rotate(stack[:, :, m], strike), cmap='jet', vmin=stack[:, :, :].min(), vmax=stack[:, :, :].max(), interpolation='none', origin='lower')
    fig_bp.savefig('bp_' + str(m) + '_' + str(f_ech) + 'Hz.png')

ttime = np.arange(0, len(stack[0, 0, :]))
ttime = ttime/f_ech

fig_bptr, ax_bptr = plt.subplots(1, 1)
ax_bptr.set_xlabel('time (s)')
ax_bptr.plot(time, signal - l_fault)
for jk in range(l_fault):
    ax_bptr.plot(ttime, stack[jk, 7, :] + jk - l_fault/2)
ax_bptr.set_xlim(0, 20)
fig_bptr.savefig('bp_traces.pdf')

print('     figures bp stationnaire')

os.chdir(path_bp_cos)

time_cos = np.arange(0, 2*f_ech/f_cos)
time_cos = time_cos/f_ech
signal_cos = np.zeros((len(time_cos)))
for i in range(len(signal_cos)):
    signal_cos[i] = math.cos(2*math.pi*f_cos*time_cos[i] + d2r(ph_cos))

fig_cos, ax_cos = plt.subplots(1, 1)
ax_cos.set_xlabel('time (s)')
ax_cos.plot(time_cos, signal_cos - l_fault)
#ax_cos.plot(time_cos, math.cos(2*math.pi*f_cos*time_cos + d2r(ph_cos)) - l_fault)
for jk in range(l_fault):
    ax_cos.plot(time_cos, stack_cos[jk, 7, :] + jk - l_fault/2)
fig_cos.savefig('bp_cos_traces.pdf')

fig_bp_cos, ax_bp_cos = plt.subplots(1, 1)
ax_bp_cos.set_xlabel('x')
ax_bp_cos.set_ylabel('y')
cax_bp_cos = ax_bp_cos.imshow(ndimage.rotate(stack_cos[:, :, 0], strike), cmap='jet', interpolation='none', origin='lower')
fig_bp_cos.savefig('bp_cos_' + str(f_cos) + '_Hz.pdf')











