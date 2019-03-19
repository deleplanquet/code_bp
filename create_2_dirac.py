import os
from obspy import read
from obspy import Trace
import numpy as np
import math
import pickle

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion coordonnees geographiques -> cartesien
def geo2cart(vect):
    r = vect[0]
    rlat = d2r(vect[1])
    rlon = d2r(vect[2])
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#distance entre deux points, coordonnees cartesiennes
def dist(vect1, vect2):
    x1, y1, z1 = geo2cart(vect1)
    x2, y2, z2 = geo2cart(vect2)
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2), 0.5)

#sigma gaussienne
# la largeur a mi-hauteur d'une gaussienne est egale a 2,3548 fois son ecart type (wikipwdia, a verifier)
# on va supposer un signal d'amplitude maximale egale a 1 (facteur egale a 1 devant l'exponentielle)
# et une largeur a mi-hauteur de 1 (sec) (sigma = 1/2.3548)
sigma = 1./2.3548
#        /    (x - dist)*(x - dist)  \
# f = exp| -  ---------------------  |
#        \        2*sigma*sigma      /

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    param = mdpk.load()

R_Earth = param['R_Earth']
vS = param['vS']
dossier_dirac = '20160401000001'
dossier_2_dirac = '20160401000003'

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

lat_hyp = dict_seis[dossier_dirac]['lat']
lon_hyp = dict_seis[dossier_dirac]['lon']
dep_hyp = dict_seis[dossier_dirac]['dep']

pos_hyp = [R_Earth - dep_hyp, lat_hyp, lon_hyp]
#pos_hyp1 = [R_Earth - dep_hyp, 32.7222, 130.7259]
#pos_hyp2 = [R_Earth - dep_hyp, 32.7868, 130.8001] # 5 km de chaque cote
pos_hyp1 = [R_Earth - dep_hyp, 32.6898, 130.6888]
pos_hyp2 = [R_Earth - dep_hyp, 32.8192, 130.8373] # 10 km de chaque cote

path_data = (path_origin + '/'
             + 'Kumamoto/'
             + dossier_dirac + '/'
             + dossier_dirac + '_sac_inf100km_picks-save')

path_results = (path_origin + '/'
                + 'Kumamoto/'
                + dossier_2_dirac + '/'
                + dossier_2_dirac + '_sac_inf100km')

if os.path.isdir(path_results) == False:
    os.makedirs(path_results)

lst_fch = []
lst_fch = os.listdir(path_data)

factor = 1*100*100

for fichier in lst_fch:
    if (('EW1' in fichier) or ('NS1' in fichier) or ('UD1' in fichier)) == False:
        os.chdir(path_data)
        st = read(fichier)
        stz = read(fichier[:7] + 'UD' + fichier[9:])
        #vecteur de base pour creer le signal dirac
        vect = np.linspace(0, st[0].stats.npts/st[0].stats.sampling_rate, st[0].stats.npts)
        #position station et distance a l'hypocentre
        pos_sta = [R_Earth + 0.001*st[0].stats.sac.stel,
                   st[0].stats.sac.stla,
                   st[0].stats.sac.stlo]
        dst = dist(pos_hyp, pos_sta)
        dst1 = dist(pos_hyp1, pos_sta)
        dst2 = dist(pos_hyp2, pos_sta)
        if dst <= 100:
            #bruit blanc distribution normale
            nois = np.random.normal(0, 0.5, st[0].stats.npts)
            tr = [math.exp(-(pow(a - dst1/vS, 2))/(2*pow(sigma, 2)))*factor/pow(dst, 2)
                  + 0.5*math.exp(-(pow(a - dst2/vS, 2))/(2*pow(sigma, 2)))*factor/pow(dst, 2)
                  + 0.1*b for a, b in zip(vect, nois)]
            tstart = stz[0].stats.starttime + stz[0].stats.sac.a - 5
            tend = tstart + 50
            tr = Trace(np.asarray(tr, np.ndarray), st[0].stats)
            tr = tr.trim(tstart, tend, pad = True, fill_value = 0)
            #tr.stats.sac.t0 = stz[0].stats.sac.a
            #tr.stats.sac.a = stz[0].stats.sac.a
            tr.stats.sac.t0 = 5
            tr.stats.sac.a = 5
            os.chdir(path_results)
            if ('EW2' in fichier) or ('NS2' in fichier) or ('UD2' in fichier) == True:
                tr.write(fichier[:6] + fichier[-8:], format = 'SAC')
            else:
                tr.write(fichier[:6] + fichier[-7:], format = 'SAC')
