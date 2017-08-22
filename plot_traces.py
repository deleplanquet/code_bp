


import numpy as np
from obspy import read
import matplotlib.pyplot as plt
import sys
import os

dossier = sys.argv[1]
station = sys.argv[2] + dossier[2:-2]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_sac = path + '/' + dossier + '_sac_inf100km'
path_vel = path + '/' + dossier + '_vel'

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_pth_vel_frq = []
lst_pth_vel_frq_3cp = []
lst_pth_vel_frq_hor = []
lst_pth_vel_frq_ver = []
lst_pth_vel_frq_3cp_env = []
lst_pth_vel_frq_hor_env = []
lst_pth_vel_frq_ver_env = []

for freq in lst_frq:
    lst_pth_vel_frq.append(path + '/' + dossier + '_vel_' + freq + 'Hz')
    lst_pth_vel_frq_3cp.append(path + '/' + dossier + '_vel_' + freq + 'Hz_3comp')
    lst_pth_vel_frq_hor.append(path + '/' + dossier + '_vel_' + freq + 'Hz_hori')
    lst_pth_vel_frq_ver.append(path + '/' + dossier + '_vel_' + freq + 'Hz_vert')
    lst_pth_vel_frq_3cp_env.append(path + '/' + dossier + '_vel_' + freq + 'Hz_3comp_env')
    lst_pth_vel_frq_hor_env.append(path + '/' + dossier + '_vel_' + freq + 'Hz_hori_env')
    lst_pth_vel_frq_ver_env.append(path + '/' + dossier + '_vel_' + freq + 'Hz_vert_env')

fig, ax = plt.subplots(9, 7, sharex = 'col', sharey = 'row')



os.chdir(path_sac)
st = read(station + '.EW.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[0, 0].plot(st[0].data, lw = 0.5)
st = read(station + '.NS.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[1, 0].plot(st[0].data, lw = 0.5)
st = read(station + '.UD.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[2, 0].plot(st[0].data, lw = 0.5)

os.chdir(path_vel)
st = read(station + '.EW_vel.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[0, 1].plot(st[0].data, lw = 0.5)
st = read(station + '.NS_vel.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[1, 1].plot(st[0].data, lw = 0.5)
st = read(station + '.UD_vel.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax[2, 1].plot(st[0].data, lw = 0.5)

for freq in lst_frq:
    os.chdir(lst_pth_vel_frq[lst_frq.index(freq)])
    st = read(station + '.EW_vel_' + freq + 'Hz.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[0, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    st = read(station + '.NS_vel_' + freq + 'Hz.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[1, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    st = read(station + '.UD_vel_' + freq + 'Hz.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[2, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)

    os.chdir(lst_pth_vel_frq_3cp[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[3, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_hor[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_hori.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[5, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_ver[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_vert.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[7, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_3cp_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[4, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[6, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_ver_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_vert_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[8, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)


os.chdir(path)
fig.savefig('tttraces.pdf')

fig2, ax2 = plt.subplots(3, 1, sharex = 'col')
ax2[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax2[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax2[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
os.chdir(path_sac)
st = read(station + '.EW.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax2[0].plot(t, st[0].data, lw = 0.5)
st = read(station + '.NS.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax2[1].plot(t, st[0].data, lw = 0.5)
st = read(station + '.UD.sac')
t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
ax2[2].plot(t, st[0].data, lw = 0.5)
os.chdir(path)
fig2.savefig('accelero.pdf')
fig2.savefig('accelero.png')

fig3, ax3 = plt.subplots(5, 1, sharex = 'col')
ax3[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax3[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax3[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax3[3].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax3[4].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
for freq in lst_frq:
    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax3[lst_frq.index(freq)].plot(t, st[0].data, lw = 0.5)
os.chdir(path)
fig3.savefig('envfreq.pdf')
fig3.savefig('envfreq.png')

fig4, ax4 = plt.subplots(5, 1, sharex = 'col', sharey = 'all')
ax4[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax4[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax4[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax4[3].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax4[4].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
for freq in lst_frq:
    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax4[lst_frq.index(freq)].plot(t, st[0].data, lw = 0.5)
os.chdir(path)
fig4.savefig('envfreqmmax.pdf')
fig4.savefig('envfreqmmax.png')

fig5, ax5 = plt.subplots(3, 3, sharex = 'col')
ax5[0, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[0, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[0, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[1, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[1, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[1, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[2, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[2, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax5[2, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
for freq in lst_frq[2:]:
    os.chdir(lst_pth_vel_frq_3cp_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax5[0, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax5[1, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
    os.chdir(lst_pth_vel_frq_ver_env[lst_frq.index(freq)])
    st = read(station + '.vel_' + freq + 'Hz_vert_env.sac')
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax5[2, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
os.chdir(path)
fig5.savefig('composition.pdf')
fig5.savefig('composition.png')




















