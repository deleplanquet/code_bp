import pickle
import os
import sys

variables = {}

variables['path_origin'] = os.getcwd()[:-6]
variables['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')
variables['R_Earth'] = 6400
variables['dist_min'] = input('distance min: ')
variables['dist_max'] = input('distance max: ')
variables['couronne'] = variables['dist_min'] + '-' + variables['dist_max']
variables['freq_min'] = input('frequence min: ')
variables['freq_max'] = input('frequence max: ')
variables['band_freq'] = variables['freq_min'] + '-' + variables['freq_max']
variables['composante'] = input('composante (3comp/hori/vert): ')
variables['ratioSP'] = input('ratio S/P: ')
variables['smooth'] = input('longueur fenetre smooth (s): ')
variables['impulse'] = input('longueur fenetre impulse (s): ')
variables['angle_min'] = input('angle_min: ')
variables['angle_max'] = input('angle_max: ')
variables['angle'] = variables['angle_min'] + '-' + variables['angle_max']
variables['vP'] = input('vitesse des ondes P: ')
variables['vS'] = input('vitesse des ondes S: ')

os.chdir(variables['path_origin'] + '/Kumamoto')

with open('variables_bin', 'wb') as my_exit:
    my_pck = pickle.Pickler(my_exit)
    my_pck.dump(variables)

with open('variables.txt', 'w') as my_ext:
    my_ext.write('path_origin: ' + variables['path_origin'] + '\n')
    my_ext.write('dossier: ' + variables['dossier'] + '\n')
    my_ext.write('R_Earth: ' + str(variables['R_Earth']) + '\n')
    my_ext.write('couronne: ' + variables['couronne'] + '\n')
    my_ext.write('band_freq: ' + variables['band_freq'] + '\n')
    my_ext.write('composante: ' + variables['composante'] + '\n')
    my_ext.write('ratio S/P: ' + variables['ratioSP'] + '\n')
    my_ext.write('fenetre smooth: ' + variables['smooth'] + '\n')
    my_ext.write('fenetre impulse: ' + variables['impulse'] + '\n')
    my_ext.write('fenetre azimuth: ' + variables['angle'] + '\n')
    my_ext.write('vitesse P: ' + variables['vP'] + ' # 5.8' + '\n')
    my_ext.write('vitesse S: ' + variables['vS'] + ' # 3.4' + '\n')
