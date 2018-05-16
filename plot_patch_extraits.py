import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from obspy import read
from matplotlib.colors import LinearSegmentedColormap

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    param = mdpck.load()

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']
length_time = param['length_t']
samp_rate = param['samp_rate']
w_fault = param['w_fault']
l_fault = param['l_fault']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_patch = (path + '/'
              + dossier
              + '_results/'
              + dossier
              + '_vel_'
              + couronne + 'km_'
              + frq + 'Hz')

path_data = (path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz')

lst_pth_dat = [path_data + '/'
               + dossier
               + '_vel_'
               + couronne + 'km_'
               + frq + 'Hz_'
               + dt_type
               + '_env_smooth_'
               + hyp_bp + '_'
               + azim + 'deg']

lst_sta = [os.listdir(lst_pth_dat[0])]
lst_sta[0].sort()
lst_clr = ['gold', 'yellowgreen', 'lightskyblue']#, 'blue']
#lst_clr = ['orange', 'red', 'blue']

for i in range(2):
    lst_pth_dat.append(lst_pth_dat[i]
                       + '_patch_80')

for i in range(2):
    lst_pth_dat[i + 1] = lst_pth_dat[i + 1] + '_complementaire'
    lst_sta.append(os.listdir(lst_pth_dat[i+1]))
    lst_sta[i+1].sort()

print(lst_pth_dat)

path_results = (path + '/'
                + dossier
                + '_results/'
                + dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz')

path_traces = (path_results + '/'
               + 'Traces_modifiess_comparison')

pth_pdf = (path_traces + '/'
           + 'pdf')

pth_png = (path_traces + '/'
           + 'png')

path_plots_bp = (path_results + '/'
                 + 'Patchs_cumules_bp')

pth_bp_pdf = (path_plots_bp + '/'
              + 'pdf')

pth_bp_png = (path_plots_bp + '/'
              + 'png')

if os.path.isdir(pth_pdf) == False:
    os.makedirs(pth_pdf)
if os.path.isdir(pth_png) == False:
    os.makedirs(pth_png)

if os.path.isdir(pth_bp_pdf) == False:
    os.makedirs(pth_bp_pdf)
if os.path.isdir(pth_bp_png) == False:
    os.makedirs(pth_bp_png)

for station in lst_sta[0]:
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Energy')
    st = []
    for chemin in lst_pth_dat:
        os.chdir(chemin)
        st.append(read(lst_sta[lst_pth_dat.index(chemin)][lst_sta[0].index(station)]))

    t = np.arange(st[0][0].stats.npts)/st[0][0].stats.sampling_rate

    for elt in st:
        ax.fill_between(t[:-1],
                        0,
                        elt[0].data[:-1],
                        linewidth = 0.2,
                        color = lst_clr[st.index(elt)])
        ax.plot(t[:-1],
                elt[0].data[:-1],
                linewidth = 0.5,
                color = 'black')

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 1.1*st[-1][0].data[-1])

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    os.chdir(pth_png)
    fig.savefig(station[:-4] + '.png')
    os.chdir(pth_pdf)
    fig.savefig(station[:-4] + '.pdf')

##############################
##############################
##############################



os.chdir(path_patch)
with open(dossier
          + '_vel_'
          + couronne + 'km_'
          + frq + 'Hz_'
          + dt_type
          + '_env_smooth_'
          + hyp_bp + '_'
          + azim + 'deg_stack3D', 'rb') as mfch:
    mdpck = pickle.Unpickler(mfch)
    origin_stack = mdpck.load()

stckmx = origin_stack[:, :, :].max()

length_t = int(length_time*samp_rate)
stack = np.zeros((int(l_fault/2),
                  int(w_fault/2),
                  length_t))
stack_tmp = None

lst_patch = ['_patch_80', '_patch_80_patch_80', '_patch_80_patch_80_patch_80']

os.chdir(path_patch)
for i in range(2):
    with open(dossier
              + '_vel_'
              + couronne + 'km_'
              + frq + 'Hz_'
              + dt_type
              + '_env_smooth_'
              + hyp_bp + '_'
              + azim + 'deg_stack3D' + lst_patch[i], 'rb') as mfch:
        mdpck = pickle.Unpickler(mfch)
        stack_tmp = mdpck.load()

    for j in range(len(stack[:, 0, 0])):
        for k in range(len(stack[0, :, 0])):
            for l in range(len(stack[0, 0, :])):
                stack[j, k, l] = stack[j, k, l] + stack_tmp[j, k, l]

cmap_name = 'mycmp'
colors = [(1, 1, 1), (0, 0, 1)]
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N = 100)
v1 = [0, 0.2, 0.4, 0.6, 0.8, 1]
levels = np.arange(0, 1, 0.1)

for i in range(length_t):
    fig, ax = plt.subplots(1, 1)
    ax.set_xlabel('Dip (km)')
    ax.set_ylabel('Strike (km)')
    im = ax.imshow(stack[:, :, i]**2/stckmx**2,
                   cmap = cm,
                   vmin = 0,
                   vmax = 1,
                   interpolation = 'none',
                   origin = 'lower',
                   extent = (0,
                             w_fault,
                             0,
                             l_fault))

    ax.scatter(w_fault/2,
               l_fault/2,
               300,
               marker = '*',
               color = 'red',
               linewidth = 0.2)

    ax.text(38,
            90,
            str((i - 50)/10) + ' s',
            fontsize = 15,
            color = 'black',
            ha = 'right')

    ax.set_xlim(0, w_fault)
    ax.set_ylim(0, l_fault)

    fig.colorbar(im, ax = ax, ticks = v1)

    os.chdir(pth_bp_pdf)
    fig.savefig(dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz_'
                + dt_type
                + '_env_'
                + hyp_bp + '_'
                + azim + 'deg_stack3D_' + str(i*100) + '.pdf')
    os.chdir(pth_bp_png)
    fig.savefig(dossier
                + '_vel_'
                + couronne + 'km_'
                + frq + 'Hz_'
                + dt_type
                + '_env_'
                + hyp_bp + '_'
                + azim + 'deg_stack3D_' + str(i*100) + '.png')
