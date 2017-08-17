import matplotlib.pyplot as plt
import os
import sys
import pickle

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_pth_dt = path + '/' + dossier + '_vel_results'

os.chdir(lst_pth_dt)
with open('stack_vel_env', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('Time')
ax.set_ylabel('Strike')
ax.imshow(stack, cmap = 'jet', interpolation = 'none', origin = 'lower')
ax.set_aspect('auto')

fig.savefig('bp_vel_env.pdf')




















