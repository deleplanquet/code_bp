#!/usr/bin/env python
import sys
from obspy import read
import os

path_data = '/localstorage/deleplanque/Data/Kumamoto'
path_sac = '/localstorage/deleplanque/Data/Kumamoto_sac'
os.chdir(path_sac)

dossier = sys.argv[1]
ext = dossier[-4:]
dossier = dossier[0:-4]

if os.path.isdir(str(dossier)) == False:
    os.makedirs(str(dossier))

path_dossier = path_data + '/' + str(dossier) + '/' + str(dossier) + str(ext)

list_fichiers = os.listdir(path_dossier)
if ext == '.kik':
    list_fichiers = [a for a in list_fichiers if '.NS2' in a]
else:
    list_fichiers = [a for a in list_fichiers if '.UD' in a]

for fichier in list_fichiers:
    os.chdir(path_dossier)
    tr = read(fichier)[0]
    os.chdir(path_sac + '/' + str(dossier))
    tr.write(fichier + '.sac', format='SAC')
