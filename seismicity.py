import os
from obspy.imaging.beachball import beach
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
from obspy import read

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
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']

path_sta = (path + '/'
            + dossier + '/'
            + dossier
            + '_vel_'
            + couronne + 'km_'
            + frq + 'Hz/'
            + dossier
            + '_vel_'
            + couronne + 'km_'
            + frq + 'Hz_'
            + dt_type
            + '_env_smooth')

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
                labels=[1, 1, 0, 0],
                labelstyle = '+/-',
                linewidth = 0.01)
m.drawmeridians(np.arange(0., 180, 1),
                labels=[0, 0, 1, 1],
                labelstyle = '+/-',
                linewidth = 0.01)

x_bef = []
y_bef = []
s_bef = []
x_aft = []
y_aft = []
s_aft = []

for eq in sorted(seism.keys(), reverse = True):
    lat = seism[eq]['lat']
    lon = seism[eq]['lon']
    day = seism[eq]['day']
    hou = seism[eq]['hou']
    mnn = seism[eq]['min']
    per = None
    if lat < n_bord and lat > s_bord and lon < e_bord and lon > w_bord and seism[eq]['Mj'] > 3:
        x_epi, y_epi = m(lon, lat)

        if ((day == 14 and ((hou == 21 and mnn > 26) or hou > 21))
            or (day == 15)
            or (day == 16 and (hou < 1 or (hou == 1 and mnn < 25)))):
            x_bef.append(x_epi)
            y_bef.append(y_epi)
            s_bef.append(seism[eq]['Mj']**2)

        elif ((day == 16 and ((hou == 1 and mnn > 25) or hou > 1))
            or (day > 16 and day < 21)
            or (day == 21 and (hou < 1 or (hou == 1 and mnn < 25)))):
            x_aft.append(x_epi)
            y_aft.append(y_epi)
            s_aft.append(seism[eq]['Mj']**2)

axa.scatter(x_bef,
            y_bef,
            1*s_bef,
            marker = 'o',
            edgecolors = 'dodgerblue',
            facecolors = 'none',
            zorder = 2,
            linewidth = 0.1,
            label = 'JMA hypo. Mw 6.1 - Mw 7.1')

axa.scatter(x_aft,
            y_aft,
            1*s_aft,
            marker = 'o',
            edgecolors = 'black',
            facecolors = 'none',
            zorder = 2,
            linewidth = 0.1,
            label = 'JMA hypo. Mw 7.1 - 5days after')

os.chdir(path_sta)
lst_sta = os.listdir(path_sta)

x_kik = []
y_kik = []
x_kn = []
y_kn = []

for sta in lst_sta:
    st = read(sta)
    xx, yy = m(st[0].stats.sac.stlo, st[0].stats.sac.stla)

    if sta[3] == 'H': #KiK-net
        x_kik.append(xx)
        y_kik.append(yy)

    else: #K-NET
        x_kn.append(xx)
        y_kn.append(yy)

axa.scatter(x_kik,
            y_kik,
            15,
            marker = '^',
            color = 'orangered',
            zorder = 3,
            linewidth = 0.1,
            label = 'KiK-net')

axa.scatter(x_kn,
            y_kn,
            15,
            marker = '^',
            color = 'forestgreen',
            zorder = 3,
            linewidth = 0.1,
            label = 'K-NET')

#Mont Aso
xaso = 131.09
yaso = 32.88
xvol = [- 0.03,
        + 0.03,
        + 0.02,
        + 0.01,
        + 0.00,
        - 0.01,
        - 0.02,
        - 0.03]
yvol = [- 0.02,
        - 0.02,
        + 0.02,
        + 0.01,
        + 0.03,
        + 0.01,
        + 0.02,
        - 0.02]

for i in range(len(xvol) - 1):
    xx1, yy1 = m(xaso + 1.5*xvol[i], yaso + 1.5*yvol[i])
    xx2, yy2 = m(xaso + 1.5*xvol[i + 1], yaso + 1.5*yvol[i + 1])
    axa.plot((xx1, xx2),
             (yy1, yy2),
             color = 'red',
             zorder = 3,
             linewidth = 0.8)

xx, yy = m(xaso + 0.05, yaso)
axa.text(xx,
         yy,
         'Mt. Aso',
         color = 'black',
         zorder = 4,
         ha = 'left',
         va = 'center',
         style = 'italic',
         fontsize = 6)

#Kumamoto sequence
for mnsh in ms_lst:
    xx, yy = m(ref_s[mnsh]['lon'], ref_s[mnsh]['lat'])
            
    if mnsh == ms_lst[2]:
        clr = 'white'
    else:
        clr = '0.7'

    axa.scatter(xx,
                yy,
                5*ref_s[mnsh]['Mw']**2,
                marker = '*',
                edgecolors = 'black',
                facecolors = clr,
                zorder = 4,
                linewidth = 0.3)

#prefectures
xpref = [131,
         129.95,
         130.1,
         130.75,
         131.6,
         131.3]
ypref = [32.55,
         32.8,
         33.25,
         33.5,
         33,
         32.15]
npref = ['Kumamoto',
         'Nagasaki',
         'Saga',
         'Fukuoka',
         'Oita',
         'Miyazaki']

for i in range(len(xpref)):
    xx, yy = m(xpref[i], ypref[i])
    axa.text(xx,
             yy,
             npref[i],
             color = 'black',
             zorder = 4,
             ha = 'center',
             va = 'center',
             fontsize = 7)

#legend
axa.legend(fontsize = 6,
           loc = 1)

#title figure

#save figure
os.chdir(path)
figa.savefig('seismicite_article.pdf')
