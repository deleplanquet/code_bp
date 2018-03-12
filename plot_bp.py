import matplotlib.pyplot as plt
from pylab import *
import os
import sys
import pickle
import math
import numpy as np

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

#dossier = param['dossier']
dossier = '20160414212600'
dt_type = param['composante']
frq = param['band_freq']
couronne = param['couronne']
length_time = param['length_t']
samp_rate = param['samp_rate']
hyp_bp = param['ondes_select']
azim = param['angle']
R_Earth = param['R_Earth']




degree = '\u00b0'

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_results/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz'
path_rslt_pdf = path_data + '/pdf_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_rslt_png = path_data + '/png_' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'

if os.path.isdir(path_rslt_pdf) == False:
    os.makedirs(path_rslt_pdf)
if os.path.isdir(path_rslt_png) == False:
    os.makedirs(path_rslt_png)

os.chdir(path)
nbr_subfaults = file_length(dossier + '_subfault_positions.txt')
coord_cub = np.zeros((nbr_subfaults, 3))
cf_tmp = None
cpt = 0

os.chdir(path)
with open(dossier + '_subfault_positions.txt', 'r') as myf:
    for line in myf:
        spliit = line.split(' ')
        spliit = [i for i in spliit if i != '']
        cf_tmp = geo2cart(R_Earth - float(spliit[2]), float(spliit[0]), float(spliit[1]))
        coord_cub[cpt, 0] = cf_tmp[0]
        coord_cub[cpt, 1] = cf_tmp[1]
        coord_cub[cpt, 2] = cf_tmp[2]
        cpt = cpt + 1

os.chdir(path_origin + '/Kumamoto')
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


u_strike = norm([coord_fault[0, 0] - coord_fault[1, 0], coord_fault[0, 1] - coord_fault[1, 1], coord_fault[0, 2] - coord_fault[1, 2]])
u_dip = norm([coord_fault[0, 0] - coord_fault[9, 0], coord_fault[0, 1] - coord_fault[9, 1], coord_fault[0, 2] - coord_fault[9, 2]])

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']

strike = 225
dip = 65

dir_cen_fault = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)), math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)), math.sin(d2r(lat_hyp))]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])
vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
vect_dip = rotation(vect_perp_strike, dip, vect_strike)

#coord_flt = np.zeros((49*(file_length('SEV_slips_rake1.txt') - 1), 3))
coord_flt = np.zeros((50*50, 3))
#print(len(coord_flt[:, 0]), 49*len(coord_fault[:, 0]))
if dossier == '20160415000300':
    for a in range(50):
        for b in range(50):
            #for i in range(len(coord_fault[:, 0])):
                #coord_flt[i + b*len(coord_fault[:, 0]) + 7*a*len(coord_fault[:, 0]), 0] = coord_fault[i, 0] + (a - 3)*u_strike[0] + (b - 3)*u_dip[0]
                #coord_flt[i + b*len(coord_fault[:, 0]) + 7*a*len(coord_fault[:, 0]), 1] = coord_fault[i, 1] + (a - 3)*u_strike[1] + (b - 3)*u_dip[1]
                #coord_flt[i + b*len(coord_fault[:, 0]) + 7*a*len(coord_fault[:, 0]), 2] = coord_fault[i, 2] + (a - 3)*u_strike[2] + (b - 3)*u_dip[2]
            coord_flt[b + 50*a, 0] = coord_fault[0, 0] + (a - 30)*u_strike[0] + (b - 30)*u_dip[0]
            coord_flt[b + 50*a, 1] = coord_fault[0, 1] + (a - 30)*u_strike[1] + (b - 30)*u_dip[1]
            coord_flt[b + 50*a, 2] = coord_fault[0, 2] + (a - 30)*u_strike[2] + (b - 30)*u_dip[2]
elif dossier == '20160414212600':
    for a in range(50):
        for b in range(50):
            coord_flt[b + 50*a, 0] = coord_cub[5, 0] + (a - 40)*norm(vect_strike)[0] + (b - 5)*norm(vect_dip)[0]
            coord_flt[b + 50*a, 1] = coord_cub[8, 1] + (a - 40)*norm(vect_strike)[1] + (b - 5)*norm(vect_dip)[1]
            coord_flt[b + 50*a, 2] = coord_cub[10, 2] + (a - 40)*norm(vect_strike)[2] + (b - 5)*norm(vect_dip)[2]

#coord_used = np.zeros((49*(file_length('SEV_slips_rake1.txt') - 1)))
#coord_used = np.zeros((file_length('SEV_slips_rake1.txt') - 1))
coord_used = np.zeros((50*50))

for i in range(len(coord_flt[:, 0])):
#for i in range(len(coord_fault[:, 0])):
    stk_tmp = 100000000000
    stk_tmp_old = 100000000000
    for j in range(len(coord_cub[:, 0])):
        stk_tmp = 0
        for k in range(3):
            stk_tmp = stk_tmp + pow(coord_flt[i, k] - coord_cub[j, k], 2)
            #stk_tmp = stk_tmp + pow(coord_fault[i, k] - coord_cub[j, k], 2)
        if stk_tmp < stk_tmp_old:
            stk_tmp_old = stk_tmp
            coord_used[i] = j





length_t = int(length_time*samp_rate)

os.chdir(path_data)
stack = None
with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack3D', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    stack = my_dpck.load()

os.chdir(path_origin + '/Kumamoto')
#stack_used = np.zeros((int(49*(file_length('SEV_slips_rake1.txt') - 1)/63), 63, length_t))
#stack_used = np.zeros((int((file_length('SEV_slips_rake1.txt') - 1)/9), 9, length_t))
stack_used = np.zeros((50, 50, length_t))

for i in range(len(coord_flt[:, 0])):
#for i in range(len(coord_fault[:, 0])):
    for j in range(len(stack[0, :, 0])):
        for k in range(length_t):
            #stack_used[int((i - i%63)/63), i%63, k] = stack_used[int((i - i%63)/63), i%63, k] + stack[int(coord_used[i]), j, k]
            stack_used[int((i - i%50)/50), i%50, k] = stack_used[int((i - i%50)/50), i%50, k] + stack[int(coord_used[i]), j, k]

#stack_used[0, 0, 0] = stack_used[:, :, :].max()
#stack_used[0, 1, 0] = stack_used[:, :, :].max()

stack_used_max = stack_used[:, :, :].max()
print(stack_used_max)
ttp = 0
for i in range(50):
    for j in range(50):
        for k in range(length_t):
            if ttp < stack_used[i, j, k]:
                ttp = stack_used[i, j, k]
                print(i, j, k, ttp)
thresh = 0.95
cpt = 0

dict_ok = {}

os.chdir(path)
with open(dossier + '_premier_patch_09', 'wb') as my_ext:
    my_pck = pickle.Pickler(my_ext)
    for i in range(len(stack_used[:, 0, 0])):
        for j in range(len(stack_used[0, :, 0])):
            if cpt != 0:
                dict_ok[str(50*i + j)] = lst_ok
            cpt = 0
            lst_ok = []
            for k in range(length_t):
                if stack_used[i, j, k] > thresh*stack_used_max:
                    cpt = cpt + 1
                    lst_ok.append(k)
    my_pck.dump(dict_ok)

for cles in dict_ok.keys():
    print(cles, dict_ok[cles])

skr = 30
dkr = 30
strkr = 13.5
dipkr = 15

for i in range(length_t):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Dip (km)')
    ax.set_ylabel('Strike (km)')
    ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(stack_used[:, :, :].max(), 2), interpolation = 'none', origin = 'lower')#, extent = (0, 50, 0, 50))
    #ax.imshow(stack_used[:, :, i]**2, cmap = 'viridis', vmin = pow(stack_used[:, :, :].min(), 2), vmax = pow(84.5033811494, 2), interpolation = 'none', origin = 'lower')#, extent = (0, 50, 0, 50))
    #ax.text(x, y, 'position' + degree, fontsize = 20, ha = 'center', va = 'center' color = 'white')
    #ax.text(x, y, 'position', fontsize = 20, ha = 'center', va = 'center', color = 'white')
    #ax.scatter(x, y, 30, marker = '*', color = 'white', linewidth = 0.2)

    ax.axvline(dkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
    ax.axvline(dkr - dipkr, (skr - strkr + 0.5)/50, (skr + 0.5)/50, color = 'white', linewidth = 1)
    ax.axhline(skr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)
    ax.axhline(skr - strkr, (dkr - dipkr + 0.5)/50, (dkr + 0.5)/50, color = 'white', linewidth = 1)

    os.chdir(path_rslt_pdf)
    fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D_' + str(i*100) + '.pdf')
    os.chdir(path_rslt_png)
    fig.savefig(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_' + hyp_bp + '_' + azim + 'deg_stack3D_' + str(i*100) + '.png')





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




















