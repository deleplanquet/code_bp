import matplotlib.pyplot as plt
import os
import sys
import pickle

dossier = sys.argv[1]
dt_type = sys.argv[2]

if dt_type != '3comp' and dt_type != 'hori' and dt_type != 'vert':
    print('ERROR TYPO')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
path_data = path + '/' + dossier + '_results'

os.chdir(path_data)

for freq in lst_frq:
    stack = None
    with open('',  'rb') as my_fch:
    	my_dpck = pickle.Unpickler(my_fch)
    	stack = my_dpck.load()

    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.imshow(stack, cmap = 'jet', interpolation = 'none', origin = 'lower')
    ax.set_aspect('auto')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    fig.savefig('.pdf')
    fig.savefig('.png')
    	



































