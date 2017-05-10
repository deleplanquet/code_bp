from obspy import read
from obspy.signal.util import smooth
import numpy as np
import os
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.pyplot as plt

#normalisation
def norm1(vect):
    norm_v = 0
    for a in vect:
        norm_v = norm_v + a*a
    return [a/pow(norm_v, 0.5) for a in vect]

path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/20160414224700'
path_plots = path + '/LaTeX/Poster_jpgu_2017'

list_sta = ['FKO0141604142247.EW.sac', 'FKO0141604142247.NS.sac', 'FKO0141604142247.UD.sac']

fig_brute, ax_brute = plt.subplots(3, sharex = True)
#ax_brute.set_xlabel('Time (s)')
#ax_brute.set_ylabel('Amplitude')
grid_brute = AxesGrid(fig_brute, 143, nrows_ncols = (1, 3), axes_pad = 0.1, label_mode = '1', share_all = True)

fig_filtree, ax_filtree = plt.subplots(3, sharex = True)
#ax_filtree.set_xlabel('Time (s)')
#ax_filtree.set_ylabel('Amplitude')
grid_filtree = AxesGrid(fig_filtree, 143, nrows_ncols = (1, 3), axes_pad = 0.1, label_mode = '1', share_all = True)

fig_filt_sqr, ax_filt_sqr = plt.subplots(3, sharex = True)
#ax_filt_sqr.set_xlabel('Time (s)')
#ax_filt_sqr.set_ylabel('Amplitude')
grid_filt_sqr = AxesGrid(fig_filt_sqr, 143, nrows_ncols = (1, 3), axes_pad = 0.1, label_mode = '1', share_all = True)

fig_env_norm, ax_env_norm = plt.subplots(3, sharex = True)
#ax_env_norm.set_xlabel('Time (s)')
#ax_env_norm.set_ylabel('Normalized amplitude')
grid_env_norm = AxesGrid(fig_env_norm, 143, nrows_ncols = (1, 3), axes_pad = 0.1, label_mode = '1', share_all = True)

os.chdir(path_data)
for station in list_sta:
    st = read(station)
    st.detrend(type = 'constant')
    tstart = st[0].stats.starttime + st[0].stats.sac.t0 - 15
    tend = tstart + 50
    st[0].trim(tstart, tend, pad=True, fill_value=0)
    tr_brut = st[0]
    tr_filt = tr_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
    squared_tr = [a**2 for a in tr_filt]
    env_smoothed = norm1(smooth(squared_tr, 20))

    t = np.arange(tr_brut.stats.npts)/tr_brut.stats.sampling_rate
    print('boubou')
    #traces brute, filtree, au carre, smoothee
    ista = list_sta.index(station)

    grid_brute[ista].plot(t, tr_brut)
    grid_filtree[ista].plot(t, tr_filt)
    grid_filt_sqr[ista].plot(t, squared_tr)
    grid_env_norm[ista].plot(t, env_smoothed)

os.chdir(path_plots)
print('baba')
#grid_brute.axes_llc.set_yticks([-2, 0, 2])
fig_brute.savefig('tr_brute.pdf')

#grid_filtree.axes_llc.set_yticks([-2, 0, 2])
fig_filtree.savefig('tr_filt.pdf')

#grid_filt_sqr.axes_llc.set_yticks([-2, 0, 2])
fig_filt_sqr.savefig('tr_filt_sqr.pdf')

#grid_env_norm.axes_llc.set_yticks([-2, 0, 2])
fig_env_norm.savefig('env_norm.pdf')



