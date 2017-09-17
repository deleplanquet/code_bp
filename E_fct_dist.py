import matplotlib.pyplot as plt
import sys
import os
from obspy import read


dossier = sys.argv[1]
dt_type = sys.argv[2]
select_station = sys.argv[3]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_results = path + '/' + dossier + '_results'

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []

for freq in lst_frq:
    pth_dt = path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz'
    lst_pth_dt.append(pth_dt + '_' + dt_type + '_env_smooth_' + select_station + '_impulse')

lst_pth_fch = []

for freq in lst_frq:
    lst_pth_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

for freq in lst_frq:
    os.chdir(lst_pth_dt[lst_frq.index(freq)])
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Energy')
    for fichier in lst_pth_fch[lst_frq.index(freq)]:
        st = read(fichier)
        tr = st[0].integrate(method = 'cumtrapz')
        ax.scatter(st[0].stats.sac.dist, tr[-1])
    ax.set_yscale('log')
        
    os.chdir(path_results)
    fig.savefig('E_fct_dist_' + dossier + '_vel_' + freq + '_Hz_' + dt_type + '_env_smooth_' + select_station + '_impulse.pdf')
