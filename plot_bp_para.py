import matplotlib.pyplot as plt
from pylab import *
import os
import sys
import pickle
import math
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

np.set_printoptions(threshold=np.nan)

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographisques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#nombre de ligne d'un fichier
def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#normalisation
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]

#rotation 3d d'angle theta et d'axe passant par l'origine porte par le vecteur (a, b, c) de norme 1, repere orthonormal direct
def rotation(u, theta, OM):
    """ attention OM unitaire """
    a = norm(OM)[0]
    b = norm(OM)[1]
    c = norm(OM)[2]
    radian = d2r(theta)
    #coefficients de la matrice de rotation
    mat = array([[a*a + (1 - a*a)*math.cos(radian), a*b*(1 - math.cos(radian)) - c*math.sin(radian), a*c*(1 - math.cos(radian)) + b*math.sin(radian)], [a*b*(1 - math.cos(radian)) + c*math.sin(radian), b*b + (1 - b*b)*math.cos(radian), b*c*(1 - math.cos(radian)) - a*math.sin(radian)], [a*c*(1 - math.cos(radian)) - b*math.sin(radian), b*c*(1 - math.cos(radian)) + a*math.sin(radian), c*c + (1 - c*c)*math.cos(radian)]])
    #rearrangement du vecteur auquel on applique la rotation
    vect = array([[u[0]],
                    [u[1]],
                    [u[2]]])
    #rotation du vecteur u de theta autour de OM
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])


path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = param['dossier']
dt_type = param['composante']
frq = param['band_freq']
couronne = param['couronne']
length_time = param['length_t']
samp_rate = param['samp_rate']
hyp_bp = param['ondes_select']
azim = param['angle']
R_Earth = param['R_Earth']
l_fault = param['l_fault']
w_fault = param['w_fault']


degree = '\u00b0'

lst_pth = []
lst_pth_dat = []
for i in range(3):
    lst_pth.append(path_origin + '/Kumamoto/' + dossier[:-1] + str(i))
    lst_pth_dat.append(lst_pth[i] + '/' + dossier[:-1] + str(i) + '_results/' + dossier[:-1] + str(i) + '_vel_' + couronne + 'km_' + frq + 'Hz')
path_rslt_pdf = lst_pth_dat[2] + '/pdf_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_rslt_png = lst_pth_dat[2] + '/png_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'

if os.path.isdir(path_rslt_pdf) == False:
    os.makedirs(path_rslt_pdf)
if os.path.isdir(path_rslt_png) == False:
    os.makedirs(path_rslt_png)

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

length_t = int(length_time*samp_rate)

lst_stk = []
for i in range(3):
    os.chdir(lst_pth_dat[i])
    with open(dossier[:-1] + str(i) + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack3D', 'rb') as my_fch:
        my_dpck = pickle.Unpickler(my_fch)
        lst_stk.append(my_dpck.load())

thresh_1 = 90
thresh_2 = 80
thresh_3 = 70
nbr_trsh = 3

#dict_ok_1 = {}
#dict_ok_2 = {}
#dict_ok_3 = {}

lst_trsh = [thresh_1, thresh_2, thresh_3]
#lst_cpt = [0, 0, 0]
#lst_dct_ok = [dict_ok_1, dict_ok_2, dict_ok_3]
#lst_lst_ok = [[], [], []]

lst_lst_cntr = [[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]]
lst_clr = ['red', 'orange', 'yellow']

#for i in range(len(stack[:, 0, 0])):
#    for j in range(len(stack[0, :, 0])):
#        for k in range(nbr_trsh):
#            if lst_cpt[k] != 0:
#                lst_dct_ok[k][str(i*len(stack[0, :, 0]) + j)] = lst_lst_ok[k]
#            lst_cpt[k] = 0
#            lst_lst_ok[k] = []
#        for k in range(length_t):
#            for l in range(nbr_trsh):
#                if stack[i, j, k] > 0.01*lst_trsh[l]*stack[:, :, :].max():
#                    for m in range(nbr_trsh):
#                        if m >= l:
#                            lst_cpt[m] = lst_cpt[m] + 1
#                            lst_lst_ok[m].append(k)

#os.chdir(path)
#for i in range(nbr_trsh):
#    with open(dossier + '_premier_patch_' + str(lst_trsh[i]), 'wb') as my_ext:
#        my_pck = pickle.Pickler(my_ext)
#        my_pck.dump(lst_dct_ok[i])

for j in range(3):
    os.chdir(lst_pth[j])
    print(lst_pth[j])
    for i in range(nbr_trsh):
        with open(dossier[:-1] + str(j) + '_premier_patch_' + str(lst_trsh[i]), 'rb') as my_in:
            my_dpck = pickle.Unpickler(my_in)
            dict_ook = my_dpck.load()

        for cles in dict_ook.keys():
            for tps in range(len(dict_ook[cles])):
                yyy = 2*(int(cles)//len(lst_stk[0][0, :, 0]))
                xxx = 2*(int(cles)%len(lst_stk[0][0, :, 0]))
                if xxx > 0:
                    for segm in [[[xxx, xxx], [yyy, yyy + 2]], [[xxx - 2, xxx - 2], [yyy, yyy + 2]], [[xxx, xxx - 2], [yyy, yyy]], [[xxx, xxx - 2], [yyy + 2, yyy + 2]]]:
                        if dict_ook[cles][tps] in lst_lst_cntr[j][i]:
                            if (segm in lst_lst_cntr[j][i][dict_ook[cles][tps]]) == False:
                                lst_lst_cntr[j][i][dict_ook[cles][tps]].append(segm)
                            else:
                                lst_lst_cntr[j][i][dict_ook[cles][tps]] = [i for i in lst_lst_cntr[j][i][dict_ook[cles][tps]] if i != segm]
                        else:
                            lst_lst_cntr[j][i][dict_ook[cles][tps]] = [segm]

skr = 30
dkr = 30
strkr = 13.5
dipkr = 15

#cmap = mpl.colors.ListedColormap(['white'], ['blue'], ['green'], ['yellow'], ['orange'], ['red'])
#bounds = [0, 1, 50, 75, 90, 95, 100]
#nnmm = mpl.colors.BoundaryNorm(bounds, cmap.N)

#stk_max = max([lst_stk[0][:, :, :].max(), lst_stk[1][:, :, :].max(), lst_stk[2][:, :, :].max()])
#print(stk_max)

colors = [(1, 1, 1), (0, 0, 1)]
cmap_name = 'mycmp'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N = 100)
#v1 = np.linspace(0, 1, endpoint = True)
v1 = [0, 0.2, 0.4, 0.6, 0.8, 1]
levels = np.arange(0, 1, 0.1)

print(len(lst_stk[0][:, 0, 0]), len(lst_stk[0][0, :, 0]))

stckmx1 = lst_stk[0][:, :, :].max()
stckmx2 = lst_stk[1][:, :, :].max()
stckmx3 = lst_stk[2][:, :, :].max()
stckmx = max([stckmx1, stckmx2, stckmx3])

for i in range(length_t):
    fig, ax = plt.subplots(1, 3)
    ax[1].set_xlabel('Dip (km)')
    ax[0].set_ylabel('Strike (km)')
    for k in range(3):
        #ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(stack_used[:, :, :].max(), 2), interpolation = 'none', origin = 'lower', extent = (0, 50, 0, 50))
        im = ax[k].imshow(lst_stk[k][:, :, i]**2/stckmx**2,
                          cmap = cm,
                          vmin = 0,
                          vmax = 1,
                          interpolation = 'none',
                          origin = 'lower',
                          extent = (0,
                                    w_fault,
                                    0,
                                    l_fault))

        ax[k].set_xlim(0, w_fault)
        ax[k].set_ylim(0, l_fault)
        #ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(66.72, 2), interpolation = 'none', origin = 'lower', extent = (0, 50, 0, 50))
        #ax.text(x, y, 'position' + degree, fontsize = 20, ha = 'center', va = 'center' color = 'white')
        #ax.text(x, y, 'position', fontsize = 20, ha = 'center', va = 'center', color = 'white')
        ax[k].scatter(w_fault/2, l_fault/2, 300, marker = '*', color = 'red', linewidth = 0.2)

        for j in range(nbr_trsh):
            if i in lst_lst_cntr[k][nbr_trsh - 1 - j]:
                print(i, '   ', nbr_trsh, '   ', j, '   ', nbr_trsh - 1 - j)#, dict_contour[i])
                for segm in lst_lst_cntr[k][nbr_trsh - 1 - j][i]:
                    ax[k].plot(segm[0], segm[1], linestyle = '-', color = lst_clr[nbr_trsh - 1 - j], linewidth = 2)

        ax[k].text(38,
                   92,
                   str((i - 50)/10) + ' s',
                   fontsize = 15,
                   color = 'black',
                   ha = 'right')
        #ax.axvline(dkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axvline(dkr - dipkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axhline(skr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
        #ax.axhline(skr - strkr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
    cbar = fig.add_axes([0.92, 0.13, 0.03, 0.74])
    #fig.colorbar(im, ax = ax[1], ticks = v1)
    fig.colorbar(im, cax = cbar, ticks = v1)

    if i == 0:
        hh = '0000'
    elif i < 10:
        hh = '00'
    elif i < 100:
        hh = '0'
    else:
        hh = ''

    os.chdir(path_rslt_pdf)
    fig.savefig(dossier[:-1] + 'o' + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D_' + hh + str(i*100) + '.pdf')
    os.chdir(path_rslt_png)
    fig.savefig(dossier[:-1] + 'o' + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D_' + hh + str(i*100) + '.png')








