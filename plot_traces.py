


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







