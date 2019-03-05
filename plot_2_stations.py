# plot deux stations l'une sous l'autre
# elles sont alignees sur l'arrivee P
# les arrivees P et S sont pointees
# on utilise les envelopes smoothees

from obspy import read
import os
import matplotlib.pyplot as plt
import numpy as np

dossier = '20160415173900'

pth_ori = os.getcwd()[:-6]
pth = (pth_ori + '/'
       + 'Kumamoto/'
       + dossier + '/'
       + dossier + '_vel_0-100km_2.0-8.0Hz/'
       + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env_smooth')

pth_rst = (pth_ori + '/'
           + 'Kumamoto/'
           + dossier + '/'
           + dossier + '_results')

fil_1 = 'KMM0181604151739.vel_0-100km_2.0-8.0Hz_hori_env_smooth.sac'
fil_2 = 'MYZ0071604151739.vel_0-100km_2.0-8.0Hz_hori_env_smooth.sac'

fig, ax = plt.subplots(2, 1)

os.chdir(pth)
for i, fil in enumerate([fil_1, fil_2]):
    st = read(fil)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    Emax = max(st[0].data)
    nrm_dat = [i/Emax for i in st[0].data]
    ax[i].plot(t, nrm_dat,
                 color = 'black', lw = '0.5')
    ax[i].set_xlim([0, 30])
    ax[i].set_ylim(bottom = 0)
    ax[i].arrow(5, 0.25,
                0, - 1./6,
                head_width = 30./100,
                head_length = 1./20,
                color = 'forestgreen')
    ax[i].arrow(st[0].stats.sac.t0, 0.25,
                0, - 1./6,
                head_width = 30./100,
                head_length = 1./20,
                color = 'darkorchid')

plt.subplots_adjust(hspace = 0.05)
ax[0].xaxis.set_visible(False)

os.chdir(pth_rst)
fig.savefig('Comparaison_KMM018-MYZ007_20160415173900.pdf')
