import numpy as np
import math
import cmath
import matplotlib.pyplot
import os

#recuperation position stations
path = '/home/deleplanque/Documents/back_proj/en_cours'
dossier_seisme = '20160414212600'
path1 = path + '/data_kumamoto/' + dossier_seisme + '/' + dossier_seisme + '.kik'
path2 = path + '/data_kumamoto/' + dossier_seisme + '/' + dossier_seisme + '.knt'
list_fichier1 = os.listdir(path1)
list_fichier2 = os.listdir(path2)
list_fichier1 = [a for a in list_fichier1 if ('ps.gz' in a) == False]
list_fichier2 = [a for a in list_fichier2 if ('ps.gz' in a) == False]

info_stations = [('Origin Date',
		  'Origin Time',
		  'Lat.',
		  'Long.',
		  'Depth (km)',
		  'Mag.',
		  'Network',
		  'Station Code',
		  'Station Lat.',
		  'Station Long.',
		  'Station Height (m)',
		  'Record Date',
		  'Record Time',
		  'Sampling Freq (Hz)',
		  'Duration Time (s)',
		  'Dir.',
		  'Scale Factor',
		  'Max. Acc. (gal)',
		  'Last Correction Date',
		  'Last Correction Time'
		 )]

for fichier in list_fichier1:
    data = open(path1 + '/' + fichier, 'r')
    contenu = data.read()
    info = contenu.split('Memo')[0]
    info = info.split('\n')
    info_stations.append((info[0].split(' ')[8],
                          info[0].split(' ')[9],
                          info[1].split(' ')[14],
                          info[2].split(' ')[13],
		          info[3].split(' ')[8],
		          info[4].split(' ')[14],
		          'KiK-net',
		          info[5].split(' ')[7],
		          info[6].split(' ')[7],
		          info[7].split(' ')[6],
		          info[8].split(' ')[2],
                          info[9].split(' ')[8],
                          info[9].split(' ')[9],
                          info[10].split(' ')[2],
                          info[11].split(' ')[3],
                          info[12].split(' ')[14],
                          info[13].split(' ')[6],
                          info[14].split(' ')[5],
                          info[15].split(' ')[4],
                          info[15].split(' ')[5]
			 ))
    data.close()

for fichier in list_fichier2:
    date = open(path2 + '/' + fichier, 'r')
    contenu = date.read()
    info = contenu.split('Memo')[0]
    info = info.split('\n')
    info_stations.append((info[0].split(' ')[8],
                          info[0].split(' ')[9],
                          info[1].split(' ')[14],
                          info[2].split(' ')[13],
                          info[3].split(' ')[8],
                          info[4].split(' ')[14],
                          'K-NET',
                          info[5].split(' ')[7],
                          info[6].split(' ')[7],
                          info[7].split(' ')[6],
                          info[8].split(' ')[2],
                          info[9].split(' ')[8],
                          info[9].split(' ')[9],
                          info[10].split(' ')[2],
                          info[11].split(' ')[3],
                          info[12].split(' ')[14],
                          info[13].split(' ')[6],
                          info[14].split(' ')[5],
                          info[15].split(' ')[4],
                          info[15].split(' ')[5]
                         ))
    data.close()

print info_stations

#recuperation position faille

#calcul matrice temps de trajet

#ARF figures

#stacks

#plots
