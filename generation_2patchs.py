import os
from pylab import *
import pickle
from obspy import read
from obspy import Trace
import numpy as np
import math

#conversion angle degre -> radian
def d2r(angle):
    return angle*math.pi/180

#conversion angle radian -> degre
def r2d(angle):
    return angle*180/math.pi

#conversion coordonnees geographisques -> cartesien
def geo2cart(r, lat, lon):
    rlat = d2r(lat)
    rlon = d2r(lon)
    xx = r*math.cos(rlat)*math.cos(rlon)
    yy = r*math.cos(rlat)*math.sin(rlon)
    zz = r*math.sin(rlat)
    return [xx, yy, zz]

#conversion coordonnees cartesien -> geographiques
def cart2geo(x, y, z):
    r = math.sqrt(x*x + y*y + z*z)
    lat = math.acos(math.sqrt((x*x + y*y)/(r*r)))
    lon = math.acos(x/math.sqrt(x*x + y*y))
    return [r, r2d(lat), r2d(lon)]

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
    mat = array([[a*a + (1 - a*a)*math.cos(radian),
                a*b*(1 - math.cos(radian)) - c*math.sin(radian),
                a*c*(1 - math.cos(radian)) + b*math.sin(radian)],
                [a*b*(1 - math.cos(radian)) + c*math.sin(radian),
                b*b + (1 - b*b)*math.cos(radian),
                b*c*(1 - math.cos(radian)) - a*math.sin(radian)],
                [a*c*(1 - math.cos(radian)) - b*math.sin(radian),
                b*c*(1 - math.cos(radian)) + a*math.sin(radian),
                c*c + (1 - c*c)*math.cos(radian)]])
    #rearrangement du vecteur auquel on applique la rotation
    vect = array([[u[0]], [u[1]], [u[2]]])
    #rotation du vecteur u de theta autour de OM
    vect_rot = dot(mat, vect)
    return (vect_rot[0][0], vect_rot[1][0], vect_rot[2][0])

def dist_azim(ptA, ptB, R):
    '''distance et azimuth de B par rapport a A -> dist_azim(A, B)'''
    latA = d2r(ptA[0])
    lonA = d2r(ptA[1])
    latB = d2r(ptB[0])
    lonB = d2r(ptB[1])
    dist_rad = math.acos(math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(lonB - lonA))
    angle_brut = math.acos((math.sin(latB) - math.sin(latA)*math.cos(dist_rad))/(math.cos(latA)*math.sin(dist_rad)))
    if math.sin(lonB - lonA) > 0:
        return R*dist_rad, r2d(angle_brut)
    else:
        return R*dist_rad, 360 - r2d(angle_brut)

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as myfch:
    mydpck = pickle.Unpickler(myfch)
    param = mydpck.load()

strike = param['strike']
dip = param['dip']
R_Earth = param['R_Earth']

dossier = param['dossier']
nbr_ptch = dossier[-1]
dossier = dossier_source[:-1] + '0'

path = path_origin + '/Kumamoto/' + dossier + '/' + dossier + '_sac_inf100km'
path_data = path_origin + '/Kumamoto/' + dossier_source + '/' + dossier_source + '_sac_0-100km'

if os.path.isdir(path) == False:
    os.makedirs(path)

lst_fch = os.listdir(path_data)

os.chdir(path_origin + '/Kumamoto')
with open('ref_seismes_bin', 'rb') as myfch:
    mydpck = pickle.Unpickler(myfch)
    dict_seis = mydpck.load()

lat_hyp = dict_seis[dossier_source]['lat']
lon_hyp = dict_seis[dossier_source]['lon']
dep_hyp = dict_seis[dossier_source]['dep']
print(lat_hyp, lon_hyp, dep_hyp)

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

dir_cen_fault = [math.cos(d2r(lat_hyp))*math.cos(d2r(lon_hyp)), math.cos(d2r(lat_hyp))*math.sin(d2r(lon_hyp)), math.sin(d2r(lat_hyp))]
vect_nord = rotation(dir_cen_fault, 90, [math.sin(d2r(lon_hyp)), -math.cos(d2r(lon_hyp)), 0])
vect_strike = rotation(vect_nord, -strike, dir_cen_fault)
vect_perp_strike = rotation(vect_nord, -strike-90, dir_cen_fault)
vect_dip = rotation(vect_perp_strike, dip, vect_strike)

x_hyp, y_hyp, z_hyp = geo2cart(R_Earth - dep_hyp, lat_hyp, lon_hyp)

#x_hyp_2 = x_hyp - 10*u_strike[0] - 4*u_dip[0]
#y_hyp_2 = y_hyp - 10*u_strike[1] - 4*u_dip[1]
#z_hyp_2 = z_hyp - 10*u_strike[2] - 4*u_dip[2]

x_hyp_2 = x_hyp - 30*u_strike[0] - 0*u_dip[0]
y_hyp_2 = y_hyp - 30*u_strike[1] - 0*u_dip[1]
z_hyp_2 = z_hyp - 30*u_strike[2] - 0*u_dip[2]

dep_hyp_2, lat_hyp_2, lon_hyp_2 = cart2geo(x_hyp_2, y_hyp_2, z_hyp_2)
dep_hyp_2 = R_Earth - dep_hyp_2
print(lat_hyp_2, lon_hyp_2, dep_hyp_2)

dst_hh, azm_hh = dist_azim([lat_hyp_2, lon_hyp_2], [lat_hyp, lon_hyp], R_Earth)
print(dst_hh, azm_hh)

for fich in lst_fch:
    os.chdir(path_data)
    st = read(fich)
    st.detrend(type = 'constant')
    tr = st[0].data
    #cpt = len(tr)

    dst_hs, azm_hs = dist_azim([lat_hyp, lon_hyp], [st[0].stats.sac.stla, st[0].stats.sac.stlo], R_Earth)
    tt = 10 + math.sqrt(dst_hh*dst_hh + dst_hs*dst_hs + 2*dst_hh*dst_hs*math.cos(azm_hs - azm_hh))/3.4 - dst_hs/3.4

    if tt >= 0:
        cpt = len(tr)
        for dat in tr:
            cpt = cpt - 1
            if cpt > tt*st[0].stats.sampling_rate:
                if nbr_ptch == '2':
                    tr[cpt] = tr[cpt] + tr[cpt - int(tt*st[0].stats.sampling_rate)]
                elif nbr_ptch == '1':
                    tr[cpt] = tr[cpt - int(tt*st[0].stats.sampling_rate)]
            else:
                tr[cpt] = 0

    else:            
        cpt = -1
        for dat in tr:
            cpt = cpt + 1
            if cpt < len(tr) + tt*st[0].stats.sampling_rate:
                if nbr_ptch == '2':
                    tr[cpt] = tr[cpt] + tr[cpt - int(tt*st[0].stats.sampling_rate)]
                elif nbr_ptch == '1':
                    tr[cpt] = tr[cpt - int(tt*st[0].stats.sampling_rate)]
            else:
                tr[cpt] = 0

    os.chdir(path)
    if 'UD' in fich:
        print(fich, '   ', st[0].stats.sac.t0, '   ', tt, '   ',  st[0].stats.sac.t0 + tt, '   ', int(tt*st[0].stats.sampling_rate))
        st[0].stats.sac.user1 = st[0].stats.sac.t0 + tt
    tr_reg = Trace(np.asarray(tr), st[0].stats)
    tr_reg.write(fich[:15] + str(nbr_ptch) + fich[16:-4] + '.sac', format = 'SAC')




