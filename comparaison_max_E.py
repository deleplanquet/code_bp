import pickle
import os
import numpy as np

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('max_E_values_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dct_val = mdpk.load()

with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    seism = mdpk.load()

#for key in dct_val.keys():
#    print(key)
#    for mw in dct_val[key].keys():
#        print(mw, dct_val[key][mw])

lst_seism = list(dct_val['KMM003'].keys())
lst_seism.append('20160417005900')
lst_sta = list(dct_val.keys())
lst_seism.sort()
lst_sta.sort()

print(lst_seism)

tab_val = np.zeros((len(lst_sta) + 1, len(lst_seism)))

for key in dct_val.keys():
    for mw in dct_val[key].keys():
        print(lst_sta.index(key))
        tab_val[lst_sta.index(key) + 1][lst_seism.index(mw)] = round(dct_val[key][mw], 3)

for seism in lst_seism:
    tab_val[0][lst_seism.index(seism)] = seism
#for sta in lst_sta:
#    tab_val[lst_sta.index(sta)][0] = sta

with open('max_E_values.txt', 'w') as mfch:
    for i in range(len(lst_sta)):
        tmp = ' '
        for k in range(len(lst_seism)):
            if lst_seism[k] in dct_val[lst_sta[i]].keys():
                tmp = tmp + ' ' + str(dct_val[lst_sta[i]][lst_seism[k]])
            else:
                tmp = tmp + ' 0'
        mfch.write(lst_sta[i] + tmp + '\n')

