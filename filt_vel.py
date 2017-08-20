from obspy import read
import numpy as np
from obspy import Trace
import os
import sys

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel'

lst_frq_mi = ['02', '05', '1', '2', '4']
lst_frq_ma = ['05', '1', '2', '4', '10']
lst_pth_rslt = []

for freq in lst_frq_mi:
    lst_pth_rslt.append(path + '/' + dossier + '_vel_' + freq + '_' + lst_frq_ma[lst_frq_mi.index(freq)] + 'Hz')
    if os.path.isdir(lst_pth_rslt[lst_frq_mi.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt[lst_frq_mi.index(freq)])

lst_fch_x = [a for a in os.listdir(path_data) if ('EW' in a) == True]
lst_fch_y = [a for a in os.listdir(path_data) if ('NS' in a) == True]
lst_fch_z = [a for a in os.listdir(path_data) if ('UD' in a) == True]

lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

for freq in lst_frq_mi:
    print('   ', freq, lst_frq_ma[lst_frq_mi.index(freq)])
    if freq == '02':
    	fqmi = 0.2
    	fqma = 0.5
    elif freq == '05':
    	fqmi = 0.5
    	fqma = 1
    elif freq == '1':
    	fqmi = 1
    	fqma = 2
    elif freq == '2':
    	fqmi = 2
    	fqma = 4
    elif freq == '4':
    	fqmi = 4
    	fqma = 10
    else:
    	print('ERROR LIST_FREQ')
    	sys.exit(0
)
    for station in lst_fch_x:
    	print('     ', station)

    	os.chdir(path_data)
    	stx = read(station)
    	sty = read(lst_fch_y[lst_fch_x.index(station)])
    	stz = read(lst_fch_z[lst_fch_x.index(station)])
    	stx.detrend(type = 'constant')
    	sty.detrend(type = 'constant')
    	stz.detrend(type = 'constant')
    	stx[0].taper(0.05, type = 'hann', max_length = None, side = 'both')
    	sty[0].taper(0.05, type = 'hann', max_length = None, side = 'both')
    	stz[0].taper(0.05, type = 'hann', max_length = None, side = 'both')
    	tr_x = stx[0].filter('bandpass', freqmin = fqmi, freqmax = fqma, corners = 4, zerophase = False)
    	tr_y = sty[0].filter('bandpass', freqmin = fqmi, freqmax = fqma, corners = 4, zerophase = False)
    	tr_z = stz[0].filter('bandpass', freqmin = fqmi, freqmax = fqma, corners = 4, zerophase = False)
    	tr_x = Trace(np.asarray(tr_x), stz[0].stats)
    	tr_y = Trace(np.asarray(tr_y), stz[0].stats)
    	tr_z = Trace(np.asarray(tr_z), stz[0].stats)

    	os.chdir(lst_pth_rslt[lst_frq_mi.index(freq)])
    	tr_x.write(station[:-4] + '_' + freq + '_' + lst_frq_ma[lst_frq_mi.index(freq)] + 'Hz.sac', format = 'SAC')
    	tr_y.write(lst_fch_y[lst_fch_x.index(station)][:-4] + '_' + freq + '_' + lst_frq_ma[lst_frq_mi.index(freq)] + 'Hz.sac', format = 'SAC')
    	tr_z.write(lst_fch_z[lst_fch_x.index(station)][:-4] + '_' + freq + '_' + lst_frq_ma[lst_frq_mi.index(freq)] + 'Hz.sac', format = 'SAC')


























