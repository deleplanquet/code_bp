import numpy as np
import math
import cmath
from math import sqrt
import matplotlib.pyplot as plt
import os
import obspy
from scipy import interpolate
from scipy.optimize import curve_fit

def fit_vit_abs(x_data, alpha, beta, gamma):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
        y_data[i] = alpha * math.exp(-pow(x_data[i]-beta, 2)/gamma)

    return y_data

def func_1(x_data, alpha, beta, gamma, delta):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
	y_data[i] = alpha*math.exp(-beta*pow(x, 2) + gamma) + delta

    return y_data

def func_2(x_data, alpha, beta, b):
    y_data = np.zeros(len(x_data))
    for i in range(len(x_data)):
	y_data[i] = abs(math.sin(alpha*x_data[i])*math.sin(beta*x_data[i])) + b

    return y_data

i_inc_sta = 20. #angle incidence station
i_inc_fault = 45. #angle incidence faille
d_btw_sta = 3.e4 #distance entre station
d_fault_surf = 1.e6 #distance centre faille surface
r_S_0 = d_fault_surf/math.cos(i_inc_sta*math.pi/180.) #distance centre faille centre reseau de stations
Lx = 50000. #longueur supposee faille direction x
Ly = 50000. #longueur supposee faille direction y
dt = 200./3000. #pas en temps

alpha = 6000. #vitesse ondes P
nx = 51 #nbre points faille direction x
ny = 51 #nbre points faille direction y
dx = Lx/(nx - 1) #pas en espace direction x
dy = Ly/(ny - 1) #pas en espace direction y
nx_sta = 11 #nbre stations direction x
ny_sta = 11 #nbre stations direction y
r_S = np.zeros((nx_sta, ny_sta)) #matrice distance centre faille station (i, j)
theta_S = np.zeros((nx_sta, ny_sta)) #matrice angle theta centre faille station (i, j)
phi_S = np.zeros((nx_sta, ny_sta)) #matrice angle phi centre faille station (i, j)

#pour chaque station, calcul de la distance de l'angle theta et de l'angle phi par rapport au centre de la faille
for i in range(nx_sta):
    for j in range(ny_sta):
	x = - r_S_0*math.sin(i_inc_fault*math.pi/180) + d_btw_sta*(i - (nx_sta - 1)/2)*math.cos((i_inc_fault - i_inc_sta)*math.pi/180)
	y = d_btw_sta*(j - (ny_sta - 1)/2)
	z = r_S_0*math.cos(i_inc_fault*math.pi/180) + d_btw_sta*(i - (nx_sta - 1)/2)*math.sin((i_inc_fault - i_inc_sta)*math.pi/180)
	r_S[j, i] = pow(pow(x, 2) + pow(y, 2) + pow(z, 2), 0.5)
	theta_S[j, i] = (math.acos(z/r_S[j, i]))*180/math.pi
	if (j - (ny_sta - 1)/2) >= 0:
	    phi_S[j, i] = (math.acos(x/pow(pow(x, 2) + pow(y, 2), 0.5)))*180/math.pi
	else:
	    phi_S[j, i] = 360 - (math.acos(x/pow(pow(x, 2) + pow(y, 2), 0.5)))*180/math.pi
print "   calcul distance et angles termine"

tp = np.zeros((nx, ny, nx_sta, ny_sta)) #matrice temps trajet entre chaque point de la faille et chaque station
t = np.zeros((nx, ny, nx_sta, ny_sta))
#pour chaque station et chaque point de la faille, calcul du temps de trajet
for k in range(nx):
    for l in range(ny):
        for i in range(nx_sta):
            for j in range(ny_sta):
		xx = r_S[i, j]*math.sin(theta_S[i, j]*math.pi/180)*math.cos(phi_S[i, j]*math.pi/180) + (k - (nx - 1)/2)*dx
		yy = r_S[i, j]*math.sin(theta_S[i, j]*math.pi/180)*math.sin(phi_S[i, j]*math.pi/180) + (l - (ny - 1)/2)*dy
		zz = r_S[i, j]*math.cos(theta_S[i, j]*math.pi/180)
		tp[(nx - 1)-k, l, j, (nx_sta - 1)-i] = pow(pow(xx, 2) + pow(yy, 2) + pow(zz, 2), 0.5)/alpha
print "   calcul temps de trajet termine"

fig_test, ax_test = plt.subplots(1, 2)
ax_test[0].set_title("Theta")
ax_test[0].set_xlabel('i')
ax_test[0].set_ylabel('j')
cax_test1 = ax_test[0].imshow(theta_S[:, :], cmap='jet', interpolation = 'none', origin='lower')
ax_test[1].set_title("Phi")
ax_test[1].set_xlabel('i')
ax_test[1].set_ylabel('j')
cax_test2 = ax_test[1].imshow(phi_S[:, :], cmap='jet', interpolation = 'none', origin='lower')
fig_test.savefig('test.pdf')

#filtrage signaux
stack = np.zeros((nx, ny, 5000))

for k in range(nx):
    for l in range(ny):
        for i in range(nx_sta):
            for j in range(ny_sta):
                t[k, l, i, j] = tp[k, l, i, j] - tp[:, :, :, :].min()

#fig_test2, ax_test2 = plt.subplots(2, 3)
#ax_test2[0, 0].set_title("k=0 l=0")
#ax_test2[0, 0].set_xlabel('i')
#ax_test2[0, 0].set_ylabel('j')
#cax_test21 = ax_test2[0, 0].imshow(np.transpose(t[0, 0, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[0, 0].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
#ax_test2[0, 1].set_title("k=0 l=" + str(ny - 1))
#ax_test2[0, 1].set_xlabel('i')
#ax_test2[0, 1].set_ylabel('j')
#cax_test22 = ax_test2[0, 1].imshow(np.transpose(t[0, ny - 1, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[0, 1].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
#ax_test2[0, 2].set_title("k=" + str(nx - 1) + " l=" + str((ny - 1)/2))
#ax_test2[0, 2].set_xlabel('i')
#ax_test2[0, 2].set_ylabel('j')
#cax_test21 = ax_test2[0, 2].imshow(np.transpose(t[nx - 1, (ny - 1)/2, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[0, 2].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
#ax_test2[1, 0].set_title("i=0 j=0")
#ax_test2[1, 0].set_xlabel('k')
#ax_test2[1, 0].set_ylabel('l')
#cax_test22 = ax_test2[1, 0].imshow(np.transpose(t[:, :, 0, 0]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[1, 0].axhline((ny - 1)/2, color = 'k', linewidth = 2)
#ax_test2[1, 1].set_title("i=0 j=" + str(ny_sta - 1))
#ax_test2[1, 1].set_xlabel('k')
#ax_test2[1, 1].set_ylabel('l')
#cax_test21 = ax_test2[1, 1].imshow(np.transpose(t[:, :, 0, ny_sta - 1]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[1, 1].axhline((ny - 1)/2, color = 'k', linewidth = 2)
#ax_test2[1, 2].set_title("i=" + str(nx_sta - 1) + " j=" + str((ny_sta - 1)/2))
#ax_test2[1, 2].set_xlabel('k')
#ax_test2[1, 2].set_ylabel('l')
#cax_test22 = ax_test2[1, 2].imshow(np.transpose(t[:, :, nx_sta - 1, (ny_sta - 1)/2]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
#ax_test2[1, 2].axhline((ny - 1)/2, color = 'k', linewidth = 2)
#fig_test2.savefig('test2.pdf')

ARF_complex = np.zeros((nx, ny, 10), dtype = complex)
ARF = np.zeros((nx, ny, 10))
Nbre_sta = nx_sta*ny_sta
freq_list = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

#spread leakage
for k in range(nx):
    for l in range(ny):
	for frequency in range(len(freq_list)):
	    for i in range(nx_sta):
		for j in range(ny_sta):
		    ARF_complex[k, l, frequency] = ARF_complex[k, l, frequency] + cmath.exp(2*math.pi*1j*freq_list[frequency]*(t[k, l, i, j] - t[(nx-1)/2, (ny-1)/2, i, j]))
	    ARF[k, l, frequency] = pow(abs(ARF_complex[k, l, frequency]/Nbre_sta), 2)

fig_ARF, ax_ARF = plt.subplots(2, 5)
for frequency in range(len(freq_list)):
    ax_ARF[frequency//5, frequency%5].set_title(str(freq_list[frequency]) + 'Hz')
    ax_ARF[frequency//5, frequency%5].set_xlabel('k')
    ax_ARF[frequency//5, frequency%5].set_ylabel('l')
    ax_ARF[frequency//5, frequency%5].imshow(ARF[:, :, frequency], cmap='jet', interpolation='none', origin = 'lower')
    
    fig_ARF_unique, ax_ARF_unique = plt.subplots(1, 1)
    ax_ARF_unique.set_xlabel('k')
    ax_ARF_unique.set_ylabel('l')
    ax_ARF_unique.imshow(ARF[:, :, frequency], cmap='jet', interpolation='none', origin='lower')
    fig_ARF_unique.savefig('ARF_' + str(freq_list[frequency]) + 'Hz.pdf')

fig_ARF.savefig('ARF.pdf')



#for i in range(nx_sta):
for i in [5]:
    #for j in range(ny_sta):
    for j in [0, 10]:
        name = "/home/deleplanque/Documents/back_proj/en_cours/slippy_product-utilisepourbp/RC_250/x0_0/y0_0/v_R_3000/vel_vect/RC_250-x0_0-y0_0-vR_3000-x_%.0f-y_%.0f_tR0" % (i, j)
        tr = obspy.Trace(np.loadtxt(name))
        tr.stats.delta = dt
        tr_filt = tr.copy()
        tr_filt.filter('lowpass', freq=2.5, corners=2, zerophase=True)
        tr_filt.filter('highpass', freq=1.5, corners=2, zerophase=True)

        time = np.arange(0, len(tr_filt))
        time = time*dt

        #popt, pcov = curve_fit(fit_vit_abs, time, abs(tr_filt.data))

        print len(time), len(tr_filt.data), i, j
        #f = interpolate.interp1d(time, abs(tr_filt.data))
        f = interpolate.interp1d(time, tr_filt.data)
        #vel = np.zeros(len(time))
        #for j_t in range(len(time)):
        #    vel[j_t] = popt[0] * math.exp(- pow(time[j_t]-popt[1], 2)/popt[2])
        #f = interpolate.interp1d(time, vel)

        for k in range(nx):
            for l in range(ny):
                for m in range(5000):
                    if t[k, l, i, j] + m*dt > 430:
                        break
                    else:
                        stack[k, l, m] = stack[k, l, m] + f(t[k, l, i, j] + m*dt)

print stack[:, :, :].min(), stack[:, :, :].max()

stack_integre = np.zeros((nx, ny))
stack_integre_xt = np.zeros((nx, len(stack[0, 0, :])))
stack_integre_yt = np.zeros((ny, len(stack[0, 0, :])))
for k in range(nx):
    for l in range(ny):
	for m in range(len(stack[0, 0, :])):
	    stack_integre[k, l] = stack_integre[k, l] + stack[k, l, m]
	    stack_integre_xt[k, m] = stack_integre_xt[k, m] + stack[k, l, m]
	    stack_integre_yt[l, m] = stack_integre_yt[l, m] + stack[k, l, m]
print 'min integre ', stack_integre[:, :].min()
print 'max integre ', stack_integre[:, :].max()

stack_sin = np.zeros((nx, ny, 50))
#for i in [10]:
for i in range(nx_sta):
    #for j in [5]:
    for j in range(ny_sta):
	for k in range(nx):
	    for l in range(ny):
		for m in range(50):
		    stack_sin[k, l, m] = stack_sin[k, l, m] + 1./(nx_sta*ny_sta)*math.sin(math.pi/2 + 2*math.pi*m/50 + 2*math.pi*200/dx*(t[k, l, i, j] - t[(nx - 1)/2, (ny - 1)/2, i, j]))
		
print 'min sin ', stack_sin[:, :].min()
print 'max sin ', stack_sin[:, :].max()

ouverture_max = math.acos(math.cos(theta_S[10, 0])*math.cos(theta_S[10, 10]) + math.sin(theta_S[10, 0])*math.sin(theta_S[10, 10])*math.cos(phi_S[10, 0] - phi_S[10, 10]))

posx = np.arange(0, nx)
posx = posx*dx
print len(posx), len(stack_integre[:, 0])
#fig_stack_int, ax_stack_int = plt.subplots(2, 2)
#ax_stack_int[0, 0].set_title('Signal integre en valeur absolue')
#ax_stack_int[0, 0].set_xlabel('X (m)')
#ax_stack_int[0, 0].set_ylabel('Y (m)')
#cax_stack_int1 = ax_stack_int[0, 0].imshow(np.transpose(stack_integre[:, :]), cmap='jet', extent = (0, Lx, 0, Ly), interpolation = 'none', origin = 'lower')
##ax_stack_int[0, 0].axhline((Ly)/2, color = 'k', linewidth = 2)
#ax_stack_int[0, 0].axvline((Ly)/2 - 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axvline((Ly)/2 - 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axvline((Ly)/2 + 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axvline((Ly)/2 + 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axhline((Lx)/2 - 3./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axhline((Lx)/2 - 1./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axhline((Lx)/2 + 1./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 0].axhline((Lx)/2 + 3./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)

coordmax = np.argmax(stack[:, :, :])
xmax = coordmax//(5000*ny)
ymax = (coordmax - xmax*5000*ny)//5000
tmax = coordmax - xmax*5000*ny - ymax*5000

xmesh_dirac = np.arange(0, Lx + Lx/(nx-1), Lx/(nx-1))
ymesh_dirac = np.arange(0, Ly + Ly/(ny-1), Ly/(ny-1))
tmesh_dirac = np.arange(0, 5000)
tmesh_dirac = tmesh_dirac*dt
Xt_dirac, Yt_dirac = np.meshgrid(ymesh_dirac, xmesh_dirac)
Xy_dirac, Ty_dirac = np.meshgrid(xmesh_dirac, tmesh_dirac)
Tx_dirac, Yx_dirac = np.meshgrid(tmesh_dirac, ymesh_dirac)

xmesh_sin = np.arange(0, Lx + Lx/(nx-1), Lx/(nx-1))
ymesh_sin = np.arange(0, Ly + Ly/(ny-1), Ly/(ny-1))
zmesh_sin = np.arange(0, 50)
Xt_sin, Yt_sin = np.meshgrid(ymesh_sin, xmesh_sin)
Xy_sin, Zy_sin = np.meshgrid(xmesh_sin, zmesh_sin)
Zx_sin, Yx_sin = np.meshgrid(zmesh_sin, ymesh_sin)

print xmax, ymax, tmax
print stack[:, :, tmax].max()
print stack[:, ymax, :].max()
print stack[xmax, :, :].max()
print len(stack[:, ymax, tmax])
print len(stack[xmax, :, tmax])
print len(stack[xmax, ymax, :])

fig_dirac_3d = plt.figure()
ax_dirac_3d = fig_dirac_3d.add_subplot(111, projection = '3d')
ax_dirac_3d.contour(Xy_dirac, np.transpose(stack[:, ymax, :]), Ty_dirac, 10, zdir='y', offset=50000, cmap='jet')
ax_dirac_3d.contour(stack[xmax, :, :], Yx_dirac, Tx_dirac, 10, zdir='x', offset=0, cmap='jet')
ax_dirac_3d.contour(Xt_dirac, Yt_dirac, np.transpose(stack[:, :, tmax]), 10, zdir='z', offset=174, cmap='jet')
ax_dirac_3d.set_xlabel('X (km)')
ax_dirac_3d.set_ylabel('Y (km)')
ax_dirac_3d.set_zlabel('t (s)')
ax_dirac_3d.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_dirac_3d.yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
ax_dirac_3d.set_zlim3d(174, 182)
#ax_dirac_3d.set_zbound(170, 185)
fig_dirac_3d.savefig('50x50_dirac_proj_3d_perp.pdf')

fig_sin_3d = plt.figure()
ax_sin_3d = fig_sin_3d.add_subplot(111, projection = '3d')
ax_sin_3d.contour(Xy_sin, np.transpose(stack_sin[:, (ny-1)/2, :]), Zy_sin, 10, zdir='y', offset=50000, cmap='jet')
ax_sin_3d.contour(stack_sin[(nx-1)/2, :, :], Yx_sin, Zx_sin, 10, zdir='x', offset=0, cmap='jet')
ax_sin_3d.contour(Xt_sin, Yt_sin, np.transpose(stack_sin[:, :, 0]), 10, zdir='z', offset=0, cmap='jet')
ax_sin_3d.set_xlabel('X (km)')
ax_sin_3d.set_ylabel('Y (km)')
ax_sin_3d.set_zlabel('t (s)')
ax_sin_3d.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_sin_3d.yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
#ax_sin_3d.set_zbound(170, 185)
fig_sin_3d.savefig('50x50_sin_proj_3d_perp.pdf')

fig_3d, ax_3d = plt.subplots(2, 2, figsize=(25, 25))
ax_3d[1, 1].set_xlabel('Y (km)')
ax_3d[1, 1].set_ylabel('X (km)')
cax_3d_xy = ax_3d[1, 1].imshow(stack[:, :, tmax], cmap='jet', extent=(0, Ly, 0, Lx), interpolation='none', origin='lower')
ax_3d[1, 1].xaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
ax_3d[1, 1].yaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_3d[1, 1].invert_yaxis()
#ax_3d[1, 1].len_xaxis = 5.
#ax_3d[1, 1].len_yaxis = 5.

ax_3d[1, 0].set_xlabel('t (s)')
ax_3d[1, 0].set_ylabel('X (km)')
cax_3d_xt = ax_3d[1, 0].imshow(stack[:, ymax, :], cmap='jet', extent=(0, 5000*dt, 0, Lx), interpolation='none', origin='lower')
#ax_3d[1, 0].xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_3d[1, 0].yaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_3d[1, 0].set_xlim(174, 182)
ax_3d[1, 0].invert_xaxis()
ax_3d[1, 0].invert_yaxis()
ax_3d[1, 0].len_xaxis = 5. 
ax_3d[1, 0].len_yaxis = 5.
ax_3d[1, 0].set_aspect('auto')

ax_3d[0, 1].set_xlabel('Y (km)')
ax_3d[0, 1].set_ylabel('t (s)')
cax_3d_yt = ax_3d[0, 1].imshow(np.transpose(stack[xmax, :, :]), cmap='jet', extent=(0, Ly, 0, 5000*dt), interpolation='none', origin='lower')
ax_3d[0, 1].xaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
#ax_3d[0, 1].yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
ax_3d[0, 1].set_ylim(174, 182)
ax_3d[0, 1].len_xaxis = 5. 
ax_3d[0, 1].len_yaxis = 5.
ax_3d[0, 1].set_aspect('auto')
fig_3d.savefig('50x50_dirac_int_xyxtyt_perp.pdf')

fig_xy, ax_xy = plt.subplots(1, 1)
ax_xy.set_xlabel('Y (km)')
ax_xy.set_ylabel('X (km)')
cax_xy_xy = ax_xy.imshow(stack_integre[:, :], cmap='jet', extent=(0, Ly, 0, Lx), interpolation='none', origin='lower')
ax_xy.xaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
ax_xy.yaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_xy.invert_yaxis()
fig_xy.savefig('50x50_dirac_int_xy_perp.pdf')

fig_xt, ax_xt = plt.subplots(1, 1)
ax_xt.set_xlabel('t (s)')
ax_xt.set_ylabel('X (km)')
cax_xt_xt = ax_xt.imshow(stack_integre_xt[:, :], cmap='jet', extent=(0, 5000*dt, 0, Lx), interpolation='none', origin='lower')
ax_xt.yaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_xt.invert_xaxis()
ax_xt.invert_yaxis()
fig_xt.savefig('50x50_dirac_int_xt_perp.pdf')

fig_yt, ax_yt = plt.subplots(1, 1)
ax_yt.set_xlabel('Y (km)')
ax_yt.set_ylabel('t (s)')
cax_yt_yt = ax_yt.imshow(np.transpose(stack_integre_yt[:, :]), cmap='jet', extent=(0, Ly, 0, 5000*dt), interpolation='none', origin='lower')
ax_yt.xaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
fig_yt.savefig('50x50_dirac_int_yt_perp.pdf')

fig_dirac_int, ax_dirac_int = plt.subplots(1,1)
#ax_dirac_int.set_title('Absolute signal integrated')
ax_dirac_int.set_xlabel('X (km)')
ax_dirac_int.set_ylabel('Y (km)')
cax_dirac_int = ax_dirac_int.imshow(np.transpose(stack_integre[:, :]), cmap='jet', extent=(0, Lx, 0, Ly), interpolation='none', origin ='lower')
ax_dirac_int.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_dirac_int.yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
fig_dirac_int.savefig('50x50_dirac_int_perp.pdf')

#ax_dirac_int.axvline((Ly)/2 - 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axvline((Ly)/2 - 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axvline((Ly)/2 + 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axvline((Ly)/2 + 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axhline((Lx)/2 - 3./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axhline((Lx)/2 - 1./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axhline((Lx)/2 + 1./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_dirac_int.axhline((Lx)/2 + 3./2*(dx/(math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)

#ax_stack_int[0, 1].set_title('Signal sinusoidal en valeur abolue')
#ax_stack_int[0, 1].set_xlabel('X (m)')
#ax_stack_int[0, 1].set_ylabel('Y (m)')
#cax_stack_int2 = ax_stack_int[0, 1].imshow(np.transpose(stack_sin[:, :]), cmap='jet', extent = (0, Lx, 0, Ly), interpolation = 'none', origin = 'lower')
##ax_stack_int[0, 1].axhline((Ly)/2, color = 'k', linewidth = 2)
#ax_stack_int[0, 1].axvline((Ly)/2 - 3./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axvline((Ly)/2 - 1./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axvline((Ly)/2 + 1./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axvline((Ly)/2 + 3./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axhline((Lx)/2 - 3./2*(dx*alpha/(1000*math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axhline((Lx)/2 - 1./2*(dx*alpha/(1000*math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axhline((Lx)/2 + 1./2*(dx*alpha/(1000*math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[0, 1].axhline((Lx)/2 + 3./2*(dx*alpha/(1000*math.sin(0.5*ouverture_max))), color = 'k', linewidth = 1)

fig_sin_int, ax_sin_int = plt.subplots(1,1)
#ax_sin_int.set_title('Absolute sinusoidal signal')
ax_sin_int.set_xlabel('X (km)')
ax_sin_int.set_ylabel('Y (km)')
cax_sin_int = ax_sin_int.imshow(np.transpose(stack_sin[:, :, 0]), cmap='jet', extent = (0, Lx, 0, Ly), interpolation = 'none', origin = 'lower')
ax_sin_int.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
ax_sin_int.yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
fig_sin_int.savefig('50x50_sin_int_perp.pdf')

#popt_1, pcov_1 = curve_fit(func_1, posx, np.transpose(stack_integre[:, (ny-1)/2]), bounds=([0.0002, 0.1, 24900, 0.00004],[0.0003, 1, 25100, 0.00005]))
#, bounds=([0.00001, 1e-12, 1e5, 0], [0.1, 0.01, 1e20, 0.001]))
#popt_2, pcov_2 = curve_fit(func_2, posx, np.transpose(stack_sin[:, (ny-1)/2]), bounds=([0.00002, 0.0005, 0.4], [0.00003, 0.0007, 0.6]))

#print popt_1
#print popt_2

#ax_stack_int[1, 0].set_title('Coupe')
#ax_stack_int[1, 0].set_xlabel('X (m)')
#ax_stack_int[1, 0].set_ylabel('Intensite')
#ax_stack_int[1, 0].plot(posx, np.transpose(stack_integre[:, (ny-1)/2]))
##ax_stack_int[1, 0].plot(posx, popt_1[0]*np.exp(-popt_1[1]*pow(posx, 2) + popt_1[2]) + popt_1[3])
#ax_stack_int[1, 0].axvline((Ly)/2 - 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 0].axvline((Ly)/2 - 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 0].axvline((Ly)/2 + 1./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 0].axvline((Ly)/2 + 3./2*(dx/(math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)

fig_dirac_int_coupe, ax_dirac_int_coupe = plt.subplots(1,1) 
#ax_dirac_int.set_title('Cross-section')
ax_dirac_int_coupe.set_xlabel('X (km)')
ax_dirac_int_coupe.set_ylabel('Amplitude')
ax_dirac_int_coupe.plot(posx, np.transpose(stack_integre[:, (ny-1)/2]))
ax_dirac_int_coupe.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
#ax_dirac_int_coupe.xaxis.set_ticklabels([])
fig_dirac_int_coupe.savefig('50x50_dirac_int_coupe_perp.pdf')

#ax_stack_int[1, 1].set_title('Coupe')
#ax_stack_int[1, 1].set_xlabel('X (m)')
#ax_stack_int[1, 1].set_ylabel('Intensite')
#ax_stack_int[1, 1].plot(posx, np.transpose(stack_sin[:, (ny-1)/2]))
##ax_stack_int[1, 1].plot(posx, np.sin(popt_2[0]*posx)*np.sin(popt_2[1]*posx) + popt_2[2])
#ax_stack_int[1, 1].axvline((Ly)/2 - 3./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 1].axvline((Ly)/2 - 1./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 1].axvline((Ly)/2 + 1./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#ax_stack_int[1, 1].axvline((Ly)/2 + 3./2*(dx*alpha/(1000*math.cos(0.5*ouverture_max))), color = 'k', linewidth = 1)
#fig_stack_int.savefig('20x20_signaux_int_coupes_largeur_env.pdf')

fig_sin_int_coupe, ax_sin_int_coupe = plt.subplots(1,1)
#ax_sin_int_coupe.set_title('Coupe')
ax_sin_int_coupe.set_xlabel('X (km)')
ax_sin_int_coupe.set_ylabel('Amplitude')
ax_sin_int_coupe.plot(posx, np.transpose(stack_sin[:, (ny-1)/2, 0]))
ax_sin_int_coupe.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
#ax_dirac_int.xaxis.set_ticklabels(['x=0', 'x=10', 'x=20', 'x=30', 'x=40', 'x=50'])
fig_sin_int_coupe.savefig('50x50_sin_int_coupe_perp.pdf')

path = "/home/deleplanque/Documents/back_proj/en_cours/bp_plot"
os.makedirs(path)
os.chdir(path)
time = np.arange(0, 5000)
time = time*dt
for m in range(225):
    n = 2550 + m
    fig_backproj, ax_backproj = plt.subplots(1, 2)
    fig_backproj_map, ax_backproj_map = plt.subplots(1, 1)
    #fig_backproj_traces, ax_backproj_traces = plt.subplots(1, 1)
    ax_backproj[0].set_title(str(n*dt))
    ax_backproj[0].set_xlabel('X (m)')
    ax_backproj_map.set_xlabel('X (km)')
    #ax_backproj_traces.set_xlabel('time (s)')
    ax_backproj[0].set_ylabel('Y (m)')
    ax_backproj_map.set_ylabel('Y (km)')
    cax_backproj = ax_backproj[0].imshow(np.transpose(stack[:, :, n]), cmap='bwr', vmax=stack[:, :, :].max(), vmin=stack[:, :, :].min(), extent = (0, Lx, 0, Ly), interpolation='none', origin = "lower")
    cax_backproj_map = ax_backproj_map.imshow(np.transpose(stack[:, :, n]), cmap='bwr', vmax=stack[:, :, :].max(), vmin=stack[:, :, :].min(), extent = (0, Lx, 0, Ly), interpolation='none', origin = "lower")
    ax_backproj[0].axvline(Lx/2, color = 'k', linewidth = 2)
    ax_backproj_map.plot(Lx/2, Ly/2, color='k', linestyle = 'none')
    ax_backproj_map.xaxis.set_ticklabels([0*Lx, 0.0002*Lx, 0.0004*Lx, 0.0006*Lx, 0.0008*Lx, 0.001*Lx])
    ax_backproj_map.yaxis.set_ticklabels([0*Ly, 0.0002*Ly, 0.0004*Ly, 0.0006*Ly, 0.0008*Ly, 0.001*Ly])
    for l in range(ny):
        ax_backproj[1].plot(time, stack[(nx-1)/2, l, :] + (l-(ny-1)/2)*1.1*stack[:, :, :].max())
    ax_backproj[1].set_xlim(174, 182)
    ax_backproj[1].grid(True, which="both")
    fig_backproj_map.savefig('backproj_map' + str(n) + '.jpg')
    fig_backproj.savefig(str(n) + '.jpg')

fig_backproj_traces, ax_backproj_traces = plt.subplots(1, 1)
ax_backproj_traces.set_xlabel('time (s)')
for l in range(ny):
    ax_backproj_traces.plot(time, stack[(nx-1)/2, l, :] + (l - (ny-1)/2)*1.1*stack[:, :, :].max())
ax_backproj_traces.set_xlim(174, 182)
ax_backproj_traces.grid(True, which='both')
fig_backproj_traces.savefig('back_proj_traces_perp.jpg')
