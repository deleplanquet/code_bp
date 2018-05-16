import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from obspy import read

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    param = mdpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz')

lst_pth_dat = [path_data + '/'
               + dossier
               + '_vel_'
               + couronne + 'km_'
               + frq + 'Hz_'
               + dt_type
               + '_env_smooth_'
               + hyp_bp + '_'
               + azim + 'deg']

lst_sta = [os.listdir(lst_pth_dat[0])]
lst_sta[0].sort()
lst_clr = ['yellow', 'orange', 'red', 'blue']

for i in range(1):
    lst_pth_dat.append(lst_pth_dat[i]
                       + '_patch_90')

for i in range(1):
    lst_pth_dat[i + 1] = lst_pth_dat[i + 1] + '_complementaire'
    lst_sta.append(os.listdir(lst_pth_dat[i+1]))
    lst_sta[i+1].sort()

path_results = (path + '/'
                + dossier
                + '_results/'
                + dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz/'
                + 'Traces_modifiees_comparison')

pth_pdf = (path_results + '/'
           + 'pdf')

pth_png = (path_results + '/'
           + 'png')

if os.path.isdir(pth_pdf) == False:
    os.makedirs(pth_pdf)
if os.path.isdir(pth_png) == False:
    os.makedirs(pth_png)

for station in lst_sta[0]:
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Energy')
    st = []
    for chemin in lst_pth_dat:
        os.chdir(chemin)
        st.append(read(lst_sta[lst_pth_dat.index(chemin)][lst_sta[0].index(station)]))

    t = np.arange(st[0][0].stats.npts)/st[0][0].stats.sampling_rate

    for elt in st:
        ax.fill_between(t,
                        0,
                        elt[0].data,
                        linewidth = 0.2,
                        color = lst_clr[st.index(elt)])

    os.chdir(pth_png)
    fig.savefig(station[:-4] + '.png')
    os.chdir(pth_pdf)
    fig.savefig(station[:-4] + '.pdf')







