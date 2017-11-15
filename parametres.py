import pickle
import os
import sys
import datetime

param = {}

param['path_origin'] = os.getcwd()[:-6]
param['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')
param['R_Earth'] = float(6400)
param['dist_min'] = float(input('distance min [0 -> 100]: '))
param['dist_max'] = float(input('distance max [dist_min -> 100]: '))
param['couronne'] = str(int(param['dist_min'])) + '-' + str(int(param['dist_max']))
param['freq_min'] = float(input('frequence min [02/05/1/2/4/8/16]: '))
param['freq_max'] = float(input('frequence max [05/1/2/4/8/16/30] (> freq_min): '))
param['band_freq'] = str(param['freq_min']) + '-' + str(param['freq_max'])
param['composante'] = input('composante [3comp/hori/vert]: ')
param['ratioSP'] = float(input('ratio S/P (> 1): '))
param['smooth'] = float(input('longueur fenetre smooth (s): '))
param['impulse'] = float(input('longueur fenetre impulse (s): '))
param['angle_min'] = float(input('angle_min (sens horaire) [0 -> 180]: '))
param['angle_max'] = float(input('angle_max (sens horaire) [angle_min -> 180]: '))
param['angle'] = str(int(param['angle_min'])) + '-' + str(int(param['angle_max']))
param['vP'] = float(input('vitesse des ondes P (km/s) (5.8?): '))
param['vS'] = float(input('vitesse des ondes S (km/s) (3.4?): '))
param['ondes_select'] = input('hypothese de bp [P/S]: ')
param['strike'] = float(input('strike (224?): '))
param['dip'] = float(input('dip (65?): '))
param['l_fault'] = float(input('longueur fault (km) (dans la direction du strike): '))
param['w_fault'] = float(input('largeur fault (km) (dans la direction du dip): '))
param['pas_l'] = float(input('pas longueur fault (km): '))
param['pas_w'] = float(input('pas largeur fault (km): '))
param['samp_rate'] = float(input('nombre d images de bp par seconde (inferieur a 100): '))
param['length_t'] = float(input('duree de la bp (> 5 sec): '))

os.chdir(param['path_origin'] + '/Kumamoto')

with open('parametres_bin', 'wb') as my_exit:
    my_pck = pickle.Pickler(my_exit)
    my_pck.dump(param)

yy = str(datetime.datetime.now().year)
mm = str(datetime.datetime.now().month)
dd = str(datetime.datetime.now().day)
hh = str(datetime.datetime.now().hour)
mi = str(datetime.datetime.now().minute)
ss = str(datetime.datetime.now().second)

while len(yy) != 4:
    if len(yy) > 4:
        print('Error length year')
    yy = '0' + yy
while len(mm) != 2:
    if len(mm) > 2:
        print('Error length month')
    mm = '0' + mm
while len(dd) != 2:
    if len(dd) > 2:
        print('Error length day')
    dd = '0' + dd
while len(hh) != 2:
    if len(hh) > 2:
        print('Error length hour')
    hh = '0' + hh
while len(mi) != 2:
    if len(mi) > 2:
        print('Error length minute')
    mi = '0' + mi
while len(ss) != 2:
    if len(ss) > 2:
        print('Error length second')
    ss = '0' + ss

with open('parametres_' + yy + mm + dd + '-' + hh + mi + ss + '.txt', 'w') as my_ext:
    my_ext.write('path_origin: ' + param['path_origin'] + '\n')
    my_ext.write('dossier: ' + param['dossier'] + '\n')
    my_ext.write('R_Earth: ' + str(param['R_Earth']) + ' km\n')
    my_ext.write('couronne: ' + param['couronne'] + ' km\n')
    my_ext.write('band_freq: ' + param['band_freq'] + ' Hz\n')
    my_ext.write('composante: ' + param['composante'] + '\n')
    my_ext.write('ratio S/P: ' + str(param['ratioSP']) + '\n')
    my_ext.write('fenetre smooth: ' + str(param['smooth']) + ' s\n')
    my_ext.write('fenetre impulse: ' + str(param['impulse']) + ' s\n')
    my_ext.write('fenetre azimuth: ' + param['angle'] + ' deg\n')
    my_ext.write('vitesse P: ' + str(param['vP']) + ' km/s # 5.8\n')
    my_ext.write('vitesse S: ' + str(param['vS']) + ' km/s # 3.4\n')
    my_ext.write('hypothese de bp: ' + param['ondes_select'] + '\n')
    my_ext.write('fault strike: ' + str(param['strike']) + ' deg # 224 for mainshock from Kubo et al. (2016)\n')
    my_ext.write('fault dip: ' + str(param['dip']) + ' deg # 65 for mainshock from Kubo et al. (2016)\n')
    my_ext.write('length fault: ' + str(param['l_fault']) + ' km\n')
    my_ext.write('width fault: ' + str(param['w_fault']) + ' km\n')
    my_ext.write('pas direction strike: ' + str(param['pas_l']) + ' km\n')
    my_ext.write('pas direction dip: ' + str(param['pas_w']) + ' km\n')
    my_ext.write('echantillonage bp: ' + str(param['samp_rate']) + ' im/s\n')
    my_ext.write('duree de bp: ' + str(param['length_t']) + ' s\n')
