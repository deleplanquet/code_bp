import pickle
from obspy import read
import sys
import os
import math
from obspy import Trace

#constantes
R_Earth = 6400

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#distance entre deux points, coordonnees cartesiennes
def dist(vect1, vect2):
    x1, y1, z1 = geo2cart(vect1)
    x2, y2, z2 = geo2cart(vect2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_sac'
path_results = path + '/' + dossier + '_sac_inf100km'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

os.chdir(path_origin + '/Data')
with open('ref_seismes_bin', 'rb') as my_fich:
    my_depick = pickle.Unpickler(my_fich)
    dict_seis = my_depick.load()

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']

os.chdir(path_data)

list_stat = os.listdir(path_data)
list_stat_UD = [a for a in list_stat if ('UD' in a) == True and ('UD1' in a) == False]
list_stat_NS = [a for a in list_stat if ('NS' in a) == True and ('NS1' in a) == False]
list_stat_EW = [a for a in list_stat if ('EW' in a) == True and ('EW1' in a) == False]
list_stat = list_stat_UD + list_stat_NS + list_stat_EW

hypo = [R_Earth - dep_hyp, lat_hyp, lon_hyp]

for station in list_stat:
    os.chdir(path_data)
    print(station)
    st = read(station)
    pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel, st[0].stats.sac.stla, st[0].stats.sac.stlo]
    print(dist(hypo, pos_sta))
    if dist(hypo, pos_sta) < 100:
        os.chdir(path_results)
        print('selection')
        tr = Trace(st[0].data, st[0].stats)
        tr.write(station, format='SAC')















