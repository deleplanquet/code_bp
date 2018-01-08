import pickle
import os

path = os.getcwd()[:-6]
path_data = path + '/Kumamoto'
#path_results = path + 

A = {}

os.chdir(path_data)
with open('ref_seismes.txt', 'r') as mon_fich:
    #contenu = mon_fich.read()
    for line in mon_fich:
        a = {}
        my_list = line.split()
        if (my_list[0] == 'Name') == False:
            a['nFnet'] = my_list[1]
            a['Mw'] = float(my_list[2])
            a['Mj'] = float(my_list[3])
            a['lat'] = float(my_list[4])
            a['lon'] = float(my_list[5])
            a['dep'] = float(my_list[6])
            a['str1'] = float(my_list[7])
            a['dip1'] = float(my_list[8])
            a['rak1'] = float(my_list[9])
            a['str2'] = float(my_list[10])
            a['dip2'] = float(my_list[11])
            a['rak2'] = float(my_list[12])
            A[my_list[0]] = a

with open('ref_seismes_bin', 'wb') as ma_sortie:
    mon_pick = pickle.Pickler(ma_sortie)
    mon_pick.dump(A)


