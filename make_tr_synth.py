import pickle
import math
import numpy as np
from obspy import Trace
from obspy import read
import os

def d2r(angle):
    return angle*math.pi/180

def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

def dist(v1, v2):
    x1, y1, z1 = geo2cart(v1)
    x2, y2, z2 = geo2cart(v2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/'

lst_EQ = ['20160419222600', '20160415173900', '20160416215000', '20160417005900']
lst_pos_hyp = [[6390.68, 32.5613, 130.6495], [6388.03, 32.8408, 130.8845], [6388.3, 32.9650, 131.0658], [6390.87, 33.0128, 131.2022]]
lst_pth_dt = []

for EQ in lst_EQ:
    lst_pth_dt.append(path + EQ + '/' + EQ + '_vel_4_10Hz_hori')
    print(len(lst_pth_dt[lst_EQ.index(EQ)]))

path_results = path + 'syn/ligne'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = []

for pth in lst_pth_dt:
    lst_fch.append(os.listdir(pth))
    lst_fch[lst_pth_dt.index(pth)].sort()
    print(len(lst_fch[lst_pth_dt.index(pth)]))

lst_sta = []

for pth in lst_pth_dt:
    for fch in lst_fch[lst_pth_dt.index(pth)]:
    	if (lst_fch[lst_pth_dt.index(pth)][lst_fch[lst_pth_dt.index(pth)].index(fch)][:6] in lst_sta) == False:
    	    lst_sta.append([lst_fch[lst_pth_dt.index(pth)][lst_fch[lst_pth_dt.index(pth)].index(fch)][:6]])

print(len(lst_sta))

lst_sta_db = []

for pth in lst_pth_dt:
    for fch in lst_fch[lst_pth_dt.index(pth)]:
    	lst_sta_db.append([lst_fch[lst_pth_dt.index(pth)][lst_fch[lst_pth_dt.index(pth)].index(fch)][:6], fch])

print(len(lst_sta_db))
print(lst_sta_db)

for ista in lst_sta_db:
    for sta in lst_sta:
    	if ista[0] == sta[0]:
    	    lst_sta[lst_sta.index(sta)].append(ista[1])

os.chdir(path + lst_EQ[0])
with open(lst_EQ[0] + '_veldata', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_vel = my_dpck.load()

dict_vel_used = dict_vel[1]
dict_delai = dict_vel[2]

for sta in lst_sta:
#    if len(sta) == 2:
#    	print(len(sta), 'boubou')
#    	os.chdir(lst_pth_dt[lst_EQ.index('20' + sta[1][6:16] + '00')])
#    	st = read(sta[1])
#    	tr = Trace(st[0].data, st[0].stats)
#    	os.chdir(path_results)
#    	tr.write(sta[1][:6] + sta[1][16:], format = 'SAC')
#    else:
#    	print(len(sta))
#    	lst_st = []
#    	lst_dist = []
#    	for seism in sta[1:]:
#    	    pos_hyp = lst_pos_hyp[lst_EQ.index('20' + sta[sta.index(seism)][6:16] + '00')]
#    	    os.chdir(lst_pth_dt[lst_EQ.index('20' + sta[sta.index(seism)][6:16] + '00')])
#    	    lst_st.append(read(sta[sta.index(seism)]))
#    	    st1 = lst_st[sta.index(seism) - 1]
#    	    pos_sta = [6400 + 0.001*st1[0].stats.sac.stel, st1[0].stats.sac.stla, st1[0].stats.sac.stlo]
#    	    lst_dist.append(dist(pos_sta, pos_hyp))
#    	print(lst_dist)
#    	mdist = min(lst_dist)
#    	for dst in lst_dist:
#    	    lst_dist[lst_dist.index(dst)] = lst_dist[lst_dist.index(dst)] - mdist
#    	print(lst_dist)
#    	tr = [a for a in lst_st[lst_dist.index(0)][0].data]
#    	for st in lst_st:
#    	    if lst_dist[lst_st.index(st)] != 0:
#    	    	i0 = int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate)
#    	    	for itr in tr[int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate):]:
#    	    	    tr[tr.index(itr)] = itr + st[0].data[tr.index(itr) - i0]
#    	tr = Trace(np.asarray(tr), lst_st[lst_dist.index(0)][0].stats)
#    	os.chdir(path_results)
#    	tr.write(sta[1][:6] + sta[1][16:], format = 'SAC')


    print(len(sta))
    lst_st = []
    lst_dist = []
    for seism in sta[1:]:
    	pos_hyp = lst_pos_hyp[lst_EQ.index('20' + sta[sta.index(seism)][6:16] + '00')]
    	os.chdir(lst_pth_dt[lst_EQ.index('20' + sta[sta.index(seism)][6:16] + '00')])
    	lst_st.append(read(sta[sta.index(seism)]))
    	st1 = lst_st[sta.index(seism) - 1]
    	pos_sta = [6400 + 0.001*st1[0].stats.sac.stel, st1[0].stats.sac.stla, st1[0].stats.sac.stlo]
    	lst_dist.append(dist(pos_sta, pos_hyp))
    mdist = min(lst_dist)
    for dst in lst_dist:
    	lst_dist[lst_dist.index(dst)] = lst_dist[lst_dist.index(dst)] - mdist
    if ((sta[0] + lst_EQ[0][2:-2] + '.vel_4_10Hz_hori.sac') in sta) == False:
    	os.chdir(path + '20' + sta[1][6:16] + '00/20' + sta[1][6:16] + '00_vel_4_10Hz_hori')
    	st2 = read(sta[1])
    	dict_vel_used[sta[0]] = 0
    	dict_delai[sta[0]] = dist(lst_pos_hyp[0], [6400 + 0.001*st2[0].stats.sac.stel, st2[0].stats.sac.stla, st2[0].stats.sac.stlo])/3.4
    	tr = [0 for a in lst_st[0][0].data]
    	for st in lst_st:
    	    i0 = int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate)# + lst_dist[lst_st.index(st)]/2.5*st[0].stats.sampling_rate)
    	    for itr in tr[int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate):]:# + lst_dist[lst_st.index(st)]/2.5*st[0].stats.sampling_rate):]:
    	    	tr[tr.index(itr)] = itr + st[0].data[tr.index(itr) - i0]
    else:
    	tr = [a for a in lst_st[sta.index(sta[0] + lst_EQ[0][2:-2] + '.vel_4_10Hz_hori.sac') - 1][0].data]
    	for st in lst_st[1:]:
    	    i0 = int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate)# + lst_dist[lst_st.index(st)]/2.5*st[0].stats.sampling_rate)
    	    for itr in tr[int(lst_dist[lst_st.index(st)]/3.4*st[0].stats.sampling_rate):]:# + lst_dist[lst_st.index(st)]/2.5*st[0].stats.sampling_rate):]:
    	    	tr[tr.index(itr)] = itr + st[0].data[tr.index(itr) - i0]
    tr = Trace(np.asarray(tr), lst_st[lst_dist.index(0)][0].stats)
    os.chdir(path_results)
    tr.write(sta[1][:6] + sta[1][16:], format = 'SAC')

to_register = [dict_vel_used, dict_delai]

os.chdir(path + 'syn')
with open('ligne_veldata', 'wb') as my_fch:
    my_pk = pickle.Pickler(my_fch)
    my_pk.dump(to_register)














