import math
import matplotlib.pyplot as plt
import os
from obspy import read
from mpl_toolkits.basemap import Basemap
import numpy as np
from obspy.imaging.beachball import beach

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#dossier = '20160416080200'
#dossier = '20160415072000'
dossier = '20160414230200'

path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_env/' + dossier
path_results = path + '/LaTeX/Poster_jpgu_2017'

list_station = os.listdir(path_data)
list_station = [a for a in list_station if ('UD' in a) == True and ('UD1' in a) == False]

lat_fault = [32.65, 32.86]
long_fault = [130.72, 131.07]

#np1 = [276.2, 69.9, -27.6]
strike = 276.2
dip = 69.9
rake = -27.6

Mxx = - math.sin(d2r(dip))*math.cos(d2r(rake))*math.sin(d2r(2* strike)) - math.sin(d2r(2*dip))*math.sin(d2r(rake))*math.sin(d2r(2*strike))
Myy = math.sin(d2r(dip))*math.cos(d2r(rake))*math.sin(d2r(2*strike)) - math.sin(d2r(2*dip))*math.sin(d2r(rake))*math.cos(d2r(2*strike))
Mzz = math.sin(d2r(2*dip))*math.sin(d2r(rake))
Mxy = math.sin(d2r(dip))*math.cos(d2r(rake))*math.cos(d2r(2*strike)) + math.sin(d2r(2*dip))*math.sin(d2r(rake))*math.sin(d2r(strike))*math.cos(d2r(strike))
Mxz = - math.cos(d2r(dip))*math.cos(d2r(rake))*math.cos(d2r(strike)) - math.cos(d2r(2*dip))*math.sin(d2r(rake))*math.sin(d2r(strike))
Myz = - math.cos(d2r(dip))*math.cos(d2r(rake))*math.sin(d2r(strike)) + math.cos(d2r(2*dip))*math.sin(d2r(rake))*math.cos(d2r(strike))

moment_tensor = [Mxx, Myy, Mzz, Mxy, Mxz, Myz]

#base de la carte
fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
            llcrnrlon=129,
            llcrnrlat=31,
            urcrnrlon=132,
            urcrnrlat=34,
            resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(31, 34, 1),
                labels=[1, 0, 0, 0],
                linewidth=1)
m.drawmeridians(np.arange(129, 132, 1),
                labels=[0, 0, 0, 1],
                linewidth=1)
ax.plot(x_fault,
        y_fault,
        color='green',
        linewidth = 0.3,
        zorder = 1)

#epicentre
os.chdir(path_data)
st = read(list_station[0])
x_epi, y_epi = m(st[0].stats.sac.evlo, st[0].stats.sac.evla)
ax.scatter(x_epi, y_epi, 30, marker = '*', color = 'black', zorder = 2)

bx, by = m(131, 33)
bb = beach(moment_tensor, xy = (bx, by), width=200, linewidth=1)
bb.set_zorder(10)

#stations
x_sta = []
y_sta = []
rapport_PS = []
name_sta = []

for station in list_station:
    stP = read(station)
    stS = read(station)
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
    stS[0].trim(arrival_S, arrival_S + 5)
    trP = stP[0]
    trS = stS[0]
    rapport_PS.append(math.log10(trP.max()/trS.max()))
    #rapport_PS.append(0.5)
    name_sta.append(st[0].stats.station)

print(rapport_PS)
rapport_PS = [a if (a<1 and a>-1) else -1 if (a<-1) else 1 if (a>1) else a for a in rapport_PS]
print(rapport_PS)
#couleur = tuple(rapport_PS)
ax.add_collection(bb)
ax.scatter(x_sta, y_sta, 15, marker = 'o', cmap = 'seismic', c = rapport_PS, zorder = 3)
ax.text(x_sta, y_sta, st[0].stats.station, fontsize = 1, ha = 'right', va = 'center', zorder = 4)

os.chdir(path_results)
fig.savefig('map' + str(dossier) + '.pdf')









