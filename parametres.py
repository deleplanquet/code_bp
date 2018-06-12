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

print('')
param['dossier'] = None
print('   Enter EQ name from ref_seismes.txt')
while (param['dossier'] in dict_seis.keys()) == False:
    param['dossier'] = input('dossier au format YYYYMMDDHHMMSS: ')

param['R_Earth'] = float(6400)

print('')
param['dist_min'] = None
print('   Expected value: integer or float between 0 and 100 km')
while ((type(param['dist_min']) is float) == False
       or param['dist_min'] < 0
       or param['dist_min'] >= 100):
    param['dist_min'] = float(input('distance min [0 -> 100]: '))

print('')
param['dist_max'] = None
print('   Expected value: integer or float between dist_min(previous value) and 100 km')
while ((type(param['dist_max']) is float) == False
       or param['dist_max'] <= param['dist_min']
       or param['dist_max'] > 100):
    param['dist_max'] = float(input('distance max [dist_min -> 100]: '))

param['couronne'] = str(int(param['dist_min'])) + '-' + str(int(param['dist_max']))

print('')
param['freq_min'] = None
print('   Expected value: integer or float between 0.2 and 30 Hz')
print('   Suggested values: 0.2 / 0.5 / 1 / 2 / 4 / 8 / 16 Hz')
while ((type(param['freq_min']) is float) == False
       or param['freq_min'] < 0.2
       or param['freq_min'] >= 30):
    param['freq_min'] = float(input('frequence min [02/05/1/2/4/8/16]: '))

print('')
param['freq_max'] = None
print('   Expected value: integer or float between freq_min(previous value) and 30 Hz')
print('   Suggested values: 0.5 / 1 / 2 / 4 / 8 / 16 / 30 Hz')
while ((type(param['freq_max']) is float) == False
       or param['freq_max'] <= param['freq_min']
       or param['freq_max'] > 30):
    param['freq_max'] = float(input('frequence max [05/1/2/4/8/16/30] (> freq_min): '))

param['band_freq'] = str(param['freq_min']) + '-' + str(param['freq_max'])

print('')
param['composante'] = None
print('   Expected value: > 3comp <, > hori < or > vert <')
print('   Other values are not accepted')
while (param['composante'] != '3comp'
       and param['composante'] != 'hori'
       and param['composante'] != 'vert'):
    param['composante'] = input('composante [3comp/hori/vert]: ')

print('')
param['ratioSP'] = None
print('   Comparison between maximum amplitude of S and P waves')
print('   Expected value: strictly positive integer or float')
print('   To have higher P waves, ratio must be < 1')
while ((type(param['ratioSP']) is float) == False
       or param['ratioSP'] <= 0):
    param['ratioSP'] = float(input('ratio S/P (> 1): '))

print('')
param['smooth'] = None
print('   Expected value: positive integer or float')
print('   If the value is smaller than delay between two snapshots,')
print('   the value will be adapted to this delay')
while ((type(param['smooth']) is float) == False
       or param['smooth'] < 0):
    param['smooth'] = float(input('longueur fenetre smooth (s): '))

print('')
param['impulse'] = None
print('   Expected value: strictly positive integer or float')
print('   Too small values are non sense')
while ((type(param['impulse']) is float) == False
       or param['impulse'] <= 0):
    param['impulse'] = float(input('longueur fenetre impulse (s): '))

print('')
param['angle_min'] = None
print('   Expected value: positive integer of float between up to 180 deg')
print('   0 deg is North, counting clockwise')
print('   The other angle, by point(hypocenter) reflection, will be also considered')
while ((type(param['angle_min']) is float) == False
       or param['angle_min'] < 0
       or param['angle_min'] >= 180):
    param['angle_min'] = float(input('angle_min (sens horaire) [0 -> 180]: '))

print('')
param['angle_max'] = None
print('   Expected value: positive integer or float between angle_min(previous value) and 180 deg')
print('   0 deg is North, counting clockwise')
print('   The other angle, by point(hypocenter) reflection, will be also considered')
while ((type(param['angle_max']) is float) == False
       or param['angle_max'] <= param['angle_min']
       or param['angle_max'] > 180):
    param['angle_max'] = float(input('angle_max (sens horaire) [angle_min -> 180]: '))

param['angle'] = str(int(param['angle_min'])) + '-' + str(int(param['angle_max']))

print('')
param['vP'] = None
print('   Expected value: strictly positive integer or float in km.s-1')
while ((type(param['vP']) is float) == False
       or param['vP'] <= 0):
    param['vP'] = float(input('vitesse des ondes P (km/s) (5.8?): '))

print('')
param['vS'] = None
print('   Expected value: strictly positive integer of float in km.s-1')
print('   Of course P-waves are faster so value should be smaller than vP(previous value)')
while ((type(param['vS']) is float) == False
       or param['vS'] <= 0
       or param['vS'] >= param['vP']):
    param['vS'] = float(input('vitesse des ondes S (km/s) (3.4?): '))

print('')
param['ondes_select'] = None
print('   Expected value: > P < or > S <')
print('   Other values are not accepted')
while (param['ondes_select'] != 'P'
       and param['ondes_select'] != 'S'):
    param['ondes_select'] = input('hypothese de bp [P/S]: ')

print('')
param['strike'] = None
print('   Strike direction of the fault')
print('   Expected value: positive integer or float up to 360 deg')
print('   0 deg is North, counting clockwise')
print('   Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/04/16 Kumamoto EQ')
while ((type(param['strike']) is float) == False
       or param['strike'] < 0
       or param['strike'] >= 360):
    param['strike'] = float(input('strike (224?): '))

print('')
param['dip'] = None
print('   Dip direction of the fault')
print('   Expected value: positive integer or float up to 90 deg')
print('   0 deg is horizontal fault plane, 90 deg is vertical one')
print('   Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/;04/16 Kumamoto EQ')
while ((type(param['dip']) is float) == False
       or param['dip'] <= 0
       or param['dip'] > 90):
    param['dip'] = float(input('dip (65?): '))

print('')
param['l_fault'] = None
print('   Length of the fault, that means in the direction of the strike')
print('   Width can be bigger than length, no restriction')
print('   Expected value: stricly positive integer or float in km')
print('   No matter the length, hypocenter is always at the center')
while ((type(param['l_fault']) is float) == False
       or param['l_fault'] <= 0):
    param['l_fault'] = float(input('longueur fault (km) (dans la direction du strike): '))

print('')
param['w_fault'] = None
print('   Width of the fault, that means in the direction of the dip')
print('   Width can be bigger than length, no restriction')
print('   Expected value: stricly positive integer or float in km')
print('   No matter the width, hypocenter is always at the center')
print('   due to that, some points of the grid may be above the surface')
while ((type(param['w_fault']) is float) == False
       or param['w_fault'] <= 0):
    param['w_fault'] = float(input('largeur fault (km) (dans la direction du dip): '))

print('')
param['pas_l'] = None
print('   Length of each subfault in the direction of the strike')
print('   Expected value: strictly positive integer of float in km')
print('   Should be smaller than l_fault to have at least few points')
while ((type(param['pas_l']) is float) == False
       or param['pas_l'] <= 0
       or param['pas_l'] >= param['l_fault']):
    param['pas_l'] = float(input('pas longueur fault (km): '))

print('')
param['pas_w'] = None
print('   Width of each subfault in the direction of the dip')
print('   Expected value: strictly positive integer or float in km')
print('   Should be smaller than w_fault to have at least few points')
while ((type(param['pas_w']) is float) == False
       or param['pas_w'] <= 0
       or param['pas_w'] >= param['w_fault']):
    param['pas_w'] = float(input('pas largeur fault (km): '))

print('')
param['samp_rate'] = None
print('   Number of snapshots per sec')
print('   Expected value: strictly positive integer or float below 100 (station sampling rate))')
print('   Suggested values are between 0.5 and 10')
while ((type(param['samp_rate']) is float) == False
       or param['samp_rate'] > 100
       or param['samp_rate'] <= 0):
    param['samp_rate'] = float(input('nombre d images de bp par seconde (inferieur a 100): '))

if 1./param['samp_rate'] > param['smooth']:
    print('')
    print('####################################################################')
    print('Input value for smooth window length was: ' + str(param['smooth']) + ' s')
    print('However,  the delay between two bp snapshots is higher: ' + str(1./param['samp_rate']) + ' s')
    param['smooth'] = 1./param['samp_rate']
    print('Therefore, the smooth window length is defined again by the following value: ' str(param['smooth']) + ' s')
    print('####################################################################')

print('')
param['length_t'] = None
print('   Period of back projection, from 5 seconds before the start of the rupture')
print('   Expected value: integer or float between 5 and 50 sec')
print('   Suggested values are between 10 and 30 sec')
print('   For Mw ~6~ 20 sec')
print('   For Mw ~7~ 30 sec')
while ((type(param['length_t']) is float) == False
       or param['length_t'] <= 5
       or param['length_t'] >= 50):
    param['length_t'] = float(input('duree de la bp (> 5 sec): '))

path = (param['path_origin']
        + '/Kumamoto/historique_parametres')

path2 = (param['path_origin']
         + '/Kumamoto/'
         + param['dossier'] + '/'
         + param['dossier']
         + '_results/'
         + param['dossier']
         + '_vel_'
         + param['couronne'] + 'km_'
         + param['band_freq'] + 'Hz')

lst_pth = [param['path_origin'] + '/Kumamoto',
           path,
           path2]

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
        
print('')
print('')
print('      You have defined the following parameters:')
print('   EQ: ' + param['dossier'])
print('   Hyp. Dist.: ' + param['couronne'] + ' km')
print('   Freq. Band: ' + param['band_freq'] + ' Hz')
print('   Composante: ' + param['composante'])
print('   S/P ratio: ' + param['ratioSP'])
print('   Smooth window: ' + param['smooth'] + ' s')
print('   Impulse window: ' + param['impulse'] + ' s')
print('   Azimuth: ' + param['angle'] + ' deg')
print('   P vel.: ' + param['vP'] + ' km.s-1')
print('   S vel.: ' + param['vS'] + ' km.s-1')
print('   Used waves: ' + param['ondes_select'])
print('   Grid strike: ' + param['strike'] + ' deg')
print('   Grid dip: ' + param['dip'] + ' deg')
print('   Grid length: ' + param['l_fault'] + ' km')
print('   Grid width: ' + param['w_fault'] + ' km')
print('   Reso. length: ' + param['pas_l'] + ' km')
print('   Reso. width: ' + param['pas_w'] + ' km')
print('   Nbre bp snapshots: ' + param['samp_rate'] + ' s-1')
print('   Bp duration: ' + param['length_t'] + ' s')
