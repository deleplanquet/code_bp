import matplotlib.pyplot as plt
import os
import sys
import pickle
import math
import numpy as np


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
azim = param['azim']




degree = '\u00b0'

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_results/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz'
path_rslt_pdf = path_data + '/pdf_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_rslt_png = path_data + '/png_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'

if os.path.isdir(path_rslt_pdf) == False:
    os.makedirs(path_rslt_pdf)
if os.path.isdir(path_rslt_png) == False:
    os.makedirs(path_rslt_png)


nbr_subfaults = file_length(dossier + '_subfault_positions.txt')
coord_cub = np.zeros((nbr_subfaults, 3))
cf_tmp = None
cpt = 0

os.chdir(path)
with open(dossier + '_sunfault_positions.txt', 'r') as myf:
    for line in myf:
        spliit = line.split(' ')
        spliit = [i for i in spliit if i != '']
        cf_tmp = geo2cart(R_Earth - float(spliit[2]), float(spliit[0]), float(spliit[1]))
        coord_cub[cpt, 0] = cf_tmp[0]
        coord_cub[cpt, 1] = cf_tmp[1]
        coord_cub[cpt, 2] = cf_tmp[2]
        cpt = cpt + 1

coord_fault = np.zeros((file_length('SEV_slips_rake1.txt') - 1, 3))
cpt = 0

os.chdir(path_origin + '/Kumamoto')
with open('SEV_slips_rake1.txt', 'r') as myf:
    myf.readline()
    for line in myf:
        spliit = line.split(' ')
        spliit = [i for i in spliit if i != '']
        cf_tmp = geo2cart(R_Earth - float(spliit[2]), float(spliit[0]), float(spliit[1]))
        coord_fault[cpt, 0] = cf_tmp[0]
        coord_fault[cpt, 1] = cf_tmp[1]
        coord_fault[cpt, 2] = cf_tmp[2]
        cpt = cpt + 1

coord_used = np.zeros((file_length('SEV_slips_rake1.txt') - 1))

for i in range(len(coord_fault[:, 0])):
    stk_tmp = 1000
    stk_tmp_old = 1000
    for j in range(len(coord_cub[:, 0])):
        stk_tmp_old = stk_tmp
        for k in range(3):
            stk_tmp = stk_tmp + pow(coord_fault[i, k] - coord_cub[j, k], 2)
        if stk_tmp < stk_tmp_old:
            coord_used[i] = j







length_t = int(length_time*samp_rate)

os.chdir(path_data)
stack = None
with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack3D', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()

stack_used = np.zeros((int((file_length('SEV_slips_rake1.txt') - 1)/9), 9, len(length_t)))

for i in range(len(coord_fault[:, 0])):
    for j in range(len(stack[0, :, 0])):
        for k in range(len(length_t)):
            stack_used[(i - i%9)/9, i%9, k] = stack_used[(i - i%9)/9, i%9, k] + stack[coord_used[i], j, k]








for i in range(length_t):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Dip (km)')
    ax.set_ylabel('Strike (km)')
    ax.imshow(stack[:, :, i], cmap = 'viridis', vmin = stack[:, :, :].min(), vmax = stack[:, :, :].max(), interpolation = 'none', origin = 'lower')#, extent = (0, w, 0, l))
    #ax.text(x, y, 'position' + degree, fontsize = 20, ha = 'center', va = 'center' color = 'white')
    #ax.text(x, y, 'position', fontsize = 20, ha = 'center', va = 'center', color = 'white')
    #ax.scatter(x, y, 30, marker = '*', color = 'white', linewidth = 0.2)

    os.chdir(path_rslt_pdf)
    fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D' + str(i*100) + '.pdf')
    os.chdir(path_rslt_png)
    fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D' + str(i*100) + '.png')





#dossier = sys.argv[1]
#tp_data = sys.argv[2]

#if tp_data != '3comp' and tp_data != 'hori' and tp_data != 'vert':
#    print('ERROR TYPO')
#    sys.exit(0)

#path_origin = os.getcwd()[:-6]
#path = path_origin + '/Kumamoto/' + dossier

#lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_10']
#lst_pth_dt = []

#for freq in lst_frq:
#    lst_pth_dt.append(path + '/' + dossier + '_vel_' + freq + 'Hz_' + tp_data + '_env_results')

#for freq in lst_frq:
#    stack = None
#    os.chdir(lst_pth_dt[lst_frq.index(freq)])
#    with open('stack_vel_' + freq + 'Hz_' + tp_data + '_env', 'rb') as my_fch:
#    	my_dpck = pickle.Unpickler(my_fch)
#    	stack = my_dpck.load()

#    fig, ax = plt.subplots(1, 1)
#    ax.set_xlabel('Time (s)')
#    ax.set_ylabel('Strike (km)')
#    ax.imshow(stack, cmap = 'jet', interpolation = 'none', origin = 'lower')
#    ax.set_aspect('auto')
#    ax.set_xticklabels([0, 0, 5, 10, 15, 20, 25, 30])
#    ax.set_yticklabels([0, 0, 20, 40, 60, 80, 100])
#    print(stack.max()/len(lst_pth_dt[0]))

#    fig.savefig('bp_vel_' + freq + 'Hz_' + tp_data + '_env.pdf')
#    fig.savefig('bp_vel_' + freq + 'Hz_' + tp_data + '_env.png')




















