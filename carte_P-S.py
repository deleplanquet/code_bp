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

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth'
path_results = path + '/' + dossier + '_results'

lst_sta = os.listdir(path_data)

#lat_fault = [32.65, 32.86]
#long_fault = [130.72, 131.07]

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

#base de la carte
fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
            llcrnrlon=129,
            llcrnrlat=31.5,
            urcrnrlon=132,
            urcrnrlat=33.5,
            resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')

m.drawmapscale(130.35, 32.22, -3.25, 39.5, 100, barstyle = 'fancy')

#epicentre
x_epi, y_epi = m(lon_eq, lat_eq)
ax.scatter(x_epi, y_epi, 30, marker = '*', color = 'black', zorder = 2)

bx, by = m()

ax.plot([x_epi, bx], [y_epi, by], color = 'black', linewidth = 0.2)

bb = beach(angles, xy = (bx, by), width = 20000, linewidth = 0.1)
bb.set_zorder(4)

#stations
x_sta = []
y_sta = []
rapport_SP = []
name_sta = []

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
    rapport_SP.append(math.log10(trS.max()/trP.max()))
    name_sta.append(st[0].stats.station)

rapport_SP = [-1 if (a<-1) else 1 if (a>1) else a for a in rapport_SP]
print(rapport_SP)

ax = plt.gca()
ax.add_collection(bb)
#cax = fig.add_axes([0.17, 0.15, 0.02, 0.3])
#cax.zorder = 5
im = ax.scatter(x_sta, y_sta, 15, marker = 'o', cmap = 'seismic', c = rapport_SP, zorder = 3)
cb = fig.colorbar(im, cax = cax, orientation = 'vertical')
tick_locator = ticker.MaxNLocator(nbins = 3)
cb.set_ticks([-1, 0, 1])
cb.set_ticklabels([0.1, 1, 10])
cb.locator = tick_locator
cn.update_ticks()

os.chdir(path_results)
fig_savefig('map_rapport-SP_' + dossier + '.pdf')









