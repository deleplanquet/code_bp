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
path_data = path + '/' + dossier + '_vel_2_4Hz_' + tp_data + '_env_results'

os.chdir(path_data)
with open('stack_vel_2_4Hz_' + tp_data + '_env', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time')
ax.set_ylabel('Strike')
ax.imshow(stack, cmap = 'jet', interpolation = 'none', origin = 'lower')
ax.set_aspect('auto')

fig.savefig('bp_vel_2_4Hz_' + tp_data + '_env.pdf')




















