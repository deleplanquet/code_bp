import math
from obspy import read
import os
import sys
from obspy import Trace
import numpy as np

dossier = sys.argv[1]

path = os.getcwd()[:-6] + '/Data/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_env/'
path_resultsP = path + '/' + dossier + '_vel_env_selectP/'
path_resultsS = path + '/' + dossier + '_vel_env_selectS/'

if os.path.isdir(path_resultsP) == False:
    os.makedirs(path_resultsP)

if os.path.isdir(path_resultsS) == False:
    os.makedirs(path_resultsS)

list_station = os.listdir(path_data)
list_station = [a for a in list_station if ('DS_Store' in a) == False]

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
    stS[0].trim(arrival_S, stS[0].stats.endtime)
    trP = stP[0]
    trS = stS[0]
    #rapport_PS.append(math.log10(trP.max()/trS.max()))
    rapport_PS = math.log10(trP.max()/trS.max())
    if rapport_PS > math.log10(3):
        st = read(station)
        os.chdir(path_resultsP)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format='SAC')
    if rapport_PS < math.log10(1./3):
        st = read(station)
        os.chdir(path_resultsS)
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format='SAC')


















