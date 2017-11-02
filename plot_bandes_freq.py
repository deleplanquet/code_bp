import matplotlib.pyplot as plt
import numpy as np
import os
from obspy import read

plt.rc('font', size = 15)

fig, ax = plt.subplots(7, 1, sharex = True)
#ax[3].set_ylabel('Energy', fontsize = 20)
#ax[6].set_xlabel('Time (s)', fontsize = 20)

dossier = '20160415173900'

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
os.chdir(path + '/' + dossier + '_vel_02_05Hz/' + dossier + '_vel_02_05Hz_hori_env_smooth')
st0 = read('KMM0051604151739.vel_02_05Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_05_1Hz/' + dossier + '_vel_05_1Hz_hori_env_smooth')
st1 = read('KMM0051604151739.vel_05_1Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_1_2Hz/' + dossier + '_vel_1_2Hz_hori_env_smooth')
st2 = read('KMM0051604151739.vel_1_2Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_2_4Hz/' + dossier + '_vel_2_4Hz_hori_env_smooth')
st3 = read('KMM0051604151739.vel_2_4Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_4_8Hz/' + dossier + '_vel_4_8Hz_hori_env_smooth')
st4 = read('KMM0051604151739.vel_4_8Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_8_16Hz/' + dossier + '_vel_8_16Hz_hori_env_smooth')
st5 = read('KMM0051604151739.vel_8_16Hz_hori_env_smooth.sac')

os.chdir(path + '/' + dossier + '_vel_16_30Hz/' + dossier + '_vel_16_30Hz_hori_env_smooth')
st6 = read('KMM0051604151739.vel_16_30Hz_hori_env_smooth.sac')

t = np.arange(st0[0].stats.npts)/st0[0].stats.sampling_rate

ax[0].plot(t, st0[0].data)
ax[1].plot(t, st1[0].data)
ax[2].plot(t, st2[0].data)
ax[3].plot(t, st3[0].data)
ax[4].plot(t, st4[0].data)
ax[5].plot(t, st5[0].data)
ax[6].plot(t, st6[0].data)

ax[0].set_xlim([0, 50])
ax[1].set_xlim([0, 50])
ax[2].set_xlim([0, 50])
ax[3].set_xlim([0, 50])
ax[4].set_xlim([0, 50])
ax[5].set_xlim([0, 50])
ax[6].set_xlim([0, 50])


plt.rc('font', size = 20)

os.chdir(path)
fig.savefig('bandes_freq_KMM005.pdf')
