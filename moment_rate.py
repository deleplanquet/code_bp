import os
import matplotlib.pyplot as plt
import pickle

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

dossier = '20160414212600'
couronne = '50-80'
frq = '4-8'
dt_type = 'hori'
hyp_bp = 'S'
azim = '90-180'

path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_results'
path_results = path_data + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_2D'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

os.chdir(path_data)
#with open(dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg_stack2D', 'rb') as my_fch:
with open(dossier + '_vel_' + couronne + 'km_4_8Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_latlon10_stack2D', 'rb') as my_fich:
    my_dpick = pickle.Unpickler(my_fich)
    stack = my_dpick.load()

plt.rc('font', size = 0)

figm, axm = plt.subplots(1, 1)
#axm.set_xlabel('Time (s)')
#axm.set_ylabel('Energy rate')
figmc, axmc = plt.subplots(1, 1)
#axmc.set_xlabel('Time (s)')
#axmc.set_ylabel('Cumulative energy rate')
fig50, ax50 = plt.subplots(1, 1)
#ax50.set_xlabel('Time (s)')
#ax50.set_ylabel('Energy rate')
fig50c, ax50c = plt.subplots(1, 1)
#ax50c.set_xlabel('Time (s)')
#ax50c.set_ylabel('Cumulative energy rate')
fig65, ax65 = plt.subplots(1, 1)
#ax65.set_xlabel('Time (s)')
#ax65.set_ylabel('Energy rate')
fig65c, ax65c = plt.subplots(1, 1)
#ax65c.set_xlabel('Time (s)')
#ax65c.set_ylabel('Cumulative energy rate')
fig80, ax80 = plt.subplots(1, 1)
#ax80.set_xlabel('Time (s)')
#ax80.set_ylabel('Energy rate')
fig80c, ax80c = plt.subplots(1, 1)
#ax80c.set_xlabel('Time (s)')
#ax80c.set_ylabel('Cumulative energy rate')
mc = 0
t50 = 0
c50 = 0
t65 = 0
c65 = 0
t80 = 0
c80 = 0
length_t = int(20*10)
for i in range(length_t):
    if i > 49:
        axm.scatter((i-50)/10, stack[:, :, i].max(), color = 'darkblue')
        mc = mc + stack[:, :, i].max()
        axmc.scatter((i-50)/10, mc, color = 'darkblue')
        t50 = 0
        t65 = 0
        t80 = 0
        for ix in range(len(stack[:, 0, 0])):
            for iy in range(len(stack[0, :, 0])):
                if stack[ix, iy, i] > 0.8*stack[:, :, :].max():
                    t80 = t80 + stack[ix, iy, i]
                    t65 = t65 + stack[ix, iy, i]
                    t50 = t50 + stack[ix, iy, i]
                elif stack[ix, iy, i] > 0.65*stack[:, :, :].max():
                    t65 = t65 + stack[ix, iy, i]
                    t50 = t50 + stack[ix, iy, i]
                elif stack[ix, iy, i] > 0.5*stack[:, :, :].max():
                    t50 = t50 + stack[ix, iy, i]
        ax50.scatter((i-50)/10, t50, color = 'darkblue')
        ax65.scatter((i-50)/10, t65, color = 'darkblue')
        ax80.scatter((i-50)/10, t80, color = 'darkblue')
        c50 = c50 + t50
        c65 = c65 + t65
        c80 = c80 + t80
        ax50c.scatter((i-50)/10, c50, color = 'darkblue')
        ax65c.scatter((i-50)/10, c65, color = 'darkblue')
        ax80c.scatter((i-50)/10, c80, color = 'darkblue')
        print(stack[:, :, i].max(), mc, t50, c50, t65, c65, t80, c80)

os.chdir(path_results)
figm.savefig('energy_rate_max.pdf')
figmc.savefig('energy_rate_max_cumul.pdf')
fig50.savefig('energy_rate_50.pdf')
fig50c.savefig('energy_rate_50_cumul.pdf')
fig65.savefig('energy_rate_65.pdf')
fig65c.savefig('energy_rate_65_cumul.pdf')
fig80.savefig('energy_rate_80.pdf')
fig80c.savefig('energy_rate_80_cumul.pdf')
