from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path = '/localstorage/deleplanque'
#path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/' + str(dossier)
path_env = path + '/Data/Kumamoto_env/'
path_env_dossier = path_env + str(dossier)

os.chdir(path_env)

if os.path.isdir(str(dossier)) == False:
    os.makedirs(str(dossier))

list_fich = os.listdir(path_data)
list_fich = [a for a in list_fich if ('UD' in a) == True and ('UD1' in a) == False]

for station in list_fich:
    print(station)
    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    old_a = st[0].stats.sac.a
    tstart = st[0].stats.starttime + st[0].stats.sac.a - 5
    st[0].stats.sac.a = 5
    st[0].stats.sac.t0 = st[0].stats.sac.t0 - old_a + 5
    tend = tstart + 50
    tr = st[0].trim(tstart, tend, pad=True, fill_value=0)
    tr = tr.filter('bandpass', freqmin = 0.2, freqmax = 10, corners = 4, zerophase = True)
    tr = [a**2 for a in tr]
    tr = np.asarray(smooth(tr, 20))
    tr = Trace(tr, st[0].stats)
    os.chdir(path_env_dossier)
    tr.write('env_' + station, format = 'SAC')





