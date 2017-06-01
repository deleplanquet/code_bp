import pickle
import os

path = os.getcwd()[:-6]
path_data = path + '/Data'
#path_results = path + 

A = {}

os.chdir(path_data)
with open('ref_seismes.txt', 'r') as mon_fich:
    #contenu = mon_fich.read()
    for line in mon_fich:
        a = {}
        my_list = line.split()
        a['nFnet'] = my_list[1]
        a['Mw'] = my_list[2]
        a['Mj'] = my_list[3]
        a['lat'] = my_list[4]
        a['lon'] = my_list[5]
        a['dep'] = my_list[6]
        A[my_list[0]] = a

with open('ref_seismes_bin', 'wb') as ma_sortie:
    mon_pick = pickle.Pickler(ma_sortie)
    mon_pick.dump(A)


