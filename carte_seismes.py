import os
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach
import numpy as np
from collections import OrderedDict

path = os.getcwd()[:-6]
path_data = path + '/Data'
path_results = path + '/Results'

os.chdir(path_data)
with open('ref_seismes_bin', 'rb') as my_fich:
    mon_depick = pickle.Unpickler(my_fich)
    my_dict = mon_depick.load()

min_lat = None
min_lon = None
max_lat = None
max_lon = None
N_pt_seis = 0

for cles in my_dict.keys():
    if min_lat is None or my_dict[cles]['lat'] < min_lat:
        min_lat = my_dict[cles]['lat']
    if min_lon is None or my_dict[cles]['lon'] < min_lon:
        min_lon = my_dict[cles]['lon']
    if max_lat is None or my_dict[cles]['lat'] > max_lat:
        max_lat = my_dict[cles]['lat']
    if max_lon is None or my_dict[cles]['lon'] > max_lon:
        max_lon = my_dict[cles]['lon']
    if my_dict[cles]['Mw'] < 5:
        N_pt_seis = N_pt_seis + 1

min_lon = min_lon - 1
min_lat = min_lat - 0.5
max_lon = max_lon + 1
max_lat = max_lat + 0.5

fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
            llcrnrlon=min_lon,
            llcrnrlat=min_lat,
            urcrnrlon=max_lon,
            urcrnrlat=max_lat,
            resolution='i')

m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(min_lat, max_lat, 0.5),
                labels=[1, 0, 0, 0],
                linewidth=1)
m.drawmeridians(np.arange(min_lon, max_lon, 0.5),
                labels=[0, 0, 0, 1],
                linewidth=1)

i = 0
j = 0
lon_prm = 0
lon_tmp = 360

for cpt in range(len(my_dict)):
    for cles in my_dict.keys():
        if my_dict[cles]['lon'] > lon_prm and my_dict[cles]['lon'] < lon_tmp:
            lon_tmp = my_dict[cles]['lon']
            cpt_cle = cles
    lon_prm = lon_tmp
    lon_tmp = 360
    x_epi, y_epi = m(my_dict[cpt_cle]['lon'], my_dict[cpt_cle]['lat'])
    angles = [my_dict[cpt_cle]['str1'], my_dict[cpt_cle]['dip1'], my_dict[cpt_cle]['rak1']]
    bx, by = m(min_lon + (max_lon - min_lon)/50 + (max_lon - min_lon)*i/25, max_lat - 0.2)
    xtxtt, ytxtt = m(min_lon + (max_lon - min_lon)/50 + (max_lon - min_lon)*i/25, max_lat - 0.1)
    xtxtb, ytxtb = m(min_lon + (max_lon - min_lon)/50 + (max_lon - min_lon)*i/25, max_lat - 0.35)
    if my_dict[cpt_cle]['Mw'] < 5:
        lat_bb = min_lat + (max_lat - min_lat)/(2*N_pt_seis) + (max_lat - min_lat)*i/N_pt_seis
        bx, by = m(min_lon + 0.3, lat_bb)
        xtxte, ytxte = m(min_lon + 0.12, lat_bb)
        xtxti, ytxti = m(min_lon + 0.4, lat_bb)
        i = i + 1
        clr = 'blue'
        siz = 30
    else:
        lat_bb = min_lat + (max_lat - min_lat)/(2*(len(my_dict) - N_pt_seis)) + (max_lat - min_lat)*j/(len(my_dict) - N_pt_seis)
        bx, by = m(max_lon - 0.3, lat_bb)
        xtxte, ytxte = m(max_lon - 0.12, lat_bb)
        xtxti, ytxti = m(max_lon - 0.4, lat_bb)
        j = j + 1
        if my_dict[cpt_cle]['Mw'] < 7:
            clr = 'green'
            siz = 60
        else:
            clr = 'red'
            siz = 75
    ax.scatter(x_epi, y_epi, siz, marker = '*', color = clr, zorder = 2)
    ax.plot([x_epi, bx], [y_epi, by], color = 'black', linewidth = 0.2)
    bb = beach(angles, xy=(bx, by), facecolor = clr, width=10000, linewidth=0.2)
    bb.set_zorder(4)
    ax.add_collection(bb)
    ax.text(xtxti, ytxti, my_dict[cpt_cle]['Mw'], fontsize=7, ha = 'center', va = 'center', zorder = 5)
    ax.text(xtxte, ytxte, cpt_cle[6:8] + ' ' + cpt_cle[8:10] + ':' + cpt_cle[10:12], fontsize=7, ha = 'center', va = 'center', zorder = 5)

os.chdir(path_results)
fig.savefig('carte_seismes.pdf')
















