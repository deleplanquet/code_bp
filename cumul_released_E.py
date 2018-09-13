from obspy import read
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt

print('')
print('      python3 cumul_released_E.py')

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']

path = path_origin + '/Kumamoto/' + dossier
path_data = (path + '/'
             + dossier + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz/'
             + dossier + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz_'
             + dt_type + '_env_smooth')
path_results_pdf = (path + '/'
                + dossier + '_results/'
                + dossier + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz/'
                + 'Cumulative_Energy_pdf')

path_results_png = (path + '/'
                    + dossier + '_results/'
                    + dossier + '_vel_'
                    + couronne + 'km_'
                    + frq + 'Hz/'
                    + 'Cumulative_Energy_png')

if os.path.isdir(path_results_pdf) == False:
    os.makedirs(path_results_pdf)

if os.path.isdir(path_results_png) == False:
    os.makedirs(path_results_png)

lst_fch = []
lst_fch = os.listdir(path_data)

for station in lst_fch:
    print(station)
    fig, ax = plt.subplots(1, 1)
    os.chdir(path_data)
    st = read(station)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    x = [0]
    i = 0
    while i < len(st[0].data) - 1:
        #print(i, st[0].data[i], st[0].data[i + 1], len(st[0].data))
        x.append(x[i] + st[0].data[i + 1])
        i = i + 1
    ax.plot(t, x, lw = 0.5)
    os.chdir(path_results_pdf)
    fig.savefig(station[:6] + '.pdf')
    os.chdir(path_results_png)
    fig.savefig(station[:6] + '.png')
