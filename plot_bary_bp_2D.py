import matplotlib.pyplot as plt
import sys
import os
import pickle
import numpy as np

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

    maax = stack[:, :, :].max()
    strike = []
    dip = []
    sizes = []
    colors = []

    for it in range(int(length_t)):
    	xm = 0
    	ym = 0
    	om = 0
    	pm = 0.001
    	if stack[:, :, it].max() > 0.4*maax:
    	    for ix in range(len(stack[:, 0, 0])):
    	    	for iy in range(len(stack[0, :, 0])):
    	    	    xm = xm + stack[ix, iy, it]*ix
    	    	    ym = ym + stack[ix, iy, it]*iy
    	    	    om = stack[:, :, it].max()/maax
    	    	    pm = pm + stack[ix, iy, it]
    	#if pm != 0:
    	strike.append(2*xm/pm)
    	dip.append(2*ym/pm)
    	sizes.append(om*50)
    	colors.append(it/length_t)

    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Strike (km)')
    ax.set_ylabel('Dip (km)')
    ax.scatter(strike, dip, s = sizes, c = colors, edgecolors = 'none')
    ax.set_xlim(0, 56)
    ax.set_ylim(0, 24)

    fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_bary.png')
    fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_bary.pdf')
