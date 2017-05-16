from obspy import read
from obspy.signal.util import smooth
import numpy as np
import os
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

#normalisation
def norm1(vect):
    return [a/vect.max() for a in vect]

#path = '/localstorage/deleplanque'
path = '/Users/deleplanque/Documents'
path_data = path + '/Data/Kumamoto_sac/20160414224700'
path_plots = path + '/LaTeX/Poster_jpgu_2017'

list_sta = ['FKO0141604142247.EW.sac', 'FKO0141604142247.NS.sac', 'FKO0141604142247.UD.sac']

fig_brute, ax_brute = plt.subplots(3, 1)#, sharex = True)
ax_brute[2].set_xlabel('Time (s)')
ax_brute[1].set_ylabel('Amplitude')
ax_brute[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_brute[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_brute[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

fig_filtree, ax_filtree = plt.subplots(3, 1)#, sharex = True)
ax_filtree[2].set_xlabel('Time (s)')
ax_filtree[1].set_ylabel('Amplitude')
ax_filtree[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_filtree[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_filtree[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

fig_filt_sqr, ax_filt_sqr = plt.subplots(3, 1)#, sharex = True)
ax_filt_sqr[2].set_xlabel('Time (s)')
ax_filt_sqr[1].set_ylabel('Squared amplitude')
ax_filt_sqr[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_filt_sqr[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_filt_sqr[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

fig_env_norm, ax_env_norm = plt.subplots(3, 1)#, sharex = True)
ax_env_norm[2].set_xlabel('Time (s)')
ax_env_norm[1].set_ylabel('Normalized squared amplitude')
ax_env_norm[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_env_norm[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
ax_env_norm[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))

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
    #traces brute, filtree, au carre, smoothee
    ista = list_sta.index(station)
    ax_brute[ista].plot(t, tr_brut)#, aspect = 50)#, aspect = 50/(abs(1.1*tr_brut.max()) + abs(1.1*tr_brut.max())))
    ax_filtree[ista].plot(t, tr_filt)#, aspect = 50)#, aspect = 50/(abs(1.1*tr_filt.max()) + abs(1.1*tr_filt.max())))
    ax_filt_sqr[ista].plot(t, squared_tr)#, aspect = 50)#, aspect = 50/(abs(1.1*squared_tr.max()) + abs(1.1*squared_tr.max())))
    ax_env_norm[ista].plot(t, env_smoothed)#, aspect = 50)#, aspect = 50/(abs(1.1*env_smoothed.max()) + abs(1.1*env_smoothed.max())))

    if st[0].stats.channel == 'EW':
        ax_brute[ista].text(45, abs(tr_brut.max())/2, 'EW')
        ax_filtree[ista].text(45, abs(tr_filt.max())/2, 'EW')
        ax_filt_sqr[ista].text(45, max(squared_tr)/2, 'EW')
        ax_env_norm[ista].text(45, max(env_smoothed)/2, 'EW')
    elif st[0].stats.channel == 'NS':
        ax_brute[ista].text(45, abs(tr_brut.max())/2, 'NS')
        ax_filtree[ista].text(45, abs(tr_filt.max())/2, 'NS')
        ax_filt_sqr[ista].text(45, max(squared_tr)/2, 'NS')
        ax_env_norm[ista].text(45, max(env_smoothed)/2, 'NS')
    else:
        ax_brute[ista].text(45, abs(tr_brut.max())/2, 'UD')
        ax_filtree[ista].text(45, abs(tr_filt.max())/2, 'UD')
        ax_filt_sqr[ista].text(45, max(squared_tr)/2, 'UD')
        ax_env_norm[ista].text(45, max(env_smoothed)/2, 'UD')

os.chdir(path_plots)
#ax_brute.set_aspect('auto')
fig_brute.savefig('tr_brute.pdf')

#ax_filtree.set_aspect('auto')
fig_filtree.savefig('tr_filt.pdf')

#ax_filt_sqr.set_aspect('auto')
fig_filt_sqr.savefig('tr_filt_sqr.pdf')

#ax_env_norm.set_aspect('auto')
fig_env_norm.savefig('env_norm.pdf')
