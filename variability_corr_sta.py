import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

lst_doss = ['182042', '191752', '160125', '160355', '150003', '142126']
lst_doss = ['191752', '150003', '160125', '142126', '182042', '160355']
dst_doss = [0, 22.727, 27.159, 28.122, 74.027, 75.387]
for i in range(len(lst_doss)):
    lst_doss[i] = '201604' + lst_doss[i] + '00'

path_origin = os.getcwd()[:-6]

lst_sta = {}

for dossier in lst_doss:
    os.chdir(path_origin + '/Kumamoto/' + dossier)

    with open(dossier + '_veldata', 'rb') as my_fch:
        my_dpck = pickle.Unpickler(my_fch)
        corr_sta = my_dpck.load()

    corr_staS = corr_sta[1]

    for cles in corr_staS.keys():
        if cles in lst_sta:
            lst_sta[cles][dossier] = corr_staS[cles]
        else:
            lst_sta[cles] = {}
            lst_sta[cles][dossier] = corr_staS[cles]

fig, ax = plt.subplots(1, 1)

nbr_sta = 0

for keys in lst_sta.keys():
    nbr_sta = nbr_sta + 1
    if nbr_sta == 10:
        break
    vx = np.zeros(len(lst_doss))
    vy = np.zeros(len(lst_doss))
    vxx = []
    vyy = []
    for kkeys in lst_sta[keys].keys():
        vx[lst_doss.index(kkeys)] = dst_doss[lst_doss.index(kkeys)]
        vy[lst_doss.index(kkeys)] = nbr_sta*2 + lst_sta[keys][kkeys]
    for i in range(len(vy)):
        if vy[i] != 0:
            vxx.append(vx[i])
            vyy.append(vy[i])
    ax.plot(vxx, vyy, linewidth = 0.5)
    ax.axhline(nbr_sta*2, 0, 5, linewidth = 0.1, color = 'black')

os.chdir(path_origin + '/Kumamoto')
fig.savefig('variability_corrsta.pdf')
