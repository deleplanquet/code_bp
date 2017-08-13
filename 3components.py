from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_pth_dt = []
lst_pth_rslt = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz')
    lst_pth_rslt.append(path + '/' + dossier + '_vel_' + freq + 'Hz_3comp')

for pth in lst_pth_rslt:
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
    for station in lst_fch_x[lst_frq.index(freq)]:
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
    	    tr = [math.sqrt(a**2 + b**2 + c**2) for a,b,c in zip(tr_x, tr_y, tr_z)]
    	    tr = np.asarray(tr)
    	    os.chdir(lst_pth_rslt[lst_frq.index(freq)])
    	    tr = Trace(tr, stz[0].stats)
    	    tr.write(station[:17] + 'vel_' + freq + 'Hz.sac', format = 'SAC')
    	else:
    	    print('     ', stx[0].stats.station, sty[0].stats.station, stz[0].stats.station)

