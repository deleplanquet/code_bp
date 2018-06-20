import os
from obspy.imaging.beachball import beach
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np

print('')
print('      python3 seismicity.py')

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

period_lst = ['7th - 24th',
              '7th - 14th',
              '14th - 15th',
              '15th - 16th',
              '16th - 24th']

ms_lst = ['20160414212600',
          '20160415000300',
          '20160416012500']

figa, axa = plt.subplots(1, 1)
m.drawcoastlines(linewidth = 0.1)
m.drawmapboundary(fill_color = '0.7')
m.fillcontinents(color = '0.9',
                 lake_color = '0.7')
m.drawmapscale(w_bord + 0.55,
               s_bord + 0.15,
               lon_eq,
               lat_eq,
               100,
               zorder = 6)
m.drawparallels(np.arange(0., 90, 1),
                labels=[1, 0, 1, 0],
                linewidth = 0.01)
m.drawmeridians(np.arange(0., 180, 1),
                labels=[0, 1, 0, 1],
                linewidth = 0.01)


for period in range(5):
    fig, ax = plt.subplots(1, 1)
    m.drawcoastlines(linewidth = 0.1)
    m.drawmapboundary(fill_color = '0.7')
    m.fillcontinents(color = '0.95',
                     lake_color = '0.7')
    m.drawmapscale(w_bord + 0.55,
                   s_bord + 0.15,
                   lon_eq,
                   lat_eq,
                   100,
                   barstyle = 'fancy',
                   zorder = 6)

    for eq in sorted(seism.keys(), reverse = True):
        lat = seism[eq]['lat']
        lon = seism[eq]['lon']
        day = seism[eq]['day']
        hou = seism[eq]['hou']
        mnn = seism[eq]['min']
        per = None
        if lat < n_bord and lat > s_bord and lon < e_bord and lon > w_bord and seism[eq]['Mj'] > 3:
            x_epi, y_epi = m(lon, lat)
            if day < 14 or (day == 14 and hou < 21) or (day == 14 and hou == 21 and mnn < 28):
                per = 1
                clra = 'red'
            elif day < 15 or (day == 15 and hou < 0) or (day == 15 and hou == 0 and mnn < 3):
                per = 2
                clra = 'dodgerblue'
            elif day < 16 or (day == 16 and hou < 1) or (day == 16 and hou == 1 and mnn < 25):
                per = 3
                clra = 'dodgerblue'
            elif day < 21 or (day == 21 and hou < 1) or (day == 21 and hou == 1 and mnn < 25):
                per = 4
                clra = 'black'
            else:
                per = 4
                clra = 'yellow'

            if period == 0 or (period == 1 and per == 1) or (period == 2 and per == 2) or (period == 3 and per == 3) or (period == 4 or per == 4):
                ax.scatter(x_epi,
                           y_epi,
                           3*seism[eq]['Mj']**2,
                           marker = 'o',
                           edgecolors = 'black',
                           facecolors = 'none',
                           zorder = 2,
                           linewidth = 0.1)

            if period == 0 and per >= 2 and clra != 'yellow':
                axa.scatter(x_epi,
                            y_epi,
                            1*seism[eq]['Mj']**2,
                            marker = 'o',
                            edgecolors = clra,
                            facecolors = 'none',
                            zorder = 2,
                            linewidth = 0.1)

    if period == 0:
        #Mont Aso
        #xx, yy = m(131.09, 32.88)
        xx, yy = m(131.09, 32.88)
        axa.text(xx,
                yy,
                'Mt. Aso',
                color = 'black',
                zorder = 4,
                ha = 'center',
                va = 'center',
                fontsize = 8)
        xx1, yy1 = m(131.03, 32.84)
        xx2, yy2 = m(131.15, 32.84)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx1, yy1 = m(131.13, 32.92)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx2, yy2 = m(131.11, 32.90)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx1, yy1 = m(131.09, 32.96)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx2, yy2 = m(131.07, 32.90)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx1, yy1 = m(131.05, 32.92)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        xx2, yy2 = m(131.03, 32.84)
        axa.plot((xx1, xx2),
                (yy1, yy2),
                color = 'red',
                zorder = 3,
                linewidth = 0.8)
        #ax.scatter(xx, yy, 120, marker = 'o', edgecolors = 'black', facecolors = 'orange', zorder = 3, linewidth = 0.1)

        for mnsh in ms_lst:
            xx, yy = m(ref_s[mnsh]['lon'], ref_s[mnsh]['lat'])
            
            if mnsh == ms_lst[2]:
                clr = 'white'
            else:
                clr = '0.7'

            axa.scatter(xx,
                       yy,
                       7*ref_s[mnsh]['Mw']**2,
                       marker = '*',
                       edgecolors = 'black',
                       facecolors = clr,
                       zorder = 4,
                       linewidth = 0.3)

        #Kumamoto city
        xx, yy = m(131, 32.6)
        axa.text(xx,
                   yy,
                   'Kumamoto',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        xx, yy = m(130.2, 32.8)
        axa.text(xx,
                   yy,
                   'Nagasaki',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        xx, yy = m(130.1, 33.3)
        axa.text(xx,
                   yy,
                   'Saga',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        xx, yy = m(130.7, 33.5)
        axa.text(xx,
                   yy,
                   'Fukuoka',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        xx, yy = m(131.6, 33)
        axa.text(xx,
                   yy,
                   'Oita',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        xx, yy = m(131.3, 32.2)
        axa.text(xx,
                   yy,
                   'Miyazaki',
                   color = 'black',
                   zorder = 4,
                   ha = 'center',
                   va = 'center',
                   fontsize = 8)

        #xx, yy = m(130.85, 32.8)
        #ax.text(xx, yy, 'Kumamoto', color = 'red', zorder = 3, ha = 'left', va = 'center', fontsize = 20)

        figa.savefig('seismicite_article.pdf')

    for mainsh in ms_lst:
        xx, yy = m(ref_s[mainsh]['lon'], ref_s[mainsh]['lat'])
        angles = [ref_s[mainsh]['str1'], ref_s[mainsh]['dip1'], ref_s[mainsh]['rak1']]
        bx, by = m(w_bord + 0.12, n_bord - 0.6 + 0.2*ms_lst.index(mainsh))

        if mainsh == ms_lst[2]:
            clr = 'red'
        elif mainsh == ms_lst[1]:
            clr = 'green'
        else:
            clr = 'blue'

        ax.scatter(xx,
                   yy,
                   20*ref_s[mainsh]['Mw']**2,
                   marker = '*',
                   edgecolors = 'white',
                   facecolor = clr,
                   zorder = 4,
                   linewidth = 0.1)
        bb = beach(angles,
                   xy = (bx, by),
                   facecolor = clr,
                   width = 20000,
                   linewidth = 0.1)
        bb.set_zorder(4)
        ax.add_collection(bb)

        xx, yy = m(w_bord + 0.4, n_bord - 0.62 + 0.2*ms_lst.index(mainsh))
        ax.text(xx, yy, ref_s[mainsh]['Mw'], ha = 'center', va = 'center', fontsize = 20)

        xx, yy = m(w_bord + 1.0, n_bord - 0.62 + 0.2*ms_lst.index(mainsh))
        ax.text(xx, yy, mainsh[6:8] + 'th', ha = 'center', va = 'center', fontsize = 20)

    #legende main shocks
    xx, yy = m(w_bord + 0.4, n_bord - 0.07)
    ax.text(xx, yy, 'Mw', ha = 'center', va = 'center', fontsize = 20)

    xx, yy = m(w_bord + 1.0, n_bord - 0.07)
    ax.text(xx, yy, '2016 April', ha = 'center', va = 'center', fontsize = 20)

    #Kumamoto city
    xx, yy = m(130.78, 32.78)
    ax.scatter(xx, yy, 120, marker = 'o', edgecolors = 'black', facecolors = 'orange', zorder = 3, linewidth = 0.1)

    xx, yy = m(130.85, 32.8)
    ax.text(xx, yy, 'Kumamoto', color = 'red', zorder = 3, ha = 'left', va = 'center', fontsize = 20)

    #Mont Aso
    xx, yy = m(131.09, 32.88)
    ax.scatter(xx, yy, 120, marker = 'o', edgecolors = 'black', facecolors = 'orange', zorder = 3, linewidth = 0.1)

    xx, yy = m(131.14, 32.9)
    ax.text(xx, yy, 'Mt. Aso', color = 'red', zorder = 3, ha = 'left', va = 'center', fontsize = 20)

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
    ax.set_title('2016 April ' + period_lst[period] + ' seismicity', fontsize = 24)

    #save figure
    fig.savefig('sismicite_' + period_lst[period] + '.pdf')


