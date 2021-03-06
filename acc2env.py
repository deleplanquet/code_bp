from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path = os.getcwd()[:-6] + '/Data/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_sac_inf100km/'
path_env = path + '/' + dossier + '_acc_env/'

if os.path.isdir(path_env) == False:
    os.makedirs(path_env)

list_fich = os.listdir(path_data)
list_fich = [a for a in list_fich if ('UD' in a) == True and ('UD1' in a) == False]

for station in list_fich:
    print(station)
    os.chdir(path_data)
    st = read(station)
    st.detrend(type='constant')
    tstart = st[0].stats.starttime + st[0].stats.sac.a - 5
    tend = tstart + 50
    tr = st[0].trim(tstart, tend, pad = True, fill_value = 0)
    st[0].stats.sac.nzyear = st[0].stats.starttime.year
    st[0].stats.sac.nzjday = st[0].stats.starttime.julday
    st[0].stats.sac.nzhour = st[0].stats.starttime.hour
    st[0].stats.sac.nzmin = st[0].stats.starttime.minute
    st[0].stats.sac.nzsec = st[0].stats.starttime.second
    st[0].stats.sac.nzmsec = st[0].stats.starttime.microsecond
    st[0].stats.sac.t0 = st[0].stats.sac.t0 - st[0].stats.sac.a + 5
    st[0].stats.sac.a = 5
    tr = tr.filter('bandpass', freqmin = 0.2, freqmax = 10, corners = 4, zerophase = True)
    tr = [a**2 for a in tr]
    tr = np.asarray(smooth(tr, 20))
    tr = Trace(tr, st[0].stats)
    os.chdir(path_env)
    tr.write('env_' + station, format = 'SAC')

