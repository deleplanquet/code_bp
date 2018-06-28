from obspy import read
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from scipy.fftpack import fft

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

dossier = param['dossier']
couronne = '0-100'

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km')

path_factor = (path + '/'
               + dossier
               + '_brut')

path_results = (path + '/'
                + dossier
                + '_results/'
                + 'Frequency')

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

dict_factor = {}
os.chdir(path_factor)
with open('factor.txt', 'r') as mfch:
    for line in mfch:
        if 'UD1' not in line and 'NS1' not in line and 'EW1' not in line:
            if line[19:25] not in dict_factor.keys():
                dict_factor[str(line[19:25])] = float(line[-18:-14])/float(line[-8:-1])

lst_fch = os.listdir(path_data)
lst_fch_W = [a for a in lst_fch if ('EW' in a) == True]
lst_fch_N = [a for a in lst_fch if ('NS' in a) == True]
lst_fch_U = [a for a in lst_fch if ('UD' in a) == True]

lst_fch_W.sort()
lst_fch_N.sort()
lst_fch_U.sort()

for fichier in lst_fch_W:
    fig, ax = plt.subplots(2, 1)

    os.chdir(path_data)
    stW = read(fichier)
    stN = read(lst_fch_N[lst_fch_W.index(fichier)])
    stU = read(lst_fch_U[lst_fch_W.index(fichier)])

    t = np.arange(stW[0].stats.npts)/stW[0].stats.sampling_rate
    t0 = stU[0].stats.sac.t0
    N = stW[0].stats.npts
    T = 1./stW[0].stats.sampling_rate

    stW = np.asarray(stW)
    stN = np.asarray(stN)
    stU = np.asarray(stU)
    stW = stW*dict_factor[fichier[:6]]
    stN = stN*dict_factor[fichier[:6]]
    stU = stU*dict_factor[fichier[:6]]
    Wmin = min(stW[0].data)
    Wmax = max(stW[0].data)
    Nmin = min(stN[0].data)
    Nmax = max(stN[0].data)
    zero = - min(Wmin, Nmin)/(max(Wmax, Nmax) - min(Wmin, Nmin))

    ax[0].plot(t,
               stW[0].data,
               lw = 0.5,
               color = 'orangered',
               label = fichier[:6] + ' EW vel.')
    ax[0].plot(t,
               stN[0].data,
               lw = 0.5,
               color = 'dodgerblue',
               label = fichier[:6] + ' NS vel.')
    ax[0].axvline(5,
                  ymin = zero - 0.2,
                  ymax = zero + 0.2,
                  color = 'forestgreen')
    ax[0].axvline(t0,
                  ymin = zero - 0.2,
                  ymax = zero + 0.2,
                  color = 'darkorchid')

    ax[0].set_xlim([0, 50])
    ax[0].ticklabel_format(style = 'scientific',
                           axis = 'y',
                           scilimits = (0, 2))
    ax[0].legend(fontsize = 5,
                 loc = 3)
    ax[0].set_xlabel('Time (s)',
                     fontsize = 8)
    ax[0].set_ylabel('Velocity (cm/s)',
                     fontsize = 8)
    ax[0].xaxis.set_label_coords(0.5, -0.1)
    ax[0].yaxis.set_label_coords(-0.08, 0.5)
    ax[0].tick_params(labelsize = 8)
    ax[0].yaxis.offsetText.set_fontsize(8)

    fW = fft(stW[0].data)
    fN = fft(stN[0].data)
    xf = np.linspace(0., 1./(2.*T), N//2)
    ax[1].loglog(xf,
                 2./N*np.abs(fW[0:N//2]),
                 color = 'orangered',
                 lw = 0.5,
                 label = fichier[:6] + ' EW vel. fft.')
    ax[1].loglog(xf,
                 2./N*np.abs(fN[0:N//2]),
                 color = 'dodgerblue',
                 lw = 0.5,
                 label = fichier[:6] + ' NS vel. fft.')

    ax[1].set_xlim([0, 1./(2.*T)])
    ax[1].legend(fontsize = 5,
                 loc = 3)
    ax[1].set_xlabel('Frequency (Hz)',
                     fontsize = 8)
    ax[1].set_ylabel('Amplitude (cm)',
                     fontsize = 8)
    ax[1].xaxis.set_label_coords(0.5, -0.15)
    ax[1].yaxis.set_label_coords(-0.08, 0.5)
    ax[1].tick_params(labelsize = 8)

    os.chdir(path_results)
    fig.savefig(fichier[:6] + '_spectrum.pdf')
