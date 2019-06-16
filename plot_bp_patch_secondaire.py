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

if m_or_c == 'M':
    path_pdf = (path_common + '/'
                + 'iteration-' + it_nb_i + '/'
                + 'pdf')
    path_png = (path_common + '/'
                + 'iteration-' + it_nb_i + '/'
                + 'png')
elif m_or_c == 'C':
    path_pdf = (path_common + '/'
                + 'iteration-' + it_nb_i + '_patch_2/'
                + 'pdf')
    path_png = (path_common + '/'
                + 'iteration-' + it_nb_i + '_patch_2/'
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
if m_or_c == 'M':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_i + '_stack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        stack = mdpk.load()
elif m_or_c == 'C':
    with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                + 'it-' + it_nb_i + '_patch_2_stack', 'rb') as mfch:
        mdpk = pickle.Unpickler(mfch)
        stack = mdpk.load()

# load the original back projection stack to get the maximum
os.chdir(path_data)
with open(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
            + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
            + 'it-0_stack', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    stack_orgn = mdpk.load()

stck_or_mx = stack_orgn[:, :, :].max()
stck_mx = stack[:, :, :].max()
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
    im = ax.imshow(list(zip(*stack[t, :, :]))/stck_or_mx,
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
    iso = [0.8*stck_mx/stck_or_mx, 0.9*stck_mx/stck_or_mx]
    # second layer of picture
    cs = ax.contour(np.arange(-len(stack[0, :, 0])/2*l_grid_step,
                              len(stack[0, :, 0])/2*l_grid_step,
                              l_grid_step),
                    np.arange(-len(stack[0, 0, :])/2*w_grid_step,
                              len(stack[0, 0, :])/2*w_grid_step,
                              w_grid_step),
                    (list(zip(*stack[t, :, :]))/stck_or_mx).reshape(int(len(stack[0, 0, :])),
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
    if m_or_c == 'M':
        os.chdir(path_pdf)
        fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                    + 'it-' + it_nb_i + '_'
                    + str(int(t*1000/bp_samp_rate)) + '.pdf')
        os.chdir(path_png)
        fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                    + 'it-' + it_nb_i + '_'
                    + str(int(t*1000/bp_samp_rate)) + '.png')
    elif m_or_c == 'C':
        os.chdir(path_pdf)
        fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                    + 'it-' + it_nb_i + '_patch_2_'
                    + str(int(t*1000/bp_samp_rate)) + '.pdf')
        os.chdir(path_png)
        fig.savefig(event + '_vel_env_' + frq_bnd + 'Hz_' + cpnt + '_smooth_'
                    + couronne + 'km_' + hyp_bp + '_' + azim + 'deg_'
                    + 'it-' + it_nb_i + '_patch_2_'
                    + str(int(t*1000/bp_samp_rate)) + '.png')
    print('Number of images already created: {} / {}'.format(t + 1, length_t))
