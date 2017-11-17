import pickle
import os
import matplotlib.pyplot as plt

lst_doss = ['182042', '191752', '160125', '160355', '150003', '142126']
for i in range(len(dossier)):
    lst_doss[i] = '201604' + lst_doss[i] + '00'

path_origin = os.getcwd()[:-6]

lst_sta = {}

for dossier in lst_doss:
    os.chdir(path_origin + '/Kumamoto/' + dossier)

    with open(dossier + '_veldata', 'rb') as my_fch:
        my_dpck = pickle.Unpickler(my_fch)
        corr_sta = my_dpck.load()

    corr_staS = corr_sta[1]

    for cles in corr_staS.key():
        if cles in lst_sta:
            lst_sta[cles][dossier] = corr_staS[cles]
        else:
            lst_sta[cles] = {}
            lst_sta[cles][dossier] = corr_staS[cles]

fig, ax = plt.subplots(1, 1)

nbr_sta = 0

for keys in lst_sta.keys():
    nbr_sta = nbr_sta + 1
    for kkeys in lst_sta[keys].keys():
        if kkeys == dossier[0]:
            xx = 4
        elif kkeys == dossier[1]:
            xx = 0
        elif kkeys == dossier[2]:
            xx = 2
        elif kkeys == dossier[3]:
            xx = 5
        elif kkeys == dossier[4]:
            xx = 1
        elif kkeys == dossier[5]:
            xx = 3
        yy = nbr_sta * 2 + lst_sta[keys][kkeys]
        ax.scatter(xx, yy, 20, marker = 'o', color = 'black')

fig.savefig('variability_corrsta.pdf')
