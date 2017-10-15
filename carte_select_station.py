import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from obspy import read
import sys
import os
import pickle
import numpy as np

dossier = sys.argv[1]
dt_type = 'hori'
select_station = 'S'

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_fch_origin = [a for a in os.listdir(path + '/' + dossier + '_sac') if ('UD' in a) == True and ('UD1' in a) == False]
lst_fch_inf100 = [a for a in os.listdir(path + '/' + dossier + '_sac_inf100km') if ('UD' in a) == True and ('UD1' in a) == False]

freq = '4_8Hz'
lst_fch_frq = os.listdir(path + '/' + dossier + '_vel_' + freq + '/' + dossier + '_vel_' + freq + '_hori_env_smooth_S')

#lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
#lst_pth_dt = []
#lst_fch = []

#for freq in lst_frq:
#    lst_pth_dt.append()
#    lst_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

min_lat = None
min_lon = None
max_lat = None
max_lon = None

os.chdir(path + '/' + dossier + '_sac')
for fichier in lst_fch_origin:
    st = read(fichier)
    if min_lat == None or st[0].stats.sac.stla < min_lat:
        min_lat = st[0].stats.sac.stla
    if min_lon == None or st[0].stats.sac.stlo < min_lon:
        min_lon = st[0].stats.sac.stlo
    if max_lat == None or st[0].stats.sac.stla > max_lat:
        max_lat = st[0].stats.sac.stla
    if max_lon == None or st[0].stats.sac.stlo > max_lon:
        max_lon = st[0].stats.sac.stlo

fig, ax = plt.subplots(1, 1)
m = Basemap(projection = 'merc', llcrnrlon = min_lon - 0.5, llcrnrlat = min_lat - 0.15, urcrnrlon = max_lon + 0.5, urcrnrlat = max_lat + 0.15, resolution = 'i')

m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(int(min_lat - 0.15), int(max_lat + 0.15) + 1, 1), labels = [1, 0, 0, 0], linewidth = 0.1)
m.drawmeridians(np.arange(int(min_lon - 0.5), int(max_lon + 0.5) + 1, 2), labels = [0, 0, 0, 1], linewidth = 0.1)

x_epi, y_epi = m(dict_seis[dossier]['lon'], dict_seis[dossier]['lat'])
ax.scatter(x_epi, y_epi, 50, marker = '*', color = 'black', zorder = 4, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_sac')
for station in lst_fch_origin:
    st = read(station)
    x_sta, y_sta = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    ax.scatter(x_sta, y_sta, 2, marker = '^', facecolors = 'none', edgecolors = 'blue', zorder = 5, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_sac_inf100km')
for station in lst_fch_inf100:
    st = read(station)
    x_sta, y_sta = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    ax.scatter(x_sta, y_sta, 2, marker = '^', color = 'blue', zorder = 5, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_results')
fig.savefig('map_' + dossier + '_inf_100km.pdf')

min_lat = None
max_lat = None
min_lon = None
max_lon = None

os.chdir(path + '/' + dossier + '_sac_inf100km')
for fichier in lst_fch_inf100:
    st = read(fichier)
    if min_lat == None or st[0].stats.sac.stla < min_lat:
        min_lat = st[0].stats.sac.stla
    if min_lon == None or st[0].stats.sac.stlo < min_lon:
        min_lon = st[0].stats.sac.stlo
    if max_lat == None or st[0].stats.sac.stla > max_lat:
        max_lat = st[0].stats.sac.stla
    if max_lon == None or st[0].stats.sac.stlo > max_lon:
        max_lon = st[0].stats.sac.stlo

fig2, ax2 = plt.subplots(1, 1)
m2 = Basemap(projection = 'merc', llcrnrlon = min_lon - 0.5, llcrnrlat = min_lat - 0.15, urcrnrlon = max_lon + 0.5, urcrnrlat = max_lat + 0.15, resolution = 'i')

m2.drawcoastlines(linewidth = 0.2)
m2.fillcontinents('yellow')
m2.drawparallels(np.arange(int(min_lat - 0.15), int(max_lat + 0.15) + 1, 1), labels = [1, 0, 0, 0], linewidth = 0.1)
m2.drawmeridians(np.arange(int(min_lon - 0.5), int(max_lon + 0.5) + 1, 1), labels = [0, 0, 0, 1], linewidth = 0.1)

x_epi, y_epi = m2(dict_seis[dossier]['lon'], dict_seis[dossier]['lat'])
ax2.scatter(x_epi, y_epi, 50, marker = '*', color = 'black', zorder = 4, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_sac_inf100km')
for station in lst_fch_inf100:
    st = read(station)
    x_sta, y_sta = m2(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    ax2.scatter(x_sta, y_sta, 7, marker = '^', color = 'blue', zorder = 4, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_vel_' + freq + '/' + dossier + '_vel_' + freq + '_hori_env_smooth_S')
for station in lst_fch_frq:
    st = read(station)
    x_sta, y_sta = m2(st[0].stats.sac.stlo, st[0].stats.sac.stla)
    ax2.scatter(x_sta, y_sta, 7, marker = '^', color = 'red', zorder = 5, linewidth = 0.2)

os.chdir(path + '/' + dossier + '_results')
fig2.savefig('map' + dossier + '_' + freq + '.pdf')
