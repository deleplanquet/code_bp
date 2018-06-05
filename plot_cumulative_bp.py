

import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

path_origin = os.getcwd()[:-6]                  #
os.chdir(path_origin + '/Kumamoto')             #
with open('parametres_bin', 'rb') as mfch:      #
    mdpck = pickle.Unpickler(mfch)              #
    param = mdpck.load()                        #   load parametres

with open('ref_seismes_bin', 'rb') as mfch:     #
    mdpck = pickle.Unpickler(mfch)              #
    dict_seis = mdpck.load()                    #   load caracteristiques seismes

dossier = param['dossier']                  #
couronne = param['couronne']                #
frq = param['band_freq']                    #
dt_type = param['composante']               #
hyp_bp = param['ondes_select']              #
azim = param['angle']                       #
stack = None                                #
length_time = param['length_t']             #
samp_rate = param['samp_rate']              #
length_t = int(length_time*samp_rate)       #   parametres stockes
lst_trsh = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
nbr_col = 4
nbr_lin = 5
w_fault = param['w_fault']
l_fault = param['l_fault']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = (path + '/'
             + dossier
             + '_results/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz')

os.chdir(path_data)                                 #
with open(dossier                                   #
          + '_vel_'                                 #
          + couronne + 'km_'                        #
          + frq + 'Hz_'                             #
          + dt_type                                 #
          + '_env_smooth_'                          #
          + hyp_bp + '_'                            #
          + azim + 'deg_stack3D', 'rb') as mfch:    #
    mdpck = pickle.Unpickler(mfch)                  #
    stack = mdpck.load()                            #   load stack

mx_stck = stack[:, :, :].max()
stck_cumul = np.zeros((len(stack[:, 0, 0]),
                       len(stack[0, :, 0]),
                       len(lst_trsh)))

for i in range(length_t):
    print(i)
    for trsh in lst_trsh:
        for ix in range(len(stack[:, 0, 0])):
            for iy in range(len(stack[0, :, 0])):
                if stack[ix, iy, i] > trsh*mx_stck/100:
                    stck_cumul[ix,
                               iy,
                               lst_trsh.index(trsh)] = (stck_cumul[ix,
                                                                  iy,
                                                                  lst_trsh.index(trsh)]
                                                        + stack[ix, iy, i])

v1 = [0, 0.2, 0.4, 0.6, 0.8, 1]

fig, ax = plt.subplots(nbr_lin, nbr_col, figsize = (20, 40))
ax[nbr_lin - 1, 0].set_ylabel('Strike (km)')
ax[nbr_lin - 1, 0].set_xlabel('Dip (km)')
for trsh in lst_trsh:
    iindex = lst_trsh.index(trsh)
    stck_cumul_max = stck_cumul[:, :, iindex].max()
    ind_axx = iindex//nbr_col
    ind_axy = iindex%nbr_col
    im = ax[ind_axx,
            ind_axy].imshow(stck_cumul[:, :, iindex]**2/stck_cumul_max**2,
                           cmap = 'jet',
                           vmin = 0,
                           vmax = 1,
                           interpolation = 'none',
                           origin = 'lower',
                           extent = (0,
                                     w_fault,
                                     0,
                                     l_fault))
    
    ax[ind_axx, ind_axy].set_xlim(0, w_fault)
    ax[ind_axx, ind_axy].set_ylim(0, l_fault)

    ax[ind_axx, ind_axy].scatter(w_fault/2,
                                 l_fault/2,
                                 300,
                                 marker = '*',
                                 color = 'red',
                                 linewidth = 0.2)

    ax[ind_axx, ind_axy].text(w_fault - 2,
                              l_fault - 10,
                              str(trsh),
                              fontsize = 15,
                              color = 'white',
                              ha = 'right')
   
    if trsh != lst_trsh[len(lst_trsh) - nbr_col]:
        ax[ind_axx, ind_axy].xaxis.set_visible(False)
        ax[ind_axx, ind_axy].yaxis.set_visible(False)

    #if trsh == lst_trsh[-1]:
    fig.colorbar(im, ax = ax[ind_axx, ind_axy], ticks = v1)

#for i in range(len(stck_cumul[0, 0, :])):
#    print(i, i, i, i, i, i, i, i, i, i)
#    for j in range(len(stck_cumul[0, :, 0])):
#        print(stck_cumul[:, j, i])

plt.subplots_adjust(hspace = 0.1,
                    wspace = 0.1)

os.chdir(path_data)
fig.savefig(dossier
            + '_vel_'
            + couronne + 'km_'
            + frq + 'Hz_'
            + dt_type
            + '_env_'
            + hyp_bp + '_'
            + azim + 'deg_cumulative.pdf')

fig.savefig(dossier
            + '_vel_'
            + couronne + 'km_'
            + frq + 'Hz_'
            + dt_type
            + '_env_'
            + hyp_bp + '_'
            + azim + 'deg_cumulative.png')
