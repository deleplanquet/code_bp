#

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pylab import *
import os
import sys
import pickle
import math
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

print('##############################',
    '\n###   python3 plot_bp.py   ###',
    '\n##############################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
cpnt = param['component']
frq_bnd = param['frq_band']
couronne = param['hypo_interv']
bp_len_t = param['bp_length_time']
bp_samp_rate = param['bp_samp_rate']
hyp_bp = param['selected_waves']
azim = param['angle']
R_Earth = param['R_Earth']
degree = '\u00b0'
l_grid = param['l_grid']
w_grid = param['w_grid']
strike = param['strike']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']

# directories used in this script
# path_common is root directory of the following used directories (defined to
# prevent repetitions):
# - path_data is the directory of the stack previously built
# - path_pdf is the directory with the pictures done from the stack and
#   recorded in pdf format
# - path_png is the directory with the pictures done from the stack and
#   recorded in png format
path_common = (root_folder + '/'
               + 'Kumamoto/'
               + event + '/'
               + 'results/'
               + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
               + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_data = (path_common + '/'
             + 'others')
path_pdf = (path_common + '/'
            + 'pdf')
path_png = (path_common + '/'
            + 'png')

# in case they do not exist, the following directories are created:
# - path_pdf
# - path_png
for d in [path_pdf, path_png]:
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print('Creation of the directory {} failed'.format(d))
        else:
            print('Successfully created the directory {}'.format(d))
    else:
        print('{} is already existing'.format(d))

# load location of the studied earthquake
os.chdir(root_folder + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

length_t = int(bp_len_t*bp_samp_rate)

# load the back projection stack to plot
os.chdir(path_data)
stack = None
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
          + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_stack',
          'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()

stckmx = stack[:, :, :].max()
print('Creation of the back projection images of the event {}'.format(event),
        'with the following parameters:',
        '\n   -      frequency band : {} Hz'.format(frq_bnd),
        '\n   -           component : {}'.format(cpnt),
        '\n   - hypocenter interval : {} km'.format(couronne),
        '\n   -      selected waves : {}'.format(hyp_bp),
        '\n   -   azimuth selection : {} deg'.format(azim))
for t in range(length_t):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Along strike (km)')
    ax.set_ylabel('Down dip (km)')
    im = ax.imshow(list(zip(*stack[t, :, :]))/stckmx,
                   cmap = 'jet',
                   vmin = 0,
                   vmax = 1,
                   interpolation = 'none',
                   origin = 'lower',
                   extent = (-l_grid/2,
                             l_grid/2,
                             -w_grid/2,
                             w_grid/2))

    cs = ax.contour(np.arange(-len(stack[0, :, 0])/2*l_grid_step,
                              len(stack[0, :, 0])/2*l_grid_step,
                              l_grid_step),
                    np.arange(-len(stack[0, 0, :])/2*w_grid_step,
                              len(stack[0, 0, :])/2*w_grid_step,
                              w_grid_step),
                    (list(zip(*stack[t, :, :]))/stckmx).reshape(int(len(stack[0, 0, :])),
                                                                int(len(stack[0, :, 0]))),
                    [0.8, 0.9],
                    origin = 'lower',
                    linestyle = '-',
                    extent = (-l_grid/2, l_grid/2, -w_grid/2, w_grid/2),
                    colors = 'white')

    ax.set_xlim(-l_grid/2, l_grid/2)
    ax.set_ylim(-w_grid/2, w_grid/2)

    ax.scatter(0, 0, 500, marker = '*', color = 'white', linewidth = 0.2)
    ax.scatter(0,
               0,
               300,
               marker = '*',
               color = 'red',
               linewidth = 0.2)

    supertxt = ax.text(l_grid/2 - 2,
            -w_grid/2 + 4,
            str((t - 5*bp_samp_rate)/bp_samp_rate) + ' s',
            fontsize = 15,
            color = 'white', #'black',
            ha = 'right')

    supertxt.set_path_effects([path_effects.Stroke(linewidth = 1,
                                                   foreground = 'black'),
                               path_effects.Normal()])

    ax.set_title('N' + str(strike) + str(degree) + 'E' + '$\longrightarrow$',
                 loc = 'right')
    plt.gca().invert_yaxis()

    v1 = [1, 0.8, 0.6, 0.4, 0.2, 0]#, 0.2, 0.4, 0.6, 0.8, 1]
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size = '3%', pad = 0.1)
    cb = fig.colorbar(im, cax = cax, ticks = v1)
    cb.ax.plot([0, 1], [0.80, 0.80], 'white')
    cb.ax.plot([0, 1], [0.90, 0.90], 'white')

    os.chdir(path_pdf)
    fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + str(int(t*1000/bp_samp_rate)) + '.pdf')
    os.chdir(path_png)
    fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + str(int(t*1000/bp_samp_rate)) + '.png')

"""

#thresh_1 = 95
#thresh_2 = 90
#thresh_3 = 85
#thresh_4 = 80
#nbr_trsh = 4

#dict_ok_1 = {}
#dict_ok_2 = {}
#dict_ok_3 = {}
#dict_ok_4 = {}

#lst_trsh = [thresh_1, thresh_2, thresh_3, thresh_4]
#lst_cpt = [0, 0, 0, 0]
#lst_dct_ok = [dict_ok_1, dict_ok_2, dict_ok_3, dict_ok_4]
#lst_lst_ok = [[], [], [], []]

#dict_contour_1 = {}
#dict_contour_2 = {}
#dict_contour_3 = {}
#dict_contour_4 = {}

lst_cntr = [dict_contour_1, dict_contour_2, dict_contour_3, dict_contour_4]
lst_clr = ['red', 'orange', 'yellow', 'blue']

stckmx = stack[:, :, :].max()

for i in range(len(stack[:, 0, 0])):
    for j in range(len(stack[0, :, 0])):
        for k in range(nbr_trsh):
            if lst_cpt[k] != 0:
                lst_dct_ok[k][str(i*len(stack[0, :, 0]) + j)] = lst_lst_ok[k]
            lst_cpt[k] = 0
            lst_lst_ok[k] = []
        for k in range(length_t):
            for l in range(nbr_trsh):
                if stack[i, j, k] > 0.01*lst_trsh[l]*stckmx:
                    for m in range(nbr_trsh):   #   stocke dans un dictionnaire
                        if m >= l:      #   avec pour cle la position a une dimension
                            lst_cpt[m] = lst_cpt[m] + 1     #   (i*len(j) + j)
                            lst_lst_ok[m].append(k)
                            #   une liste contenant les temps verifiant le critere

os.chdir(path)
for i in range(nbr_trsh):
    with open(dossier + '_patch_' + str(lst_trsh[i]), 'wb') as my_ext:
        my_pck = pickle.Pickler(my_ext)
        my_pck.dump(lst_dct_ok[i])

#for i in range(nbr_trsh):
#    os.chdir(path)
#    with open(dossier + '_patch_' + str(lst_trsh[i]), 'rb') as my_in:
#        my_dpck = pickle.Unpickler(my_in)
#        dict_ook = my_dpck.load()

#    for cles in dict_ook.keys():
#        for tps in range(len(dict_ook[cles])):
#            yyy = 2*(int(cles)//len(stack[0, :, 0]))
#            xxx = 2*(int(cles)%len(stack[0, :, 0]))
#            if xxx > 0:
#                for segm in [[[xxx, xxx], [yyy, yyy + 2]],
#                             [[xxx - 2, xxx - 2], [yyy, yyy + 2]],
#                             [[xxx, xxx - 2], [yyy, yyy]],
#                             [[xxx, xxx - 2], [yyy + 2, yyy + 2]]]:
#                    if dict_ook[cles][tps] in lst_cntr[i]:
#                        if (segm in lst_cntr[i][dict_ook[cles][tps]]) == False:
#                            lst_cntr[i][dict_ook[cles][tps]].append(segm)
#                        else:
#                            lst_cntr[i][dict_ook[cles][tps]] = [i for i in lst_cntr[i][dict_ook[cles][tps]] if i != segm]
#                    else:
#                        lst_cntr[i][dict_ook[cles][tps]] = [segm]

skr = 30
dkr = 30
strkr = 13.5
dipkr = 15

#cmap = mpl.colors.ListedColormap(['white'],
#                                 ['blue'],
#                                 ['green'],
#                                 ['yellow'],
#                                 ['orange'],
#                                 ['red'])
#bounds = [0, 1, 50, 75, 90, 95, 100]
#nnmm = mpl.colors.BoundaryNorm(bounds, cmap.N)

colors = [(1, 1, 1), (0, 0, 1)]
cmap_name = 'mycmp'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N = 100)
#v1 = np.linspace(0, 1, endpoint = True)
v1 = [1, 0.8, 0.6, 0.4, 0.2, 0]#, 0.2, 0.4, 0.6, 0.8, 1]
levels = np.arange(0,
                   1,
                   0.1)

print(len(stack[:, 0, 0]), len(stack[0, :, 0]))

for i in range(length_t):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Along strike (km)')
    ax.set_ylabel('Down dip (km)')
    #ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(stack_used[:, :, :].max(), 2), interpolation = 'none', origin = 'lower', extent = (0, 50, 0, 50))
    im = ax.imshow(list(zip(*stack[:, :, i]))/stckmx,
                   cmap = 'jet', #cm,
                   vmin = 0,
                   vmax = 1,
                   interpolation = 'none',
                   origin = 'lower',
                   extent = (-l_fault/2,
                             l_fault/2,
                             -w_fault/2,
                             w_fault/2))

    cs = ax.contour(np.arange(-len(stack[:, 0, 0])/2*pas_l, len(stack[:, 0, 0])/2*pas_l, pas_l),
                    np.arange(-len(stack[0, :, 0])/2*pas_w, len(stack[0, :, 0])/2*pas_w, pas_w),
                    (list(zip(*stack[:, :, i]))/stckmx).reshape(int(len(stack[0, :, 0])), int(len(stack[:, 0, 0]))),
                    [0.8, 0.9],
                    origin = 'lower',
                    linestyle = '-',
                    extent = (-l_fault/2, l_fault/2, -w_fault/2, w_fault/2),
                    colors = 'white')
    #ax.clabel(cs, [0.85, 0.9, 0.95])

    ax.set_xlim(-l_fault/2, l_fault/2)
    ax.set_ylim(-w_fault/2, w_fault/2)
    #ax.xaxis.tick_top()
    #ax.xaxis.set_label_position('top')
    #ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(66.72, 2), interpolation = 'none', origin = 'lower', extent = (0, 50, 0, 50))
    #ax.text(x, y, 'position' + degree, fontsize = 20, ha = 'center', va = 'center' color = 'white')
    #ax.text(x, y, 'position', fontsize = 20, ha = 'center', va = 'center', color = 'white')
    ax.scatter(0, 0, 500, marker = '*', color = 'white', linewidth = 0.2)
    ax.scatter(0,
               0,
               300,
               marker = '*',
               color = 'red',
               linewidth = 0.2)

    #for j in range(nbr_trsh):
    #    if i in lst_cntr[nbr_trsh - 1 - j]:
    #        print(i, '   ', nbr_trsh, '   ', j, '   ', nbr_trsh - 1 - j)#, dict_contour[i])
    #        for segm in lst_cntr[nbr_trsh - 1 - j][i]:
    #            plot(segm[0],
    #                 segm[1],
    #                 linestyle = '-',
    #                 color = lst_clr[nbr_trsh - 1 - j],
    #                 linewidth = 2)

    supertxt = ax.text(l_fault/2 - 2,
            -w_fault/2 + 4,
            str((i - 5*samp_rate)/samp_rate) + ' s',
            fontsize = 15,
            color = 'white', #'black',
            ha = 'right')

    supertxt.set_path_effects([path_effects.Stroke(linewidth = 1, foreground = 'black'), path_effects.Normal()])

    ax.set_title('N' + str(strike) + str(degree) + 'E' + '$\longrightarrow$', loc = 'right')
    plt.gca().invert_yaxis()
    #ax.axvline(dkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
    #ax.axvline(dkr - dipkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
    #ax.axhline(skr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
    #ax.axhline(skr - strkr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size = '3%', pad = 0.1)
    cb = fig.colorbar(im, cax = cax, ticks = v1)
    cb.ax.plot([0, 1], [0.80, 0.80], 'white')
    cb.ax.plot([0, 1], [0.90, 0.90], 'white')

    os.chdir(path_rslt_pdf)
    fig.savefig(dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz_'
                + dt_type
                + '_env_'
                + hyp_bp + '_'
                + azim + 'deg_stack3D_' + str(int(i*1000/samp_rate)) + '.pdf')
    os.chdir(path_rslt_png)
    fig.savefig(dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz_'
                + dt_type
                + '_env_'
                + hyp_bp + '_'
                + azim + 'deg_stack3D_' + str(int(i*1000/samp_rate)) + '.png')
"""
