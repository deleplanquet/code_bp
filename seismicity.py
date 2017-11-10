import os
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('seismicity_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    seism = my_dpck.load()

with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    ref_s = my_dpck.load()

path = path_origin + '/Kumamoto'

min_lat = None
min_lon = None
max_lat = None
max_lon = None

for cles in ref_s.keys():
    if min_lat is None or ref_s[cles]['lat'] < min_lat:
        min_lat = ref_s[cles]['lat']
    if min_lon is None or ref_s[cles]['lon'] < min_lon:
        min_lon = ref_s[cles]['lon']
    if max_lat is None or ref_s[cles]['lat'] > max_lat:
        max_lat = ref_s[cles]['lat']
    if max_lon is None or ref_s[cles]['lon'] > max_lon:
        max_lon = ref_s[cles]['lon']

min_lat = min_lat - 0.4
min_lon = min_lon - 0.8
max_lat = max_lat + 0.4
max_lon = max_lon + 0.8

m = Basemap(projection = 'merc',
            llcrnrlon = min_lon,
            llcrnrlat = min_lat,
            urcrnrlon = max_lon,
            urcrnrlat = max_lat,
            resolution = 'i')

fig, ax = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels = [1, 0, 0, 0],
                linewidth = 0.2)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels = [0, 0, 0, 1],
                linewidth = 0.2)

fig1, ax1 = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels = [1, 0, 0, 0],
                linewidth = 0.2)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels = [0, 0, 0, 1],
                linewidth = 0.2)

fig2, ax2 = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels = [1, 0, 0, 0],
                linewidth = 0.2)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels = [0, 0, 0, 1],
                linewidth = 0.2)

fig3, ax3 = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels = [1, 0, 0, 0],
                linewidth = 0.2)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels = [0, 0, 0, 1],
                linewidth = 0.2)

fig4, ax4 = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels = [1, 0, 0, 0],
                linewidth = 0.2)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels = [0, 0, 0, 1],
                linewidth = 0.2)

for eq in seism.keys():
    lat = seism[eq]['lat']
    lon = seism[eq]['lon']
    day = seism[eq]['day']
    mnn = seism[eq]['min']
    sec = seism[eq]['sec']
    if lat < max_lat and lat > min_lat and lon < max_lon and lon > min_lon:
        x_epi, y_epi = m(lon, lat)
        ax.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'black', facecolors = 'none', zorder = 2, linewidth = 0.1)
        if day < 14 or (day == 14 and mnn < 21) or (day == 14 and mnn == 21 and sec < 28):
            ax1.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'black', facecolors = 'none', zorder = 2, linewidth = 0.1)
        elif day < 15 or (day == 15 and mnn < 0) or (day == 15 and mnn == 0 and sec < 3):
            ax2.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'red', facecolors = 'none', zorder = 2, linewidth = 0.1)
        elif day < 16 or (day == 16 and mnn < 1) or (day == 16 and mnn == 1 and sec < 25):
            ax3.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'blue', facecolors = 'none', zorder = 2, linewidth = 0.1)
        else:
            ax4.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'green', facecolors = 'none', zorder = 2, linewidth = 0.1)

fig.savefig('sismicite.pdf')
fig1.savefig('sismicite_before142128.pdf')
fig2.savefig('sismicite_before150003.pdf')
fig3.savefig('sismicite_before160125.pdf')
fig4.savefig('sismicite_after160125.pdf')



