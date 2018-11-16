import matplotlib.pyplot as plt
from obspy import read
import os
import pickle
import numpy as np

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']

path = (path_origin + '/'
        + 'Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz')

lst_pth_dt = [path_data + '/'
              + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_patch_85_complementaire_bp_inv/'
              + 'smoothed_traces']

path_results = (path + '/'
                + dossier + '_results/'
                + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/'
                + 'Traces_bpinv_successives')

pth_rslt_png = path_results + '_png'
pth_rslt_pdf = path_results + '_pdf'

if os.path.isdir(pth_rslt_png) == False:
    os.makedirs(pth_rslt_png)
if os.path.isdir(pth_rslt_pdf) == False:
    os.makedirs(pth_rslt_pdf)

for i in range(17):
    lst_pth_dt.append(lst_pth_dt[i][:-38] + '_patch_85_complementaire_bp_inv/smoothed_traces')

lst_sta = os.listdir(lst_pth_dt[0])

for station in lst_sta:
    fig, ax = plt.subplots(1, 1)
    lab = 0
    vleft = 0
    vright = 50
    megamax = 0
    for succ in lst_pth_dt:
        os.chdir(succ)
        st = read(station)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax.plot(t,
                st[0].data,
                lw = 0.5,
                label = lab)

        cpt = 0
        tmp = 0

        while tmp == 0:
            if st[0].data[-cpt] > 0:
                tmp = 1
                print(lab, cpt)
            cpt = cpt + 1

        if lab == 0:
            megamax = max(st[0].data)
            cpt = 0
            tmp = 0
            while tmp == 0:
                if st[0].data[cpt] > 0:
                    tmp = 1
                    vleft = cpt/100
                cpt = cpt + 1
            cpt = 0
            tmp = 0
            while tmp == 0:
                if st[0].data[-cpt] > 0:
                    tmp = 1
                    vright = 50 - cpt/100
                cpt = cpt + 1

        lab = str(int(lab) + 1)

    ax.set_xlim([vleft - 6, vright + 1])
    ax.set_xlabel('Time(s)', fontsize = 8)
    ax.set_ylabel('Normalised energy', fontsize = 8)
    os.chdir(pth_rslt_png)
    fig.savefig(station + '.png')
    os.chdir(pth_rslt_pdf)
    fig.savefig(station + '.pdf')
