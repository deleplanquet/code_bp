#!/usr/bin/env python
import sys
from obspy import read
import os
import obspy.io.sac
import pickle

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']

path = path_origin + '/Data/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_brut'
path_kik = path_data + '/' + dossier + '.kik'
path_knt = path_data + '/' + dossier + '.knt'
path_sac = path_origin + '/Kumamoto/' + dossier + '/' + dossier + '_sac'

if os.path.isdir(path_sac) == False:
    os.makedirs(path_sac)

list_fichiers = os.listdir(path_kik)
list_fichiers = [a for a in list_fichiers if ('ps.gz' in a) == False]

for fichier in list_fichiers:
    os.chdir(path_kik)
    tr = read(fichier)[0]
    tr.stats.sac = tr.stats.knet
    os.chdir(path_sac)
    tr.write(fichier + '.sac', format='SAC')

list_fichiers = os.listdir(path_knt)
list_fichiers = [a for a in list_fichiers if ('ps.gz' in a) == False]

for fichier in list_fichiers:
    os.chdir(path_knt)
    tr = read(fichier)[0]
    tr.stats.sac = tr.stats.knet
    os.chdir(path_sac)
    tr.write(fichier + '.sac', format='SAC')

