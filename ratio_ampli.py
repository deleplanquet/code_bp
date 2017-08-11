import pickle
from obspy import read
import os
import sys

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data1 = path + '/' + dossier + '_vel_env_02_05Hz'
path_data2 = path + '/' + dossier + '_vel_env_05_1Hz'
path_data3 = path + '/' + dossier + '_vel_env_1_2Hz'
path_data4 = path + '/' + dossier + '_vel_env_2_4Hz'
path_data5 = path + '/' + dossier + '_vel_env_4_10Hz'

t_wd = 1
ampli = {}
lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_path = [path_data1, path_data2, path_data3, path_data4, path_data5]

for freq in range(5):
    os.chdir(lst_path[freq])
    list_fich = os.listdir(lst_path[freq])
    frq = {}
    for station in list_fich:
    	lst = []
    	st = read(station)
    	for i in range(int(50./t_wd)):
    	    clcl = 0
    	    for j in range(int(st[0].stats.sampling_rate*t_wd)):
    	    	clcl = clcl + st[0].data[int(i*t_wd*st[0].stats.sampling_rate) + j]/st[0].stats.sampling_rate
    	    lst.append(clcl)
    	frq[st[0].stats.station] = lst
    ampli[lst_frq[freq]] = frq

os.chdir(path)
with open(dossier + '_mat_vel_ampli_bin', 'wb') as ma_sortie:
    mon_pick = pickle.Pickler(ma_sortie)
    mon_pick.dump(ampli)





















