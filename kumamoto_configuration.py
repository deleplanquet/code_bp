import numpy as np
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

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
    rlat1 = d2r(lat1)
    rlong1 = d2r(long1)
    rlat2 = d2r(lat2)
    rlong2 = d2r(long2)
    xx = math.cos(rlat1)*math.cos(rlong1) + math.cos(rlat2)*math.cos(rlong2)
    yy = math.cos(rlat1)*math.sin(rlong1) + math.cos(rlat2)*math.sin(rlong2)
    zz = math.sin(rlat1) + math.sin(rlat2)
    return [r2d(math.asin(zz/math.sqrt(xx*xx + yy*yy + zz*zz))),
	    r2d(math.acos(xx/math.sqrt(xx*xx + yy*yy)))]

#calcul de la matrice des tps de trajet pour une station
def fault(cen_fault, length, width, u_strike, u_dip, pasx, pasy):
    rad = cen_fault[0]
    rlat = d2r(cen_fault[1])
    rlong = d2r(cen_fault[2])
    x_cf = rad*math.cos(rlat)*math.cos(rlong)
    y_cf = rad*math.cos(rlat)*math.sin(rlong)
    z_cf = rad*math.sin(rlat)
    print(cen_fault)
    print(x_cf, y_cf, z_cf)
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
    r_sta = R_Earth + station[2]/1000
    rlat_sta = d2r(station[0])
    rlong_sta = d2r(station[1])
    x_sta = r_sta*math.cos(rlat_sta)*math.cos(rlong_sta)
    y_sta = r_sta*math.cos(rlat_sta)*math.sin(rlong_sta)
    z_sta = r_sta*math.sin(rlat_sta)
    mat_time = np.zeros((len(fault[:, 0, 0]), len(fault[0, :, 0])))
    for a in range(len(fault[:, 0, 0])):
    	for b in range(len(fault[0 , :, 0])):
    	    mat_time[a, b] = math.sqrt(pow(x_sta - fault[a, b, 0], 2)
					+ pow(y_sta - fault[a, b, 1], 2)
					+ pow(z_sta - fault[a, b, 2], 2))/v_s
    return mat_time

#recuperation position stations
path = '/home/deleplanque/Documents/back_proj/en_cours'
dossier_seisme = '20160414212600'
path1 = path + '/data_kumamoto/' + dossier_seisme + '/' + dossier_seisme + '.kik'
path2 = path + '/data_kumamoto/' + dossier_seisme + '/' + dossier_seisme + '.knt'
path_results = path + '/results/' + dossier_seisme
os.makedirs(path_results)

list_fichier1 = os.listdir(path1)
list_fichier2 = os.listdir(path2)
list_fichier1 = [a for a in list_fichier1 if ('ps.gz' in a) == False]
list_fichier2 = [a for a in list_fichier2 if ('ps.gz' in a) == False]

info_stations = [('Origin Date',
		  'Origin Time',
		  'Lat.',
		  'Long.',
		  'Depth (km)',
		  'Mag.',
		  'Network',
		  'Station Code',
		  'Station Lat.',
		  'Station Long.',
		  'Station Height (m)',
		  'Record Date',
		  'Record Time',
		  'Sampling Freq (Hz)',
		  'Duration Time (s)',
		  'Dir.',
		  'Scale Factor',
		  'Max. Acc. (gal)',
		  'Last Correction Date',
		  'Last Correction Time')]

for fichier in list_fichier1:
    data = open(path1 + '/' + fichier, 'r')
    contenu = data.read()
    info = contenu.split('Memo')[0]
    info = info.split('\n')
    info_stations.append((info[0].split(' ')[8],
                          info[0].split(' ')[9],
                          float(info[1].split(' ')[14]),
                          float(info[2].split(' ')[13]),
		          float(info[3].split(' ')[8]),
		          float(info[4].split(' ')[14]),
		          'KiK-net',
		          info[5].split(' ')[7],
		          float(info[6].split(' ')[7]),
		          float(info[7].split(' ')[6]),
		          float(info[8].split(' ')[2]),
                          info[9].split(' ')[8],
                          info[9].split(' ')[9],
                          info[10].split(' ')[2],
                          float(info[11].split(' ')[3]),
                          info[12].split(' ')[14],
                          info[13].split(' ')[6],
                          float(info[14].split(' ')[5]),
                          info[15].split(' ')[4],
                          info[15].split(' ')[5]))
    data.close()

for fichier in list_fichier2:
    date = open(path2 + '/' + fichier, 'r')
    contenu = date.read()
    info = contenu.split('Memo')[0]
    info = info.split('\n')
    info_stations.append((info[0].split(' ')[8],
                          info[0].split(' ')[9],
                          float(info[1].split(' ')[14]),
                          float(info[2].split(' ')[13]),
                          float(info[3].split(' ')[8]),
                          float(info[4].split(' ')[14]),
                          'K-NET',
                          info[5].split(' ')[7],
                          float(info[6].split(' ')[7]),
                          float(info[7].split(' ')[6]),
                          float(info[8].split(' ')[2]),
                          info[9].split(' ')[8],
                          info[9].split(' ')[9],
                          info[10].split(' ')[2],
                          float(info[11].split(' ')[3]),
                          info[12].split(' ')[14],
                          info[13].split(' ')[6],
                          float(info[14].split(' ')[5]),
                          info[15].split(' ')[4],
                          info[15].split(' ')[5]))
    data.close()

#recuperation position faille

strike = 234
dip = 64
l_fault = 40
w_fault = 15
lat_fault = [32.65, 32.86]
long_fault = [130.72, 131.07]

#print position des stations

lat_sta = [a[8] for a in info_stations]
long_sta = [a[9] for a in info_stations]
color_sta = ['b' if a[6] == 'KiK-net' else 'r' for a in info_stations]
code_sta = [a[7] for a in info_stations]
del lat_sta[0]
del long_sta[0]
del color_sta[0]
del code_sta[0]

os.chdir(path_results)

fig_pos_sta, ax_pos_sta = plt.subplots(1, 1)
#ax_pos_sta.set_xlabel('Long.')
#ax_pos_sta.set_ylabel('Lat.')
m = Basemap(projection='merc',
	    llcrnrlon=128,
	    llcrnrlat=30,
	    urcrnrlon=140,
	    urcrnrlat=37,
	    resolution='i'
	   )
x, y = m(long_sta, lat_sta)
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(30, 38, 2), labels=[1, 0, 0, 0], linewidth=0)
m.drawmeridians(np.arange(128, 141, 2), labels=[0, 0, 0, 1], linewidth=0)
ax_pos_sta.plot(x_fault,
		y_fault,
		color='green',
		linewidth = 0.3,
		zorder=1
	       )
ax_pos_sta.scatter(x,
		   y,
		   2,
		   marker='^',
		   color=color_sta,
		   zorder=2
		  )
for i in range(len(code_sta)):
    ax_pos_sta.text(x[i],
		    y[i],
		    code_sta[i],
		    fontsize=2,
		    ha='center',
		    va='bottom',
		    zorder=3
		   )
fig_pos_sta.savefig('map_stations.pdf')

#placement de la faille

lat_cen_fault, long_cen_fault = milieu(lat_fault[0], long_fault[0], lat_fault[1], long_fault[1])
dir_cen_fault = [math.cos(lat_cen_fault)*math.cos(long_cen_fault), math.cos(lat_cen_fault)*math.sin(long_cen_fault), math.sin(lat_cen_fault)]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(long_cen_fault), -math.cos(long_cen_fault), 0])
vect_strike = rotation(vect_nord, strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, strike-90, dir_cen_fault)
vect_dir_fault = rotation(vect_perp_strike, 180-dip, vect_strike)

coord_fault = fault([6400, lat_cen_fault, long_cen_fault], l_fault, w_fault, norm(vect_strike), norm(rotation(vect_dir_fault, 90, vect_strike)), 1., 1.)

#calcul matrice tps de trajet

print(info_stations[1][7])
print(trav_time([info_stations[1][8], info_stations[1][9], info_stations[1][10]], coord_fault))

#ARF figures

#stacks

#plots
