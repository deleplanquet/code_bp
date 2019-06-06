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

print('###############################################',
    '\n###   python3 plot_bp_patch_secondaire.py   ###',
    '\n###############################################')

# open the file of the parameters given by the user through parametres.py and
# load them
root_folder = os.getcwd()[:-6]
os.chdir(root_folder + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

# all the parameters are not used in this script, only the following ones
event = param['event']
frq_bnd = param['frq_band']
cpnt = param['component']
couronne = param['hypo_interv']
hyp_bp = param['selected_waves']
azim = param['angle']
bp_len_t = param['bp_length_time']
bp_samp_rate = param['bp_samp_rate']
R_Earth = param['R_Earth']
l_grid = param['l_grid']
w_grid = param['w_grid']
degree = '\u00b0'                   #   parametres stockes
strike = param['strike']
l_grid_step = param['l_grid_step']
w_grid_step = param['w_grid_step']

# directories used in this script:
#
#
#
path_common = (root_folder + '/'
               + 'Kumamoto/'
               + event + '/'
               + 'results/'
               + 'vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth/'
               + couronne + 'km_' + hyp_bp + '_' + azim + 'deg')
path_data = (path_common + '/'
             + 'others')

lst_iter = os.listdir(path_data)
lst_iter = [a for a in lst_iter if '_it-' in a and '_stack' in a]
lst_iter.sort()
print('Here is a list of the iterations of back projection stack that has',
        'already been done:')
for f in lst_iter:
    print(f)
it_nb_i = None
while not isinstance(it_nb_i, int):
    try:
        it_nb_i = int(input('Pick a number corresponding to the iteration you'
                            + ' want to use as input (integer): '))
    except ValueError:
        print('No valid number, try again')
it_nb_i = str(it_nb_i)
m_or_c = None
while m_or_c != 'M' and m_or_c != 'C':
    m_or_c = input('Choose if you want to get the mask or its complementary'
                    + ' (M or C): ')

path_pdf = (path_common + '/'
            + 'iteration-' + it_nb_i + '/'
            + 'pdf')
path_png = (path_common + '/'
            + 'iteration-' + it_nb_i + '/'
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
        print('{} is already existing')

# load the back projection stack to plot
os.chdir(path_data)
stack = None
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'it-' + it_nb_i + '_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stack = mdpk.load()

# load the original back projection stack to get the maximum
os.chdir(path_data)
stack_orgn = None
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'it-0_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stack_orgn = mdpk.load()

stckmx = stack_orgn[:, :, :].max()
length_t = int(bp_len_t*bp_samp_rate)

print('Creation of the back projection images of the event {}'.format(event),
        'with the following parameters:',
        '\n   -      frequency band : {} Hz'.format(frq_bnd),
        '\n   -           component : {}'.format(cpnt),
        '\n   - hypocenter_interval : {} km'.format(couronne),
        '\n   -      selected_waves : {}'.format(hyp_bp),
        '\n   -   azimuth selection : {} deg'.format(azim))
print('This is the {} th iteration'.format(it_nb_i))
# loop over the time, one back projection image is created for every time step
for t in range(length_t):
    # creation of figure
    fig, ax = plt.subplots(1, 1)
    # name of axis
    ax.set_xlabel('Along strike (km)')
    ax.set_ylabel('Down dip (km)')
    # main part of the picture
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
    # iso-values
    iso = [0.8, 0.9]
    # second layer of picture
    cs = ax.contour(np.arange(-len(stack[0, :, 0])/2*l_grid_step,
                              len(stack[0, :, 0])/2*l_grid_step,
                              l_grid_step),
                    np.arange(-len(stack[0, 0, :])/2*w_grid_step,
                              len(stack[0, 0, :])/2*w_grid_step,
                              w_grid_step),
                    (list(zip(*stack[t, :, :]))/stckmx).reshape(int(len(stack[0, 0, :])),
                                                                int(len(stack[0, :, 0]))),
                    iso,
                    origin = 'lower',
                    linestyle = '-',
                    extent = (-l_grid/2, l_grid/2, -w_grid/2, w_grid/2),
                    colors = 'white')
    # set the limits of the pictures to be able to see everything without
    # having white strips on the edges
    ax.set_xlim(-l_grid/2, l_grid/2)
    ax.set_ylim(-w_grid/2, w_grid/2)
    # red star with white border for the hypocenter
    ax.scatter(0, 0, 500, marker = '*', color = 'white', linewidth = 0.2)
    ax.scatter(0, 0, 300, marker = '*', color = 'red', linewidth = 0.2)
    # show the time in relation to the rupture time
    supertxt = ax.text(l_grid/2 - 2,
                       - w_grid/2 + 4,
                       str((t - 5*bp_samp_rate)/bp_samp_rate) + ' s',
                       fontsize = 15,
                       color = 'white',
                       ha = 'right')
    # background effect for the time
    supertxt.set_path_effects([path_effects.Stroke(linewidth = 1,
                                                   foreground = 'black'),
                               path_effects.Normal()])
    # use the setting of thetitle of the figure to show the orientation of the
    # grid
    ax.set_title('N' + str(strike) + str(degree) + 'E' + '$\longrightarrow$',
                 loc = 'right')
    # invert yaxis to have proper orientation
    plt.gca().invert_yaxis()
    # vector of the ticks we want to show on colorbar
    v1 = [1, 0.8, 0.6, 0.4, 0.2, 0]
    # add new axis on the right for the colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size = '3%', pad = 0.1)
    # put the colorbar at the new axis position with the corresponding vector
    # of ticks
    cb = fig.colorbar(im, cax = cax, ticks = v1)
    # add two white lines by hand to show the level of iso-values defined
    # before
    for i in iso:
        cb.ax.plot([0, 1], [i, i], 'white')
    # save the figures in both pdf and png format
    os.chdir(path_pdf)
    fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_i + '_' + str(int(t*1000/bp_samp_rate)) + '.pdf')
    os.chdir(path_png)
    fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_i + '_' + str(int(t*1000/bp_samp_rate)) + '.png')
    print('Number of images already created: {} / {}'.format(t + 1, length_t))

'''
path_rslt_pdf = []
path_rslt_png = []
for scis in scission:
    print('boubou', scis, 'boubou', 'boubou', scission.index(scis))
    path_rslt_pdf.append(path_data               #
                                           + '/pdf_'               #
                                           + dossier               #
                                           + '_vel_'               #
                                           + couronne + 'km_'      #
                                           + frq + 'Hz_'           #
                                           + dt_type               #
                                           + '_env_smooth_'        #
                                           + hyp_bp + '_'          #
                                           + azim + 'deg'
                                           + past + '_'
                                           + selected_patch + scis)         #
                                         #
    path_rslt_png.append(path_data               #
                                           + '/png_'               #
                                           + dossier               #
                                           + '_vel_'               #
                                           + couronne + 'km_'      #
                                           + frq + 'Hz_'           #
                                           + dt_type               #
                                           + '_env_smooth_'        #
                                           + hyp_bp + '_'          #
                                           + azim + 'deg'
                                           + past + '_'
                                           + selected_patch + scis)         #   dossiers de travail
for scis in scission:
    if os.path.isdir(path_rslt_pdf[scission.index(scis)]) == False:   #
        os.makedirs(path_rslt_pdf[scission.index(scis)])              #
    if os.path.isdir(path_rslt_png[scission.index(scis)]) == False:   #
        os.makedirs(path_rslt_png[scission.index(scis)])              #   si un des dossiers n'existe pas, le cree

os.chdir(path_data)
with open(dossier
          + '_vel_'
          + couronne + 'km_'
          + frq + 'Hz_'
          + dt_type
          + '_env_smooth_'
          + hyp_bp + '_'
          + azim + 'deg_stack3D', 'rb') as mfc:
    mdp = pickle.Unpickler(mfc)
    stk_origin = mdp.load()

stckmx = stk_origin[:, :, :].max()

os.chdir(path_origin + '/Kumamoto')                 #
with open('ref_seismes_bin', 'rb') as my_fch:       #
    my_dpck = pickle.Unpickler(my_fch)              #
    dict_seis = my_dpck.load()                      #   load caracteristiques seismes

length_t = int(length_time*samp_rate)

stack_0 = None                                            #
stack_1 = None
stack = [stack_0, stack_1]
for scis in scission:
    os.chdir(path_data)
    stack = None
    print('boubou', scis)
    with open(dossier                                       #
              + '_vel_'                                     #
              + couronne + 'km_'                            #
              + frq + 'Hz_'                                 #
              + dt_type                                     #
              + '_env_smooth_'                              #
              + hyp_bp + '_'                                #
              + azim + 'deg_stack3D'
              + past + '_'
              + selected_patch + scis, 'rb') as my_fch:      #
        my_dpck = pickle.Unpickler(my_fch)                  #
        stack = my_dpck.load()                              #   load stack

    stckmx2 = stack[:, :, :].max()
    print('max modified stack', stack[:, :, :].min(), stckmx2)

    thresh_1 = 95
    thresh_2 = 90
    thresh_3 = 85
    nbr_trsh = 3

    dict_ok_1 = {}
    dict_ok_2 = {}
    dict_ok_3 = {}

    lst_trsh = [thresh_1, thresh_2, thresh_3]
    lst_cpt = [0, 0, 0]
    lst_dct_ok = [dict_ok_1, dict_ok_2, dict_ok_3]
    lst_lst_ok = [[], [], []]

    dict_contour_1 = {}
    dict_contour_2 = {}
    dict_contour_3 = {}

    lst_cntr = [dict_contour_1, dict_contour_2, dict_contour_3]
    lst_clr = ['red', 'orange', 'yellow']

    for i in range(len(stack[:, 0, 0])):                                                #
        for j in range(len(stack[0, :, 0])):                                            #
            for k in range(nbr_trsh):                                                   #
                if lst_cpt[k] != 0:                                                     #
                    lst_dct_ok[k][str(i*len(stack[0, :, 0]) + j)] = lst_lst_ok[k]       #
                lst_cpt[k] = 0                                                          #
                lst_lst_ok[k] = []                                                      #
            for k in range(length_t):                                                   #
                for l in range(nbr_trsh):                                               #
                    if stack[i, j, k] > 0.01*lst_trsh[l]*stack[:, :, :].max():          #
                        for m in range(nbr_trsh):                                       #   stocke dans un dictionnaire
                            if m >= l:                                                  #   avec pour cle la position a une dimension
                                lst_cpt[m] = lst_cpt[m] + 1                             #   (i*len(j) + j)
                                lst_lst_ok[m].append(k)                                 #   une liste contenant les temps verifiant le critere

    os.chdir(path)
    for i in range(nbr_trsh):
        with open(dossier + past + '_' + selected_patch + '_patch_' + str(lst_trsh[i]), 'wb') as my_ext:
            my_pck = pickle.Pickler(my_ext)
            my_pck.dump(lst_dct_ok[i])

    #for i in range(nbr_trsh):
    #    os.chdir(path)
    #    with open(dossier + '_' + past + selected_patch + '_patch_' + str(lst_trsh[i]), 'rb') as my_in:
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

    #skr = 30
    #dkr = 30
    #strkr = 13.5
    #dipkr = 15

    #cmap = mpl.colors.ListedColormap(['white'], ['blue'], ['green'], ['yellow'], ['orange'], ['red'])
    #bounds = [0, 1, 50, 75, 90, 95, 100]
    #nnmm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    colors = [(1, 1, 1), (0, 0, 1)]
    cmap_name = 'mycmp'
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N = 100)
    #v1 = np.linspace(0, 1, endpoint = True)
    v1 = [0, 0.2, 0.4, 0.6, 0.8, 1]
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
                        (list(zip(*stack[:, :, i]))/stckmx2).reshape((len(stack[0, :, 0]), len(stack[:, 0, 0]))),
                        [0.8, 0.9],
                        origin = 'lower',
                        linestyle = '-',
                        extent = (-l_fault/2, l_fault/2, -w_fault/2, w_fault/2),
                        colors = 'white')
        #ax.clabel(cs, [0.85, 0.9, 0.95])

        ax.set_xlim(-l_fault/2, l_fault/2)
        ax.set_ylim(-w_fault/2, w_fault/2)
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

        supertxt =  ax.text(l_fault/2 - 2,
                -w_fault/2 + 4,
                str((i - 5*samp_rate)/samp_rate) + ' s',
                fontsize = 15,
                color = 'white', #'black',
                ha = 'right')

        supertxt.set_path_effects([path_effects.Stroke(linewidth = 1, foreground = 'black'), path_effects.Normal()])

        ax.set_title('N' + str(strike) + str(degree) + 'E ' + '$\longrightarrow$', loc = 'right')
        plt.gca().invert_yaxis()
        #ax.axvline(dkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axvline(dkr - dipkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axhline(skr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axhline(skr - strkr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size = '3%', pad = 0.1)
        cb = fig.colorbar(im, cax = cax, ticks = v1)
        cb.ax.plot([0, 1], [0.80*(stckmx2/stckmx), 0.80*(stckmx2/stckmx)], 'white')
        cb.ax.plot([0, 1], [0.90*(stckmx2/stckmx), 0.90*(stckmx2/stckmx)], 'white')

        os.chdir(path_rslt_pdf[scission.index(scis)])
        fig.savefig(dossier
                    + '_vel_'
                    + couronne + 'km_'
                    + frq + 'Hz_'
                    + dt_type
                    + '_env_'
                    + hyp_bp + '_'
                    + azim + 'deg_stack3D'
                    + past + '_'
                    + selected_patch + scis
                    + str(i*100) + '.pdf')
        os.chdir(path_rslt_png[scission.index(scis)])
        fig.savefig(dossier
                    + '_vel_'
                    + couronne + 'km_'
                    + frq + 'Hz_'
                    + dt_type
                    + '_env_'
                    + hyp_bp + '_'
                    + azim + 'deg_stack3D'
                    + past + '_'
                    + selected_patch + scis
                    + str(i*100) + '.png')
'''
