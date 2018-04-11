import numpy as np
from matplotlib import ticker
from pylab import *
import math
import cmath
import matplotlib.pyplot as plt
import os
import sys
from mpl_toolkits.basemap import Basemap
from scipy import interpolate
from scipy.signal import hilbert
from obspy import read
from obspy.signal.util import smooth
from scipy import ndimage
from obspy.imaging.beachball import beach
import pickle

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    param = mdpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
ratioSP = param['ratioSP']

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth'
path_results = path + '/' + dossier + '_results'

lst_sta = os.listdir(path_data)

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    dict_seis = mdpck.load()

strike_eq = dict_seis[dossier]['str1']
dip_eq = dict_seis[dossier]['dip1']
rake_eq = dict_seis[dossier]['rak1']
lat_eq = dict_seis[dossier]['lat']
lon_eq = dict_seis[dossier]['lon']

angles = [strike_eq, dip_eq, rake_eq]

w_bord = dict_seis['20160416012500']['lon'] - 1.5
e_bord = dict_seis['20160416012500']['lon'] + 1.5
n_bord = dict_seis['20160416012500']['lat'] + 1.2
s_bord = dict_seis['20160416012500']['lat'] - 1.2
print(w_bord, s_bord, e_bord, n_bord)

#base de la carte
fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
            llcrnrlon = w_bord,
            llcrnrlat = s_bord,
            urcrnrlon = e_bord,
            urcrnrlat = n_bord,
            resolution='f')
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')

m.drawmapscale(e_bord - 0.55, s_bord + 0.15, lon_eq, lat_eq, 100, barstyle = 'fancy', zorder = 6)

#main shocks
ms_lst = ['20160416012500', '20160414212600', '20160415000300']
clr_lst = ['red', 'blue', 'green']
siz_lst = [80, 60, 60]
lbl_lst = ['MS Mw 7.1', '1st FS Mw 6.1', '2nd FS Mw 6.0']

for mshock in ms_lst:
    if mshock != dossier:
        print(dict_seis[mshock]['lon'], dict_seis[mshock]['lat'])
        xm, ym = m(dict_seis[mshock]['lon'], dict_seis[mshock]['lat'])
        ax.scatter(xm, ym, siz_lst[ms_lst.index(mshock)], marker = '*', color = clr_lst[ms_lst.index(mshock)], zorder = 3, linewidth = 0.1)
        ax.scatter(xm, ym, 0.5*siz_lst[ms_lst.index(mshock)], marker = '*', color = 'white', zorder = 3, linewidth = 0)

        bsx, bsy = m(e_bord - 0.15, (n_bord + s_bord)/2 + 0.8 + 0.2*(1 - ms_lst.index(mshock)))
        ax.plot([xm, bsx], [ym, bsy], color = 'black', linewidth = 0.2, zorder = 2)
        bbms = beach([dict_seis[mshock]['str1'], dict_seis[mshock]['dip1'], dict_seis[mshock]['rak1']], xy = (bsx, bsy), width = 10000, linewidth = 0.1, facecolor = clr_lst[ms_lst.index(mshock)])
        bbms.set_zorder(3)
        ax.add_collection(bbms)

        xx, yy = m(e_bord - 0.15, (n_bord + s_bord)/2 + 0.85 + 0.2*(1 - ms_lst.index(mshock)))
        ax.text(xx, yy, lbl_lst[ms_lst.index(mshock)], fontsize = 5, ha = 'center', va = 'bottom')

#epicentre
print(lon_eq, lat_eq)
x_epi, y_epi = m(lon_eq, lat_eq)
ax.scatter(x_epi, y_epi, 100, marker = '*', color = 'black', zorder = 4, linewidth = 0.1)

bx, by = m(e_bord - 0.2, (n_bord + s_bord)/2 - 0.5)

ax.plot([x_epi, bx], [y_epi, by], color = 'black', linewidth = 0.2, zorder = 2)

bb = beach(angles, xy = (bx, by), width = 20000, linewidth = 0.1)
bb.set_zorder(4)

#stations
x_sta = []
y_sta = []
rapport_SP = []
name_sta = []

os.chdir(path_data)
for station in lst_sta:
    stP = read(station)
    stS = read(station)
    sta_name = stP[0].stats.station
    xst, yst = m(stP[0].stats.sac.stlo, stP[0].stats.sac.stla)
    x_sta.append(xst)
    y_sta.append(yst)
    arrival_P = stP[0].stats.starttime + stP[0].stats.sac.a
    arrival_S = stS[0].stats.starttime + stS[0].stats.sac.t0
    delai_PS = arrival_S - arrival_P
    if delai_PS < 5:
        stP[0].trim(arrival_P, arrival_P + delai_PS - 0.1)
    else:
        stP[0].trim(arrival_P, arrival_P + 5)
    stS[0].trim(arrival_S, arrival_S + 10)
    trP = stP[0]
    trS = stS[0]
    rapport_SP.append(math.log10(trS.max()/trP.max())/math.log10(ratioSP))
    name_sta.append(stP[0].stats.station)

print(ratioSP, math.log10(ratioSP), math.log10(1/ratioSP))

ax = plt.gca()
ax.add_collection(bb)
cax = fig.add_axes([0.21, 0.12, 0.015, 0.2])
cax.zorder = 6
im = ax.scatter(x_sta, y_sta, 15, marker = 'o', cmap = 'seismic', c = rapport_SP, zorder = 5, linewidth = 0.1, vmin = -3, vmax = 3)
cb = fig.colorbar(im, cax = cax, orientation = 'vertical')
tick_locator = ticker.MaxNLocator(nbins = 3)
cb.set_clim(vmin = -ratioSP, vmax = ratioSP) #defini les bornes de la palette
cb.set_ticks([-ratioSP, 0, ratioSP])
cb.set_ticklabels(['1/' + str(int(ratioSP)), 1, int(ratioSP)])
cb.locator = tick_locator
cb.update_ticks()

os.chdir(path_results)
fig.savefig('map_rapport-SP_' + dossier + '.pdf')









