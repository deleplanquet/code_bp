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

#normalisation
def norm1(vect):
    return [5*a/vect.max() for a in vect]

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_sac_inf100km'
path_results = path + '/' + dossier + '_vel'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

os.chdir(path_origin + '/Data')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

dict_doss = dict_seis[dossier]

lst_fch_x = [a for a in os.listdir(path_data) if ('EW' in a) == True]
lst_fch_y = [a for a in os.listdir(path_data) if ('NS' in a) == True]
lst_fch_z = [a for a in os.listdir(path_data) if ('UD' in a) == True]

lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

for station in lst_fch_x:
    #fig, ax = plt.subplots(1, 1)
    #ax.set_xlabel('Time (s)')
    #ax.set_ylabel('')

    os.chdir(path_data)

    stx = read(station)
    sty = read(lst_fch_y[lst_fch_x.index(station)])
    stz = read(lst_fch_z[lst_fch_x.index(station)])

    stx.detrend(type = 'constant')
    sty.detrend(type = 'constant')
    stz.detrend(type = 'constant')

    tstart = stx[0].stats.starttime + stx[0].stats.sac.a - 5
    tend = tstart + 50

    tr_x = stx[0].trim(tstart, tend, pad=True, fill_value=0)
    tr_y = sty[0].trim(tstart, tend, pad=True, fill_value=0)
    tr_z = stz[0].trim(tstart, tend, pad=True, fill_value=0)

    stx[0].stats.sac.nzyear = stz[0].stats.starttime.year
    stx[0].stats.sac.nzjday = stz[0].stats.starttime.julday
    stx[0].stats.sac.nzhour = stz[0].stats.starttime.hour
    stx[0].stats.sac.nzmin = stz[0].stats.starttime.minute
    stx[0].stats.sac.nzsec = stz[0].stats.starttime.second
    stx[0].stats.sac.nzmsec = stz[0].stats.starttime.microsecond
    sty[0].stats.sac.nzyear = stz[0].stats.starttime.year
    sty[0].stats.sac.nzjday = stz[0].stats.starttime.julday
    sty[0].stats.sac.nzhour = stz[0].stats.starttime.hour
    sty[0].stats.sac.nzmin = stz[0].stats.starttime.minute
    sty[0].stats.sac.nzsec = stz[0].stats.starttime.second
    sty[0].stats.sac.nzmsec = stz[0].stats.starttime.microsecond
    stz[0].stats.sac.nzyear = stz[0].stats.starttime.year
    stz[0].stats.sac.nzjday = stz[0].stats.starttime.julday
    stz[0].stats.sac.nzhour = stz[0].stats.starttime.hour
    stz[0].stats.sac.nzmin = stz[0].stats.starttime.minute
    stz[0].stats.sac.nzsec = stz[0].stats.starttime.second
    stz[0].stats.sac.nzmsec = stz[0].stats.starttime.microsecond

    #st[0].stats.starttime = tstart
    stx[0].stats.sac.t0 = stz[0].stats.sac.t0 - stz[0].stats.sac.a + 5
    stx[0].stats.sac.a = 5
    sty[0].stats.sac.t0 = stz[0].stats.sac.t0 - stz[0].stats.sac.a + 5
    sty[0].stats.sac.a = 5
    stz[0].stats.sac.t0 = stz[0].stats.sac.t0 - stz[0].stats.sac.a + 5
    stz[0].stats.sac.a = 5

    t = np.arange(tr.stats.npts)/tr.stats.sampling_rate

    #ax.plot(t, norm1(tr.data), linewidth = 0.2, color = 'black')
    #ax.plot(norm1(np.fft.fft(tr)[range(int(tr.stats.npts/2))]), linewidth = 0.2, color = 'black')

    freq = np.arange(1, tr_x.stats.npts + 1)/tr_x.stats.sampling_rate/tr_x.stats.npts
    #freq = freq[range(tr.stats.npts/2)]
    tfx = np.fft.fft(tr_x)#/tr.stats.npts
    tfy = np.fft.fft(tr_y)#/tr.stats.npts
    tfz = np.fft.fft(tr_z)#/tr.stats.npts

    #tf = abs(np.fft.fft(tr))/tr.stats.npts
    #tf = tf[range(tr.stats.npts/2)]
    tfx_vel = tfx * (-1j) / 2 / math.pi / freq
    tfy_vel = tfy * (-1j) / 2 / math.pi / freq
    tfz_vel = tfz * (-1j) / 2 / math.pi / freq

    trx_vel = np.fft.ifft(tfx_vel)
    try_vel = np.fft.ifft(tfy_vel)
    trz_vel = np.fft.ifft(tfz_vel)
    
    #ax.plot(t, norm1(tr_vel.real) + np.arange(1, 2, 2)*5, linewidth = 0.2, color = 'red')
    #ax.plot(norm1(np.fft.fft(tr_vel)[range(int(tr.stats.npts/2))]) + np.arange(1, 2, 2)*5, linewidth = 0.2, color = 'red')

    trx_vel = Trace(trx_vel, tr_x.stats)
    try_vel = Trace(try_vel, tr_y.stats)
    trz_vel = Trace(trz_vel, tr_z.stats)

    os.chdir(path_results)
    #fig.savefig(tr.stats.station + '.pdf')
    trx_vel.write(station[:-4] + '_vel.sac', format = 'SAC')
    try_vel.write(station[:-4] + '_vel.sac', format = 'SAC')
    trz_vel.write(station[:-4] + '_vel.sac', format = 'SAC')









