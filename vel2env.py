from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
#from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_pth_dt = []
lst_pth_rslt = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz_3comp')
    lst_pth_rslt.append(path + '/' +dossier + '_vel_' + freq + 'Hz_3comp_env')
    if os.path.isdir(lst_pth_rslt[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt[lst_frq.index(freq)])

lst_fch = []

for pth in lst_pth_dt:
    lst_fch.append(os.listdir(pth))

for freq in lst_frq:
    print('     ', freq)
    for station in lst_fch[lst_frq.index(freq)]:
    	print('       ', station)
    	os.chdir(lst_pth_dt[lst_frq.index(freq)])
    	st = read(station)
    	tr = [a**2 for a in st[0].data]
    	tr = np.asarray(smooth(tr, 20))
    	tr = Trace(tr, st[0].stats)
    	os.chdir(lst_pth_rslt[lst_frq.index(freq)])
    	tr.write(station[:-4] + '_env.sac', format = 'SAC')





