from obspy import read
from obspy import Trace
import os
import sys

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt = []
lst_pth_rslt = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz_hori_env_S')
    lst_pth_rslt.append(path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz_hori_env_S_impulse')
    if os.path.isdir(lst_pth_rslt[lst_frq.index(freq)]) == False:
        os.makedirs(lst_pth_rslt[lst_frq.index(freq)])

lst_fch = []

for freq in lst_frq:
    lst_fch.append(os.listdir(lst_pth_dt[lst_frq.index(freq)]))

for freq in lst_frq:
    print('     ', freq)
    for station in lst_fch[lst_frq.index(freq)]:
        os.chdir(lst_pth_dt[lst_frq.index(freq)])
        st = read(station)
        tr = st[0].integrate(method = 'cumtrapz')
        fech = tr.stats.sampling_rate
        tS = tr.stats.sac.t0
        if (tr.data[int((tS + 5)*fech)] - tr.data[int(tS*fech)]) > 0.8*(tr.data[-1] - tr.data[int(tS*fech)]):
            st = read(station)
            os.chdir(lst_pth_rslt[lst_frq.index(freq)])
            tr = Trace(st[0].data, st[0].stats)
            tr.write(station, format = 'SAC')
