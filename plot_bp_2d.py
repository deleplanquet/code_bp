import matplotlib.pyplot as plt
import os
import sys
import pickle

dossier = sys.argv[1]
dt_type = sys.argv[2]

if dt_type != '3comp' and dt_type != 'hori' and dt_type != 'vert':
    print('ERROR TYPO')
    sys.exit(0)

path_origin = os.getcwd()[:-6]
path = path_origin + '/Kumamoto/' + dossier

lst_frq = ['02_05', '05_1', '1_2', '2_4', '4_8', '8_16', '16_30']
path_data = path + '/' + dossier + '_results'

lst_pth_rslt_pdf = []
lst_pth_rslt_png = []

for freq in lst_frq:
    lst_pth_rslt_pdf.append(path_data + '/' + dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_smooth_S_impulse_2D/pdf')
    lst_pth_rslt_png.append(path_data + '/' + dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_smooth_S_impulse_2D/png')

    if os.path.isdir(lst_pth_rslt_pdf[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt_pdf[lst_frq.index(freq)])
    if os.path.isdir(lst_pth_rslt_png[lst_frq.index(freq)]) == False:
    	os.makedirs(lst_pth_rslt_png[lst_frq.index(freq)])

length_t = int(30*10)

for freq in lst_frq:
    print('     ', freq)
    os.chdir(path_data)
    stack = None
    with open(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_smooth_S_impulse_stack2D', 'rb') as my_fch:
    	my_dpck = pickle.Unpickler(my_fch)
    	stack = my_dpck.load()

    for i in range(length_t):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlabel('Dip (km)')
        ax.set_ylabel('Strike (km)')
        ax.imshow(stack[:, :, i], cmap = 'jet', vmin = stack[:, :, :].min(), vmax = stack[:, :, :].max(), interpolation = 'none', origin = 'lower', extent = (0, 24, 0, 56))
        #ax.set_aspect('auto')
        #ax.set_xticklabels([0, 0, 4, 8, 12, 16, 20])
        #ax.set_yticklabels([0, 0, 10, 20, 30, 40, 50])
    
        os.chdir(lst_pth_rslt_pdf[lst_frq.index(freq)])
        fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_' + str(i*100) + '.pdf')
        os.chdir(lst_pth_rslt_png[lst_frq.index(freq)])
        fig.savefig(dossier + '_vel_' + freq + 'Hz_' + dt_type + '_env_S_stack2D_' + str(i*100) + '.png')
    	



































