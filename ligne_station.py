from obspy import read
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
from scipy.signal.util import smooth

path = '/Users/deleplanque/Documents/Data/Kumamoto_sac/20160415015900'
#path = '/Users/deleplanque/Documents/Data/Kumamoto_sac/20160417054100'
path_results = '/Users/deleplanque/Documents/Results'

os.chdir(path)

st1 = read('KMMH161604150159.UD2.sac')
st2 = read('KMMH031604150159.UD2.sac')
st3 = read('FKOH101604150159.UD2.sac')
#st1 = read('KMM0111604170541.UD.sac')
#st2 = read('MYZ0201604170541.UD.sac')
#st3 = read('MYZH081604170541.UD2.sac')
st1 = st1.detrend(type='constant')
st2 = st2.detrend(type='constant')
st3 = st3.detrend(type='constant')
tr1_brut = st1[0]
tr2_brut = st2[0]
tr3_brut = st3[0]
tr1_filt = tr1_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
tr2_filt = tr2_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
tr3_filt = tr3_brut.filter('bandpass', freqmin=0.2, freqmax=10, corners=4, zerophase=True)
envelop1 = abs(hilbert(tr1_filt))
envelop2 = abs(hilbert(tr2_filt))
envelop3 = abs(hilbert(tr3_filt))
env1_smoothed = smooth(envelop1, 20)
env2_smoothed = smooth(envelop2, 20)
env3_smoothed = smooth(envelop3, 20)

t1 = np.arange(tr1_brut.stats.npts)/tr1_brut.stats.sampling_rate
t2 = np.arange(tr2_brut.stats.npts)/tr2_brut.stats.sampling_rate
t3 = np.arange(tr3_brut.stats.npts)/tr3_brut.stats.sampling_rate

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time (s)')
ax.plt(t1, env1_smoothed, linewidth=0.2)
ax.plt(t2, env2_smoothed, linewidth=0.2)
ax.plt(t3, env3_smoothed, linewidth=0.2)

os.chdir(path_results)
fig.savefig('stationenligne.pdf')
