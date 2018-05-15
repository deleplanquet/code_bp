import os
import pickle









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

path = (path_origin
        + '/Kumamoto/'
        + dossier)

path_data = [path + '/'
             + dossier
             + '_vel_'
             + couronne + 'km_'
             + frq + 'Hz']

lst_pth_dat = [path_data + '/'
               + dossier
               + '_vel_'
               + couronne + 'km_'
               + frq + 'Hz_'
               + dt_type
               + '_env_smooth_'
               + hyp_bp
               + azim + 'deg']
for i in range(3):
    lst_pth_dat.append(lst_pth_dat[i]
                       + '_patch_90')

for loc_fold in lst_pth_dat:
    os.chdir(loc_fold)
    lst_sta = os.listdir(loc_fold)
    lst_sta.sort()





for ptch in lst_ptch:
    os.chdir(path_data)
    with open(, 'rb') as mfch:
        mdpck = pickle.Unpickler(mfch)
        patch = mdpck.load()







