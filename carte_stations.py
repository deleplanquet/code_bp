import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from obspy import read
import sys
import os
import pickle
import numpy as np

dossier = sys.argv[1]
dt_type = sys.argv[2]
select_station = sys.argv[3]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_results = path + '/' + dossier + '_results'

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []

for freq in lst_frq:
    pth_dt = path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz'
    lst_pth_dt.append(pth_dt + '_' + dt_type + '_env_smooth_' + select_station + '_impulse')

lst_pth_fch = []

for freq in lst_frq:
    lst_pth_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))
    
os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

min_lat = None
min_lon = None
max_lat = None
max_lon = None

for freq in lst_frq:
    os.chdir(lst_pth_dt[lst_frq.index(freq)])
    for fich in lst_pth_fch[lst_frq.index(freq)]:
        st = read(fich)
        if min_lat == None or st[0].stats.sac.stla < min_lat:
            min_lat = st[0].stats.sac.stla
        if min_lon == None or st[0].stats.sac.stla < min_lon:
            min_lon = st[0].stats.sac.stlo
        if max_lat == None or st[0].stats.sac.stla > max_lat:
            max_lat = st[0].stats.sac.stla
        if max_lon == None or st[0].stats.sac.stla > max_lon:
            max_lon = st[0].stats.sac.stlo

lat_fault = [32.6477, 32.9858]
long_fault = [130.7071, 131.1216]

fig, ax = plt.subplots(1, 1)
#Basemap
print(min_lon - 1, min_lat - 0.15, max_lon + 1, max_lat + 0.15)
m = Basemap(projection='merc', llcrnrlon=min_lon - 1, llcrnrlat=min_lat - 0.15, urcrnrlon=max_lon + 1, urcrnrlat=max_lat + 0.15, resolution='i')
#Coord fault
x_fault, y_fault = m(long_fault, lat_fault)
#Coastlines
m.drawcoastlines(linewidth=0.2)
#Fill color
m.fillcontinents('yellow')
#Parallels
m.drawparallels(np.arange(int(min_lat - 0.15), int(max_lat + 0.15) + 1, 0.5),
    labels=[1, 0, 0, 0],
    linewidth=0.1)
#Meridians
m.drawmeridians(np.arange(int(min_lon - 1), int(max_lon + 1) + 1, 0.5),
    labels=[0, 0, 0, 1],
    linewidth=0.1)
#Plot fault
ax.plot(x_fault,
        y_fault,
        color='green',
        linewidth = 0.3,
        zorder=1)
#Epicenter
x_epi, y_epi = m(dict_seis[dossier]['lon'], dict_seis[dossier]['lat'])
ax.scatter(x_epi, y_epi, 5, marker = '*', color = 'green', zorder = 4)

for freq in lst_frq:
    os.chdir(lst_pth_dt[lst_frq.index(freq)])
    for fichier in lst_pth_fch[lst_frq.index(freq)]:
        st = read(fichier)
        x_sta, y_sta = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)
        ax.scatter(x_sta, y_sta, 2, marker='^', color = 'blue', zorder=2)
        ax.text(x_sta, y_sta, st[0].stats.station, fontsize=2, ha='center', va='bottom', zorder=3)

    os.chdir(path_results)
    fig.savefig('map_' + dossier + '_vel_' + freq + '_Hz_' + dt_type + '_env_smooth_' + select_station + '_impulse.pdf')
