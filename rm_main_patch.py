import numpy as np
import os
from obspy import read
from scipy import interpolate






#nombres de lignes d'un fichier
def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#normalisation avec max = 1
def norm1(vect):
    return [a/vect.max() for a in vect]

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

#dossier = param['dossier']
dossier = '20160415000300'

path = path_origin + '/Kumamoto/' + dossier

os.chdir(path)
with open(dossier + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

dt_type = param['composante']
hyp_bp = param['ondes_select']
couronne = param['couronne']
azim = param['angle']
frq = param['band_freq']
R_Earth = param['R_Earth']

if hyp_bp == 'P':
    vel_used = param['vP']
    dict_vel_used = dict_vel[0]
elif hyp_bp = 'S':
    vel_used = param['vS']
    dict_vel_used = dict_vel[1]

samp_rate = param['samp_rate']
length_time = param['length_t']


path = path_origin + '/Kumamoto/' + dossier
path_data = path + '/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz_' + dt_type + '_env_smooth_' + hyp_bp + '_' + azim + 'deg'
path_results = path + '/' + dossier + '_results/' + dossier + '_vel_' + couronne + 'km_' + frq + 'Hz'

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = os.listdir(path_data)
lst_fch.sort()

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    dict_seis = my_dpck.load()

yea_seis = int(dict_seis[dossier]['nFnet'][0:4])
mon_seis = int(dict_seis[dossier]['nFnet'][4:6])
day_seis = int(dict_seis[dossier]['nFnet'][6:8])
hou_seis = int(dict_seis[dossier]['nFnet'][8:10])
min_seis = int(dict_seis[dossier]['nFnet'][10:12])
sec_seis = int(dict_seis[dossier]['nFnet'][12:14])
mse_seis = int(dict_seis[dossier]['nFnet'][14:16])

t_origin_rupt = UTCDateTime(yea_seis, mon_seis, day_seis, hou_seis, min_seis, sec_seis, mse_seis)

lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']


nbr_sfaults = file_length(dossier + '_subfault_positions.txt')

stack = np.zeros((nbr_sfaults, len(lst_fch), length_t))
for station in lst_fch:
    os.chdir(path_data)
    st = read(station)
    tstart = st[0].stats.starttime
    env_norm = norm1(st[0].data)
    t = np.arange(st[0].stats.npts)/st[0].stats.sampling_rate
    f = interpolate.interp1d(t, env_norm)
    fmax = 0
    for it in t:
        if f(it) > fmax:
            fmax = f(it)

    ista = lst_fch.index(station)

    for ix in range(nbr_sfaults):
        for it in range(length_t):
            tshift = travt[ista][ix] - (st[0].stats.starttime - t_origin_rupt) + dict_ve_used[st[0].stats.station] - 5 + it/samp_rate
            if tshift > 0 and tshift < t[-1]:
                if (it > <) and (ix > < (it)) and (f(tshift) > 0.1*fmax):
                    stack[ix, ista, it] = 0.1 * f.max
                else:
                    stack[ix, ista, it] = f(tshift)



















