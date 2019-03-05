from obspy import read
import os
from obspy.signal.util import smooth
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]

#dossier = '20160401000001'
dossier = '20160415173900'

path = path_origin + '/Kumamoto/' + dossier

path_data_1 = path + '/' + dossier + '_sac_inf100km'
path_data_2 = path + '/' + dossier + '_vel_0-100km'
path_data_3 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz'
path_data_4 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env'

#path_data_1 = path + '/' + dossier + '_sac_inf100km_picks-save'
#path_data_int = path + '/' + 'noise_03'
#path_data_2 = path_data_int + '/' + dossier + '_vel_0-100km'
#path_data_3 = path_data_int + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz'
#path_data_4 = path_data_int + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env'

fig, ax = plt.subplots(6, 1)

os.chdir(path_data_1)
st1 = read('KMM0181604151739.NS.sac')
#st1 = read('KMM006.NS.sac')
#st1 = read('KMM018.NS.sac')
st1.detrend(type = 'constant')
t1 = np.arange(st1[0].stats.npts)/st1[0].stats.sampling_rate
st1_max = max(st1[0].data)
st1_min = min(st1[0].data)

st6 = read('KMM0181604151739.EW.sac')
st6.detrend(type = 'constant')
t6 = np.arange(st6[0].stats.npts)/st6[0].stats.sampling_rate
st6_max = max(st6[0].data)
st6_min = min(st6[0].data)

os.chdir(path_data_2)
st2 = read('KMM0181604151739.NS_vel_0-100km.sac')
#st2 = read('KMM006_NS_20160401000001_vel_0-100km.sac')
#st2 = read('KMM018_NS_20160401000001_vel_0-100km.sac')
t2 = np.arange(st2[0].stats.npts)/st2[0].stats.sampling_rate
st2_max = max(st2[0].data)
st2_min = min(st2[0].data)

os.chdir(path_data_3)
st3 = read('KMM0181604151739.NS_vel_0-100km-2.0-8.0Hz.sac')
#st3 = read('KMM006_NS_20160401000001_vel_0-100km_2.0-8.0Hz.sac')
#st3 = read('KMM018_NS_20160401000001_vel_0-100km_2.0-8.0Hz.sac')
t3 = np.arange(st3[0].stats.npts)/st3[0].stats.sampling_rate
st3_max = max(st3[0].data)
st3_min = min(st3[0].data)

os.chdir(path_data_4)
st4 = read('KMM0181604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')
#st4 = read('KMM00620160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')
#st4 = read('KMM01820160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')
t4 = np.arange(st4[0].stats.npts)/st4[0].stats.sampling_rate
st4_max = max(st4[0].data)
st4_min = min(st4[0].data)

dat5 = smooth(st4[0].data, int(0.1/st4[0].stats.delta))
st5_max = max(dat5)
st5_min = min(dat5)

ax[0].plot(t1, st1[0],
           color = 'black',
           lw = 0.5)
ax[0].set_xlim([3.9, 3.9 + 30])
ax[0].set_ylim([st1_min - 0.05*(st1_max - st1_min), st1_max + 0.05*(st1_max - st1_min)])
ax[1].plot(t6, st6[0],
           color = 'black',
           lw = 0.5)
ax[1].set_xlim([3.9, 3.9 + 30])
ax[1].set_ylim([st6_min - 0.05*(st6_max - st6_min), st6_max + 0.05*(st6_max - st6_min)])
ax[2].plot(t2, st2[0],
           color = 'black',
           lw = 0.5)
ax[2].set_xlim([0, 30])
ax[2].set_ylim([st2_min - 0.05*(st2_max - st2_min), st2_max + 0.05*(st2_max - st2_min)])
ax[3].plot(t3, st3[0],
           color = 'black',
           lw = 0.5)
ax[3].set_xlim([0, 30])
ax[3].set_ylim([st3_min - 0.05*(st3_max - st3_min), st3_max + 0.05*(st3_max - st3_min)])
ax[4].plot(t4, st4[0],
           color = 'black',
           lw = 0.5)
ax[4].set_xlim([0, 30])
ax[4].set_ylim(bottom = 0)
ax[4].set_ylim([0, st4_max + 0.1*st4_max])
ax[5].plot(t4, dat5,
           color = 'black',
           lw = 0.5)
ax[5].set_xlim([0, 30])
ax[5].set_ylim(bottom = 0)
ax[5].set_ylim([0, st5_max + 0.1*st5_max])

plt.subplots_adjust(hspace = 0.1)
ax[0].xaxis.set_visible(False)
ax[1].xaxis.set_visible(False)
ax[2].xaxis.set_visible(False)
ax[3].xaxis.set_visible(False)
ax[4].xaxis.set_visible(False)
#ax[5].xaxis.set_visible(False)

#ax[0].yaxis.set_visible(False)
#ax[1].yaxis.set_visible(False)
#ax[2].yaxis.set_visible(False)
#ax[3].yaxis.set_visible(False)
#ax[4].yaxis.set_visible(False)
#ax[5].yaxis.set_visible(False)

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
ax[5].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))

ax[0].yaxis.set_label_position('right')
ax[1].yaxis.set_label_position('right')
ax[2].yaxis.set_label_position('right')
ax[3].yaxis.set_label_position('right')
ax[4].yaxis.set_label_position('right')
ax[5].yaxis.set_label_position('right')

ax[0].yaxis.offsetText.set_visible(False)
offset0 = ax[0].yaxis.get_major_formatter().get_offset()
print(offset0)
ax[0].text(4, st1_max, '1e3', fontsize = 8, va = 'top')
ax[1].yaxis.offsetText.set_visible(False)
offset1 = ax[1].yaxis.get_major_formatter().get_offset()
ax[1].text(4, st6_max, '1e4', fontsize = 8, va = 'top')
ax[2].yaxis.offsetText.set_visible(False)
offset2 = ax[2].yaxis.get_offset_text()
ax[2].text(0.2, st2_max, '1e5', fontsize = 8, va = 'top')
ax[3].yaxis.offsetText.set_visible(False)
offset3 = ax[3].yaxis.get_offset_text()
ax[3].text(0.2, st3_max, '1e5', fontsize = 8, va = 'top')
ax[4].yaxis.offsetText.set_visible(False)
offset4 = ax[4].yaxis.get_offset_text()
ax[4].text(0.2, st4_max, '1e11', fontsize = 8, va = 'top')
ax[5].yaxis.offsetText.set_visible(False)
offset5 = ax[5].yaxis.get_offset_text()
ax[5].text(0.2, st5_max, '1e10', fontsize = 8, va = 'top')

ax[0].tick_params(labelsize = 8)
ax[1].tick_params(labelsize = 8)
ax[2].tick_params(labelsize = 8)
ax[3].tick_params(labelsize = 8)
ax[4].tick_params(labelsize = 8)
ax[5].tick_params(labelsize = 8)

ax[0].yaxis.offsetText.set_fontsize(8)
ax[1].yaxis.offsetText.set_fontsize(8)
ax[2].yaxis.offsetText.set_fontsize(8)
ax[3].yaxis.offsetText.set_fontsize(8)
ax[4].yaxis.offsetText.set_fontsize(8)
ax[5].yaxis.offsetText.set_fontsize(8)

#ax[0].yaxis.set_offset_position('right')
#ax[1].yaxis.set_offset_position('right')
#ax[2].yaxis.set_offset_position('right')
#ax[3].yaxis.set_offset_position('right')
#ax[4].yaxis.set_offset_position('right')

ax[5].set_xlabel('Time (s)',
                 fontsize = 8)
ax[0].set_ylabel('Acceleration\nNS (cm/s/s)',
                 fontsize = 7)
ax[1].set_ylabel('Acceleration\nEW (cm/s/s)',
                 fontsize = 7)
ax[2].set_ylabel('Velocity\n(cm/s)',
                 fontsize = 7)
ax[3].set_ylabel('2 to 8 Hz\nvelocity\n(cm/s)',
                 fontsize = 7)
ax[4].set_ylabel('Envelope\n(cm*cm/s/s)',
                 fontsize = 7)
ax[5].set_ylabel('Smoothed\nenvelope\n(cm*cm/s/s)',
                 fontsize = 7)

os.chdir(path)
fig.savefig(dossier + '_chrono.pdf')

fig2, ax2 = plt.subplots(2, 1)

os.chdir(path_data_4)
#sta = read('MYZ0071604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')
#sta = read('MYZ00720160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')

#data = smooth(sta[0].data, int(0.5/sta[0].stats.delta))

#ax2[0].plot(t4, dat5)
#ax2[1].plot(t4, data)

#plt.subplots_adjust(hspace = 0.001)
#ax2[0].xaxis.set_visible(False)
#ax2[1].xaxis.set_visible(False)

#ax2[0].yaxis.set_visible(False)
#ax2[1].yaxis.set_visible(False)

#os.chdir(path)
#fig2.savefig(dossier + '_comparaison_SP.pdf')
