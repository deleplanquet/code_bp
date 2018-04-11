import pickle
import os

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto'

A = {}

os.chdir(path)
with open('seismicity.txt', 'r') as my_fch:
    for line in my_fch:
        a = {}
        my_list = line.split()
        a['year'] = float(my_list[0])
        a['month'] = float(my_list[1])
        a['day'] = float(my_list[2])
        a['hou'] = float(my_list[3])
        a['min'] = float(my_list[4])
        a['lon'] = float(my_list[6])
        a['lat'] = float(my_list[7])
        a['dep'] = float(my_list[8])
        a['Mj'] = float(my_list[9])
        A[my_list[0] + my_list[1] + my_list[2] + my_list[3] + my_list[4]] = a

with open('seismicity_bin', 'wb') as my_fch:
    my_pck = pickle.Pickler(my_fch)
    my_pck.dump(A)
