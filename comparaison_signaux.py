from mpl_toolkits.basemap import Basemap
from obspy.signal.util import smooth
from scipy.signal import hilbert
import matplotlib.pyplot as plt
from obspy import read
import numpy as np
import os

#path = '/localstorage/deleplanque/'
path = '/Users/deleplanque/Documents/'
path_data = path + 'Data/Kumamoto_sac'

path_results = path + '/Results/Kumamoto'

list_dossier = os.listdir(path_data)
list_dossier = [a for a in list_dossier if (a == '.DS_Store') == False]
print(list_dossier)

list_fichier = []

for dossier in list_dossier:
    print('     ', dossier, str(list_dossier.index(dossier) + 1), '/', len(list_dossier))
    path_fichier = path_data + '/' + str(dossier)
    os.chdir(path_fichier)
    list_fichier_dossier = os.listdir(path_fichier)
    list_fichier_temp = []
    for fichier in list_fichier_dossier:
    	st = read(fichier)
    	if st[0].stats.sac.mag >= 3.8 or st[0].stats.sac.mag <= 3.5:
    	    print(st[0].stats.sac.mag)
    	    break
    	else:
    	    if st[0].stats.channel == 'UD2':
    	    	list_fichier_temp.append(fichier)
    	    elif st[0].stats.channel == 'UD':
    	    	list_fichier_temp.append(fichier)
    list_fichier.append(list_fichier_temp)

print(list_fichier)

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
ccpptt = 0
for seisme in list_fichier:
    if seisme != []:
    	if ccpptt == 5:
    	    break
    	ccpptt = ccpptt + 1
    	path_seisme = path_data + '/' + str(list_dossier[list_fichier.index(seisme)])
    	os.chdir(path_seisme)
    	st = read(seisme[0])
    	x_epi, y_epi = m(st[0].stats.sac.evlo, st[0].stats.sac.evla)
    	ax.scatter(x_epi,
    	    	   y_epi,
    	    	   1,
    	    	   marker = '*',
    	    	   color = 'black',
    	    	   zorder = 2)
    	ax.text(x_epi,
    	    	y_epi,
    	    	list_dossier[list_fichier.index(seisme)],
    	    	fontsize=1,
    	    	ha='left',
    	    	va='center',
    	    	zorder=3)
    	for station in seisme:
    	    st = read(station)
    	    x_sta, y_sta, = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    	    ax.scatter(x_sta,
            	       y_sta,
    	    	       1,
    	    	       marker='^',
    	    	       color='red',
    	    	       zorder=4)
    	    ax.text(x_sta,
    	    	    y_sta,
    	    	    st[0].stats.station,
    	    	    fontsize=1,
    	    	    ha='center',
    	    	    va='bottom',
    	    	    zorder=5)

os.chdir(path_results + '/Station_par_station_3-6')
fig.savefig('map.pdf')

list_station = []
list_seisme = []

for seisme in list_fichier:
    if seisme != []:
    	print('     ', str(list_dossier[list_fichier.index(seisme)]))
    	for station in seisme:
    	    path = path_data + '/' + str(list_dossier[list_fichier.index(seisme)])
    	    os.chdir(path)
    	    st = read(station)
    	    if (st[0].stats.station in list_station) == False:
    	    	list_station.append(st[0].stats.station)
    	    	list_seisme.append([list_dossier[list_fichier.index(seisme)]])
    	    else:
    	    	list_seisme[list_station.index(st[0].stats.station)].append(list_dossier[list_fichier.index(seisme)])

for station in list_station:
    print('     ', station)
    path_stabsta = path_results + '/Station_par_station_3-6/' + str(station)
    if os.path.isdir(path_stabsta) == False:
    	os.makedirs(path_stabsta)
    fig2, ax2 = plt.subplots(1, 1)
    ax2.set_xlabel('time (s)')
    cppt = 0
    for seisme in list_seisme[list_station.index(station)]:
    	path_seisme = path_data + '/' + str(seisme)
    	os.chdir(path_seisme)
    	st = read(station + '*UD*.sac')
    	if st[0].stats.channel == 'UD1':
    	    st = read(station + '*UD2.sac')
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
    fig2.savefig('envelop_' + str(station) + '.pdf')




















