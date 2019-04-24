# convert traces into SAC format
# possible warning you may encounter are because some part of the original
# header can not be converted to SAC header. In the case some of them are still
# needed, it has to be coded explicitly here

#!/usr/bin/env python
import sys
from obspy import read
import os
import obspy.io.sac
import pickle

print('############################',
    '\n###   python3 tosac.py   ###',
    '\n############################')

# open the file of the parameters given by the user through parameters.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used, only the following one
event = param['event']

# path_kik and path_knt are the locations of original files (traces) for both
# networks
path_kik = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'brut/'
            + event + '.kik')
path_knt = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'brut/'
            + event + '.knt')
# path_sac is the target directory after conversion of the traces to SAC
path_sac = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'acc/'
            + 'brut')

# create the directory path_sac in case it does not exist
if not os.path.isdir(path_sac):
    try:
        os.makedirs(path_sac)
    except OSError:
        print('Creation of the directory %s failed' %path_sac)
    else:
        print('Successfully created the directory %s' %path_sac)
else:
    print('%s is alrealy existing' %path_sac)

# make a list of files from KiK-net network
# pictures (ps.gz files) are also provided inside the same folder but we do not
# want to take them into account
list_files = os.listdir(path_kik)
list_files = [a for a in list_files if 'ps.gz' not in a]

# change format of those files into SAC format and save them in path_sac
for s in list_files:
    os.chdir(path_kik)
    tr = read(s)[0]
    tr.stats.sac = tr.stats.knet
    os.chdir(path_sac)
    tr.write(s[:6] + s[16:] + '.sac', format='SAC')

# make a list of files from K-NET network
# pictures (ps.gz files) are also provided inside the same folder but we do not
# want to take them into account
list_files = os.listdir(path_knt)
list_files = [a for a in list_files if 'ps.gz' not in a]

# change format of those files into SAC format and save them in path_sac
for s in list_files:
    os.chdir(path_knt)
    tr = read(s)[0]
    tr.stats.sac = tr.stats.knet
    os.chdir(path_sac)
    tr.write(s[:6] + s[16:] + '.sac', format='SAC')
