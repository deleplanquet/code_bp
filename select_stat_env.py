import math
from obspy import read
import os
import sys
from obspy import Trace
import numpy as np

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz_hori_env')

lst_pth_rslt_P = []
lst_pth_rslt_S = []

for freq in lst_frq:
    pth_dt = path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz'
    lst_pth_rslt_P.append(pth_dt + '_hori_env_P')
    lst_pth_rslt_S.append(pth_dt + '_hori_env_S')
    if os.path.isdir(lst_pth_rslt_P[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt_P[lst_frq.index(freq)])
    if os.path.isdir(lst_pth_rslt_S[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt_S[lst_frq.index(freq)])

lst_fch = []

for freq in lst_frq:
    lst_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

for freq in lst_frq:
    print('     ', freq)
    for station in lst_fch[lst_frq.index(freq)]:
    	os.chdir(lst_pth_dt[lst_frq.index(freq)])
    	stP = read(station)
    	stS = read(station)
    	arrival_P = stP[0].stats.starttime + stP[0].stats.sac.a
    	arrival_S = stS[0].stats.starttime + stS[0].stats.sac.t0
    	delai_PS = arrival_S - arrival_P
    	if delai_PS < 5:
    	    stP[0].trim(arrival_P, arrival_P + delai_PS + 0.1)
    	else:
    	    stP[0].trim(arrival_P, arrival_P + 5)
    	stS[0].trim(arrival_S, stS[0].stats.endtime)
    	trP = stP[0]
    	trS = stS[0]
    	rapport_PS = math.log10(trP.max()/trS.max())
    	if rapport_PS > math.log10(3):
    	    st = read(station)
    	    os.chdir(lst_pth_rslt_P[lst_frq.index(freq)])
    	    tr = Trace(st[0].data, st[0].stats)
    	    tr.write(station, format = 'SAC')
    	if rapport_PS < math.log10(1./3):
    	    st = read(station)
    	    os.chdir(lst_pth_rslt_S[lst_frq.index(freq)])
    	    tr = Trace(st[0].data, st[0].stats)
    	    tr.write(station, format = 'SAC')


















