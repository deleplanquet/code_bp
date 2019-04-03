# create binary file containing all the parameters potentialy needed for back
# projection study
# parameters are asked through the terminal
# /Codes is the name of the directory containing all the scripts related to
# bp study
# it may have different name without consequences

import pickle
import os
import sys
import datetime

# root: root of the /Codes folder
# load events dictionnary
# be careful, folder containing data has relative position to /Codes folder
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto') # has to be changed in case of another EQ
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

param = {}

print('')
print('   ###################')
print('   ### root_folder ###')
print('   ###################')
# root of the /Codes folder
param['root_folder'] = root_folder
print(root_folder)

print('')
print('   #############')
print('   ### event ###')
print('   #############')
# print name of available events
print('list of available events')
for eq in dict_seis.keys():
    print(eq)
# initialisation of the name of the selected event
param['event'] = None
print('Enter EQ name from ref_seismes.txt')
# the name of the event is asked while the input is not inside
# the vents dictionnary
while param['event'] not in dict_seis.keys():
    param['event'] = input('dossier au format YYYYMMDDHHMMSS: ')

# Earth radius 6400 km
param['R_Earth'] = float(6400)

print('')
print('   ################')
print('   ### hypo_min ###')
print('   ################')
# initialisation of the minimum value of the hypocenter distance
param['hypo_min'] = None
print('minimal distance between hypocenter and station')
print('stations with lower hypocentral distance are not considered')
print('Expected value: integer or float between 0 and 100 km')
# check the type, should be float
# should also be positive
# above 100 km is not allowed
while (not isinstance(param['hypo_min'], float)
       or param['hypo_min'] < 0
       or param['hypo_min'] >= 100):
    try:
        param['hypo_min'] = float(input('distance min [0 -> 100]: '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ################')
print('   ### hypo_max ###')
print('   ################')
# initialisation of the maximum value of the hypocenter distance
param['hypo_max'] = None
print('maximal distance between hypocenter and station')
print('stations with higher hypocentral distance are not considered')
print('Expected value: integer or float between hypo_min (previous value) = '
       + str(int(param['hypo_min'])) + ' and 100 km')
# check the type, should be float
# should also be above hypo_min and below 100 km
while (not isinstance(param['hypo_max'], float)
       or param['hypo_max'] <= param['hypo_min']
       or param['hypo_max'] > 100):
    try:
        param['hypo_max'] = float(input('distance max ['
                                         + str(int(param['hypo_min']))
                                         + ' -> 100]: '))
    except ValueError:
        print('No valid number, try again')

# combination of hypo_min and hypo_max as hypo_interv
# for easier creation of file/directory names
param['hypo_interv'] = (str(int(param['hypo_min'])) + '-'
                        + str(int(param['hypo_max'])))

print('')
print('   ###############')
print('   ### frq_min ###')
print('   ###############')
# some filter will be applied on velocity traces during the bp process
# considered frequencies are corner frequencies for those filters
# different tests have shown that above 8 Hz, stability decreases
# and below 2 Hz, resolution decreases
# the networks used for the Kumamoto EQ
# impose high frequency of the filter < 30 Hz
# initialisation of the minimum value of the frequency
param['frq_min'] = None
print('velocity traces will be filtered')
print('choice of the low frequency for the filter band')
print('Expected value: integer or float between 0.2 and 30 Hz')
print('Suggested values: 0.2 / 0.5 / 1 / 2 / 4 / 8 / 16 Hz')
while (not isinstance(param['frq_min'], float)
       or param['frq_min'] < 0.2
       or param['frq_min'] >= 30):
    try:
        param['frq_min'] = float(input('frequence min'
                                        + '[0.2/0.5/1/2/4/8/16]: '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ###############')
print('   ### frq_max ###')
print('   ###############')
# some filter will be applied on velocity traces during the bp process
# considered frequencies are corner frequencies for those filters
# different tests have shown that above 8 Hz, stability decreases
# and below 2 Hz, resolution decreases
# the network used for the Kumamoto EQ
# imposes high frequency of the filter < 30 Hz
# initialisation of the maximum value of the frequency
param['frq_max'] = None
print('choice of the high frequency for the filter band')
print('Expected value: integer or float between freq_min (previous value) = '
        + str(param['frq_min']) + ' and 30 Hz')
print('Suggested values: 0.5 / 1 / 2 / 4 / 8 / 16 / 30 Hz')
while (not isinstance(param['frq_max'], float)
       or param['frq_max'] <= param['frq_min']
       or param['frq_max'] > 30):
    try:
        param['frq_max'] = float(input('frequence max '
                                    + '[05/1/2/4/8/16/30] (> '
                                    + str(param['frq_min']) + '): '))
    except ValueError:
        print('No valid number, try again')

# combination of frq_min and fra_max as frq_band
# for easier creation of file/directory names
param['frq_band'] = str(param['frq_min']) + '-' + str(param['frq_max'])

print('')
print('   #################')
print('   ### component ###')
print('   #################')
# the three components are EW, NS and UD
# here we ask which component should be used for the bp study
# we refer as:
# - 3comp: combination of the three components EW, NS and UD
# - hori: combination of the two horizontal components EW and NS
# - vert: only the vertical component UD is considered
# initialisation of the component
param['component'] = None
print('Expected value: > 3comp <, > hori < or > vert <')
print(' - 3comp: combination of the three components EW, NS and UD')
print(' - hori: combination of the two horizontal components EW and NS')
print(' (recommended for S-waves bp)')
print(' - vert: only the vertical component UD is considered')
print(' (recommended for P-waves bp)')
print('Other values are not accepted')
while (param['component'] != '3comp'
       and param['component'] != 'hori'
       and param['component'] != 'vert'):
    param['component'] = input('component [3comp/hori/vert]: ')

print('')
print('   ###############')
print('   ### ratioSP ###')
print('   ###############')
# criteria for selection of stations
# a comparison between the maximum values of S and P-waves is done
# the ratio should be above the value given by the user
# for instance, if the value is 3
# stations which maximum value of S-waves is
# less than 3 times the maximum value of P-waves
# are not used for the bp process
# values > 1 give an advantage to S-waves
# values < 1 give an advantage to P-waves
# the choice of component and ratioSP should be consistent for the study
# initialisation of ratioSP
param['ratioSP'] = None
print('Comparison between maximum amplitude of S and P waves')
print('Expected value: strictly positive integer or float')
print('To have higher P waves, ratio must be < 1')
while (not isinstance(param['ratioSP'], float)
       or param['ratioSP'] <= 0):
    try:
        param['ratioSP'] = float(input('ratio S/P (> 1): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ################')
print('   ### l_smooth ###')
print('   ################')
# length of the time-window for the smoothing of the traces
# to take into account all the points between two pictures of bp
# the length of the time-window should be at least
# the delay between two snapshots
# it can be higher
# the check between the value given by the user
# and the minimum value between two snapshots is done later in this script
# initialisation of the length of the time-window for the smoothing
param['l_smooth'] = None
print('Expected value: positive integer or float')
print('If the value is smaller than delay between two snapshots,')
print('the value will be adapted to this delay')
while (not isinstance(param['l_smooth'], float)
       or param['l_smooth'] < 0):
    try:
        param['l_smooth'] = float(input('longueur fenetre smooth (s): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   #################')
print('   ### l_impulse ###')
print('   #################')
# criteria for selection of stations
# The purpose of this criteria is to remove stations with high energy content
# late in time compared to the arrival time of the considered phase
# typical stations with long coda, site effects...
# ratioSP is a duration in second
# the reference point in time is the arrival time of the considered phase 't0'
# the energy between t0 and t0 + l_impulse
# is compared to all the energy after t0
# if it is above a certain quantity (defined in the associated script)
# the station is kept, otherwise no
# initialisation of the length of 'impulsive signal'
param['l_impulse'] = None
print('Expected value: strictly positive integer or float')
print('Too small values are non sense')
while (not isinstance(param['l_impulse'], float)
       or param['l_impulse'] <= 0):
    try:
        param['l_impulse'] = float(input('longueur fenetre impulse (s): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   #################')
print('   ### angle_min ###')
print('   #################')
# stations can be selected depending on their orientation (azimuth) from the
# hypocenter
# the angle is equal to 0 in the North direction and is counted clockwise
# by symetry, only angles from 0 to 180 are considered
# for instance, if the selected azimuth band is the following: 0 -> 30 deg;
# then, stations with corresponding azimuth between 180 + 0 and 180 + 30 deg
# will also be considered
# initialisation of the minimum angle for the azimuth selection
param['angle_min'] = None
print('Expected value: positive integer of float between up to 180 deg')
print('0 deg is North, counting clockwise')
print('The other angle, by point(hypocenter) reflection, will be also considered')
while (not isinstance(param['angle_min'], float)
       or param['angle_min'] < 0
       or param['angle_min'] >= 180):
    try:
        param['angle_min'] = float(input('angle_min (sens horaire) [0 -> 180]: '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   #################')
print('   ### angle_max ###')
print('   #################')
# initialisation of the maximum angle for the azimuth selection
param['angle_max'] = None
print('Expected value: positive integer or float between angle_min(previous value) and 180 deg')
print('0 deg is North, counting clockwise')
print('The other angle, by point(hypocenter) reflection, will be also considered')
while (not isinstance(param['angle_max'], float)
       or param['angle_max'] <= param['angle_min']
       or param['angle_max'] > 180):
    try:
        param['angle_max'] = float(input('angle_max (sens horaire) [angle_min -> 180]: '))
    except ValueError:
        print('No valid number, try again')

# combination of angle_min and angle_max as angle
# for an easier creation of file/directory names
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
    print('Therefore, the smooth window length is defined again by the following value: ' + str(param['smooth']) + ' s')
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
print('                  EQ: ' + param['dossier'])
print('          Hyp. Dist.: ' + param['couronne'] + '          km')
print('          Freq. Band: ' + param['band_freq'] + '        Hz')
print('          Composante: ' + param['composante'])
print('           S/P ratio: ' + str(param['ratioSP']))
print('       Smooth window: ' + str(param['smooth']) + '            s')
print('      Impulse window: ' + str(param['impulse']) + '            s')
print('             Azimuth: ' + str(param['angle']) + '          deg')
print('              P vel.: ' + str(param['vP']) + '            km.s-1')
print('              S vel.: ' + str(param['vS']) + '            km.s-1')
print('          Used waves: ' + param['ondes_select'])
print('         Grid strike: ' + str(param['strike']) + '          deg')
print('            Grid dip: ' + str(param['dip']) + '           deg')
print('         Grid length: ' + str(param['l_fault']) + '           km')
print('          Grid width: ' + str(param['w_fault']) + '           km')
print('        Reso. length: ' + str(param['pas_l']) + '            km')
print('         Reso. width: ' + str(param['pas_w']) + '            km')
print('   Nbre bp snapshots: ' + str(param['samp_rate']) + '            s-1')
print('         Bp duration: ' + str(param['length_t']) + '           s')
