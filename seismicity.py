import os
from obspy.imaging.beachball import beach
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto'

os.chdir(path)
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('seismicity_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    seism = my_dpck.load()

with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    ref_s = my_dpck.load()

dossier = param['dossier']

lon_eq = ref_s[dossier]['lon']
lat_eq = ref_s[dossier]['lat']

w_bord = ref_s['20160416012500']['lon'] - 1.5
e_bord = ref_s['20160416012500']['lon'] + 1.5
n_bord = ref_s['20160416012500']['lat'] + 1.2
s_bord = ref_s['20160416012500']['lat'] - 1.2

m = Basemap(projection = 'merc',
            llcrnrlon = w_bord,
            llcrnrlat = s_bord,
            urcrnrlon = e_bord,
            urcrnrlat = n_bord,
            resolution='f')

period_lst = ['7th - 24th', '7th - 14th', '14th - 15th', '15th - 16th', '16th - 24th']
ms_lst = ['20160414212600', '20160415000300', '20160416012500']

for period in range(5):
    fig, ax = plt.subplots(1, 1)
    m.drawcoastlines(linewidth = 0.2)
    m.fillcontinents('yellow')
    m.drawmapscale(w_bord + 0.55, s_bord + 0.15, lon_eq, lat_eq, 100, barstyle = 'fancy', zorder = 6)

    for eq in seism.keys():
        lat = seism[eq]['lat']
        lon = seism[eq]['lon']
        day = seism[eq]['day']
        hou = seism[eq]['hou']
        mnn = seism[eq]['min']
        per = None
        if lat < n_bord and lat > s_bord and lon < e_bord and lon > w_bord:
            x_epi, y_epi = m(lon, lat)
            if day < 14 or (day == 14 and hou < 21) or (day == 14 and hou == 21 and mnn < 28):
                per = 1
            elif day < 15 or (day == 15 and hou < 0) or (day == 15 and hou == 0 and mnn < 3):
                per = 2
            elif day < 16 or (day == 16 and hou < 1) or (day == 16 and hou == 1 and mnn < 25):
                per = 3
            else:
                per = 4

            if period == 0 or (period == 1 and per == 1) or (period == 2 and per == 2) or (period == 3 and per == 3) or (period == 4 or per == 4):
                ax.scatter(x_epi, y_epi, seism[eq]['Mj']**2, marker = 'o', edgecolors = 'black', facecolors = 'none', zorder = 2, linewidth = 0.1)

    for mainsh in ms_lst:
        xx, yy = m(ref_s[mainsh]['lon'], ref_s[mainsh]['lat'])
        angles = [ref_s[mainsh]['str1'], ref_s[mainsh]['dip1'], ref_s[mainsh]['rak1']]
        bx, by = m(w_bord + 0.12, n_bord - 0.4 + 0.1*ms_lst.index(mainsh))

        if mainsh == ms_lst[2]:
            clr = 'red'
        elif mainsh == ms_lst[1]:
            clr = 'green'
        else:
            clr = 'blue'

        ax.scatter(xx, yy, 3*ref_s[mainsh]['Mw']**2, marker = '*', color = clr, zorder = 4, linewidth = 0.1)
        bb = beach(angles, xy = (bx, by), facecolor = clr, width = 10000, linewidth = 0.1)
        bb.set_zorder(4)
        ax.add_collection(bb)

        xx, yy = m(w_bord + 0.3, n_bord - 0.4 + 0.1*ms_lst.index(mainsh))
        ax.text(xx, yy, ref_s[mainsh]['Mw'], ha = 'center', va = 'center')

        xx, yy = m(w_bord + 0.7, n_bord - 0.4 + 0.1*ms_lst.index(mainsh))
        ax.text(xx, yy, mainsh[6:8] + 'th', ha = 'center', va = 'center')

    #legende main shocks
    xx, yy = m(w_bord + 0.3, n_bord - 0.1)
    ax.text(xx, yy, 'Mw', ha = 'center', va = 'center')

    xx, yy = m(w_bord + 0.7, n_bord - 0.1)
    ax.text(xx, yy, '2016 April', ha = 'center', va = 'center')

    #Kumamoto city
    xx, yy = m(130.78, 32.78)
    ax.scatter(xx, yy, 40, marker = 'o', edgecolors = 'black', facecolors = 'orange', zorder = 3, linewidth = 0.1)

    xx, yy = m(130.78, 32.8)
    ax.text(xx, yy, 'Kumamoto', color = 'red', zorder = 3, ha = 'center', va = 'center')

    #Mont Aso
    xx, yy = m(131.09, 32.88)
    ax.scatter(xx, yy, 40, marker = 'o', edgecolors = 'black', facecolors = 'orange', zorder = 3, linewidth = 0.1)

    xx, yy = m(131.09, 32.9)
    ax.text(xx, yy, 'Mt. Aso', color = 'red', zorder = 3, ha = 'center', va = 'center')

    #legende magnitude sismicite
    xx, yy = m(e_bord - 0.15, s_bord + 0.5)
    ax.text(xx, yy, 'Mw', ha = 'center', va = 'center')

    for i in range(4):
        #cercle pour magnitude donnee
        xx, yy = m(e_bord - 0.2, s_bord + 0.1 + 0.1*i)
        ax.scatter(xx, yy, pow(i + 2, 2), marker = 'o', edgecolors = 'black', facecolors = 'none', zorder = 2, linewidth = 0.1)

        #magnitude sismicite
        xx, yy = m(e_bord - 0.15, s_bord + 0.1 + 0.1*i)
        ax.text(xx, yy, '   ' + str(i + 2), ha = 'center', va = 'center')

    #title figure
    ax.set_title('2016 April ' + period_lst[period] + ' seismicity')

    #save figure
    fig.savefig('sismicite_' + period_lst[period] + '.pdf')


