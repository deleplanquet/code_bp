from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path = os.getcwd()[:-6] + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel/'
path_env_02 = path + '/' + dossier + '_vel_env_02_05Hz/'
path_env_05 = path + '/' + dossier + '_vel_env_05_1Hz/'
path_env_1 = path + '/' + dossier + '_vel_env_1_2Hz/'
path_env_2 = path + '/' + dossier + '_vel_env_2_4Hz/'
path_env_4 = path + '/' + dossier + '_vel_env_4_10Hz/'

if os.path.isdir(path_env_02) == False:
    os.makedirs(path_env_02)
if os.path.isdir(path_env_05) == False:
    os.makedirs(path_env_05)
if os.path.isdir(path_env_1) == False:
    os.makedirs(path_env_1)
if os.path.isdir(path_env_2) == False:
    os.makedirs(path_env_2)
if os.path.isdir(path_env_4) == False:
    os.makedirs(path_env_4)

list_fich = os.listdir(path_data)
list_fich = [a for a in list_fich if ('_2016' in a) == True]

for station in list_fich:
    print(station)
    os.chdir(path_data)
    st = read(station)
    tr02 = st[0].filter('bandpass', freqmin = 0.2, freqmax = 0.5, corners = 4, zerophase = True)
    tr05 = st[0].filter('bandpass', freqmin = 0.5, freqmax = 1, corners = 4, zerophase = True)
    tr1 = st[0].filter('bandpass', freqmin = 1, freqmax = 2, corners = 4, zerophase = True)
    tr2 = st[0].filter('bandpass', freqmin = 2, freqmax = 4, corners = 4, zerophase = True)
    tr4 = st[0].filter('bandpass', freqmin = 4, freqmax = 10, corners = 4, zerophase = True)
    tr02 = [a**2 for a in tr02]
    tr05 = [a**2 for a in tr05]
    tr1 = [a**2 for a in tr1]
    tr2 = [a**2 for a in tr2]
    tr4 = [a**2 for a in tr4]
    tr02 = np.asarray(smooth(tr02, 20))
    tr05 = np.asarray(smooth(tr05, 20))
    tr1 = np.asarray(smooth(tr1, 20))
    tr2 = np.asarray(smooth(tr2, 20))
    tr4 = np.asarray(smooth(tr4, 20))
    tr02 = Trace(tr02, st[0].stats)
    tr05 = Trace(tr05, st[0].stats)
    tr1 = Trace(tr1, st[0].stats)
    tr2 = Trace(tr2, st[0].stats)
    tr4 = Trace(tr4, st[0].stats)
    os.chdir(path_env_02)
    tr02.write('02_05Hz_' + station, format = 'SAC')
    os.chdir(path_env_05)
    tr05.write('05_1Hz_' + station, format = 'SAC')
    os.chdir(path_env_1)
    tr1.write('1_2Hz_' + station, format = 'SAC')
    os.chdir(path_env_2)
    tr2.write('2_4Hz_' + station, format = 'SAC')
    os.chdir(path_env_4)
    tr4.write('4_10Hz_' + station, format = 'SAC')





