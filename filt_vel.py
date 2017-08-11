from obspy import read
from obspy import Trace
import os
import sys

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel'
path_rslt1 = path + '/' + dossier + '_vel_02_05Hz'
path_rslt2 = path + '/' + dossier + '_vel_05_1Hz'
path_rslt3 = path + '/' + dossier + '_vel_1_2Hz'
path_rslt4 = path + '/' + dossier + '_vel_2_4Hz'
path_rslt5 = path + '/' + dossier + '_vel_4_10Hz'

lst_pth_rslt = [path_rslt1, path_rslt2, path_rslt3, path_rslt4, path_rslt5]

for pth in lst_path_rslt:
    if os.path.isdir(pth) == False:
    	os.makedirs(pth)

lst_fch = os.listdir(path_data)

for station in lst_fch:
    print(station)

    os.chdir(path_data)
    st = read(station)
    tr = Trace(st[0].filter('bandpass', freqmin = 0.2, freqmax = 0.5, corners = 4, zerophase = True), st[0].stats)
    os.chdir(path_rslt1)
    tr.write(station + '_02_05Hz', format = 'SAC')
    
    os.chdir(path_data)
    st = read(station)
    tr = Trace(st[0].filter('bandpass', freqmin = 0.5, freqmax = 1, corners = 4, zerophase = True), st[0].stats)
    os.chdir(path_rslt2)
    tr.write(station + '_05_1Hz', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    tr = Trace(st[0].filter('bandpass', freqmin = 1, freqmax = 2, corners = 4, zerophase = True), st[0].stats)
    os.chdir(path_rslt3)
    tr.write(station + '_1_2Hz', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    tr = Trace(st[0].filter('bandpass', freqmin = 2, freqmax = 4, corners = 4, zerophase = True), st[0].stats)
    os.chdir(path_rslt4)
    tr.write(station + '_2_4Hz', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    tr = Trace(st[0].filter('bandpass', freqmin = 4, freqmax = 10, corners = 4, zerophase = True), st[0].stats)
    os.chdir(path_rslt5)
    tr.write(station + '_4_10Hz', format = 'SAC')


























