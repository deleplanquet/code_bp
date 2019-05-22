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
from obspy import Trace
from obspy.core import UTCDateTime
#from mpl_toolkits.basemap import Basemap

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
    #y_fault = np.arange(0, width/pasy)
    y_fault = np.arange(-width/2/pasy, width/2/pasy)
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
    return [a/vect.max() for a in vect]

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

#nombre de lignes d'un fichier
def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#union d'intervalles
def interv_uni(list_inter):
    list_debut = [ a[0] for a in list_inter]
    list_fin = [ a[1] for a in list_inter]
    list_debut.sort()
    list_fin.sort()
    list_inter_final = []
    nb_superp = 0
    debut_inter_courant = 0
    while list_debut:
        if list_debut[0] < list_fin[0]:
            pos_debut = list_debut.pop(0)
            if nb_superp == 0:
                debut_inter_courant = pos_debut
            nb_superp += 1
        elif list_debut[0] > list_fin[0]:
            pos_fin = list_fin.pop(0)
            nb_superp -= 1
            if nb_superp == 0:
                list_inter_final.append([debut_inter_courant, pos_fin])
        else:
            list_debut.pop(0)
            list_fin.pop(0)
    if list_fin:
        pos_fin = list_fin[-1]
        list_inter_final.append([debut_inter_courant, pos_fin])
    return list_inter_final

#recuperation position stations
print('     recuperation position stations')

path_origin = os.getcwd()[:-6]                  #
os.chdir(path_origin + '/Kumamoto')             #
with open('parametres_bin', 'rb') as my_fch:    #
    my_dpck = pickle.Unpickler(my_fch)          #
    param = my_dpck.load()                      #   load parametres

dossier = param['dossier']                                                                          #   |
path = path_origin + '/Kumamoto/' + dossier                                                         #   v

dt_type = param['composante']                                                                       #   |
hyp_bp = param['ondes_select']                                                                      #   |
couronne = param['couronne']                                                                        #   |
azim = param['angle']                                                                               #   v
frq = param['band_freq']                                                                            #
R_Earth = param['R_Earth']                                                                          #

os.chdir(path + '/'
         + dossier + '_results/'
         + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz')                                          #
with open(dossier + '_veldata', 'rb') as mon_fich:      #
    mon_depick = pickle.Unpickler(mon_fich)             #
    dict_vel = mon_depick.load()                        #   load station corrections

if hyp_bp == 'P':                                                                                   #
    vel_used = param['vP']                                                                          #
    dict_vel_used = dict_vel[0]                                                                     #
elif hyp_bp == 'S':                                                                                 #
    vel_used = param['vS']                                                                          #
    dict_vel_used = dict_vel[1]                                                                     #
strike = param['strike']                                                                            #
dip = param['dip']                                                                                  #
l_fault = param['l_fault']                                                                          #
w_fault = param['w_fault']                                                                          #
pas_l = param['pas_l']                                                                              #
pas_w = param['pas_w']                                                                              #
samp_rate = param['samp_rate']                                                                      #
length_time = param['length_t']                                                                     #   parametres stockes
selected_patch = 'patch_85'
l_smooth = param['smooth']

###########################
###########################
past = ''
#past = 'patch_85' # ce qui va avant slected_patch
pastpast = '' # a garder vide pour modifier a chaque fois la trace originelle
#pastpast = 'patch_85' # le dossier des fichiers utilises
###########################
###########################

if past != '':
    past = '_' + past
if pastpast != '':
    pastpast = '_' + pastpast

path = (path_origin                                     #
        + '/Kumamoto/'                                  #
        + dossier)                                      #
                                                        #
path_data = (path + '/'                                 #
             + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/'                              #
             + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg')                            #
                                                        #

path_data_1 = (path_data + pastpast)

if past == '':
    path_retrait = (path_data + '_bpinv/'
                + 'smoothed_traces')
else:
    path_retrait = (path_data + past + '_complementaire_bp_inv/'
                    + 'smoothed_traces')

path_data_2 = (path_data + past + '_' + selected_patch)                        #
                                                        #
path_data_3 = (path_data + past + '_' + selected_patch + '_complementaire')    #

path_bpinv = (path_data_3 + '_bp_inv/'
              + 'releves')

path_bpinvtr = (path_data_3 + '_' + 'bp_inv/'
                + 'traces')

path_bpinvsm = (path_data_3 + '_' + 'bp_inv/'
                + 'smoothed_traces')

pth_ptch = [path_data_2, path_data_3]
                                                        #
path_results = (path + '/'                              #
                + dossier + '_results/'                           #
                + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz')                           #
                                                        #
path_results_2 = (path_results + '/'                         #
                  + 'Traces_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg')                       #   dossiers de travail

if os.path.isdir(path_data_2) == False:         #
    os.makedirs(path_data_2)                    #
                                                #
if os.path.isdir(path_data_3) == False:         #
    os.makedirs(path_data_3)                    #
                                                #
if os.path.isdir(path_results) == False:        #
    os.makedirs(path_results)                   #
                                                #
if os.path.isdir(path_results_2) == False:      #   creation des dossiers de travail
    os.makedirs(path_results_2)                 #   dans le cas ou il n'existe pas deja

if os.path.isdir(path_bpinv) == False:
    os.makedirs(path_bpinv)

if os.path.isdir(path_bpinvtr) == False:
    os.makedirs(path_bpinvtr)

if os.path.isdir(path_bpinvsm) == False:
    os.makedirs(path_bpinvsm)
            
lst_fch = []                        #
lst_fch = os.listdir(path_data_1)     #   recupere la liste des noms des fichiers contenant les donnees
lst_fch.sort()                      #   les trie

os.chdir(path_origin + '/Kumamoto')             #
with open('ref_seismes_bin', 'rb') as my_fch:   #
    my_dpck = pickle.Unpickler(my_fch)          #
    dict_seis = my_dpck.load()                  #   load caracteristiques seismes

yea_seis = int(dict_seis[dossier]['nFnet'][0:4])        #
mon_seis = int(dict_seis[dossier]['nFnet'][4:6])        #
day_seis = int(dict_seis[dossier]['nFnet'][6:8])        #
hou_seis = int(dict_seis[dossier]['nFnet'][8:10])       #
min_seis = int(dict_seis[dossier]['nFnet'][10:12])      #
sec_seis = int(dict_seis[dossier]['nFnet'][12:14])      #
mse_seis = int(dict_seis[dossier]['nFnet'][14:16])      #
                                                        #
t_origin_rupt = UTCDateTime(yea_seis,                   #
                            mon_seis,                   #
                            day_seis,                   #
                            hou_seis,                   #
                            min_seis,                   #
                            sec_seis,                   #
                            mse_seis)                   #   temps du debut de la rupture

lat_hyp = dict_seis[dossier]['lat']     #
lon_hyp = dict_seis[dossier]['lon']     #
dep_hyp = dict_seis[dossier]['dep']     #   position de l'hypocentre du seisme etudie

dir_cen_fault = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)),                 #
                 math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)),                 #
                 math.sin(d2r(lat_hyp))]                                        #   defini le vecteur CH: "centre Terre" -> "hypocentre"
                                                                                #
vect_nord = rotation(dir_cen_fault,                                             #   defini le vecteur N: nord local
                     90,                                                        #   par la rotation du vecteur CH de 90 degres
                     [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])      #   autour du vecteur Ouest-Est local
                                                                                #
vect_strike = rotation(vect_nord,                                               #   defini le vecteur S: direction du strike
                       - strike,                                                #   par la rotation du vecteur N de "strike" degres
                       dir_cen_fault)                                           #   autour du vecteur CH
                                                                                #
vect_perp_strike = rotation(vect_nord,                                          #   defini le vecteur PS: perpendiculaire a S
                            - strike - 90,                                      #   par la rotation du vecteur N de "strike" + 90 degres
                            dir_cen_fault)                                      #   autour du vecteur CH
                                                                                #
vect_dip = rotation(vect_perp_strike,                                           #   defini le vecteur D: direction du dip
                    dip,                                                        #   par la rotation du vecteur PS de "dip" degres
                    vect_strike)                                                #   autour du vecteur S
                                                                                #
coord_fault = fault([R_Earth - dep_hyp, lat_hyp, lon_hyp],                      #
                    l_fault,                                                    #
                    w_fault,                                                    #
                    norm(vect_strike),                                          #
                    norm(vect_dip),                                             #   defini les coordonnees de chaque subfault
                    pas_l,                                                      #   l'ensemble centre sur l'hypocentre
                    pas_w)                                                      #   oriente selon les vecteurs S et D

tstart_ref = None                                                       #
                                                                        #
os.chdir(path_data_1)                                                     #
for fichier in lst_fch:                                                 #
    st = read(fichier)                                                  #
    if tstart_ref == None or tstart_ref - st[0].stats.starttime > 0:    #   sonde toutes les stations
        tstart_ref = st[0].stats.starttime                              #   pour trouver celle qui detecte le plus tot
        
os.chdir(path_data_1)                                                                             #
travt = []                                                                                      #
tmin = None                                                                                     #
dmin = None                                                                                     #
                                                                                                #
for fichier in lst_fch:                                                                         #
    st = read(fichier)                                                                          #
    travt.append(trav_time([st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo],  #
                           coord_fault,                                                         #
                           vel_used))                                                           #
    if dmin == None or dmin > st[0].stats.sac.dist:                                             #
        dmin = st[0].stats.sac.dist                                                             #
    if tmin == None or tmin > st[0].stats.sac.t0:                                               #   calcule les temps de trajet
        tmin = st[0].stats.sac.t0                                                               #   entre chaque station
print(tmin)                                                                                     #   et chaque subfault

#os.chdir(path)                                                  #
#with open(dossier + '_' + past + selected_patch, 'rb') as my_fch:      #
#    my_dpck = pickle.Unpickler(my_fch)                          #
#    dict_ok = my_dpck.load()                                    #   load le patch
    
#print(dossier + '_' + past + selected_patch + ' loaded')
#identified_patch = {}                                                                   #
                                                                                        #
#os.chdir(path_data_1)                                                                     #
#for station in lst_fch:                                                                 #   pour chaque station
#    list_inter = []                                                                     #
#    st = read(station)                                                                  #
#    ista = lst_fch.index(station)                                                       #
#    for ip in dict_ok.keys():                                                           #   pour chaque subfault "eclairee"
#        ix = int(int(ip)//len(coord_fault[0, :, 0]))                                    #
#        iy = int(int(ip)%len(coord_fault[0, :, 0]))                                     #
#        for it in dict_ok[ip]:                                                          #   pour chaque tps ou il y a eu "eclairage"
#            tshift = (travt[ista][ix, iy]                                               #
#                      - (st[0].stats.starttime - t_origin_rupt)                         #
#                      + dict_vel_used[st[0].stats.station]                              #
#                      - 5                                                               #
#                      + it/samp_rate)                                                   #   on stocke l'interval temporel
#            list_inter.append([tshift, tshift + 1.01/samp_rate])                        #   associe a la trace
#    identified_patch[st[0].stats.station] = interv_uni(list_inter)                      #   fait l'union des intervales
#                                                                                        #
#for station in identified_patch.keys():                                                 #
#    print(station, identified_patch[station][0][0], identified_patch[station][0][1])    #   affiche dans le terminal

length_t = int(length_time*samp_rate)
stack_0 = np.zeros((len(coord_fault[:, 0, 0]),
                     len(coord_fault[0, :, 0]),
                     length_t))
stack_1 = np.zeros((len(coord_fault[:, 0, 0]),
                     len(coord_fault[0, :, 0]),
                     length_t))
stack = [stack_0, stack_1]
scission = ['', '_complementaire']

print(path_data_1)
for station in lst_fch:
    for scis in scission:
        os.chdir(path_data_1)
        st = read(station)
        os.chdir(path_retrait)
        st_r = read(st[0].stats.station)
        st_r_max = (st_r[0].data).max()
        tr = np.zeros(st[0].stats.npts)
        cpt = 0
        for i in range(len(tr)):
            cpt = cpt + 1
            time = cpt/st[0].stats.sampling_rate
            if scis == scission[0]:
                tr[i] = st[0].data[i]*st_r[0].data[i]
            else:
                tr[i] = st[0].data[i]*(st_r_max - st_r[0].data[i])
            #if (time >= identified_patch[st[0].stats.station][0][0]                                                 #
            #    and time <= identified_patch[st[0].stats.station][0][1]):                                           #
                #tr[cpt] = 0.2*tr[cpt]                                                                              #
                #tmp = math.pi/4*math.sin(math.pi*(time
            #    tmp = math.sin(math.pi*(time
            #                                - identified_patch[st[0].stats.station][0][0])
            #                              /(identified_patch[st[0].stats.station][0][1]
            #                                - identified_patch[st[0].stats.station][0][0]))
            #    if scis == scission[0]:
            #        tr[cpt] = tmp*tr[cpt]
            #    else:
            #        tr[cpt] = (1 - tmp)*tr[cpt]
            #elif cpt < 5000:
            #    if scis == scission[0]:
            #        tr[cpt] = 0
        tr[-1] = (st[0].data).max()

        os.chdir(pth_ptch[scission.index(scis)])                                                                    #   enregistre les traces modifiees
        #st[0].stats.sac.user1 = identified_patch[st[0].stats.station][0][0]                                         #   
        #st[0].stats.sac.user2 = identified_patch[st[0].stats.station][0][1]                                         #   trace modifiee =
        tr_reg = Trace(np.asarray(tr), st[0].stats)                                                                 #   trace originale
        tr_reg.write(station[:-4] + '_' + selected_patch + scis + '.sac', format = 'SAC')                    #   - partie contribuant au patch

        st = read(station[:-4] + '_' + selected_patch + scis + '.sac')
        tstart = st[0].stats.starttime
        env_norm = norm1(st[0].data)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        f = interpolate.interp1d(t, env_norm)
        ista = lst_fch.index(station)
        print('     ', station, st[0].stats.sampling_rate, str(ista + 1), '/', len(lst_fch), '     ', scission.index(scis)) 
        for ix in range(len(coord_fault[:, 0, 0])):
            for iy in range(len(coord_fault[0, :, 0])):
                for it in range(length_t):
                    tshift = (travt[ista][ix, iy]
                              - (st[0].stats.starttime - t_origin_rupt)
                              + dict_vel_used[st[0].stats.station]
                              - 5
                              + it/samp_rate)
                    if tshift > 0 and tshift < t[-1]:
                        stack[scission.index(scis)][ix, iy, it] = (stack[scission.index(scis)][ix, iy, it]
                                                                   + 1./len(lst_fch)*f(tshift))

os.chdir(path_results)
for scis in scission:
    with open(dossier
              + '_vel_'
              + couronne + 'km_'
              + frq + 'Hz_'
              + dt_type
              + '_env_smooth_'
              + hyp_bp + '_'
              + azim + 'deg_stack3D'
              + past + '_'
              + selected_patch + scis, 'wb') as my_fch:
        my_pck = pickle.Pickler(my_fch)
        my_pck.dump(stack[scission.index(scis)])

###############################
# bp inverse
###############################

stckmx = stack[0][:, :, :].max()
thresh = int(selected_patch[-2:]) *0.01

for sta in lst_fch:
    os.chdir(path_data_1)
    st = read(sta)
    #print(sta, st[0].stats.starttime, dict_vel_used[st[0].stats.station], t_origin_rupt)
    ista = lst_fch.index(sta)
    station = {}
    for i in range(len(stack[1][:, 0, 0])):
        for j in range(len(stack[1][0, :, 0])):
            for k in range(len(stack[1][0, 0, :])):
                tshift = (travt[ista][i,j]
                          - (st[0].stats.starttime - t_origin_rupt)
                          + dict_vel_used[st[0].stats.station]
                          - 5
                          + k/samp_rate)
                station[tshift] = stack[0][i, j, k]
    os.chdir(path_bpinv)
    with open(st[0].stats.station, 'wb') as mfch:
        mpck = pickle.Pickler(mfch)
        mpck.dump(station)

lst_bpinv = os.listdir(path_bpinv)

for sta in lst_fch:
    os.chdir(path_data_1)
    st = read(sta)
    os.chdir(path_bpinv)
    bpinv = np.zeros(st[0].stats.npts)
    with open(sta[:6], 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        station = mdpk.load()
    for key in station.keys():
        bpinv[int(key*100)] = bpinv[int(key*100)] + station[key]
        #print(bpinv[int(key*100)])
    os.chdir(path_bpinvtr)
    tr = Trace(bpinv, st[0].stats)
    tr.write(sta[:6], format = 'SAC')

vect = np.linspace(0, st[0].stats.npts/st[0].stats.sampling_rate, st[0].stats.npts)
sigma = 1./samp_rate

for sta in lst_fch:
    os.chdir(path_bpinvtr)
    st = read(sta[:6])
    dst, azm = dist_azim([st[0].stats.sac.stla, st[0].stats.sac.stlo], [lat_hyp, lon_hyp])
    trg = [math.exp(-(pow(a - 25, 2))/(2*pow(sigma, 2))) for a in vect]
    tr = np.convolve(st[0].data, trg, mode = 'same')
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(path_bpinvsm)
    tr.write(sta[:6], format = 'SAC')



















