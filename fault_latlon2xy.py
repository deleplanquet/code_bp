







import pickle
import math
import os

#conversion angel degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]





path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpxk = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']

path = path_origin + '/Kumamoto/' + dossier

os.chdir(path)
with open(dossier + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

dt_type = param['composante']
hyp_bp = param['ondes_select']



R_Earth = param['R_Earth']





coord = []

with open('.txt', 'r') as myf:
    texte = myf.read()

for line in texte:
    spliit = line.split(' ')
    coord.append(geo2cart(R_Earth - spliit[2], spliit[0], spliit[1]))

travtime
