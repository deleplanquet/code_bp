import pickle
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Data/Kumamoto/' + dossier

os.chdir(path)
with open('stack_vel_S', 'rb') as my_fich:
    my_dep = pickle.Unpickler(my_fich)
    my_st = my_dep.load()

stack_t = np.zeros((len(my_st[:, 0, 0]), len(my_st[0, :, 0])))

for t in range(len(my_st[0, 0, :])):
    for i in range(len(my_st[:, 0, 0])):
        for j in range(len(my_st[0, :, 0])):
            stack_t[i, j] = stack_t[i, j] + my_st[i, j, t]

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('strike (km)')
ax.set_ylabel('dip (km)')
ax.imshow(np.transpose(stack_t), cmap = 'jet', interpolation = 'none', origin = 'lower', extent = [0, 56, 0, 24])
ax.axis('auto')
fig.savefig('stack_time_' + dossier + '.pdf')
