from obspy import read
import os
from obspy.signal.util import smooth
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]

dossier = '20160415173900'

path = path_origin + '/Kumamoto/' + dossier

path_data_1 = path + '/' + dossier + '_sac_inf100km'
path_data_2 = path + '/' + dossier + '_vel'
path_data_3 = path + '/' + dossier + '_vel_4_8Hz'
path_data_4 = path + '/' + dossier + '_vel_4_8Hz_hori_env'

fig, ax = plt.subplots(5, 1)

os.chdir(path_data_1)
st1 = read('KMM0181604151739.NS.sac')
t1 = np.arange(st1[0].stats.npts)/st1[0].stats.sampling_rate

os.chdir(path_data_2)
st2 = read('KMM0181604151739.NS_vel.sac')
t2 = np.arange(st2[0].stats.npts)/st2[0].stats.sampling_rate

os.chdir(path_data_3)
st3 = read('KMM0181604151739.NS_vel_4_8Hz.sac')
t3 = np.arange(st3[0].stats.npts)/st3[0].stats.sampling_rate

os.chdir(path_data_4)
st4 = read('KMM0181604151739.vel_4_8Hz_hori_env.sac')
t4 = np.arange(st4[0].stats.npts)/st4[0].stats.sampling_rate

dat5 = smooth(st4[0].data, int(0.5/st4[0].stats.delta))

ax[0].plot(t1, st1[0], color = 'black')
ax[0].set_xlim([3.6, 3.6 + 50])
ax[1].plot(t2, st2[0], color = 'black')
ax[2].plot(t3, st3[0], color = 'black')
ax[3].plot(t4, st4[0], color = 'black')
ax[4].plot(t4, dat5, color = 'black')

plt.subplots_adjust(hspace = 0.001)
ax[0].xaxis.set_visible(False)
ax[1].xaxis.set_visible(False)
ax[2].xaxis.set_visible(False)
ax[3].xaxis.set_visible(False)
ax[4].xaxis.set_visible(False)

ax[0].yaxis.set_visible(False)
ax[1].yaxis.set_visible(False)
ax[2].yaxis.set_visible(False)
ax[3].yaxis.set_visible(False)
ax[4].yaxis.set_visible(False)

os.chdir(path)
fig.savefig(dossier + '_chrono.pdf')

fig2, ax2 = plt.subplots(2, 1)

os.chdir(path_data_4)
sta = read('MYZ0071604151739.vel_4_8Hz_hori_env.sac')

data = smooth(sta[0].data, int(0.5/sta[0].stats.delta))

ax2[0].plot(t4, dat5)
ax2[1].plot(t4, data)

plt.subplots_adjust(hspace = 0.001)
ax2[0].xaxis.set_visible(False)
ax2[1].xaxis.set_visible(False)

ax2[0].yaxis.set_visible(False)
ax2[1].yaxis.set_visible(False)

os.chdir(path)
fig2.savefig(dossier + '_comparaison_SP.pdf')
