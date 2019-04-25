#

from obspy import read
from obspy import Trace
import os
import sys
import math
import numpy as np
import pickle

print('##################################',
    '\n###   python3 3components.py   ###',
    '\n##################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
couronne = param['hypo_interv']
frq_bnd = param['frq_band']

# directories used in this script
# - path_data is the directory with all the velocity waveforms that passed
# previous conditions
path_data = (root_folder + '/'
             + 'Kumamoto/'
             + event + '/'
             + 'vel/'
             + couronne + 'km_' + frq_bnd + 'Hz')
# - path_rslt is the list of directories where different combinations of the
# three original components (EW, NS and UD) will be stored
# -- 3 cpn is a combination of the 3 components (EW, NS and UD)
# -- hori is a combination of the 2 horizontal components (EW and NS)
# -- vert is the vertical component only (UD)
cpnt = ['3cpn', 'hori', 'vert']
path_r = (root_folder + '/'
          + 'Kumamoto/'
          + event + '/'
          + 'vel/')
path_rslt = []
for cpn in cpnt:
    path_rslt.append(path_r + couronne + 'km_' + frq_bnd + 'Hz_' + cpn)

# create the directories from the list path_rslt in case they do not exist
for pth in path_rslt:
    if not os.path.isdir(pth):
        try:
            os.makedirs(pth)
        except OSError:
            print('Creation of the directory {} failed'.format(pth))
        else:
            print('Successfully created the directory {}'.format(pth))
    else:
        print('{} is already existing'.format(pth))

# pick separately the stations depending on their component (EW, NS or UD)
lst_fch_x = [a for a in os.listdir(path_data) if 'EW' in a]
lst_fch_y = [a for a in os.listdir(path_data) if 'NS' in a]
lst_fch_z = [a for a in os.listdir(path_data) if 'UD' in a]

# sort the three lists so the n-element of each list is corresponding to the
# same station but for the three components
lst_fch_x.sort()
lst_fch_y.sort()
lst_fch_z.sort()

for sx, sy, sz in zip(lst_fch_x, lst_fch_y, lst_fch_z):
    os.chdir(path_data)
    stx = read(sx)
    sty = read(sy)
    stz = read(sz)
    if (stx[0].stats.station == sty[0].stats.station
        and stx[0].stats.station == stz[0].stats.station):
        #
        stx.detrend(type = 'constant')
        sty.detrend(type = 'constant')
        stz.detrend(type = 'constant')
        #
        tr_x = stx[0]
        tr_y = sty[0]
        tr_z = stz[0]
        #
        tr3 = [math.sqrt(a**2 + b**2 + c**2)
               for a, b, c in zip(tr_x, tr_y, tr_z)]
        trh = [math.sqrt(a**2 + b**2) for a, b in zip(tr_x, tr_y)]
        trv = [math.sqrt(a**2) for a in tr_z]
        #
        tr3 = Trace(np.asarray(tr3), stz[0].stats)
        trh = Trace(np.asarray(trh), stz[0].stats)
        trv = Trace(np.asarray(trv), stz[0].stats)
        #
        os.chdir(path_rslt[0])
        tr3.write(sx[:7] + cpnt[0] + sx[9:], format = 'SAC')
        os.chdir(path_rslt[1])
        trh.write(sx[:7] + cpnt[1] + sx[9:], format = 'SAC')
        os.chdir(path_rslt[2])
        trv.write(sx[:7] + cpnt[2] + sx[9:], format = 'SAC')
    else:
        print('Problem')
#for station in lst_fch_x:
#    os.chdir(pth_dt)
#    stx = read(station)
#    sty = read(lst_fch_y[lst_fch_x.index(station)])
#    stz = read(lst_fch_z[lst_fch_x.index(station)])
#    if stx[0].stats.station == sty[0].stats.station and stx[0].stats.station == stz[0].stats.station:
#        stx.detrend(type = 'constant')
#        sty.detrend(type = 'constant')
#        stz.detrend(type = 'constant')
#        tr_x = stx[0]
#        tr_y = sty[0]
#        tr_z = stz[0]
#        trh = [math.sqrt(a**2 + b**2) for a,b in zip(tr_x, tr_y)]
#        tr3 = [math.sqrt(a**2 + b**2 + c**2) for a,b,c in zip(tr_x, tr_y, tr_z)]
#        os.chdir(pth_rslt_v)
#        trv = Trace(np.asarray(tr_z), stz[0].stats)
#        trv.write(station[:6]
#                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_vert.sac', format = 'SAC')
#        os.chdir(pth_rslt_h)
#        trh = Trace(np.asarray(trh), stz[0].stats)
#        trh.write(station[:6]
#                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_hori.sac', format = 'SAC')
#        os.chdir(pth_rslt)
#        tr3 = Trace(np.asarray(tr3), stz[0].stats)
#        tr3.write(station[:6]
#                  + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz.sac', format = 'SAC')
#    else:
#        print('     ', stx[0].stats.station, sty[0].stats.station, stz[0].stats.station)
