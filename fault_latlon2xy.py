







import pickle
import math
import os

#conversion angel degre -> radian
def d2r(angle):
    return angle*math.pi/180







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










with open( '.txt', 'r') as myf:
    mydp = pickle.Unpicker(myf)
     = mydp.load()


