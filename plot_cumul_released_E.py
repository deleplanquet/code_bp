import matplotlib.pyplot as plt
import numpy as np
import os
from obspy import read
import pickle

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    seism = mdpck.load()

couronne = '0-100km'
freq = '2.0-8.0Hz'
print(seism.keys())
lst_pth_dat = []

for key in seism.keys():
    path = (path_origin + '/Kumamoto/' + key + '/'
            + key + '_vel_' + couronne + '_' + freq + '/'
            + key + '_vel_' + couronne + '_' + freq + '_hori_env_smooth_S')
    if os.path.isdir(path) == True and key[-1] == '0':
        lst_pth_dat.append(path)

dct_sta = {}

for pth in lst_pth_dat:
    lst_sta = os.listdir(pth)
    for sta in lst_sta:
        #print(sta[:6])
        if sta[:6] in dct_sta.keys():
            dct_sta[sta[:6]].append(pth)
        else:
            dct_sta[sta[:6]] = [pth]
            
pth_rslt = path_origin + '/Kumamoto/' + 'cumul_released_E'
pth_rslt_png = pth_rslt + '/plots_png'
pth_rslt_pdf = pth_rslt + '/plots_pdf'

if os.path.isdir(pth_rslt_png) == False:
    os.makedirs(pth_rslt_png)
if os.path.isdir(pth_rslt_pdf) == False:
    os.makedirs(pth_rslt_pdf)

#for sta in dct_sta.keys():
#    print(sta)
#    for pth in dct_sta[sta]:
#        print(pth)

dct_glob = {}

for sta in dct_sta.keys():
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Energy')
    dct_value = {}
    for pth in dct_sta[sta]:
        os.chdir(pth)
        st = read([a for a in os.listdir(pth) if sta in a][0])
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        x = [0]
        i = 0
        while i < len(st[0].data) - 1:
            x.append(x[i] + st[0].data[i + 1])
            i = i + 1
        ax.semilogy(t, x, lw = 0.5, label = pth[-54:-40] + '  Mw ' + str(seism[pth[-54:-40]]['Mw']))
        dct_value[pth[-54:-40]] = x[-1]
    ax.legend(fontsize = 5, loc = 4)
    os.chdir(pth_rslt_png)
    fig.savefig(sta + '.png')
    os.chdir(pth_rslt_pdf)
    fig.savefig(sta + '.pdf')
    dct_glob[sta] = dct_value

print(dct_glob)

os.chdir(path_origin + '/Kumamoto')
with open('max_E_values_bin', 'wb') as mfch:
    mdpck = pickle.Pickler(mfch)
    mdpck.dump(dct_glob)

