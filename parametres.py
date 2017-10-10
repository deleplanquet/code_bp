import pickle
import os
import sys

param = {}

param['path_origin'] = os.getcwd()[:-6]
param['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')
param['R_Earth'] = 6400
param['dist_min'] = input('distance min: ')
param['dist_max'] = input('distance max: ')
param['couronne'] = param['dist_min'] + '-' + param['dist_max']
param['freq_min'] = input('frequence min: ')
param['freq_max'] = input('frequence max: ')
param['band_freq'] = param['freq_min'] + '-' + param['freq_max']
param['composante'] = input('composante (3comp/hori/vert): ')
param['ratioSP'] = input('ratio S/P: ')
param['smooth'] = input('longueur fenetre smooth (s): ')
param['impulse'] = input('longueur fenetre impulse (s): ')
param['angle_min'] = input('angle_min: ')
param['angle_max'] = input('angle_max: ')
param['angle'] = param['angle_min'] + '-' + param['angle_max']
param['vP'] = input('vitesse des ondes P: ')
param['vS'] = input('vitesse des ondes S: ')

os.chdir(param['path_origin'] + '/Kumamoto')

with open('parametres_bin', 'wb') as my_exit:
    my_pck = pickle.Pickler(my_exit)
    my_pck.dump(param)

with open('parametres.txt', 'w') as my_ext:
    my_ext.write('path_origin: ' + param['path_origin'] + '\n')
    my_ext.write('dossier: ' + param['dossier'] + '\n')
    my_ext.write('R_Earth: ' + str(param['R_Earth']) + '\n')
    my_ext.write('couronne: ' + param['couronne'] + '\n')
    my_ext.write('band_freq: ' + param['band_freq'] + '\n')
    my_ext.write('composante: ' + param['composante'] + '\n')
    my_ext.write('ratio S/P: ' + param['ratioSP'] + '\n')
    my_ext.write('fenetre smooth: ' + param['smooth'] + '\n')
    my_ext.write('fenetre impulse: ' + param['impulse'] + '\n')
    my_ext.write('fenetre azimuth: ' + param['angle'] + '\n')
    my_ext.write('vitesse P: ' + param['vP'] + ' # 5.8' + '\n')
    my_ext.write('vitesse S: ' + param['vS'] + ' # 3.4' + '\n')
