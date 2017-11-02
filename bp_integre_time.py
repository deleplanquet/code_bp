import pickle
import matplotlib.pyplot as plt
import numpy as np
import os


dossier = '20160414212600'

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier



os.chdir(path + '/' + dossier + '_results')
with open(dossier + '_vel_4_8Hz_hori_env_smooth_S_stack2D', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()


length_t = 10
stack_temp0 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp1 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp2 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp3 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp4 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp5 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp6 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))
stack_temp7 = np.zeros((len(stack[:, 0, 0]), len(stack[0, :, 0])))

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp0[ix, iy] = stack_temp0[ix, iy] + stack[ix, iy, i+50]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp1[ix, iy] = stack_temp1[ix, iy] + stack[ix, iy, i+60]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp2[ix, iy] = stack_temp2[ix, iy] + stack[ix, iy, i+70]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp3[ix, iy] = stack_temp3[ix, iy] + stack[ix, iy, i+80]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp4[ix, iy] = stack_temp4[ix, iy] + stack[ix, iy, i+90]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp5[ix, iy] = stack_temp5[ix, iy] + stack[ix, iy, i+100]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp6[ix, iy] = stack_temp6[ix, iy] + stack[ix, iy, i+110]

for i in range(length_t):
    for ix in range(len(stack[:, 0, 0])):
        for iy in range(len(stack[0, :, 0])):
            stack_temp7[ix, iy] = stack_temp7[ix, iy] + stack[ix, iy, i+120]

vmmin = stack_temp0[:, :].min()
if stack_temp1[:, :].min() < vmmin:
    vmmin = stack_temp1[:, :].min()
if stack_temp2[:, :].min() < vmmin:
    vmmin = stack_temp2[:, :].min()
if stack_temp3[:, :].min() < vmmin:
    vmmin = stack_temp3[:, :].min()
if stack_temp4[:, :].min() < vmmin:
    vmmin = stack_temp4[:, :].min()
if stack_temp5[:, :].min() < vmmin:
    vmmin = stack_temp5[:, :].min()
if stack_temp6[:, :].min() < vmmin:
    vmmin = stack_temp6[:, :].min()
if stack_temp7[:, :].min() < vmmin:
    vmmin = stack_temp7[:, :].min()

vmmax = stack_temp0[:, :].max()
if stack_temp1[:, :].max() > vmmax:
    vmmax = stack_temp1[:, :].max()
if stack_temp2[:, :].max() > vmmax:
    vmmax = stack_temp2[:, :].max()
if stack_temp3[:, :].max() > vmmax:
    vmmax = stack_temp3[:, :].max()
if stack_temp4[:, :].max() > vmmax:
    vmmax = stack_temp4[:, :].max()
if stack_temp5[:, :].max() > vmmax:
    vmmax = stack_temp5[:, :].max()
if stack_temp6[:, :].max() > vmmax:
    vmmax = stack_temp6[:, :].max()
if stack_temp7[:, :].max() > vmmax:
    vmmax = stack_temp7[:, :].max()

fig0, ax0 = plt.subplots(1, 1)
ax0.set_xlabel('Dip (km)')
ax0.set_ylabel('Strike (km)')
ax0.imshow(stack_temp0**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax0.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax0.text(28, 88, '0 - 1 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax0.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig1, ax1 = plt.subplots(1, 1)
ax1.set_xlabel('Dip (km)')
ax1.set_ylabel('Strike (km)')
ax1.imshow(stack_temp1**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax1.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax1.text(28, 88, '1 - 2 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax1.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel('Dip (km)')
ax2.set_ylabel('Strike (km)')
ax2.imshow(stack_temp2**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax2.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax2.text(28, 88, '2 - 3 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax2.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig3, ax3 = plt.subplots(1, 1)
ax3.set_xlabel('Dip (km)')
ax3.set_ylabel('Strike (km)')
ax3.imshow(stack_temp3**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax3.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax3.text(28, 88, '3 - 4 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax3.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig4, ax4 = plt.subplots(1, 1)
ax4.set_xlabel('Dip (km)')
ax4.set_ylabel('Strike (km)')
ax4.imshow(stack_temp4**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax4.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax4.text(28, 88, '4 - 5 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax4.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig5, ax5 = plt.subplots(1, 1)
ax5.set_xlabel('Dip (km)')
ax5.set_ylabel('Strike (km)')
ax5.imshow(stack_temp5**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax5.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax5.text(28, 88, '5 - 6 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax5.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig6, ax6 = plt.subplots(1, 1)
ax6.set_xlabel('Dip (km)')
ax6.set_ylabel('Strike (km)')
ax6.imshow(stack_temp6**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax6.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax6.text(28, 88, '6 - 7 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax6.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

fig7, ax7 = plt.subplots(1, 1)
ax7.set_xlabel('Dip (km)')
ax7.set_ylabel('Strike (km)')
ax7.imshow(stack_temp7**2, cmap = 'jet', vmin = vmmin**2, vmax = vmmax**2, interpolation = 'none', origin = 'lower', extent = (0, 40, 0, 100))
ax7.text(15, 95, 'N 224' + '\u00b0' + ' E', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax7.text(28, 88, '7 - 8 s', fontsize = 15, ha = 'center', va = 'center', color = 'white')
ax7.scatter(20, 50, 20, marker = '*', color = 'white', linewidth = 0.2)

os.chdir(path + '/' + dossier + '_results')
fig0.savefig(dossier + '0-1s.pdf')
fig1.savefig(dossier + '1-2s.pdf')
fig2.savefig(dossier + '2-3s.pdf')
fig3.savefig(dossier + '3-4s.pdf')
fig4.savefig(dossier + '4-5s.pdf')
fig5.savefig(dossier + '5-6s.pdf')
fig6.savefig(dossier + '6-7s.pdf')
fig7.savefig(dossier + '7-8s.pdf')
