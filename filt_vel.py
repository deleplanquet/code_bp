from obspy import read
import numpy as np
from obspy import Trace
import os
import sys

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel'

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_pth_rslt = []

for freq in lst_frq:
    lst_pth_rslt.append(path + '/' + dossier + '_vel_' + freq + 'Hz')
    if os.path.isdir(lst_pth_rslt[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt[lst_frq.index(freq)])

lst_fch = os.listdir(path_data)

for station in lst_fch:
    print('     ', station)

    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 0.2, freqmax = 0.5, corners = 4, zerophase = True)
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(lst_pth_rslt[0])
    tr.write(station[:-4] + '_02_05Hz.sac', format = 'SAC')
    
    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 0.5, freqmax = 1, corners = 4, zerophase = True)
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(lst_pth_rslt[1])
    tr.write(station[:-4] + '_05_1Hz.sac', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 1, freqmax = 2, corners = 4, zerophase = True)
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(lst_pth_rslt[2])
    tr.write(station[:-4] + '_1_2Hz.sac', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 2, freqmax = 4, corners = 4, zerophase = True)
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(lst_pth_rslt[3])
    tr.write(station[:-4] + '_2_4Hz.sac', format = 'SAC')

    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 4, freqmax = 10, corners = 4, zerophase = True)
    tr = Trace(np.asarray(tr), st[0].stats)
    os.chdir(lst_pth_rslt[4])
    tr.write(station[:-4] + '_4_10Hz.sac', format = 'SAC')


























