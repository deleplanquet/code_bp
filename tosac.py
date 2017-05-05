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
list_fichiers = [a for a in list_fichiers if ('ps.gz' in a) == False]

for fichier in list_fichiers:
    os.chdir(path_dossier)
    st = read(fichier)
    os.chdir(path_sac + '/' + str(dossier))
    st.write(fichier + '.sac', format='SAC')
    st2 = read(fichier + '.sac')
    st2[0].stats.sac.stla = st[0].stats.knet.stla
    st2[0].stats.sac.stlo = st[0].stats.knet.stlo
    st2[0].stats.sac.stel = st[0].stats.knet.stel
