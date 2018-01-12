import matplotlib.pyplot as plt
import os
import sys
import pickle

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
#l_fault = param['l_fault']
#w_fault = param['w_fault']
l_fault = 16
w_fault = 10
#strike = param['strike']
strike = 12345

latlon = 'latlon10'

degree = '\u00b0'

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_results/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz'
path_rslt_pdf = path_data + '/pdf_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_rslt_png = path_data + '/png_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'

if os.path.isdir(path_rslt_pdf) == False:
    os.makedirs(path_rslt_pdf)
if os.path.isdir(path_rslt_png) == False:
    os.makedirs(path_rslt_png)

length_t = int(length_time*samp_rate)

os.chdir(path_data)
stack = None
if param['fault'] == 0:
    with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack2D', 'rb') as my_fch:
        my_dpck = pickle.Unpickler(my_fch)
        stack = my_dpck.load()

    for i in range(length_t):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlabel('Dip (km)')
        ax.set_ylabel('Strike (km)')
        ax.imshow(stack[:, :, i]**2, cmap = 'viridis', vmin = stack[:, :, :].min(), vmax = (stack[:, :, :].max())**2, interpolation = 'none', origin = 'lower', extent = (0, w_fault, 0, l_fault))
        ax.text(w_fault/4, 95*l_fault/100, 'N ' + str(int(strike)) + degree + ' E', fontsize = 10, ha = 'center', va = 'center', color = 'white')
        ax.text(35*w_fault/40, 95*l_fault/100, str((i - 50)/10) + ' s', fontsize = 10, ha = 'center', va = 'center', color = 'white')
        ax.scatter(w_fault/2, l_fault/2, 20, marker = '*', color = 'white', linewidth = 0.2)
    
        os.chdir(path_rslt_pdf)
        fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack2D_n=2_' + str(i*100) + '.pdf')
        os.chdir(path_rslt_png)
        fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack2D_n=2_' + str(i*100) + '.png')

else:
    with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack2D_' + param['fault'][0:3] + '_' + param['fault'][10:15], 'rb') as my_fch:
        my_dpck = pickle.Unpickler(my_fch)
        stack = my_dpck.load()

    for i in range(length_t):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlabel('Dip (km)')
        ax.set_ylabel('Strike (km)')
        ax.imshow(stack[:, :, i]**2, cmap = 'viridis', vmin = stack[:, :, :].min(), vmax = (stack[:, :, :].max())**2, interpolation = 'none', origin = 'lower', extent = (0, w_fault, 0, l_fault))
        ax.text(w_fault/4, 95*l_fault/100, 'N ' + str(int(strike)) + degree + ' E', fontsize = 10, ha = 'center', va = 'center', color = 'white')
        ax.text(35*w_fault/40, 95*l_fault/100, str((i - 50)/10) + ' s', fontsize = 10, ha = 'center', va = 'center', color = 'white')
        ax.scatter(w_fault/2, l_fault/2, 20, marker = '*', color = 'white', linewidth = 0.2)
    
        os.chdir(path_rslt_pdf)
        fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack2D_' + param['fault'][0:3] + '_' + param['fault'][10:15] + '_n=2_' + str(i*100) + '.pdf')
        os.chdir(path_rslt_png)
        fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack2D_' + param['fault'][0:3] + '_' + param['fault'][10:15] + '_n=2_' + str(i*100) + '.png')























