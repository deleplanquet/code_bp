from obspy import read
from obspy import Trace
import pickle
import numpy as np
import sys
import os
import math
import matplotlib.pyplot as plt

#constantes
R_Earth = 6400

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#distance entre deux points, coordonnees cartesiennes
def dist(la1, lo1, el1, la2, lo2, el2):
    x1, y1, z1 = geo2cart(R_Earth + el1, la1, lo1)
    x2, y2, z2 = geo2cart(R_Earth + el2, la2, lo2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#normalisation
def norm1(vect):
    return [5*a/vect.max() for a in vect]

dossier = sys.argv[1]

path = os.getcwd()[:-6]
path_data = path + '/Data/Kumamoto_sac_inf100km/' + dossier
path_results = path + '/Data/Kumamoto_vel/' + dossier

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

os.chdir(path + '/Data')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

dict_doss = dict_seis[dossier]

list_fich = os.listdir(path_data)
list_fich = [a for a in list_fich if ('UD' in a) == True and ('UD1' in a) == False]

for station in list_fich:
    #fig, ax = plt.subplots(1, 1)
    #ax.set_xlabel('Time (s)')
    #ax.set_ylabel('')

    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tstart = st[0].stats.starttime + st[0].stats.sac.a - 5
    tend = tstart + 50
    st[0].stats.sac.t0 = st[0].stats.sac.t0 - st[0].stats.sac.a + 5
    st[0].stats.sac.a = 5
    tr = st[0].trim(tstart, tend, pad=True, fill_value=0)
    t = np.arange(tr.stats.npts)/tr.stats.sampling_rate
    ordo = dist(st[0].stats.sac.stla, st[0].stats.sac.stlo, 0.001*st[0].stats.sac.stel, dict_doss['lat'], dict_doss['lon'], -dict_doss['dep'])

    #ax.plot(t, norm1(tr.data), linewidth = 0.2, color = 'black')
    #ax.plot(norm1(np.fft.fft(tr)[range(int(tr.stats.npts/2))]), linewidth = 0.2, color = 'black')

    freq = np.arange(1, tr.stats.npts + 1)/tr.stats.sampling_rate/tr.stats.npts
    #freq = freq[range(tr.stats.npts/2)]
    tf = np.fft.fft(tr)#/tr.stats.npts
    #tf = abs(np.fft.fft(tr))/tr.stats.npts
    #tf = tf[range(tr.stats.npts/2)]
    tf_vel = tf * (-1j) / 2 / math.pi / freq
    tr_vel = np.fft.ifft(tf_vel)
    
    #ax.plot(t, norm1(tr_vel.real) + np.arange(1, 2, 2)*5, linewidth = 0.2, color = 'red')
    #ax.plot(norm1(np.fft.fft(tr_vel)[range(int(tr.stats.npts/2))]) + np.arange(1, 2, 2)*5, linewidth = 0.2, color = 'red')

    tr_vel = Trace(tr_vel, tr.stats)

    os.chdir(path_results)
    #fig.savefig(tr.stats.station + '.pdf')
    tr.write('vel_' + station, format = 'SAC')










