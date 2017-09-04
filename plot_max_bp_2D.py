import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pickle

dossier = sys.argv[1]
dt_type = sys.argv[2]

if dt_type != '3comp' and dt_type != 'hori' and dt_type != 'vert':
    print('ERROR TYPO')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
path_data = path + '/' + dossier + '_results'

length_t = int(30*100)

os.chdir(path_data)
for freq in lst_frq:
    print('     ', freq)
    stack = None
    with open(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D', 'rb') as my_fch:
    	my_dpck = pickle.Unpickler(my_fch)
    	stack = my_dpck.load()

    dip = []
    strike = []
    sizes = []
    colors = []
    for it in range(int(length_t)):
    	dip.append(np.where(stack == stack[:, :, it].max())[0])
    	strike.append(np.where(stack == stack[:, :, it].max())[1])
    	sizes.append(pow(5*stack[:, :, it].max()/stack[:, :, :].max(), 3))
    	colors.append(it/length_t)

    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Dip (km)')
    ax.set_ylabel('Strike (km)')
    ax.scatter(dip, strike, s = sizes, c = colors, edgecolors = 'none')
    #for it in range(int(length_t)):
    	#ax.scatter(it/len(stack[:, 0, 0]), it/len(stack[0, :, 0]), c = it/length_t, edgecolors = 'none')
    	#ax.scatter(np.where(stack == stack[:, :, it].max())[0], np.where(stack == stack[:, :, it].max())[1], s = 50*stack[:, :, it].max()/stack[:, :, :].max(), c = length_t, edgecolors = 'none')
    	#print(it/length_t)

    ax.set_xticklabels([0, 0, 4, 8, 12, 16, 20])
    ax.set_yticklabels([0, 0, 10, 20, 30, 40, 50])

    fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_max.png')
    fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_max.pdf')
