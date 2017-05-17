import math
from obspy import read
import os
import sys
from obspy import Trace
import numpy as np

dossier = sys.argv[1]

path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_env/' + str(dossier)
path_results = path + '/Data/Kumamoto_env_select/' + str(dossier)

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

list_station = os.listdir(path_data)

for station in list_station:
    os.chdir(path_data)
    stP = read(station)
    stS = read(station)
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
    #rapport_PS.append(math.log10(trP.max()/trS.max()))
    rapport_PS = math.log10(trP.max()/trS.max())
    if rapport_PS < math.log10(1./3):
        st = read(station)
        os.chdir(path_results)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format='SAC')


















