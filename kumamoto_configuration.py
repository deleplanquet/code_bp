import numpy as np
import math
import cmath
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

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
		  'Last Correction Time'
		 )]

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
                          info[15].split(' ')[5]
			 ))
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
                          info[15].split(' ')[5]
                         ))
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
	    resolution='h'
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

#recuperation position faille

#calcul matrice temps de trajet

#ARF figures

#stacks

#plots
