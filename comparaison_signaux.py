from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from obspy import read
import numpy as np
import os

path = '/media/deleplanque/Lexar'
path_data = path + '/Data/Kumamoto'

path_results = '/home/deleplanque/Documents/back_proj/en_cours/Results'

list_dossier = os.listdir(path_data)
list_dossier = [a for a in list_dossier if ('.tar' in a) == False]

print(len(list_dossier))

list_fichier = []

for dossier in list_dossier:
    print(dossier, str(list_dossier.index(dossier) + 1), '/', len(list_dossier))
    path_fichier = path_data + '/' + str(dossier) + '/' + str(dossier) + '.kik'
    os.chdir(path_fichier)
    list_fichier_temp = os.listdir(path_fichier)
    list_fichier_temp = [a for a in list_fichier_temp if ('ps.gz' in a) == False]
    list_fichier_temp2 = []
    for fichier in list_fichier_temp:
    	st = read(fichier)
    	if st[0].stats.knet.mag >= 5:
    	    break
    	if st[0].stats.channel == 'NS1':
    	    list_fichier_temp2.append([fichier, 'kik'])
    path_fichier = path_data + '/' + str(dossier) + '/' + str(dossier) + '.knt'
    os.chdir(path_fichier)
    list_fichier_temp = os.listdir(path_fichier)
    list_fichier_temp = [a for a in list_fichier_temp if ('ps.gz' in a) == False]
    for fichier in list_fichier_temp:
    	st = read(fichier)
    	if st[0].stats.knet.mag >= 5:
    	    break
    	if st[0].stats.channel == 'NS':
    	    list_fichier_temp2.append([fichier, 'knt'])
    list_fichier.append(list_fichier_temp2)

print(len(list_fichier))

lat_fault = [32.65, 32.86]
long_fault = [130.72, 131.07]

fig, ax = plt.subplots(1, 1)
m = Basemap(projection='merc',
    	    llcrnrlon=128,
    	    llcrnrlat=30,
    	    urcrnrlon=134,
    	    urcrnrlat=35,
    	    resolution='i')
x_fault, y_fault = m(long_fault, lat_fault)
m.drawcoastlines(linewidth=0.2)
m.fillcontinents('yellow')
m.drawparallels(np.arange(30, 35, 1),
    	    	labels=[1, 0, 0, 0],
    	    	linewidth=1)
m.drawmeridians(np.arange(128, 134, 1),
    	    	labels=[0, 0, 0, 1],
    	    	linewidth=1)
ax.plot(x_fault,
    	y_fault,
    	color='green',
    	linewidth = 0.3,
    	zorder = 1)

print(list_fichier[:][0])
cpt = 1

for fichier in list_fichier:
    print(fichier)
    if fichier != []:
    	print('prout')
    	os.chdir(path_data + '/' + str(list_dossier[list_fichier.index(fichier)]) + '/' + str(list_dossier[list_fichier.index(fichier)]) + '.' + fichier[0][1])
    	st = read(fichier[0][0])
    	if st[0].stats.knet.mag < 5:
    	    x_epi, y_epi = m(st[0].stats.knet.evlo, st[0].stats.knet.evla)
    	    ax.scatter(x_epi,
    	    	       y_epi,
    	    	       3,
    	    	       marker = '*',
    	    	       color = 'black',
    	    	       zorder = 2)
    cpt = cpt + 1

os.chdir(path_results)
fig.savefig('map.pdf')
