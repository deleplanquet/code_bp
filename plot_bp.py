import matplotlib.pyplot as plt
import os
import sys
import pickle

dossier = sys.argv[1]
tp_data = sys.argv[2]

if tp_data != '3comp' and tp_data != 'hori' and tp_data != 'vert':
    print('ERROR TYPO')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
lst_pth_dt = []

for freq in lst_frq:
    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz_' + tp_data + '_env_results')

for freq in lst_frq:
    stack = None
    os.chdir(lst_pth_dt[lst_frq.index(freq)])
    with open('stack_vel_' + freq + 'Hz_' + tp_data + '_env', 'rb') as my_fch:
    	my_dpck = pickle.Unpickler(my_fch)
    	stack = my_dpck.load()

    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Strike')
    ax.imshow(stack, cmap = 'jet', interpolation = 'none', origin = 'lower')
    ax.set_aspect('auto')

    fig.savefig('bp_vel_' + freq + 'Hz_' + tp_data + '_env.pdf')




















