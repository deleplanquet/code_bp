import pickle
import os
import sys

param = {}

param['path_origin'] = os.getcwd()[:-6]
param['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')
param['R_Earth'] = 6400
param['dist_min'] = input('distance min [0 -> 100]: ')
param['dist_max'] = input('distance max [dist_min -> 100]: ')
param['couronne'] = param['dist_min'] + '-' + param['dist_max']
param['freq_min'] = input('frequence min [02/05/1/2/4/8/16]: ')
param['freq_max'] = input('frequence max [05/1/2/4/8/16/30] (> freq_min): ')
param['band_freq'] = param['freq_min'] + '-' + param['freq_max']
param['composante'] = input('composante [3comp/hori/vert]: ')
param['ratioSP'] = input('ratio S/P (> 1): ')
param['smooth'] = input('longueur fenetre smooth (s): ')
param['impulse'] = input('longueur fenetre impulse (s): ')
param['angle_min'] = input('angle_min (sens horaire) [0 -> 180]: ')
param['angle_max'] = input('angle_max (sens horaire) [angle_min -> 360]: ')
param['angle'] = param['angle_min'] + '-' + param['angle_max']
param['vP'] = input('vitesse des ondes P (km/s) (5.8?): ')
param['vS'] = input('vitesse des ondes S (km/s) (3.4?): ')
param['ondes_select'] = input('hypothese de bp [P/S]: ')
param['strike'] = input('strike (224?): ')
param['dip'] = input('dip (65?): ')
param['l_fault'] = input('longueur fault (km) (dans la direction du strike): ')
param['w_fault'] = input('largeur fault (km) (dans la direction du dip): ')
param['pas_l'] = input('pas longueur fault (km): ')
param['pas_w'] = input('pas largeur fault (km): ')
param['samp_rate'] = input('nombre d images de bp par seconde (inferieur a 100): ')
param['length_t'] = input('duree de la bp (> 5 sec): ')

os.chdir(param['path_origin'] + '/Kumamoto')

with open('parametres_bin', 'wb') as my_exit:
    my_pck = pickle.Pickler(my_exit)
    my_pck.dump(param)

with open('parametres.txt', 'w') as my_ext:
    my_ext.write('path_origin: ' + param['path_origin'] + '\n')
    my_ext.write('dossier: ' + param['dossier'] + '\n')
    my_ext.write('R_Earth: ' + str(param['R_Earth']) + ' km\n')
    my_ext.write('couronne: ' + param['couronne'] + ' km\n')
    my_ext.write('band_freq: ' + param['band_freq'] + ' Hz\n')
    my_ext.write('composante: ' + param['composante'] + '\n')
    my_ext.write('ratio S/P: ' + param['ratioSP'] + '\n')
    my_ext.write('fenetre smooth: ' + param['smooth'] + ' s\n')
    my_ext.write('fenetre impulse: ' + param['impulse'] + ' s\n')
    my_ext.write('fenetre azimuth: ' + param['angle'] + ' deg\n')
    my_ext.write('vitesse P: ' + param['vP'] + ' km/s # 5.8\n')
    my_ext.write('vitesse S: ' + param['vS'] + ' km/s # 3.4\n')
    my_ext.write('hypothese de bp: ' + param['ondes_select'] + '\n')
    my_ext.write('fault strike: ' + param['strike'] + ' deg\n')
    my_ext.write('fault dip: ' + param['dip'] + ' deg\n')
    my_ext.write('length fault: ' + param['l_fault'] + ' km\n')
    my_ext.write('width fault:' + param['w_fault'] + ' km\n')
    my_ext.write('pas direction strike: ' + param['pas_l'] + ' km\n')
    my_ext.write('pas direction dip: ' + param['pas_w'] + ' km\n')
    my_ext.write('echantillonage bp: ' + param['samp_rate'] + ' im/s\n')
    my_ext.write('duree de bp: ' + param['length_t'] + ' s\n')
