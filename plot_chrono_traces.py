from obspy import read
import os
from obspy.signal.util import smooth
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]

dossier = '20160415173900'

path = path_origin + '/Kumamoto/' + dossier

path_data_1 = path + '/' + dossier + '_sac_inf100km'
path_data_2 = path + '/' + dossier + '_vel_0-100km'
path_data_3 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz'
path_data_4 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env'

fig, ax = plt.subplots(5, 1)

os.chdir(path_data_1)
st1 = read('KMM0181604151739.NS.sac')
st1.detrend(type = 'constant')
t1 = np.arange(st1[0].stats.npts)/st1[0].stats.sampling_rate

os.chdir(path_data_2)
st2 = read('KMM0181604151739.NS_vel_0-100km.sac')
t2 = np.arange(st2[0].stats.npts)/st2[0].stats.sampling_rate

os.chdir(path_data_3)
st3 = read('KMM0181604151739.NS_vel_0-100km-2.0-8.0Hz.sac')
t3 = np.arange(st3[0].stats.npts)/st3[0].stats.sampling_rate

os.chdir(path_data_4)
st4 = read('KMM0181604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')
t4 = np.arange(st4[0].stats.npts)/st4[0].stats.sampling_rate

dat5 = smooth(st4[0].data, int(0.1/st4[0].stats.delta))

ax[0].plot(t1, st1[0],
           color = 'black',
           lw = 0.5)
ax[0].set_xlim([3.8, 3.8 + 50])
#ax[0].set_ylim([-3e3, 4e3])
ax[1].plot(t2, st2[0],
           color = 'black',
           lw = 0.5)
ax[1].set_xlim([0, 50])
#ax[1].set_ylim([-3e5, 4e5])
ax[2].plot(t3, st3[0],
           color = 'black',
           lw = 0.5)
ax[2].set_xlim([0, 50])
#ax[2].set_ylim([-3e5, 4e5])
ax[3].plot(t4, st4[0],
           color = 'black',
           lw = 0.5)
ax[3].set_xlim([0, 50])
ax[3].set_ylim(bottom = 0)
#ax[3].set_ylim([0, 1e11])
ax[4].plot(t4, dat5,
           color = 'black',
           lw = 0.5)
ax[4].set_xlim([0, 50])
ax[4].set_ylim(bottom = 0)
#ax[4].set_ylim([0, 1e11])

plt.subplots_adjust(hspace = 0.1)
ax[0].xaxis.set_visible(False)
ax[1].xaxis.set_visible(False)
ax[2].xaxis.set_visible(False)
ax[3].xaxis.set_visible(False)
#ax[4].xaxis.set_visible(False)

#ax[0].yaxis.set_visible(False)
#ax[1].yaxis.set_visible(False)
#ax[2].yaxis.set_visible(False)
#ax[3].yaxis.set_visible(False)
#ax[4].yaxis.set_visible(False)

ax[0].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[1].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[2].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[3].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[4].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))

ax[0].yaxis.set_label_position('right')
ax[1].yaxis.set_label_position('right')
ax[2].yaxis.set_label_position('right')
ax[3].yaxis.set_label_position('right')
ax[4].yaxis.set_label_position('right')

offset1 = ax[0].yaxis.get_major_formatter().get_offset()
print(offset1)
ax[0].text(53.6, 0.8*max(st1[0].data), offset1, fontsize = 8, ha = 'right')
ax[1].text(49.8, 0.8*max(st2[0].data), '1e5', fontsize = 8, ha = 'right')
ax[2].text(49.8, 0.8*max(st3[0].data), '1e5', fontsize = 8, ha = 'right')
ax[3].text(49.8, 0.9*max(st4[0].data), '1e11', fontsize = 8, ha = 'right')
ax[4].text(49.8, 0.9*max(dat5), '1e10', fontsize = 8, ha = 'right')

ax[0].tick_params(labelsize = 8)
ax[1].tick_params(labelsize = 8)
ax[2].tick_params(labelsize = 8)
ax[3].tick_params(labelsize = 8)
ax[4].tick_params(labelsize = 8)

ax[0].yaxis.offsetText.set_fontsize(8)
ax[1].yaxis.offsetText.set_fontsize(8)
ax[2].yaxis.offsetText.set_fontsize(8)
ax[3].yaxis.offsetText.set_fontsize(8)
ax[4].yaxis.offsetText.set_fontsize(8)

#ax[0].yaxis.set_offset_position('right')
#ax[1].yaxis.set_offset_position('right')
#ax[2].yaxis.set_offset_position('right')
#ax[3].yaxis.set_offset_position('right')
#ax[4].yaxis.set_offset_position('right')

ax[4].set_xlabel('Time (s)',
                 fontsize = 8)
ax[0].set_ylabel('Acceleration\n(cm/s/s)',
                 fontsize = 8)
ax[1].set_ylabel('Velocity\n(cm/s)',
                 fontsize = 8)
ax[2].set_ylabel('2 to 8 Hz\nvelocity\n(cm/s)',
                 fontsize = 8)
ax[3].set_ylabel('Envelope\n(cm*cm/s/s)',
                 fontsize = 8)
ax[4].set_ylabel('Smoothed\nenvelope\n(cm*cm/s/s)',
                 fontsize = 8)

os.chdir(path)
fig.savefig(dossier + '_chrono.pdf')

fig2, ax2 = plt.subplots(2, 1)

os.chdir(path_data_4)
sta = read('MYZ0071604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')

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
