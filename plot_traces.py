

import pickle
import numpy as np
from obspy import read
import matplotlib.pyplot as plt
import sys
import os

path_origin = os.getcwd()[:-6]              #
os.chdir(path_origin + '/Kumamoto')         #
with open('parametres_bin', 'rb') as mfch:  #
    mdpck = pickle.Unpickler(mfch)          #
    param = mdpck.load()                    #   load parametres

dossier = param['dossier']
couronne = param['couronne']
frq = param['band_freq']
dt_type = param['composante']
hyp_bp = param['ondes_select']
azim = param['angle']

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_acc = (path + '/'
            + dossier
            + '_sac_'
            + couronne + 'km')

path_vel = (path + '/'
            + dossier
            + '_vel_'
            + couronne + 'km')

path_flt = (path_vel + '_'
            + frq + 'Hz/'
            + dossier
            + '_vel_'
            + couronne + 'km_'
            + frq + 'Hz')

path_env = (path_flt + '_'
            + dt_type
            + '_env')

path_smt = (path_env
            + '_smooth')

path_slt = (path_smt + '_'
            + hyp_bp + '_'
            + azim + 'deg')

path_rslt = (path + '/'
             + dossier
             + '_results/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz/'
             + 'Traces_chrono')

path_pdf = (path_rslt
            + '_pdf')

path_png = (path_rslt
            + '_png')

if os.path.isdir(path_pdf) == False:
    os.makedirs(path_pdf)

if os.path.isdir(path_png) == False:
    os.makedirs(path_png)

lst_fch_slt = os.listdir(path_slt)  # recupere la liste des noms des fichiers contenant les donnes
lst_fch_slt.sort()                  #   les trie

lst_fch = []
for fich in lst_fch_slt:
    lst_fch.append(fich[:6])

lst_tmp = []
lst_fch_smt = os.listdir(path_smt)
lst_fch_smt.sort()
for fich in lst_fch_smt:
    if (fich[:6] in lst_fch) == False:
        lst_tmp.append(fich)
for fich in lst_tmp:
    lst_fch_smt.remove(fich)
    print(fich)

lst_tmp = []
lst_fch_env = os.listdir(path_env)
lst_fch_env.sort()
for fich in lst_fch_env:
    if (fich[:6] in lst_fch) == False:
        lst_tmp.append(fich)
for fich in lst_tmp:
    lst_fch_env.remove(fich)
    print(fich)

lst_tmp = []
lst_fch_flt = os.listdir(path_flt)
lst_fch_flt.sort()
for fich in lst_fch_flt:
    if (fich[:6] in lst_fch) == False:
        lst_tmp.append(fich)
for fich in lst_tmp:
    lst_fch_flt.remove(fich)
    print(fich)

lst_tmp = []
lst_fch_vel = os.listdir(path_vel)
lst_fch_vel.sort()
for fich in lst_fch_vel:
    if (fich[:6] in lst_fch) == False:
        lst_tmp.append(fich)
for fich in lst_tmp:
    lst_fch_vel.remove(fich)
    print(fich)

lst_tmp = []
lst_fch_acc = os.listdir(path_acc)
lst_fch_acc.sort()
for fich in lst_fch_acc:
    if (fich[:6] in lst_fch) == False:
        lst_tmp.append(fich)
for fich in lst_tmp:
    lst_fch_acc.remove(fich)
    print(fich)

print(len(lst_fch_slt),
      len(lst_fch_smt),
      len(lst_fch_env),
      len(lst_fch_flt),
      len(lst_fch_vel),
      len(lst_fch_acc))

for fich in lst_fch_slt:
    fig, ax = plt.subplots(12, 1, sharex = 'col', sharey = 'row', figsize = (20, 40))

    os.chdir(path_slt)
    st = read(fich)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[11].plot(st[0].data, lw = 0.5)
    ax[11].set_xlim([0, 5000])

    os.chdir(path_smt)
    st = read(lst_fch_smt[lst_fch_slt.index(fich)])
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[10].plot(st[0].data, lw = 0.5)

    os.chdir(path_env)
    st = read(lst_fch_env[lst_fch_slt.index(fich)])
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[9].plot(st[0].data, lw = 0.5)

    os.chdir(path_flt)
    st = read(lst_fch_flt[3*lst_fch_slt.index(fich)])
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[6].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_flt[3*lst_fch_slt.index(fich) + 1])
    ax[7].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_flt[3*lst_fch_slt.index(fich) + 2])
    ax[8].plot(st[0].data, lw = 0.5)

    os.chdir(path_vel)
    st = read(lst_fch_vel[3*lst_fch_slt.index(fich)])
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[3].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_vel[3*lst_fch_slt.index(fich) + 1])
    ax[4].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_vel[3*lst_fch_slt.index(fich) + 2])
    ax[5].plot(st[0].data, lw = 0.5)

    os.chdir(path_acc)
    st = read(lst_fch_acc[3*lst_fch_slt.index(fich)])
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    ax[0].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_acc[3*lst_fch_slt.index(fich) + 1])
    ax[1].plot(st[0].data, lw = 0.5)
    st = read(lst_fch_acc[3*lst_fch_slt.index(fich) + 2])
    ax[2].plot(st[0].data, lw = 0.5)

    os.chdir(path_pdf)
    fig.savefig(fich[:6] + '.pdf')
    os.chdir(path_png)
    fig.savefig(fich[:6] + '.png')


#os.chdir(path_sac)
#st = read(station + '.EW.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[0, 0].plot(st[0].data, lw = 0.5)
#st = read(station + '.NS.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[1, 0].plot(st[0].data, lw = 0.5)
#st = read(station + '.UD.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[2, 0].plot(st[0].data, lw = 0.5)

#os.chdir(path_vel)
#st = read(station + '.EW_vel.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[0, 1].plot(st[0].data, lw = 0.5)
#st = read(station + '.NS_vel.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[1, 1].plot(st[0].data, lw = 0.5)
#st = read(station + '.UD_vel.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax[2, 1].plot(st[0].data, lw = 0.5)

#for freq in lst_frq:
#    os.chdir(lst_pth_vel_frq[lst_frq.index(freq)])
#    st = read(station + '.EW_vel_' + freq + 'Hz.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[0, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    st = read(station + '.NS_vel_' + freq + 'Hz.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[1, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    st = read(station + '.UD_vel_' + freq + 'Hz.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[2, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)

#    os.chdir(lst_pth_vel_frq_3cp[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[3, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_hor[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_hori.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[5, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_ver[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_vert.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[7, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_3cp_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[4, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[6, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_ver_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_vert_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax[8, lst_frq.index(freq) + 2].plot(st[0].data, lw = 0.5)


#os.chdir(path)
#fig.savefig('tttraces.pdf')

#fig2, ax2 = plt.subplots(3, 1, sharex = 'col')
#ax2[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax2[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax2[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#os.chdir(path_sac)
#st = read(station + '.EW.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax2[0].plot(t, st[0].data, lw = 0.5)
#st = read(station + '.NS.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax2[1].plot(t, st[0].data, lw = 0.5)
#st = read(station + '.UD.sac')
#t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#ax2[2].plot(t, st[0].data, lw = 0.5)
#os.chdir(path)
#fig2.savefig('accelero.pdf')
#fig2.savefig('accelero.png')

#fig3, ax3 = plt.subplots(5, 1, sharex = 'col')
#ax3[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax3[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax3[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax3[3].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax3[4].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#for freq in lst_frq:
#    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax3[lst_frq.index(freq)].plot(t, st[0].data, lw = 0.5)
#os.chdir(path)
#fig3.savefig('envfreq.pdf')
#fig3.savefig('envfreq.png')

#fig4, ax4 = plt.subplots(5, 1, sharex = 'col', sharey = 'all')
#ax4[0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax4[1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax4[2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax4[3].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax4[4].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#for freq in lst_frq:
#    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax4[lst_frq.index(freq)].plot(t, st[0].data, lw = 0.5)
#os.chdir(path)
#fig4.savefig('envfreqmmax.pdf')
#fig4.savefig('envfreqmmax.png')

#fig5, ax5 = plt.subplots(3, 3, sharex = 'col')
#ax5[0, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[0, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[0, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[1, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[1, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[1, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[2, 0].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[2, 1].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#ax5[2, 2].ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0))
#for freq in lst_frq[2:]:
#    os.chdir(lst_pth_vel_frq_3cp_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax5[0, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_hor_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_hori_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax5[1, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
#    os.chdir(lst_pth_vel_frq_ver_env[lst_frq.index(freq)])
#    st = read(station + '.vel_' + freq + 'Hz_vert_env.sac')
#    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
#    ax5[2, lst_frq.index(freq) - 2].plot(t, st[0].data, lw = 0.5)
#os.chdir(path)
#fig5.savefig('composition.pdf')
#fig5.savefig('composition.png')




















