import numpy as np
from obspy import read
import matplotlib.pyplot as plt
import sys
import os

def norm1(vect):
    return [0.1*a/vect.max() for a in vect]

def translate(vect, a):
    return [b + a for b in vect]

dossier = sys.argv[1]
dt_type = 'hori'

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_results'

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []
path_rslt = []

for freq in lst_frq:
    lst_pth_dt.append(path_data + '/' + dossier + '_vel_80-100km_' + freq + 'Hz_' + dt_type + '_env_smooth_S_2D_n=2/Traces')
    path_rslt.append(path_data + '/' + dossier + '_vel_80-100km_' + freq + 'Hz_' + dt_type + '_env_smooth_S_2D_n=2')

lst_fch_dt = []

for freq in lst_frq:
    lst_fch_dt.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

for freq in lst_frq:
    os.chdir(lst_pth_dt[lst_frq.index(freq)])
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Latitude')
    for fichier in lst_fch_dt[lst_frq.index(freq)]:
        st = read(fichier)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax.plot(t, translate(norm1(st[0].data), st[0].stats.sac.stla), lw = 0.2, color = 'black')
        ax.scatter(st[0].stats.sac.user1, st[0].stats.sac.stla, color = 'red')
        ax.scatter(st[0].stats.sac.user2, st[0].stats.sac.stla, color = 'darkorange')
        ax.scatter(st[0].stats.sac.user3, st[0].stats.sac.stla, color = 'yellow')

    ax.set_xlim([10, 25])
    os.chdir(path_rslt[lst_frq.index(freq)])
    fig.savefig('plot_traces_' + dossier + '.pdf')
