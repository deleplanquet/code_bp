#

from obspy import read
import os
from obspy.signal.util import smooth
import matplotlib.pyplot as plt
import numpy as np
import pickle

print('#################################',
    '\n###   plot_chrono_traces.py   ###',
    '\n#################################')

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

# directories used in this script
#
#
path_acc = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'acc/'
            + 'inf100km_copy')
path_vel = (root_folder + '/'
            + 'Kumamoto/'
            + event + '/'
            + 'vel/'
            + 'brut')
path_vel_flt = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'vel/'
                + frq_bnd + 'Hz')
path_hori_env = (root_folder + '/'
                    + 'Kumamoto/'
                    + event + '/'
                    + 'vel_env/'
                    + frq_bnd + 'Hz_hori')
path_hori_env_smt = (root_folder + '/'
                        + 'Kumamoto/'
                        + event + '/'
                        + 'vel_env/'
                        + frq_bnd + 'Hz_hori_smooth')
path_3cpn_env = (root_folder + '/'
                    + 'Kumamoto/'
                    + event + '/'
                    + 'vel_env/'
                    + frq_bnd + 'Hz_3cpn')
path_3cpn_env_smt = (root_folder + '/'
                        + 'Kumamoto/'
                        + event + '/'
                        + 'vel_env/'
                        + frq_bnd + 'Hz_3cpn_smooth')
path_vert_env = (root_folder + '/'
                    + 'Kumamoto/'
                    + event + '/'
                    + 'vel_env/'
                    + frq_bnd + 'Hz_vert')
path_vert_env_smt = (root_folder + '/'
                        + 'Kumamoto/'
                        + event + '/'
                        + 'vel_env/'
                        + frq_bnd + 'Hz_vert_smooth')
path_rslt = (root_folder + '/'
                + 'Kumamoto/'
                + event + '/'
                + 'results/'
                + 'miscellaneous_plots')
'''
path = path_origin + '/Kumamoto/' + dossier

path_data_1 = path + '/' + dossier + '_sac_inf100km'
path_data_2 = path + '/' + dossier + '_vel_0-100km'
path_data_3 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier
                    + '_vel_0-100km_2.0-8.0Hz'
path_data_4 = path + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/' + dossier
                    + '_vel_0-100km_2.0-8.0Hz_hori_env'

#path_data_1 = path + '/' + dossier + '_sac_inf100km_picks-save'
#path_data_int = path + '/' + 'noise_03'
#path_data_2 = path_data_int + '/' + dossier + '_vel_0-100km'
#path_data_3 = path_data_int + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/'
                    + dossier + '_vel_0-100km_2.0-8.0Hz'
#path_data_4 = path_data_int + '/' + dossier + '_vel_0-100km_2.0-8.0Hz/'
                    + dossier + '_vel_0-100km_2.0-8.0Hz_hori_env'
'''
# create the directory path_rslt in case it does not exist
if not os.path.isdir(path_rslt):
    try:
        os.makedirs(path_rslt)
    except OSError:
        print('Creation of the directory {} failed'.format(path_rslt))
    else:
        print('Successfully created the directory {}'.format(path_rslt))
else:
    print('{} is already existing'.format(path_rslt))

lst_sta_acc = os.listdir(path_acc)
lst_sta_vel = os.listdir(path_vel)
lst_sta_vel_flt = os.listdir(path_vel_flt)
lst_sta_hori_env = os.listdir(path_hori_env)
lst_sta_hori_env_smt = os.listdir(path_hori_env_smt)
lst_sta_3cpn_env = os.listdir(path_3cpn_env)
lst_sta_3cpn_env_smt = os.listdir(path_3cpn_env_smt)
lst_sta_vert_env = os.listdir(path_vert_env)
lst_sta_vert_env_smt = os.listdir(path_vert_env_smt)
lst_sta = os.listdir(path_hori_env_smt)
lst_sta = [a for a in lst_sta if '.sac' in a]

cpn_lst1 = ['EW', 'NS', 'UD']
cpn_lst2 = ['EW + NS\nhorizontal',
            'EW + NS + UD\n3-dimension',
            'UD\nvertical']

nlin, ncol = 5, 3
for s in lst_sta:
    # creation fig and ax
    fig, ax = plt.subplots(nlin, ncol,
                            figsize = (13, 10),
                            constrained_layout = True)
    # first line, acceleration
    lst_acc = [a for a in lst_sta_acc if s[:6] in a]
    lst_acc.sort()
    os.chdir(path_acc)
    mn, mx = 0, 0
    stE, stN, stU = read(lst_acc[0]), read(lst_acc[1]), read(lst_acc[2])
    PP = stU[0].stats.sac.a
    for i, acc in enumerate([stE, stN, stU]):
        acc.detrend(type = 'constant')
        t = np.arange(acc[0].stats.npts)/acc[0].stats.sampling_rate
        t = [a - PP + 5 for a in t]
        ax[0, i].plot(t, acc[0].data,
                        color = 'black',
                        lw = 0.5,
                        label = cpn_lst1[i])
        mn = min([mn, acc[0].data.min()])
        mx = max([mx, acc[0].data.max()])
    for i in range(ncol):
        ax[0, i].set_ylim([1.1*mn, 1.1*mx])
    ax[0, 0].text(4, 0.6*mx, 'P',
                    color = 'blue')
    ax[0, 0].text(acc[0].stats.sac.t0 - PP + 4, 0.6*mx, 'S',
                    color = 'red')
    print(s, mx, mn, (mx - mn)/2)
    # second line, velocity
    lst_vel = [a for a in lst_sta_vel if s[:6] in a]
    lst_vel.sort()
    os.chdir(path_vel)
    mn, mx = 0, 0
    for i, vel in enumerate(lst_vel):
        st = read(vel)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[1, i].plot(t, st[0].data,
                        color = 'black',
                        lw = 0.5,
                        label = cpn_lst1[i])
        mn = min([mn, st[0].data.min()])
        mx = max([mx, st[0].data.max()])
    for i in range(ncol):
        ax[1, i].set_ylim([1.1*mn, 1.1*mx])
    # third line, filtered velocity
    lst_vel_flt = [a for a in lst_sta_vel_flt if s[:6] in a]
    lst_vel_flt.sort()
    os.chdir(path_vel_flt)
    mn, mx = 0, 0
    for i, vel_flt in enumerate(lst_vel_flt):
        st = read(vel_flt)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[2, i].plot(t, st[0].data,
                        color = 'black',
                        lw = 0.5,
                        label = cpn_lst1[i])
        mn = min([mn, st[0].data.min()])
        mx = max([mx, st[0].data.max()])
    for i in range(ncol):
        ax[2, i].set_ylim([1.1*mn, 1.1*mx])
    # fourth line, envelopes
    lst_env_cpn = ([a for a in lst_sta_hori_env if s[:6] in a]
                    + [a for a in lst_sta_3cpn_env if s[:6] in a]
                    + [a for a in lst_sta_vert_env if s[:6] in a])
    mn, mx = 0, 0
    for i, (pth, env_cpn) in enumerate(zip([path_hori_env,
                                            path_3cpn_env,
                                            path_vert_env],
                                           lst_env_cpn)):
        os.chdir(pth)
        st = read(env_cpn)
        t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[3, i].plot(t, st[0].data,
                        color = 'black',
                        lw = 0.5,
                        label = cpn_lst2[i])
        mn = min([mn, st[0].data.min()])
        mx = max([mx, st[0].data.max()])
    for i in range(ncol):
        ax[3, i].set_ylim([mn, 1.1*mx])
    # fifth line, smoothed envelopes
    lst_env_cpn_smt = ([a for a in lst_sta_hori_env_smt if s[:6] in a]
                        + [a for a in lst_sta_3cpn_env_smt if s[:6] in a]
                        + [a for a in lst_sta_vert_env_smt if s[:6] in a])
    mn, mx = 0, 0
    for i, (pth, env_cpn_smt) in enumerate(zip([path_hori_env_smt,
                                                path_3cpn_env_smt,
                                                path_vert_env_smt],
                                               lst_env_cpn_smt)):
        os.chdir(pth)
        st = read(env_cpn_smt)
        t= np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
        ax[4, i].plot(t, st[0].data,
                        color = 'black',
                        lw = 0.5,
                        label = cpn_lst2[i])
        mn = min([mn, st[0].data.min()])
        mx = max([mx, st[0].data.max()])
    for i in range(ncol):
        ax[4, i].set_ylim([mn, 1.1*mx])
    # P and S waves lines
    Pwav, Swav = st[0].stats.sac.a, st[0].stats.sac.t0
    for i in range(nlin):
        for j in range(ncol):
            ax[i, j].axvline(Pwav, color = 'blue', lw = 1)
            ax[i, j].axvline(Swav, color = 'red', lw = 1)
    # set xlim 0 to 30 and hide axes
    for i in range(ncol):
        ax[0, i].set_xlim([-5 + st[0].stats.sac.a, 25 + st[0].stats.sac.a])
    for i in range(nlin - 1):
        for j in range(ncol):
            ax[i + 1, j].set_xlim([0, 30])
            ax[i, j].xaxis.set_visible(False)
    for i in range(nlin):
        for j in range(ncol - 1):
            ax[i, j + 1].yaxis.set_visible(False)
    # scientific notations
    for i in range(nlin):
        for j in range(ncol):
            ax[i, j].ticklabel_format(style = 'scientific',
                                        axis = 'y',
                                        scilimits = (0, 2))
            ax[i, j].legend(fontsize = 10, loc = 1)
    # ax titles
    for i, tit in enumerate(['Acceleration\n($m.s^{-2}$)',
                             'Velocity\n($m.s^{-1}$)',
                             'Filtered velocity\n($m.s^{-1}$)',
                             'Envelopes\n($m^{2}.s^{2}$)',
                             'Smoothed envelopes\n($m^{2}.s^{2}$)']):
        ax[i, 0].set_ylabel(tit, fontsize = 10)
    ax[nlin - 1, int(ncol/2)].set_xlabel('Time (s)', fontsize = 10)

    os.chdir(path_rslt)
    fig.savefig(event + '_' + s[:6] + '.pdf')

'''
os.chdir(path_data_1)
st1 = read('KMM0181604151739.NS.sac')
#st1 = read('KMM006.NS.sac')
#st1 = read('KMM018.NS.sac')
st1.detrend(type = 'constant')
t1 = np.arange(st1[0].stats.npts)/st1[0].stats.sampling_rate
st1_max = max(st1[0].data)
st1_min = min(st1[0].data)

st6 = read('KMM0181604151739.EW.sac')
st6.detrend(type = 'constant')
t6 = np.arange(st6[0].stats.npts)/st6[0].stats.sampling_rate
st6_max = max(st6[0].data)
st6_min = min(st6[0].data)

os.chdir(path_data_2)
st2 = read('KMM0181604151739.NS_vel_0-100km.sac')
#st2 = read('KMM006_NS_20160401000001_vel_0-100km.sac')
#st2 = read('KMM018_NS_20160401000001_vel_0-100km.sac')
t2 = np.arange(st2[0].stats.npts)/st2[0].stats.sampling_rate
st2_max = max(st2[0].data)
st2_min = min(st2[0].data)

os.chdir(path_data_3)
st3 = read('KMM0181604151739.NS_vel_0-100km-2.0-8.0Hz.sac')
#st3 = read('KMM006_NS_20160401000001_vel_0-100km_2.0-8.0Hz.sac')
#st3 = read('KMM018_NS_20160401000001_vel_0-100km_2.0-8.0Hz.sac')
t3 = np.arange(st3[0].stats.npts)/st3[0].stats.sampling_rate
st3_max = max(st3[0].data)
st3_min = min(st3[0].data)

os.chdir(path_data_4)
st4 = read('KMM0181604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')
#st4 = read('KMM00620160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')
#st4 = read('KMM01820160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')
t4 = np.arange(st4[0].stats.npts)/st4[0].stats.sampling_rate
st4_max = max(st4[0].data)
st4_min = min(st4[0].data)

dat5 = smooth(st4[0].data, int(0.1/st4[0].stats.delta))
st5_max = max(dat5)
st5_min = min(dat5)

ax[0].plot(t1, st1[0],
           color = 'black',
           lw = 0.5)
ax[0].set_xlim([3.9, 3.9 + 30])
ax[0].set_ylim([st1_min - 0.05*(st1_max - st1_min), st1_max + 0.05*(st1_max - st1_min)])
ax[1].plot(t6, st6[0],
           color = 'black',
           lw = 0.5)
ax[1].set_xlim([3.9, 3.9 + 30])
ax[1].set_ylim([st6_min - 0.05*(st6_max - st6_min), st6_max + 0.05*(st6_max - st6_min)])
ax[2].plot(t2, st2[0],
           color = 'black',
           lw = 0.5)
ax[2].set_xlim([0, 30])
ax[2].set_ylim([st2_min - 0.05*(st2_max - st2_min), st2_max + 0.05*(st2_max - st2_min)])
ax[3].plot(t3, st3[0],
           color = 'black',
           lw = 0.5)
ax[3].set_xlim([0, 30])
ax[3].set_ylim([st3_min - 0.05*(st3_max - st3_min), st3_max + 0.05*(st3_max - st3_min)])
ax[4].plot(t4, st4[0],
           color = 'black',
           lw = 0.5)
ax[4].set_xlim([0, 30])
ax[4].set_ylim(bottom = 0)
ax[4].set_ylim([0, st4_max + 0.1*st4_max])
ax[5].plot(t4, dat5,
           color = 'black',
           lw = 0.5)
ax[5].set_xlim([0, 30])
ax[5].set_ylim(bottom = 0)
ax[5].set_ylim([0, st5_max + 0.1*st5_max])

plt.subplots_adjust(hspace = 0.1)
ax[0].xaxis.set_visible(False)
ax[1].xaxis.set_visible(False)
ax[2].xaxis.set_visible(False)
ax[3].xaxis.set_visible(False)
ax[4].xaxis.set_visible(False)
#ax[5].xaxis.set_visible(False)

#ax[0].yaxis.set_visible(False)
#ax[1].yaxis.set_visible(False)
#ax[2].yaxis.set_visible(False)
#ax[3].yaxis.set_visible(False)
#ax[4].yaxis.set_visible(False)
#ax[5].yaxis.set_visible(False)

ax[0].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[1].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[2].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[3].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[4].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))
ax[5].ticklabel_format(style = 'scientific',
                       axis = 'y',
                       scilimits = (0, 2))

ax[0].yaxis.set_label_position('right')
ax[1].yaxis.set_label_position('right')
ax[2].yaxis.set_label_position('right')
ax[3].yaxis.set_label_position('right')
ax[4].yaxis.set_label_position('right')
ax[5].yaxis.set_label_position('right')

ax[0].yaxis.offsetText.set_visible(False)
offset0 = ax[0].yaxis.get_major_formatter().get_offset()
print(offset0)
ax[0].text(4, st1_max, '1e3', fontsize = 8, va = 'top')
ax[1].yaxis.offsetText.set_visible(False)
offset1 = ax[1].yaxis.get_major_formatter().get_offset()
ax[1].text(4, st6_max, '1e4', fontsize = 8, va = 'top')
ax[2].yaxis.offsetText.set_visible(False)
offset2 = ax[2].yaxis.get_offset_text()
ax[2].text(0.2, st2_max, '1e5', fontsize = 8, va = 'top')
ax[3].yaxis.offsetText.set_visible(False)
offset3 = ax[3].yaxis.get_offset_text()
ax[3].text(0.2, st3_max, '1e5', fontsize = 8, va = 'top')
ax[4].yaxis.offsetText.set_visible(False)
offset4 = ax[4].yaxis.get_offset_text()
ax[4].text(0.2, st4_max, '1e11', fontsize = 8, va = 'top')
ax[5].yaxis.offsetText.set_visible(False)
offset5 = ax[5].yaxis.get_offset_text()
ax[5].text(0.2, st5_max, '1e10', fontsize = 8, va = 'top')

ax[0].tick_params(labelsize = 8)
ax[1].tick_params(labelsize = 8)
ax[2].tick_params(labelsize = 8)
ax[3].tick_params(labelsize = 8)
ax[4].tick_params(labelsize = 8)
ax[5].tick_params(labelsize = 8)

ax[0].yaxis.offsetText.set_fontsize(8)
ax[1].yaxis.offsetText.set_fontsize(8)
ax[2].yaxis.offsetText.set_fontsize(8)
ax[3].yaxis.offsetText.set_fontsize(8)
ax[4].yaxis.offsetText.set_fontsize(8)
ax[5].yaxis.offsetText.set_fontsize(8)

#ax[0].yaxis.set_offset_position('right')
#ax[1].yaxis.set_offset_position('right')
#ax[2].yaxis.set_offset_position('right')
#ax[3].yaxis.set_offset_position('right')
#ax[4].yaxis.set_offset_position('right')

ax[5].set_xlabel('Time (s)',
                 fontsize = 8)
ax[0].set_ylabel('Acceleration\nNS (cm/s/s)',
                 fontsize = 7)
ax[1].set_ylabel('Acceleration\nEW (cm/s/s)',
                 fontsize = 7)
ax[2].set_ylabel('Velocity\n(cm/s)',
                 fontsize = 7)
ax[3].set_ylabel('2 to 8 Hz\nvelocity\n(cm/s)',
                 fontsize = 7)
ax[4].set_ylabel('Envelope\n(cm*cm/s/s)',
                 fontsize = 7)
ax[5].set_ylabel('Smoothed\nenvelope\n(cm*cm/s/s)',
                 fontsize = 7)

os.chdir(path)
fig.savefig(dossier + '_chrono.pdf')

fig2, ax2 = plt.subplots(2, 1)

os.chdir(path_data_4)
#sta = read('MYZ0071604151739.vel_0-100km_2.0-8.0Hz_hori_env.sac')
#sta = read('MYZ00720160401000001_vel_0-100km_2.0-8.0Hz_hori_env.sac')

#data = smooth(sta[0].data, int(0.5/sta[0].stats.delta))

#ax2[0].plot(t4, dat5)
#ax2[1].plot(t4, data)

#plt.subplots_adjust(hspace = 0.001)
#ax2[0].xaxis.set_visible(False)
#ax2[1].xaxis.set_visible(False)

#ax2[0].yaxis.set_visible(False)
#ax2[1].yaxis.set_visible(False)

#os.chdir(path)
#fig2.savefig(dossier + '_comparaison_SP.pdf')
'''
