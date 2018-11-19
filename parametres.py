import pickle
import os
import sys
import datetime

# root: root of the /Codes folder
# load events dictionnary
# be careful, folder containing data has relative position to /Codes folder
root = os.getcwd()[:-6]
os.chdir(root + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

# parameters dictionnary
param = {}

# root of the /Codes folder
param['root'] = root

# print name of available events
# initialisation of the name of the selected event
# the name of the event is stored in the parameters dictionnary with the key 'event'
# the name of the selected event is then asked
# check if the name is corresponding to one of the key of the events dictionnary
# - if yes, stored in parammeters dictionnary with the corresponding key 'event'
# - else, the name is asked again
print('#############')
print('### event ###')
print('#############')
print('   list of available events')
for eq in dict_seis.keys():
    print('   ', eq)
param['event'] = None
print('')
print('   Enter EQ name from ref_seismes.txt')
while (param['event'] in dict_seis.keys()) == False:
    param['event'] = input('dossier au format YYYYMMDDHHMMSS: ')

# Earth radius 6400 km
param['R_Earth'] = float(6400)

# initialisation of the minimum value for the hypocenter distance
# stations which hypocenter distance is less than the minimum value will be ignored
# check if the type of the given value is float
# check if the value is positive and lower than 100 km (limit due to preprocessing)
# - if everything is ok, stored in the parameters dictionnary with the key 'hypo_min'
# - else, the value is asked again
print('################')
print('### hypo_min ###')
print('################')
param['hypo_min'] = None
print('   Expected value: integer or float between 0 and 100 km')
while ((type(param['hypo_min']) is float) == False
       or param['hypo_min'] < 0
       or param['hypo_min'] >= 100):
    param['hypo_min'] = float(input('distance min [0 -> 100]: '))

# initialisation of the maximum value for the hypocenter distance
# station which hypocenter distance is higher than the maximum value will be ignored
# check if the type of the given value is float
# check if the value is higher than 'hypo_min' to be consistent
# check if the value is lower than 100 km (limit due to preprocessing)
# - if everything is ok, stored in the parameters dictionnary with the key 'hypo_max'
# - else, the value is asked again
print('################')
print('### hypo_max ###')
print('################')
param['hypo_max'] = None
print('   Expected value: integer or float between dist_min(previous value) and 100 km')
while ((type(param['hypo_max']) is float) == False
       or param['hypo_max'] <= param['dist_min']
       or param['hypo_max'] > 100):
    param['hypo_max'] = float(input('distance max [dist_min -> 100]: '))

# a combination of 'hypo_min' and 'hypo_max' is created as a new parameter
# this parameter represents the considered interval for the hypocenter distances
# it is stored in the parameters dictionnary with the key 'hypo_interv'
param['hypo_interv'] = str(int(param['hypo_min'])) + '-' + str(int(param['hypo_max']))

# initialisation of the minimum value of the frequency
# a filter band will be applied on the velocity traces
# check if the type of the given value is float
# check if the value is strictly positive and lower than 30 Hz (limit imposed by the network)
# - if everything is ok, stored in the parameters dictionnary with the key 'frq_min'
# - else, the value is asked again
print('###############')
print('### frq_min ###')
print('###############')
param['frq_min'] = None
print('   Expected value: integer or float between 0.2 and 30 Hz')
print('   Suggested values: 0.2 / 0.5 / 1 / 2 / 4 / 8 / 16 Hz')
while ((type(param['frq_min']) is float) == False
       or param['frq_min'] <= 0
       or param['frq_min'] >= 30):
    param['frq_min'] = float(input('frequence min [02/05/1/2/4/8/16]: '))

# initialisation of the maximum value of the frequency
# a filter band will be applied on the velocity traces
# check if the type of the given value is float
# check if the value is higher than 'frq_min' to be consistent
# check if the value is lower than 30 Hz (limit imposed by the network)
# - if everything is ok, stored in the parameters dictionnary with the key 'frq_max'
# - else, the value is asked again
print('###############')
print('### frq_max ###')
print('###############')
param['frq_max'] = None
print('   Expected value: integer or float between freq_min(previous value) and 30 Hz')
print('   Suggested values: 0.5 / 1 / 2 / 4 / 8 / 16 / 30 Hz')
while ((type(param['frq_max']) is float) == False
       or param['frq_max'] <= param['freq_min']
       or param['frq_max'] > 30):
    param['frq_max'] = float(input('frequence max [05/1/2/4/8/16/30] (> freq_min): '))

# a combination of 'frq_min' and 'frq_max' is created as a new parameter
# this parameter represents the considered frequency band for the filtering
# it is stored in the parameters dictionnary with the kry 'frq_band'
param['frq_band'] = str(param['frq_min']) + '-' + str(param['frq_max'])

# initialisation of the component
# 
print('#################')
print('### component ###')
print('#################')
param['component'] = None
print('   Expected value: > 3comp <, > hori < or > vert <')
print('   Other values are not accepted')
while (param['component'] != '3comp'
       and param['component'] != 'hori'
       and param['component'] != 'vert'):
    param['component'] = input('composante [3comp/hori/vert]: ')

print('###############')
print('### ratioSP ###')
print('###############')
param['ratioSP'] = None
print('   Comparison between maximum amplitude of S and P waves')
print('   Expected value: strictly positive integer or float')
print('   To have higher P waves, ratio must be < 1')
while ((type(param['ratioSP']) is float) == False
       or param['ratioSP'] <= 0):
    param['ratioSP'] = float(input('ratio S/P (> 1): '))

print('################')
print('### l_smooth ###')
print('################')
param['l_smooth'] = None
print('   Expected value: positive integer or float')
print('   If the value is smaller than delay between two snapshots,')
print('   the value will be adapted to this delay')
while ((type(param['l_smooth']) is float) == False
       or param['l_smooth'] < 0):
    param['l_smooth'] = float(input('longueur fenetre smooth (s): '))

print('#################')
print('### l_impulse ###')
print('#################')
param['l_impulse'] = None
print('   Expected value: strictly positive integer or float')
print('   Too small values are non sense')
while ((type(param['l_impulse']) is float) == False
       or param['l_impulse'] <= 0):
    param['l_impulse'] = float(input('longueur fenetre impulse (s): '))

print('#################')
print('### angle_min ###')
print('#################')
param['angle_min'] = None
print('   Expected value: positive integer of float between up to 180 deg')
print('   0 deg is North, counting clockwise')
print('   The other angle, by point(hypocenter) reflection, will be also considered')
while ((type(param['angle_min']) is float) == False
       or param['angle_min'] < 0
       or param['angle_min'] >= 180):
    param['angle_min'] = float(input('angle_min (sens horaire) [0 -> 180]: '))

print('#################')
print('### angle_max ###')
print('#################')
param['angle_max'] = None
print('   Expected value: positive integer or float between angle_min(previous value) and 180 deg')
print('   0 deg is North, counting clockwise')
print('   The other angle, by point(hypocenter) reflection, will be also considered')
while ((type(param['angle_max']) is float) == False
       or param['angle_max'] <= param['angle_min']
       or param['angle_max'] > 180):
    param['angle_max'] = float(input('angle_max (sens horaire) [angle_min -> 180]: '))

param['angle'] = str(int(param['angle_min'])) + '-' + str(int(param['angle_max']))

print('##########')
print('### vP ###')
print('##########')
param['vP'] = None
print('   Expected value: strictly positive integer or float in km.s-1')
while ((type(param['vP']) is float) == False
       or param['vP'] <= 0):
    param['vP'] = float(input('vitesse des ondes P (km/s) (5.8?): '))

print('##########')
print('### vS ###')
print('##########')
param['vS'] = None
print('   Expected value: strictly positive integer of float in km.s-1')
print('   Of course P-waves are faster so value should be smaller than vP(previous value)')
while ((type(param['vS']) is float) == False
       or param['vS'] <= 0
       or param['vS'] >= param['vP']):
    param['vS'] = float(input('vitesse des ondes S (km/s) (3.4?): '))

print('######################')
print('### selected_waves ###')
print('######################')
param['selected_waves'] = None
print('   Expected value: > P < or > S <')
print('   Other values are not accepted')
while (param['selected_waves'] != 'P'
       and param['selected_waves'] != 'S'):
    param['selected_waves'] = input('hypothese de bp [P/S]: ')

print('##############')
print('### strike ###')
print('##############')
param['strike'] = None
print('   Strike direction of the fault')
print('   Expected value: positive integer or float up to 360 deg')
print('   0 deg is North, counting clockwise')
print('   Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/04/16 Kumamoto EQ')
while ((type(param['strike']) is float) == False
       or param['strike'] < 0
       or param['strike'] >= 360):
    param['strike'] = float(input('strike (224?): '))

print('###########')
print('### dip ###')
print('###########')
param['dip'] = None
print('   Dip direction of the fault')
print('   Expected value: positive integer or float up to 90 deg')
print('   0 deg is horizontal fault plane, 90 deg is vertical one')
print('   Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/;04/16 Kumamoto EQ')
while ((type(param['dip']) is float) == False
       or param['dip'] <= 0
       or param['dip'] > 90):
    param['dip'] = float(input('dip (65?): '))

print('###############')
print('### l_fault ###')
print('###############')
param['l_fault'] = None
print('   Length of the fault, that means in the direction of the strike')
print('   Width can be bigger than length, no restriction')
print('   Expected value: stricly positive integer or float in km')
print('   No matter the length, hypocenter is always at the center')
while ((type(param['l_fault']) is float) == False
       or param['l_fault'] <= 0):
    param['l_fault'] = float(input('longueur fault (km) (dans la direction du strike): '))

print('###############')
print('### w_fault ###')
print('###############')
param['w_fault'] = None
print('   Width of the fault, that means in the direction of the dip')
print('   Width can be bigger than length, no restriction')
print('   Expected value: stricly positive integer or float in km')
print('   No matter the width, hypocenter is always at the center')
print('   due to that, some points of the grid may be above the surface')
while ((type(param['w_fault']) is float) == False
       or param['w_fault'] <= 0):
    param['w_fault'] = float(input('largeur fault (km) (dans la direction du dip): '))

print('####################')
print('### l_fault_step ###')
print('####################')
param['l_fault_step'] = None
print('   Length of each subfault in the direction of the strike')
print('   Expected value: strictly positive integer of float in km')
print('   Should be smaller than l_fault to have at least few points')
while ((type(param['l_fault_step']) is float) == False
       or param['l_fault_step'] <= 0
       or param['l_fault_step'] >= param['l_fault']):
    param['l_fault_step'] = float(input('pas longueur fault (km): '))

print('####################')
print('### w_fault_step ###')
print('####################')
param['w_fault_step'] = None
print('   Width of each subfault in the direction of the dip')
print('   Expected value: strictly positive integer or float in km')
print('   Should be smaller than w_fault to have at least few points')
while ((type(param['w_fault_step']) is float) == False
       or param['w_fault_step'] <= 0
       or param['w_fault_step'] >= param['w_fault']):
    param['w_fault_step'] = float(input('pas largeur fault (km): '))

print('####################')
print('### bp_samp_rate ###')
print('####################')
param['bp_samp_rate'] = None
print('   Number of snapshots per sec')
print('   Expected value: strictly positive integer or float below 100 (station sampling rate))')
print('   Suggested values are between 0.5 and 10')
while ((type(param['bp_samp_rate']) is float) == False
       or param['bp_samp_rate'] > 100
       or param['bp_samp_rate'] <= 0):
    param['bp_samp_rate'] = float(input('nombre d images de bp par seconde (inferieur a 100): '))

if 1./param['bp_samp_rate'] > param['l_smooth']:
    print('')
    print('####################################################################')
    print('Input value for smooth window length was: ' + str(param['l_smooth']) + ' s')
    print('However,  the delay between two bp snapshots is higher: ' + str(1./param['bp_samp_rate']) + ' s')
    param['l_smooth'] = 1./param['bp_samp_rate']
    print('Therefore, the smooth window length is defined again by the following value: ' + str(param['l_smooth']) + ' s')
    print('####################################################################')

print('#################')
print('### bp_l_time ###')
print('#################')
param['bp_l_time'] = None
print('   Period of back projection, from 5 seconds before the start of the rupture')
print('   Expected value: integer or float between 5 and 50 sec')
print('   Suggested values are between 10 and 30 sec')
print('   For Mw ~6~ 20 sec')
print('   For Mw ~7~ 30 sec')
while ((type(param['bp_l_time']) is float) == False
       or param['bp_l_time'] <= 5
       or param['bp_l_time'] >= 50):
    param['bp_l_time'] = float(input('duree de la bp (> 5 sec): '))

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
        my_ext.write('         root folder: ' + param['root'] + '\n')
        my_ext.write('               event: ' + param['event'] + '\n')
        my_ext.write('             R_Earth: ' + str(param['R_Earth']) + ' km\n')
        my_ext.write('         hypo_interv: ' + param['hypo_interv'] + ' km\n')
        my_ext.write('            frq_band: ' + param['frq_band'] + ' Hz\n')
        my_ext.write('           component: ' + param['component'] + '\n')
        my_ext.write('           ratio S/P: ' + str(param['ratioSP']) + '\n')
        my_ext.write('       smooth window: ' + str(param['l_smooth']) + ' s\n')
        my_ext.write('      impulse window: ' + str(param['l_impulse']) + ' s\n')
        my_ext.write('      azimuth window: ' + param['angle'] + ' deg\n')
        my_ext.write('          P-velocity: ' + str(param['vP']) + ' km/s # 5.8\n')
        my_ext.write('          S-velocity: ' + str(param['vS']) + ' km/s # 3.4\n')
        my_ext.write('      selected waves: ' + param['selected_waves'] + '\n')
        my_ext.write('        fault strike: ' + str(param['strike']) + ' deg # 224 for mainshock from Kubo et al. (2016)\n')
        my_ext.write('           fault dip: ' + str(param['dip']) + ' deg # 65 for mainshock from Kubo et al. (2016)\n')
        my_ext.write('        length fault: ' + str(param['l_fault']) + ' km\n')
        my_ext.write('         width fault: ' + str(param['w_fault']) + ' km\n')
        my_ext.write('   length fault step: ' + str(param['l_fault_step']) + ' km\n')
        my_ext.write('    width fault step: ' + str(param['w_fault_step']) + ' km\n')
        my_ext.write('    bp sampling rate: ' + str(param['bp_samp_rate']) + ' im/s\n')
        my_ext.write('      bp length time: ' + str(param['bp_l_time']) + ' s\n')
        
print('')
print('')
print('      You have defined the following parameters:')
print('               event: ' + param['event'])
print('        Hyp. Interv.: ' + param['hypo_interv'] + '          km')
print('          Freq. Band: ' + param['frq_band'] + '        Hz')
print('           Component: ' + param['component'])
print('           S/P ratio: ' + str(param['ratioSP']))
print('       Smooth window: ' + str(param['l_smooth']) + '            s')
print('      Impulse window: ' + str(param['l_impulse']) + '            s')
print('             Azimuth: ' + str(param['angle']) + '          deg')
print('              P vel.: ' + str(param['vP']) + '            km.s-1')
print('              S vel.: ' + str(param['vS']) + '            km.s-1')
print('      Selected waves: ' + param['selected_waves'])
print('         Grid strike: ' + str(param['strike']) + '          deg')
print('            Grid dip: ' + str(param['dip']) + '           deg')
print('         Grid length: ' + str(param['l_fault']) + '           km')
print('          Grid width: ' + str(param['w_fault']) + '           km')
print('        Reso. length: ' + str(param['l_fault_step']) + '            km')
print('         Reso. width: ' + str(param['w_fault_step']) + '            km')
print('   Nbre bp snapshots: ' + str(param['bp_samp_rate']) + '            s-1')
print('         Bp duration: ' + str(param['bp_l_time']) + '           s')
