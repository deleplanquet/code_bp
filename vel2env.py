from obspy import read
from obspy import Trace
from obspy.signal.util import smooth
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
lst_pth_dt3 = []
lst_pth_dth = []
lst_pth_dtv = []
lst_pth_rslt3 = []
lst_pth_rslth = []
lst_pth_rsltv = []

for freq in lst_frq:
    pth_dt = path + '/' + dossier + '_vel_' + freq + 'Hz/' + dossier + '_vel_' + freq + 'Hz'
    lst_pth_dt3.append(pth_dt + '_3comp')
    lst_pth_dth.append(pth_dt + '_hori')
    lst_pth_dtv.append(pth_dt + '_vert')
    lst_pth_rslt3.append(pth_dt + '_3comp_env')
    lst_pth_rslth.append(pth_dt + '_hori_env')
    lst_pth_rsltv.append(pth_dt + '_vert_env')

    if os.path.isdir(lst_pth_rslt3[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt3[lst_frq.index(freq)])
    if os.path.isdir(lst_pth_rslth[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslth[lst_frq.index(freq)])
    if os.path.isdir(lst_pth_rsltv[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rsltv[lst_frq.index(freq)])

lst_fch_3 = []
lst_fch_h = []
lst_fch_v = []

for pth in lst_pth_dt3:
    lst_fch_3.append(os.listdir(pth))
for pth in lst_pth_dth:
    lst_fch_h.append(os.listdir(pth))
for pth in lst_pth_dtv:
    lst_fch_v.append(os.listdir(pth))

for freq in lst_frq:
    print('     ', freq)
    for station in lst_fch_3[lst_frq.index(freq)]:
    	os.chdir(lst_pth_dt3[lst_frq.index(freq)])
    	st = read(station)
    	tr = [a**2 for a in st[0].data]
    	tr = Trace(np.asarray(tr), st[0].stats)
    	os.chdir(lst_pth_rslt3[lst_frq.index(freq)])
    	tr.write(station[:-4] + '_env.sac', format = 'SAC')

    for station in lst_fch_h[lst_frq.index(freq)]:
    	os.chdir(lst_pth_dth[lst_frq.index(freq)])
    	st = read(station)
    	tr = [a**2 for a in st[0].data]
    	tr = Trace(np.asarray(tr), st[0].stats)
    	os.chdir(lst_pth_rslth[lst_frq.index(freq)])
    	tr.write(station[:-4] + '_env.sac', format = 'SAC')

    for station in lst_fch_v[lst_frq.index(freq)]:
    	os.chdir(lst_pth_dtv[lst_frq.index(freq)])
    	st = read(station)
    	tr = [a**2 for a in st[0].data]
    	tr = Trace(np.asarray(tr), st[0].stats)
    	os.chdir(lst_pth_rsltv[lst_frq.index(freq)])
    	tr.write(station[:-4] + '_env.sac', format = 'SAC')

