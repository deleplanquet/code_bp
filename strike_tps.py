import pickle
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Data/Kumamoto/' + dossier

os.chdir(path)
with open('stack_vel_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack_v = my_depick.load()

with open('stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack_a = my_depick.load()

mean_dip_v = np.zeros((len(my_stack_v[:, 0, 0]), len(my_stack_v[0, 0, :])))
mean_dip_a = np.zeros((len(my_stack_a[:, 0, 0]), len(my_stack_a[0, 0, :])))
print(len(my_stack_v[:, 0, 0]), len(my_stack_v[0, 0, :]))

for ix in range(len(my_stack_v[:, 0, 0])):
    for it in range(len(my_stack_v[0, 0, :])):
        for iy in range(len(my_stack_v[0, :, 0])):
            mean_dip_v[ix, it] = mean_dip_v[ix, it] + my_stack_v[ix, iy, it]/len(my_stack_v[0, :, 0])

for ix in range(len(my_stack_a[:, 0, 0])):
    for it in range(len(my_stack_a[0, 0, :])):
        for iy in range(len(my_stack_a[0, :, 0])):
            mean_dip_a[ix, it] = mean_dip_a[ix, it] + my_stack_a[ix, iy, it]/len(my_stack_a[0, :, 0])

fig_v, ax_v = plt.subplots(1, 1)
ax_v.set_xlabel('strike')
ax_v.set_ylabel('time (s)')
ax_v.imshow(np.transpose(mean_dip_v), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax_v.scatter(22, 500, s = 25, marker = '*', c = 'white')
ax_v.axis('auto')
fig_v.savefig('strike_time_' + dossier + '_vel_S.pdf')

fig_a, ax_a = plt.subplots(1, 1)
ax_a.set_xlabel('strike')
ax_a.set_ylabel('time (s)')
ax_a.imshow(np.transpose(mean_dip_a), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax_a.scatter(22, 500, s = 25, marker = '*', c = 'white')
ax_a.axis('auto')
fig_a.savefig('strike_time_' + dossier + '_acc_S.pdf')

fig_slice_v, ax_slice_v = plt.subplots(1, 1)
ax_slice_v.set_xlabel('strike')
ax_slice_v.set_ylabel('time (s)')
ax_slice_v.imshow(np.transpose(my_stack_v[:, 9, :]), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax_slice_v.scatter(22, 500, s = 25, marker = '*', c = 'white')
ax_slice_v.axis('auto')
fig_slice_v.savefig('strike_time_slice_' + dossier + '_vel_S.pdf')

fig_slice_a, ax_slice_a = plt.subplots(1, 1)
ax_slice_a.set_xlabel('strike')
ax_slice_a.set_ylabel('time (s)')
ax_slice_a.imshow(np.transpose(my_stack_a[:, 9, :]), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax_slice_a.scatter(22, 500, s = 25, marker = '*', c = 'white')
ax_slice_a.axis('auto')
fig_slice_a.savefig('strike_time_slice_' + dossier + '_acc_S.pdf')


















