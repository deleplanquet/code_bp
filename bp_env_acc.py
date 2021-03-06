import numpy as np
import pickle
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
import sys
from scipy import interpolate
from scipy.signal import hilbert
from obspy import read
from obspy.signal.util import smooth
from scipy import ndimage
from mpl_toolkits.basemap import Basemap

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
    for a in x_fault:
        for b in y_fault:
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 0] = x_cf + a*pasx*u_strike[0] + b*pasy*u_dip[0]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 1] = y_cf + a*pasx*u_strike[1] + b*pasy*u_dip[1]
            grill_fault[np.where(x_fault==a), np.where(y_fault==b), 2] = z_cf + a*pasx*u_strike[2] + b*pasy*u_dip[2]
    return grill_fault

#calcul de la matrice des tps de trajet pour une station
def trav_time(station, fault, velocity):
    x_sta, y_sta, z_sta = geo2cart(R_Earth + station[0]/1000, station[1], station[2])
    mat_time = np.zeros((len(fault[:, 0, 0]), len(fault[0, :, 0])))
    for a in range(len(fault[:, 0, 0])):
        for b in range(len(fault[0, :, 0])):
            mat_time[a, b] = math.sqrt(pow(x_sta - fault[a, b, 0], 2)
                                        + pow(y_sta - fault[a, b, 1], 2)
                                        + pow(z_sta - fault[a, b, 2], 2))/velocity
    return mat_time

#distance entre deux points, coordonnees cartesiennes
def dist(la1, lo1, el1, la2, lo2, el2):
    x1, y1, z1 = geo2cart(R_Earth + el1, la1, lo1)
    x2, y2, z2 = geo2cart(R_Earth + el2, la2, lo2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#normalisation avec max = 1
def norm1(vect):
    return [10*a/vect.max() for a in vect]

#fonction gaussienne
def gauss(x_data, H, mu):
    sigma = H/2.3548
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = 1./(sigma*math.sqrt(2))*math.exp(-(x_data[i] - mu)*(x_data[i] - mu)/(2*sigma*sigma))
    return y_data

#calcul distance et azimuth d'un point par rapport a un autre
''' distance et azimuth de B par rapport a A -> dist_azim(A, B) '''
def dist_azim(ptA, ptB):
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))/(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R_Earth*dist_rad, r2d(angle_brut)
    else:
        return R_Earth*dist_rad, 360 - r2d(angle_brut)

#recuperation position stations
print('     recuperation position stations')

dossier_seisme = sys.argv[1]
hyp_ondes = sys.argv[2]
select_station = sys.argv[3]

#dossier_seisme = dossier_seisme[0:-1]
print('     ', dossier_seisme, hyp_ondes, select_station)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Data/Kumamoto/' + dossier_seisme
if select_station == 'P':
    path_data = path + '/' + dossier_seisme + '_acc_env_selectP'
    path_results = path + '/' + dossier_seisme + '_acc_env_selectP_bp'
elif select_station == 'S':
    path_data = path + '/' + dossier_seisme + '_acc_env_selectS'
    path_results = path + '/' + dossier_seisme + '_acc_env_selectS_bp'
elif select_station == 'all':
    path_data = path + '/' + dossier_seisme + '_acc_env'
    path_results = path + '/' + dossier_seisme + '_acc_env_selectall_bp'

print(path_data)
print(path_results)

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

path_map = path_results + '/map'
path_ARF = path_results + '/ARF'
path_bp_env = path_results + '/bp_envelop'
path_bp_cos = path_results + '/bp_stationnaire'

if os.path.isdir(path_map) == False:
    os.makedirs(path_map)
if os.path.isdir(path_ARF) == False:
    os.makedirs(path_ARF)
if os.path.isdir(path_bp_env) == False:
    os.makedirs(path_bp_env)
if os.path.isdir(path_bp_cos) == False:
    os.makedirs(path_bp_cos)

list_fichier = os.listdir(path_data)
list_fichier = [a for a in list_fichier if (('UD' in a) == True and ('UD1' in a) == False)]

list_file_used = list_fichier

os.chdir(path)
with open(dossier_seisme + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

os.chdir(path_origin + '/Data')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

min_lat = None
min_lon = None
max_lat = None
max_lon = None

for cles in dict_seis.keys():
    if min_lat is None or dict_seis[cles]['lat'] < min_lat:
        min_lat = dict_seis[cles]['lat']
    if min_lon is None or dict_seis[cles]['lon'] < min_lon:
        min_lon = dict_seis[cles]['lon']
    if max_lat is None or dict_seis[cles]['lat'] > max_lat:
        max_lat = dict_seis[cles]['lat']
    if max_lon is None or dict_seis[cles]['lon'] > max_lon:
        max_lon = dict_seis[cles]['lon']

#constantes
R_Earth = 6400
#v_P = dict_vel[0]['fit']
#v_S = dict_vel[1]['fit']
v_P = 5.8
v_S = 3.4

if hyp_ondes == 'P':
    vel_used = v_P
    dict_vel_used = dict_vel[0]
elif hyp_ondes == 'S':
    vel_used = v_S
    dict_vel_used = dict_vel[1]

dict_delai = dict_vel[2]

print(vel_used)
print('vP', v_P, 'vS',  v_S)

#recuperation position faille

#strike = 223.53
#strike = 234
strike = 224
#dip = 0
#dip = 64
dip = 65
#l_fault = 90
#l_fault = 40
l_fault = 56
#w_fault = 57
#w_fault = 15
w_fault = 24
#lat_fault = [min_lat - 0.2, max_lat - 0.1]
#lat_fault = [32.65, 32.86]
lat_fault = [32.6477, 32.9858]
#long_fault = [min_lon + 0.1, max_lon + 0.2]
#long_fault = [130.72, 131.07]
long_fault = [130.7071, 131.1216]
pas_l = 2
pas_w = 2

#map avec les stations et la faille
print('     map avec stations et faille')

fig_pos_sta, ax_pos_sta = plt.subplots(1, 1)
m = Basemap(projection='merc',
            llcrnrlon=min_lon - 1,
            llcrnrlat=min_lat - 0.5,
            urcrnrlon=max_lon + 1,
            urcrnrlat=max_lat + 0.5,
            resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(int(min_lat - 0.5), int(max_lat + 0.5) + 1, 0.5), labels=[1, 0, 0, 0], linewidth=0)
m.drawmeridians(np.arange(int(min_lon - 1), int(max_lon + 1) + 1, 0.5), labels=[0, 0, 0, 1], linewidth=0)
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
#fig_pos_sta.savefig('map_stations.pdf')

#placement de la faille
print('     localisation de la faille en volume')

lat_cen_fault, long_cen_fault = milieu(lat_fault[0], long_fault[0], lat_fault[1], long_fault[1])
dir_cen_fault = [math.cos(d2r(lat_cen_fault))*math.cos(d2r(long_cen_fault)), math.cos(d2r(lat_cen_fault))*math.sin(d2r(long_cen_fault)), math.sin(d2r(lat_cen_fault))]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(long_cen_fault)), -math.cos(d2r(long_cen_fault)), 0])
vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
vect_dip = rotation(vect_perp_strike, dip, vect_strike)

coord_fault = fault([6400, lat_cen_fault, long_cen_fault], l_fault, w_fault, norm(vect_strike), norm(vect_dip), pas_l, pas_w)

#calcul matrice tps de trajet
print('     matrice tps de trajet')

travt = []

os.chdir(path_data)
for fichier in list_file_used:
    st = read(fichier)
    travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo], coord_fault, vel_used))

#ARF figures
print('     figures ARF')

frq_lst = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ARF_complex = np.zeros((len(coord_fault[:, 0, 0]), len(coord_fault[0, :, 0]), len(frq_lst)), dtype=complex)
ARF = np.zeros((len(coord_fault[:, 0, 0]), len(coord_fault[0, :, 0]), len(frq_lst)))

for ixf in range(int(l_fault/pas_l)):
    for iyf in range(int(w_fault/pas_w)):
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

stack_cos = np.zeros((int(l_fault/pas_l), int(w_fault/pas_w), int(2*f_ech/f_cos)))

for ista in range(len(list_file_used)):
    print('     ', list_file_used[ista], str(ista + 1) + '/' + str(len(list_file_used)))
    for ixf in range(int(l_fault/pas_l)):
        for iyf in range(int(w_fault/pas_w)):
            for it in range(int(2*f_ech/f_cos)):
                stack_cos[ixf, iyf, it] = stack_cos[ixf, iyf, it] + 1./len(list_file_used)*math.cos(d2r(ph_cos) + 2*math.pi*f_cos*(travt[ista][ixf, iyf] - travt[ista][x_source, y_source] + it/f_ech))

#stacks
print('     stacks envelop')

os.chdir(path_data)
length_t = int(30*st[0].stats.sampling_rate)
stack = np.zeros((int(l_fault/pas_l), int(w_fault/pas_w), length_t))

#st = read(list_file_used[0])
#tstart_ref = st[0].stats.starttime + st[0].stats.sac.t0 - 15
tstart_ref = None
for cles in dict_delai.keys():
    if tstart_ref == None or tstart_ref > dict_delai[cles]:
        tstart_ref = dict_delai[cles]

for station in list_file_used:
    st = read(station)
    tstart = st[0].stats.starttime
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    f = interpolate.interp1d(t, env_norm)

    ista = list_file_used.index(station)
    print('     ', station, str(ista + 1), '/', len(list_file_used))

    for ixf in range(int(l_fault/pas_l)):
        for iyf in range(int(w_fault/pas_w)):
            for it in range(length_t):
                #tshift = tstart_ref - tstart + travt[ista][ixf, iyf] - travt[0][0, 0] + dict_vel_used[st[0].stats.station] + it/st[0].stats.sampling_rate + 10.
                tshift = tstart_ref - dict_delai[st[0].stats.station] + travt[ista][ixf, iyf] + dict_vel_used[st[0].stats.station] + it/st[0].stats.sampling_rate
                if tshift > 0 and tshift < t[-1]:
                    stack[ixf, iyf, it] = stack[ixf, iyf, it] + 1./len(list_file_used)*f(tshift)

os.chdir(path)
with open('stack_acc_' + select_station, 'wb') as mon_fich_stack:
    mon_pick_stack = pickle.Pickler(mon_fich_stack)
    mon_pick_stack.dump(stack)

#plots projection 3d
print('     figures bp projection 3d')

os.chdir(path_bp_env)

coordmax = np.argmax(stack[:, :, :])
xmax = coordmax//(length_t*int(w_fault/pas_w))
ymax = (coordmax - xmax*length_t*int(w_fault/pas_w))//length_t
tmax = coordmax - xmax*length_t*int(w_fault/pas_w) - ymax*length_t

print(xmax, ymax, tmax)

xmesh = np.arange(0, l_fault/pas_l, 1)
ymesh = np.arange(0, w_fault/pas_w, 1)
tmesh = np.arange(0, length_t)/st[0].stats.sampling_rate

Xt, Yt = np.meshgrid(xmesh, ymesh)
Xy, Ty = np.meshgrid(xmesh, tmesh)
Tx, Yx = np.meshgrid(tmesh, ymesh)

print(len(Xt), len(Yt))
print(len(Xy), len(Ty))
print(len(Tx), len(Yx))
print(len(np.transpose(stack[:, ymax, :])), len(stack[xmax, :, :]), len(np.transpose(stack[:, :, tmax])))

fig_3d = plt.figure()
ax_3d = fig_3d.add_subplot(111, projection = '3d')
ax_3d.contour(Xy, np.transpose(stack[:, ymax, :]), Ty, 10, zdir = 'y', offset = 15, cmap = 'jet')
ax_3d.contour(stack[xmax, :, :], Yx, Tx, 10, zdir = 'x', offset = 0, cmap = 'jet')
ax_3d.contour(Xt, Yt, np.transpose(stack[:, :, tmax]), 10, zdir = 'z', offset = 0, cmap = 'jet')
ax_3d.set_xlabel('X (km)')
ax_3d.set_ylabel('Y (km)')
ax_3d.set_zlabel('t (s)')
ax_3d.set_zlim3d(0, 10)
fig_3d.savefig('plot_proj_3d.pdf')

fig_3d_2 = plt.figure()
ax_3d_2 = fig_3d_2.add_subplot(111, projection = '3d')
ax_3d_2.contour(Xt, Yt, np.transpose(stack[:, :, tmax]), 10, zdir = 'z', offset = tmax/st[0].stats.sampling_rate, cmap = 'jet')
ax_3d_2.contour(stack[xmax, :, :], Yx, Tx, 10, zdir = 'x', offset = xmax, cmap = 'jet')
ax_3d_2.contour(Xy, np.transpose(stack[:, ymax, :]), Ty, 10, zdir = 'y', offset = ymax, cmap = 'jet')
ax_3d_2.set_xlabel('X (km)')
ax_3d_2.set_ylabel('Y (km)')
ax_3d_2.set_zlabel('t (s)')
ax_3d_2.set_zlim3d(0, 10)
fig_3d_2.savefig('plot_proj_3d_intersect.pdf')

#plots
print('     figures bp envelop')

os.chdir(path_bp_env)
xxx = np.arange(0, l_fault, pas_l)
yyy = np.arange(0, w_fault, pas_w)
XXX, YYY = np.meshgrid(xxx, yyy)

dist_hyp, az_hyp = dist_azim([lat_fault[0], long_fault[0]], [dict_seis[dossier_seisme]['lat'], dict_seis[dossier_seisme]['lon']])
print([lat_fault[0], long_fault[0]], [dict_seis[dossier_seisme]['lat'], dict_seis[dossier_seisme]['lon']], dist_hyp, az_hyp)

for ij in range(int(length_t/5)):
    m = 5*ij
    fig_bp, ax_bp = plt.subplots(1, 1)
    ax_bp.set_xlabel('x')
    ax_bp.set_ylabel('y')
    #cax_bp = ax_bp.imshow(ndimage.rotate(stack[:, :, m], strike), cmap='jet', vmin=stack[:, :, :].min(), vmax=stack[:, :, :].max(), interpolation='none', origin='lower')
    cax_bp = ax_bp.imshow(stack[:, :, m], cmap='jet', vmin=stack[:, :, :].min(), vmax=stack[:, :, :].max(), interpolation='none', origin='lower')
    #cax_bp = ax_bp.imshow([XXX, YYY, stack[:, :, m]], cmap='jet', vmin=stack[:, :, :].min(), vmax=stack[:, :, :].max(), interpolation='none', origin='lower')
    im_hyp = ax_bp.scatter(- dist_hyp*math.sin(d2r(strike - az_hyp))/pas_w, (l_fault + dist_hyp*math.cos(d2r(strike - az_hyp)))/pas_l, s = 25, marker = '*', c = 'white')
    #im_hyp = ax_bp.plot(- 24.1449*math.sin(d2r(strike - 337.12))/pas_w, (l_fault + 24.1449*math.cos(d2r(strike - 337.12)))/pas_l, marker = '*', color = 'white')
    #ax_bp.imshow(ndimage.rotate(im_hyp, strike))
    fig_bp.savefig(dossier_seisme + '_acc_bp_' + str(m) + '_' + str(f_ech) + 'Hz.png')

ttime = np.arange(0, len(stack[0, 0, :]))
ttime = ttime/f_ech

fig_bptr, ax_bptr = plt.subplots(1, 1)
ax_bptr.set_xlabel('time (s)')
for jk in range(int(l_fault/pas_l)):
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
for jk in range(int(l_fault/pas_l)):
    ax_cos.plot(time_cos, stack_cos[jk, 7, :] + jk - l_fault/2)
fig_cos.savefig('bp_cos_traces.pdf')

fig_bp_cos, ax_bp_cos = plt.subplots(1, 1)
ax_bp_cos.set_xlabel('x')
ax_bp_cos.set_ylabel('y')
cax_bp_cos = ax_bp_cos.imshow(ndimage.rotate(stack_cos[:, :, 0], strike), cmap='jet', interpolation='none', origin='lower')
fig_bp_cos.savefig('bp_cos_' + str(f_cos) + '_Hz.pdf')



