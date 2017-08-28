from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []
lst_pth_rslt = []
lst_pth_rslt_h = []
lst_pth_rslt_v = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz')
    lst_pth_rslt.append(path + '/' + dossier + '_vel_' + freq + 'Hz_3comp')
    lst_pth_rslt_h.append(path + '/' + dossier + '_vel_' + freq + 'Hz_hori')
    lst_pth_rslt_v.append(path + '/' + dossier + '_vel_' + freq + 'Hz_vert')

for pth in lst_pth_rslt:
    if os.path.isdir(pth) == False:
    	os.makedirs(pth)
for pth in lst_pth_rslt_h:
    if os.path.isdir(pth) == False:
    	os.makedirs(pth)
for pth in lst_pth_rslt_v:
    if os.path.isdir(pth) == False:
    	os.makedirs(pth)

lst_fch_x = []
lst_fch_y = []
lst_fch_z = []

for pth in lst_pth_dt:
    lst_fch_x.append([a for a in os.listdir(pth) if ('EW' in a) == True])
    lst_fch_y.append([a for a in os.listdir(pth) if ('NS' in a) == True])
    lst_fch_z.append([a for a in os.listdir(pth) if ('UD' in a) == True])

    lst_fch_x[lst_pth_dt.index(pth)].sort()
    lst_fch_y[lst_pth_dt.index(pth)].sort()
    lst_fch_z[lst_pth_dt.index(pth)].sort()

for freq in lst_frq:
    print('     ', freq)
    for station in lst_fch_x[lst_frq.index(freq)]:
    	print('       ', station)
    	os.chdir(lst_pth_dt[lst_frq.index(freq)])
    	stx = read(station)
    	sty = read(lst_fch_y[lst_frq.index(freq)][lst_fch_x[lst_frq.index(freq)].index(station)])
    	stz = read(lst_fch_z[lst_frq.index(freq)][lst_fch_x[lst_frq.index(freq)].index(station)])
    	if stx[0].stats.station == sty[0].stats.station and stx[0].stats.station == stz[0].stats.station:
    	    stx.detrend(type = 'constant')
    	    sty.detrend(type = 'constant')
    	    stz.detrend(type = 'constant')
    	    tr_x = stx[0]
    	    tr_y = sty[0]
    	    tr_z = stz[0]
    	    trh = [math.sqrt(a**2 + b**2) for a,b in zip(tr_x, tr_y)]
    	    tr3 = [math.sqrt(a**2 + b**2 + c**2) for a,b,c in zip(tr_x, tr_y, tr_z)]
    	    os.chdir(lst_pth_rslt_v[lst_frq.index(freq)])
    	    trv = Trace(np.asarray(tr_z), stz[0].stats)
    	    trv.write(station[:17] + 'vel_' + freq + 'Hz_vert.sac', format = 'SAC')
    	    os.chdir(lst_pth_rslt_h[lst_frq.index(freq)])
    	    trh = Trace(np.asarray(trh), stz[0].stats)
    	    trh.write(station[:17] + 'vel_' + freq + 'Hz_hori.sac', format = 'SAC')
    	    os.chdir(lst_pth_rslt[lst_frq.index(freq)])
    	    tr3 = Trace(np.asarray(tr3), stz[0].stats)
    	    tr3.write(station[:17] + 'vel_' + freq + 'Hz.sac', format = 'SAC')
    	else:
    	    print('     ', stx[0].stats.station, sty[0].stats.station, stz[0].stats.station)

