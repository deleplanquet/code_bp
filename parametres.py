import pickle
import os
import sys
import datetime

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

param = {}

param['path_origin'] = path_origin

param['dossier'] = None
while (param['dossier'] in dict_seis.keys()) == False:
    print('Enter EQ name from ref_seismes.txt')
    param['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')
print('')

param['R_Earth'] = float(6400)

param['dist_min'] = None
while ((type(param['dist_min']) is float) == False
       or param['dist_min'] < 0
       or param['dist_min'] > 100):
    print('Expected value: integer or float between 0 and 100 km')
    param['dist_min'] = float(input('distance min [0 -> 100]: '))
print('')

param['dist_max'] = None
while ((type(param['dist_max']) is float) == False
       or param['dist_max'] <= param['dist_min']
       or param['dist_max'] > 100):
    print('Expected value: integer or float between dist_min(previous value) and 100 km')
    param['dist_max'] = float(input('distance max [dist_min -> 100]: '))
print('')

param['couronne'] = str(int(param['dist_min'])) + '-' + str(int(param['dist_max']))

param['freq_min'] = None
while ((type(param['freq_min']) is float) == False
       or param['freq_min'] < 0.2
       or param['freq_min'] > 30):
    print('Expected value: integer or float between 0.2 and 30 Hz')
    print('Suggested values: 0.2 / 0.5 / 1 / 2 / 4 / 8 / 16 Hz')
    param['freq_min'] = float(input('frequence min [02/05/1/2/4/8/16]: '))
print('')

param['freq_max'] = None
while ((type(param['freq_max']) is float) == False
       or param['freq_max'] <= param['freq_min']
       or param['freq_max'] > 30):
    print('Expected value: integer or float between freq_min(previous value) and 30 Hz')
    print('Suggested values: 0.5 / 1 / 2 / 4 / 8 / 16 / 30 Hz')
    param['freq_max'] = float(input('frequence max [05/1/2/4/8/16/30] (> freq_min): '))
print('')

param['band_freq'] = str(param['freq_min']) + '-' + str(param['freq_max'])

param['composante'] = None
while (param['composante'] != '3comp'
       and param['composante'] != 'hori'
       and param['composante'] != 'vert'):
    print('Expected value: > 3comp <, > hori < or > vert <')
    print('Other values will not be accepted')
    param['composante'] = input('composante [3comp/hori/vert]: ')
print('')

param['ratioSP'] = None
while (type(param['ratioSP'] is float) == False
       or param['ratioSP'] <= 0):
    print('Comparison between maximum amplitude of S and P waves')
    print('To have higher P waves, ratio must be < 1')
    param['ratioSP'] = float(input('ratio S/P (> 1): '))
print('')

param['smooth'] = None
while (type(param['smooth'] is float) == False
       or param['smooth'] < 0):
    print('Expected value: integer or float > 0')
    print('If the value is smaller than delay between two snapshots,')
    print('   the value will be adapted to this delay')
    param['smooth'] = float(input('longueur fenetre smooth (s): '))
print('')

param['impulse'] = None
while (type(param['impulse'] is float) == False
       or param['impulse'] <= 0):
    print('Expected value: integer or float > 0')
    print('Too small values are non sense')
    param['impulse'] = float(input('longueur fenetre impulse (s): '))
print('')

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

path = param['path_origin'] + '/Kumamoto/historique_parametres'
path2 = param['path_origin'] + '/Kumamoto/' + param['dossier'] + '/' + param['dossier'] + '_results/' + param['dossier'] + '_vel_' + param['couronne'] + 'km_' + param['band_freq'] + 'Hz'

lst_pth = [param['path_origin'] + '/Kumamoto', path, path2]

if os.path.isdir(path) == False:
    os.makedirs(path)
if os.path.isdir(path2) == False:
    os.makedirs(path2)

os.chdir(lst_pth[0])

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

for ppth in lst_pth:
    if ppth == lst_pth[0]:
        paparam = 'current_parametres.txt'
    else:
        paparam = 'parametres_' + yy + mm + dd + '-' + hh + mi + ss + '.txt'
    os.chdir(ppth)
    with open(paparam, 'w') as my_ext:
        my_ext.write('         path_origin: ' + param['path_origin'] + '\n')
        my_ext.write('             dossier: ' + param['dossier'] + '\n')
        my_ext.write('             R_Earth: ' + str(param['R_Earth']) + ' km\n')
        my_ext.write('            couronne: ' + param['couronne'] + ' km\n')
        my_ext.write('           band_freq: ' + param['band_freq'] + ' Hz\n')
        my_ext.write('          composante: ' + param['composante'] + '\n')
        my_ext.write('           ratio S/P: ' + str(param['ratioSP']) + '\n')
        my_ext.write('      fenetre smooth: ' + str(param['smooth']) + ' s\n')
        my_ext.write('     fenetre impulse: ' + str(param['impulse']) + ' s\n')
        my_ext.write('     fenetre azimuth: ' + param['angle'] + ' deg\n')
        my_ext.write('           vitesse P: ' + str(param['vP']) + ' km/s # 5.8\n')
        my_ext.write('           vitesse S: ' + str(param['vS']) + ' km/s # 3.4\n')
        my_ext.write('     hypothese de bp: ' + param['ondes_select'] + '\n')
        my_ext.write('        fault strike: ' + str(param['strike']) + ' deg # 224 for mainshock from Kubo et al. (2016)\n')
        my_ext.write('           fault dip: ' + str(param['dip']) + ' deg # 65 for mainshock from Kubo et al. (2016)\n')
        my_ext.write('        length fault: ' + str(param['l_fault']) + ' km\n')
        my_ext.write('         width fault: ' + str(param['w_fault']) + ' km\n')
        my_ext.write('pas direction strike: ' + str(param['pas_l']) + ' km\n')
        my_ext.write('   pas direction dip: ' + str(param['pas_w']) + ' km\n')
        my_ext.write('   echantillonage bp: ' + str(param['samp_rate']) + ' im/s\n')
        my_ext.write('         duree de bp: ' + str(param['length_t']) + ' s\n')
