from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

#normalisation
def norm1(vect):
    return [a/vect.max() for a in vect]

dossier = sys.argv[1]

#path = '/localstorage/deleplanque'
path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/' + str(dossier)
path_env = path + '/Data/Kumamoto_env/'
path_env_dossier = path_env + str(dossier)

os.chdir(path_env)

if os.path.isdir(str(dossier)) == False:
    os.makedirs(str(dossier))

list_fich = os.listdir(path_data)

for station in list_fich:
    print(station)
    os.chdir(path_data)
    st = read(station)
    st.detrend(type = 'constant')
    tr = st[0].filter('bandpass', freqmin = 0.2, freqmax = 10, corners = 4, zerophase = True)
    tr = [a**2 for a in tr]
    tr = np.asarray(norm1(smooth(tr, 20)))
    tr = Trace(tr, st[0].stats)
    os.chdir(path_env_dossier)
    tr.write('env_' + station, format = 'SAC')





