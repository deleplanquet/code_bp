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
print('The other angle, by point(hypocenter) reflection, will be also '
        + 'considered')
while (not isinstance(param['angle_min'], float)
       or param['angle_min'] < 0
       or param['angle_min'] >= 180):
    try:
        param['angle_min'] = float(input('angle_min (sens horaire) '
                                            + '[0 -> 180]: '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   #################')
print('   ### angle_max ###')
print('   #################')
# initialisation of the maximum angle for the azimuth selection
param['angle_max'] = None
print('Expected value: positive integer or float between angle_min '
        + '(previous value) and 180 deg')
print('0 deg is North, counting clockwise')
print('The other angle, by point(hypocenter) reflection, will be also '
        + 'considered')
while (not isinstance(param['angle_max'], float)
       or param['angle_max'] <= param['angle_min']
       or param['angle_max'] > 180):
    try:
        param['angle_max'] = float(input('angle_max (sens horaire) '
                                            + '[angle_min -> 180]: '))
    except ValueError:
        print('No valid number, try again')

# combination of angle_min and angle_max as angle
# for an easier creation of file/directory names
param['angle'] = (str(int(param['angle_min'])) + '-'
                    + str(int(param['angle_max'])))

print('')
print('   ##########')
print('   ### vP ###')
print('   ##########')
# velocity of P-waves
param['vP'] = None
print('Expected value: strictly positive integer or float in km.s-1')
while (not isinstance(param['vP'], float)
       or param['vP'] <= 0):
    try:
        param['vP'] = float(input('vitesse des ondes P (km/s) (5.8?): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ##########')
print('   ### vS ###')
print('   ##########')
# velocity of S-waves
param['vS'] = None
print('Expected value: strictly positive integer of float in km.s-1')
print('Of course P-waves are faster so value should be smaller than vP '
        + '(previous value)')
while (not isinstance(param['vS'], float)
       or param['vS'] <= 0
       or param['vS'] >= param['vP']):
    try:
        param['vS'] = float(input('vitesse des ondes S (km/s) (3.4?): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ######################')
print('   ### selected_waves ###')
print('   ######################')
# bp process needs assumption on the velocity waves
# the velocity of P and S-waves are asked just before
# here the choice between one of them has to be done
# the two velocities are asked for secondary plots
param['selected_waves'] = None
print('Expected value: > P < or > S <')
print('Other values are not accepted')
while (param['selected_waves'] != 'P'
       and param['selected_waves'] != 'S'):
    try:
        param['selected_waves'] = input('hypothese de bp [P/S]: ')
    except ValueError:
        print('No valid number, try again')

print('')
print('   ##############')
print('   ### strike ###')
print('   ##############')
# the bp process needs a grid assumption
# the grid is defined by the following parameters
# - strike: like a real fault, the grid has a strike angle counted clockwise
# from the North
# - dip: like a real fault, the grid has a dip angle counted from 0 to 90
# degres with 0 for an horizontal grid and 90 for a vertical one
# - length: the length of the grid in the direction of the strike
# - width: the length of the grid in the direction of the dip
# - discretization values in both direction: more details below
# the position of the grid is not asked, the grid will always be centered at
# the hypocenter position. The purpose of this study is to image the complexity
# during a rupture, not to locate an eqrthquake
param['strike'] = None
print('Strike direction of the grid')
print('Expected value: positive integer or float up to 360 deg')
print('0 deg is North, counting clockwise')
print('Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/04/16 '
        + 'Kumamoto EQ')
while (not isinstance(param['strike'], float)
       or param['strike'] < 0
       or param['strike'] >= 360):
    try:
        param['strike'] = float(input('strike (224?): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ###########')
print('   ### dip ###')
print('   ###########')
# as explained above, the bp process needs a grid assumption
# the dip is one of the parameter to define the grid
# its value should be between 0 and 90 degres with 0 for an horizontal grid and
# 90 for a vertical one
param['dip'] = None
print('Dip direction of the grid')
print('Expected value: positive integer or float up to 90 deg')
print('0 deg is horizontal fault plane, 90 deg is vertical one')
print('Kubo 2016: strike 224 deg, dip 65 deg for Mw 7.1 2016/;04/16 '
        + 'Kumamoto EQ')
while (not isinstance(param['dip'], float)
       or param['dip'] <= 0
       or param['dip'] > 90):
    try:
        param['dip'] = float(input('dip (65?): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ###############')
print('   ### l_grid ###')
print('   ###############')
# the bp process needs a grid assumption
# the length in the strike direction (cf strike above) is one of the parameter
# because the grid will be centered at the hypocenter location, the extension
# of the grid will be half of the length in the strike direction on the two
# sides of the hypocenter
param['l_grid'] = None
print('Length of the grid, that means in the direction of the strike')
print('Width can be bigger than length, no restriction')
print('Expected value: stricly positive integer or float in km')
print('No matter the length, hypocenter is always at the center')
while (not isinstance(param['l_grid'], float)
       or param['l_grid'] <= 0):
    try:
        param['l_grid'] = float(input('longueur grid (km) '
                                        + '(dans la direction du strike): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ###############')
print('   ### w_grid ###')
print('   ###############')
# the bp process needs a grid assumption
# the width, ie the length in the dip direction (cf dip above) is one of the
# parameter
# because the grid will be centered at the hypocenter location, the extension
# of the grid will be half of the width in the dip direction on the two sides
# of the hypocenter. It is possible to have a part of the grid which is above
# the surface if the value of the width is too high. The value is not checked
# for those kind of situations and the bp process is still feasible. However,
# energy retrieved above the surface, if there is, does not have any physical
# meaning
param['w_grid'] = None
print('Width of the grid, that means in the direction of the dip')
print('Width can be bigger than length, no restriction')
print('Expected value: stricly positive integer or float in km')
print('No matter the width, hypocenter is always at the center')
print('due to that, some points of the grid may be above the surface')
while (not isinstance(param['w_grid'], float)
       or param['w_grid'] <= 0):
    try:
        param['w_grid'] = float(input('largeur grid (km) '
                                        + '(dans la direction du dip): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ####################')
print('   ### l_grid_step ###')
print('   ####################')
# the bp process needs a grid assumption
# the length of the grid has been defined above but size of each subgrid has to
# be defined. The shape of a subgrid is generally rectangular (may be square
# shape in the case the two values are equal in the both direction). The length
# of the subgrid in both direction (strike and dip) is asked independently
# not sure what happens if the number of subgrids is not integer
param['l_grid_step'] = None
print('Length of each subgrid in the direction of the strike')
print('Expected value: strictly positive integer of float in km')
print('Should be smaller than l_grid to have at least few points')
while (not isinstance(param['l_grid_step'], float)
       or param['l_grid_step'] <= 0
       or param['l_grid_step'] >= param['l_grid']):
    try:
        param['l_grid_step'] = float(input('pas longueur grid (km): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ####################')
print('   ### w_grid_step ###')
print('   ####################')
# the bp process needs a grid assumption
# the length in the dip direction of each subgrid is one of the parameter
# not sure what happens if the number of subgrids is not integer
param['w_grid_step'] = None
print('Width of each subgrid in the direction of the dip')
print('Expected value: strictly positive integer or float in km')
print('Should be smaller than w_grid to have at least few points')
while (not isinstance(param['w_grid_step'], float)
       or param['w_grid_step'] <= 0
       or param['w_grid_step'] >= param['w_grid']):
    try:
        param['w_grid_step'] = float(input('pas largeur grid (km): '))
    except ValueError:
        print('No valid number, try again')

print('')
print('   ####################')
print('   ### bp_samp_rate ###')
print('   ####################')
# the bp process is providing an image in space (on the grid) and in time of
# an earthquake. The frequency of those images does not need to be high, only
# few images per second (typically 5 to 10) is quite enough. Also, as mentioned
# earlier (cf l_smooth), the length of the time-window for the smoothing of the
# traces has to be at least the delay between two snapshots of bp. In the case
# this condition is not verified, the value of l_smooth is modified to fit
# exactly the delay between two snapshots of bp
param['bp_samp_rate'] = None
print('Number of snapshots per sec')
print('Expected value: strictly positive integer or float below 100 '
        + '(station sampling rate))')
print('Suggested values are between 0.5 and 10')
while (not isinstance(param['bp_samp_rate'], float)
       or param['bp_samp_rate'] > 100
       or param['bp_samp_rate'] <= 0):
    try:
        param['bp_samp_rate'] = float(input('nombre d images de bp par '
                                            + 'seconde (inferieur a 100): '))
    except ValueError:
        print('No valid number, try again')

# check about the condition explained just above where l_smooth has to be
# greater or equal to the dealy between two snapshots
if 1./param['bp_samp_rate'] > param['l_smooth']:
    print('')
    print('##################################################################')
    print('Input value for smooth window length was: '
            + str(param['l_smooth']) + ' s')
    print('However,  the delay between two bp snapshots is higher: '
            + str(1./param['bp_samp_rate']) + ' s')
    param['l_smooth'] = 1./param['bp_samp_rate']
    print('Therefore, the smooth window length is defined again by the '
            + 'following value: ' + str(param['l_smooth']) + ' s')
    print('##################################################################')

print('')
print('   ######################')
print('   ### bp_length_time ###')
print('   ######################')
# the bp process does not have any limitation in space nor in time. However,
# it is limited by user on the grid for the space because the zone of interest
# is closed to the hypocenter (the grid is centered on the hypocenter). As for
# the time, the user is limiting with the parameter bp_length_time the duration
# of the bp process. The beginning is defined and can't be modified (here) at 5
# seconds before the beginning of the rupture, the end is deduced from this
# value of the beginning and the length in time of the bp process given by the
# user. Obviously, the user has to give a value greater than 5 and this value
# depends on the magnitude of the considered eqrthquake, the bigger the Eq is,
# the longer should be the duration of the bp process
param['bp_length_time'] = None
print('Period of back projection, from 5 seconds before the start of the '
        + 'rupture')
print('Expected value: integer or float between 5 and 50 sec')
print('Suggested values are between 10 and 30 sec')
print('For Mw ~6~ 20 sec')
print('For Mw ~7~ 30 sec')
while (not isinstance(param['bp_length_time'], float)
       or param['bp_length_time'] <= 5
       or param['bp_length_time'] >= 50):
    try:
        param['bp_length_time'] = float(input('duree de la bp (> 5 sec): '))
    except ValueError:
        print('No valid number, try again')

# from there, just save in different formats and in different folders the
# parameters given by the user
# binary format file is to be used later by other scripts
# txt format file is for user in case he wants to check the choosen parameters
# later

hyp_int = param['hypo_interv']
frq_bnd = param['frq_band']
cpnt = param['component']
waves = param['selected_waves']
azim = param['angle']

path = (param['root_folder'] + '/'
        + 'Kumamoto')

path1 = (param['root_folder'] + '/'
        + 'Kumamoto/'
        + 'historique_parametres')

path2 = (param['root_folder'] + '/'
         + 'Kumamoto/'
         + param['event'] + '/'
         + 'results/'
         + 'vel_' + hyp_int + 'km_' + frq_bnd + 'Hz_' + cpnt + '_env_smooth_'
                + waves + '/'
         + azim + 'deg')

lst_pth = [path, path1, path2]

for i in [path1, path2]:
    if not os.path.isdir(i):
        try:
            os.makedirs(i)
        except OSError:
            print('Creation of the directory %s failed' %i)
        else:
            print('Successfully created the directory %s' %i)
    else:
        print('%s is already existing' %i)

os.chdir(path)
with open('parametres_bin', 'wb') as my_exit:
    my_pck = pickle.Pickler(my_exit)
    my_pck.dump(param)

yy = str(datetime.datetime.now().year)
mm = str(datetime.datetime.now().month)
dd = str(datetime.datetime.now().day)
hh = str(datetime.datetime.now().hour)
mi = str(datetime.datetime.now().minute)
ss = str(datetime.datetime.now().second)

while len(yy) < 4:
    yy = '0' + yy
while len(mm) < 2:
    mm = '0' + mm
while len(dd) < 2:
    dd = '0' + dd
while len(hh) < 2:
    hh = '0' + hh
while len(mi) < 2:
    mi = '0' + mi
while len(ss) < 2:
    ss = '0' + ss

for ppth in lst_pth:
    if ppth == lst_pth[0]:
        paparam = 'current_parametres.txt'
    else:
        paparam = 'parametres_' + yy + mm + dd + '-' + hh + mi + ss + '.txt'
    os.chdir(ppth)
    with open(paparam, 'w') as my_ext:
        my_ext.write('     root folder: ' + param['root_folder']
                                            + '\n')
        my_ext.write('           event: ' + param['event']
                                            + '\n')
        my_ext.write('    Earth radius: ' + str(param['R_Earth'])
                                            + ' km\n')
        my_ext.write('     hypo interv: ' + param['hypo_interv']
                                            + ' km\n')
        my_ext.write('  frequency band: ' + param['frq_band']
                                            + ' Hz\n')
        my_ext.write('       component: ' + param['component']
                                            + '\n')
        my_ext.write('       ratio S/P: ' + str(param['ratioSP'])
                                            + '\n')
        my_ext.write('   smooth window: ' + str(param['l_smooth'])
                                            + ' s\n')
        my_ext.write('  impulse window: ' + str(param['l_impulse'])
                                            + ' s\n')
        my_ext.write('  azimuth window: ' + param['angle']
                                            + ' deg\n')
        my_ext.write('      P velocity: ' + str(param['vP'])
                                            + ' km/s # 5.8\n')
        my_ext.write('      S velocity: ' + str(param['vS'])
                                            + ' km/s # 3.4\n')
        my_ext.write('   bp hypothesis: ' + param['selected_waves']
                                            + '\n')
        my_ext.write('     grid strike: ' + str(param['strike'])
                                            + ' deg # 224 for mainshock '
                                            + 'from Kubo et al. (2016)\n')
        my_ext.write('        grid dip: ' + str(param['dip']) + ' deg '
                                            + '# 65 for mainshock from '
                                            + 'Kubo et al. (2016)\n')
        my_ext.write('     length grid: ' + str(param['l_grid'])
                                            + ' km\n')
        my_ext.write('      width grid: ' + str(param['w_grid'])
                                            + ' km\n')
        my_ext.write('length grid step: ' + str(param['l_grid_step'])
                                            + ' km\n')
        my_ext.write(' width grid step: ' + str(param['w_grid_step'])
                                            + ' km\n')
        my_ext.write('bp sampling rate: ' + str(param['bp_samp_rate'])
                                            + ' im/s\n')
        my_ext.write('     bp duration: ' + str(param['bp_length_time'])
                                            + ' s\n')
        
# finally, a resume of the selected parameters is printed in the terminal
print('')
print('')
print('      You have defined the following parameters:')
print('                 EQ: ' + param['event'])
print('         Hyp. Dist.: ' + param['hypo_interv']
                                + '          km')
print('         Freq. Band: ' + param['frq_band']
                                + '        Hz')
print('         Composante: ' + param['component'])
print('          S/P ratio: ' + str(param['ratioSP']))
print('      Smooth window: ' + str(param['l_smooth'])
                                + '            s')
print('     Impulse window: ' + str(param['l_impulse'])
                                + '            s')
print('            Azimuth: ' + str(param['angle'])
                                + '          deg')
print('             P vel.: ' + str(param['vP'])
                                + '            km.s-1')
print('             S vel.: ' + str(param['vS'])
                                + '            km.s-1')
print('         Used waves: ' + param['selected_waves'])
print('        Grid strike: ' + str(param['strike'])
                                + '          deg')
print('           Grid dip: ' + str(param['dip'])
                                + '           deg')
print('        Grid length: ' + str(param['l_grid'])
                                + '           km')
print('         Grid width: ' + str(param['w_grid'])
                                + '           km')
print('       Reso. length: ' + str(param['l_grid_step'])
                                + '            km')
print('        Reso. width: ' + str(param['w_grid_step'])
                                + '            km')
print('  Nbre bp snapshots: ' + str(param['bp_samp_rate'])
                                + '            s-1')
print('        Bp duration: ' + str(param['bp_length_time'])
                                + '           s')
