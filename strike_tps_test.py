import pickle
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

dossier = sys.argv[1]

path_origin = os.getcwd()[:-6]
path = path_origin + '/Data/Kumamoto/' + dossier

os.chdir(path)
with open('test1_stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack1 = my_depick.load()

with open('test2_stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack2 = my_depick.load()

with open('test3_stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack3 = my_depick.load()

with open('test4_stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack4 = my_depick.load()

with open('test5_stack_acc_S', 'rb') as mon_fich:
    my_depick = pickle.Unpickler(mon_fich)
    my_stack5 = my_depick.load()

my_stack = np.zeros((len(my_stack1[:, 0, 0]), len(my_stack1[0, 0, :])))
cumul = np.zeros((len(my_stack1[:, 0,0]), len(my_stack1[0, :, 0])))

for i in range(len(my_stack1[:, 0, 0])):
    print(i, '/', len(my_stack1[:, 0, 0]))
    for j in range(len(my_stack1[0, 0, :])):
        my_stack[i, j] = my_stack1[i, 10, j]/my_stack1.max() + my_stack2[i, 10, j]/my_stack2.max() + my_stack3[i, 10, j]/my_stack3.max() + my_stack4[i, 10, j]/my_stack4.max() + my_stack5[i, 10, j]/my_stack5.max()

for i in range(len(my_stack1[:, 0, 0])):
    for j in range(len(my_stack1[0, :, 0])):
        cumul[i, j] = my_stack2[i, j, int(270.96 + 1000/3)]/my_stack2.max() #+ my_stack2[i, j, int(270.96 + 1000/3)]/my_stack2.max() + my_stack3[i, j, int(270.96 + 2000/3)]/my_stack3.max() + my_stack4[i, j, int(270.96 + 3000/3)]/my_stack4.max()

fig, ax = plt.subplots(1, 1)
ax.set_xlabel('strike')
ax.set_ylabel('time (s)')
ax.imshow(np.transpose(my_stack), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax.scatter(22, 271, s=25, marker = '*', c = 'white')
ax.scatter(27, 271 + 1000/3, s=25, marker = '*', c = 'white')
ax.scatter(17, 271 + 1000/3, s=25, marker = '*', c = 'white')
ax.scatter(12, 271 + 2000/3, s=25, marker = '*', c = 'white')
ax.scatter(7, 271 + 3000/3, s=25, marker = '*', c = 'white')
#ax.scatter(2, 271 + 4000/3, s=25, marker = '*', c = 'white')
ax.axis('auto')
fig.savefig('test_sup.pdf')

fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel('strike')
ax2.set_ylabel('dip')
ax2.imshow(np.transpose(cumul), cmap = 'jet', interpolation = 'none', origin = 'lower')
ax2.scatter(22, 9, s = 25, marker = '*', c = 'white')
ax2.scatter(27, 9, s = 25, marker = '*', c = 'white')
ax2.scatter(17, 9, s = 25, marker = '*', c = 'white')
ax2.scatter(12, 9, s = 25, marker = '*', c = 'white')
ax2.scatter(7, 9, s = 25, marker = '*', c = 'white')
ax2.axis('auto')
fig2.savefig('test_plan.pdf')






