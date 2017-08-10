from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np

dossier = sys.argv[1]

path = os.getcwd()[:-6] + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_sac_inf100km'
path_results = path + '/' + dossier + '_3comp'

if os.path.isdir(path_results) == False:
	os.makedirs(path_results)

list_fich = os.listdir(path_data)
list_fich_x = [a for a in list_fich if ('EW' in a) == True and ('EW1' in a) == False]
list_fich_y = [a for a in list_fich if ('NS' in a) == True and ('NS1' in a) == False]
list_fich_z = [a for a in list_fich if ('UD' in a) == True and ('UD1' in a) == False]

list_fich_x.sort()
list_fich_y.sort()
list_fich_z.sort()

for station in list_fich_x:
	os.chdir(path_data)
	stx = read(station)
	sty = read(list_fich_y[list_fich_x.index(station)])
	stz = read(list_fich_z[list_fich_x.index(station)])
	if stx[0].stats.station == sty[0].stats.station and stx[0].stats.station == stz[0].stats.station:
		tr_x = stx[0]
		tr_y = sty[0]
		tr_z = stz[0]
		tr_s = [a/abs(a) if abs(a)>0 else 0 for a in tr_z]
		tr = [d*math.sqrt(a**2 + b**2 + c**2) for a,b,c,d in zip(tr_x, tr_y, tr_z, tr_s)]
		tr = np.asarray(tr)
		os.chdir(path_results)
		tr = Trace(tr, stz[0].stats)
		tr.write(station, format = 'SAC')
	else:
		print('     ', stx[0].stats.station, sty[0].stats.station, stz[0].stats.station)

