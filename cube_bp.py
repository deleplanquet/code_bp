











import math
import pickle
import os



#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion angle radian -> degre
def r2d(angle):
    return angle*180/math.pi

#conversion coordonnees geographiques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    x = r*math.cos(rlat)*math.cos(rlon)
    y = r*math.cos(rlat)*math.sin(rlon)
    z = r*math.sin(rlat)
    return [x, y, z]

#conversion coordonnees cartesiennes -> geographiques
def cart2geo(x, y, z):
    r = math.sqrt(x*x + y*y + z*z)
    lon = math.acos(x/math.sqrt(x*x + y*y))
    lat = math.acos(math.sqrt((x*x + y*y)/(r*r)))
    return [r, lat, lon]

#normalisation
def norm(vect):
    Norm = math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])
    return [vect[0]/Norm, vect[1]/Norm, vect[2]/Norm]


path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('ref_seismes_bin', 'rb') as mfch:
    mdpk = pickle.Unpickler(mfch)
    dict_seis = mdpk.load()

#dossier = param['dossier']
dossier = '20160415000300'

path = path_origin + '/Kumamoto/' + dossier

os.chdir(path)
with open(dossier + '_veldata', 'rb') as mon_fich:
    mon_depick = pickle.Unpickler(mon_fich)
    dict_vel = mon_depick.load()

R_Earth = param['R_Earth']




lat_hyp = dict_seis[dossier]['lat']
lon_hyp = dict_seis[dossier]['lon']
dep_hyp = dict_seis[dossier]['dep']

vhyp = geo2cart(R_Earth - dep_hyp, lat_hyp, lon_hyp)
vnor = norm([- vhyp[0]*vhyp[2], - vhyp[1]*vhyp[2], vhyp[0]*vhyp[0] + vhyp[1]*vhyp[1]])
veas = norm([- vhyp[1], vhyp[0], 0])





os.chdir(path)
with open(dossier + '_subfault_positions.txt', 'w') as myext:
    for i in range(12):
        for j in range(14):
            for k in range(10):
                xx = vhyp[0] + 2*(i-6)*veas[0] + 2*(j-5)*vnor[0] - 2*(k-3)*norm(vhyp)[0]
                yy = vhyp[1] + 2*(i-6)*veas[1] + 2*(j-5)*vnor[1] - 2*(k-3)*norm(vhyp)[1]
                zz = vhyp[2] + 2*(i-6)*veas[2] + 2*(j-5)*vnor[2] - 2*(k-3)*norm(vhyp)[2]
                rsf, latsf, lonsf = cart2geo(xx, yy, zz)
                myext.write(str(r2d(latsf)) + ' ' + str(r2d(lonsf)) + ' ' + str(rsf - R_Earth) + '\n')
