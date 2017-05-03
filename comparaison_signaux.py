from mpl_toolkits.basemap import Basemap
from obspy.signal.util import smooth
from scipy.signal import hilbert
import matplotlib.pyplot as plt
from obspy import read
import numpy as np
import os

path = '/media/deleplanque/Lexar'
path_data = path + '/Data/Kumamoto'

path_results = path + '/Results/Kumamoto'

list_dossier = os.listdir(path_data)
list_dossier = [a for a in list_dossier if ('.tar' in a) == False]

list_fichier = []

for dossier in list_dossier:
    cpt = cpt + 1
    print('     ', dossier, str(list_dossier.index(dossier) + 1), '/', len(list_dossier))
    path_fichier = path_data + '/' + str(dossier) + '/' + str(dossier) + '.kik'
    os.chdir(path_fichier)
    list_fichier_temp = os.listdir(path_fichier)
    list_fichier_temp = [a for a in list_fichier_temp if ('ps.gz' in a) == False]
    list_fichier_temp2 = []
    for fichier in list_fichier_temp:
    	st = read(fichier)
    	if st[0].stats.knet.mag >= 5:
    	    break
    	if st[0].stats.channel == 'NS1':
    	    list_fichier_temp2.append([fichier, 'kik'])
    path_fichier = path_data + '/' + str(dossier) + '/' + str(dossier) + '.knt'
    os.chdir(path_fichier)
    list_fichier_temp = os.listdir(path_fichier)
    list_fichier_temp = [a for a in list_fichier_temp if ('ps.gz' in a) == False]
    for fichier in list_fichier_temp:
    	st = read(fichier)
    	if st[0].stats.knet.mag >= 5:
    	    break
    	if st[0].stats.channel == 'NS':
    	    list_fichier_temp2.append([fichier, 'knt'])
    list_fichier.append(list_fichier_temp2)

lat_fault = [32.65, 32.86]
long_fault = [130.72, 131.07]

fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
    	    llcrnrlon=128,
    	    llcrnrlat=30,
    	    urcrnrlon=134,
    	    urcrnrlat=35,
    	    resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(30, 35, 1),
    	    	labels=[1, 0, 0, 0],
    	    	linewidth=1)
m.drawmeridians(np.arange(128, 134, 1),
    	    	labels=[0, 0, 0, 1],
    	    	linewidth=1)
ax.plot(x_fault,
    	y_fault,
    	color='green',
    	linewidth = 0.3,
    	zorder = 1)

for fichier in list_fichier:
    if fichier != []:
    	os.chdir(path_data + '/' + str(list_dossier[list_fichier.index(fichier)]) + '/' + str(list_dossier[list_fichier.index(fichier)]) + '.' + fichier[0][1])
    	st = read(fichier[0][0])
    	x_epi, y_epi = m(st[0].stats.knet.evlo, st[0].stats.knet.evla)
    	ax.scatter(x_epi,
    	    	   y_epi,
    	    	   3,
    	    	   marker = '*',
    	    	   color = 'black',
    	    	   zorder = 2)
    	ax.text(x_epi,
    	    	y_epi,
    	    	list_dossier[list_fichier.index(fichier)],
    	    	fontsize=2,
    	    	ha='center',
    	    	va='bottom',
    	    	zorder=3)

os.chdir(path_results + '/Station_par_station')
fig.savefig('map.pdf')

list_station = []
list_seisme = []

for fichier in list_fichier:
    if fichier != []:
    	for station in fichier:
    	    print('     ', station[0])
    	    os.chdir(path_data + '/' + str(list_dossier[list_fichier.index(fichier)]) + '/' + str(list_dossier[list_fichier.index(fichier)]) + '.' + station[1])
    	    st = read(station[0])
    	    if ([st[0].stats.station, station[1]] in list_station) == False:
    	    	list_station.append([st[0].stats.station, station[1]])
    	    	list_seisme.append([list_dossier[list_fichier.index(fichier)]])
    	    else:
    	    	list_seisme[list_station.index([st[0].stats.station, station[1]])].append(list_dossier[list_fichier.index(fichier)])

for station in list_station:
    path_stabsta = path_results + '/Station_par_station/' + str(station[0])
    if os.path.isdir(path_stabsta) == False:
    	os.makedirs(path_stabsta)
    fig2, ax2 = plt.subplots(1, 1)
    ax2.set_xlabel('time (s)')
    cppt = 0
    for seisme in list_seisme[list_station.index(station)]:
    	print(station[0], seisme)
    	path_seisme = path_data + '/' + str(seisme) + '/' + str(seisme) + '.' + station[1]
    	os.chdir(path_seisme)
    	if station[1] == 'kik':
    	    st = read(station[0] + '*NS1')
    	else:
    	    st = read(station[0] + '*NS')
    	st = st.detrend(type='constant')
    	tr_brut = st[0]
    	tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
    	envelop = abs(hilbert(tr_filt))
    	env_smoothed = smooth(envelop, 20)

    	t = np.arange(tr_brut.stats.npts)/tr_brut.stats.sampling_rate

#    	ax2.plot(t, tr_brut, linewidth=0.2, color='black')
    	ax2.plot(t, env_smoothed + cppt, linewidth=1)
    	cppt = cppt + 500
    os.chdir(path_stabsta)
    fig2.savefig('envelop' + str(station[0]) + '.pdf')




















