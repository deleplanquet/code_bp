import numpy as np
import math
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

i_inc_sta = 20 #angle incidence station
i_inc_fault = 45 #angle incidence faille
d_btw_sta = 3e4 #distance entre station
d_fault_surf = 1e6 #distance centre faille surface
r_S_0 = d_fault_surf/math.cos(i_inc_sta*math.pi/180) #distance centre faille centre reseau de stations
Lx = 50000 #longueur supposee faille direction x
Ly = 50000 #longueur supposee faille direction y
dt = 200./3000 #pas en temps

alpha = 6000 #vitesse ondes P
nx = 21 #nbre points faille direction x
ny = 21 #nbre points faille direction y
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

fig_test2, ax_test2 = plt.subplots(2, 3)
ax_test2[0, 0].set_title("k=0 l=0")
ax_test2[0, 0].set_xlabel('i')
ax_test2[0, 0].set_ylabel('j')
cax_test21 = ax_test2[0, 0].imshow(np.transpose(t[0, 0, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[0, 0].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
ax_test2[0, 1].set_title("k=0 l=" + str(ny - 1))
ax_test2[0, 1].set_xlabel('i')
ax_test2[0, 1].set_ylabel('j')
cax_test22 = ax_test2[0, 1].imshow(np.transpose(t[0, ny - 1, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[0, 1].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
ax_test2[0, 2].set_title("k=" + str(nx - 1) + " l=" + str((ny - 1)/2))
ax_test2[0, 2].set_xlabel('i')
ax_test2[0, 2].set_ylabel('j')
cax_test21 = ax_test2[0, 2].imshow(np.transpose(t[nx - 1, (ny - 1)/2, :, :]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[0, 2].axhline((ny_sta - 1)/2, color = 'k', linewidth = 2)
ax_test2[1, 0].set_title("i=0 j=0")
ax_test2[1, 0].set_xlabel('k')
ax_test2[1, 0].set_ylabel('l')
cax_test22 = ax_test2[1, 0].imshow(np.transpose(t[:, :, 0, 0]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[1, 0].axhline((ny - 1)/2, color = 'k', linewidth = 2)
ax_test2[1, 1].set_title("i=0 j=" + str(ny_sta - 1))
ax_test2[1, 1].set_xlabel('k')
ax_test2[1, 1].set_ylabel('l')
cax_test21 = ax_test2[1, 1].imshow(np.transpose(t[:, :, 0, ny_sta - 1]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[1, 1].axhline((ny - 1)/2, color = 'k', linewidth = 2)
ax_test2[1, 2].set_title("i=" + str(nx_sta - 1) + " j=" + str((ny_sta - 1)/2))
ax_test2[1, 2].set_xlabel('k')
ax_test2[1, 2].set_ylabel('l')
cax_test22 = ax_test2[1, 2].imshow(np.transpose(t[:, :, nx_sta - 1, (ny_sta - 1)/2]), cmap='jet', vmin = t[:, :, :, :].min(), vmax = t[:, :, :, :].max(), interpolation = 'none', origin = 'lower')
ax_test2[1, 2].axhline((ny - 1)/2, color = 'k', linewidth = 2)
fig_test2.savefig('test2.pdf')

for i in range(nx_sta):
#for i in [10]:
    for j in range(ny_sta):
    #for j in [0, 10]:
        name = "/home/deleplanque/Documents/back_proj/en_cours/slippy_product/RC_250/x0_0/y0_0/v_R_3000/vel_vect/RC_250-x0_0-y0_0-vR_3000-x_%.0f-y_%.0f_tR0" % (i, j)
        tr = obspy.Trace(np.loadtxt(name))
        tr.stats.delta = dt
        tr_filt = tr.copy()
        tr_filt.filter('lowpass', freq=4.0, corners=2, zerophase=True)
        tr_filt.filter('highpass', freq=2.0, corners=2, zerophase=True)

        time = np.arange(0, len(tr_filt))
        time = time*dt

        #popt, pcov = curve_fit(fit_vit_abs, time, abs(tr_filt.data))

        print len(time), len(tr_filt.data)
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
for k in range(nx):
    for l in range(ny):
	for m in range(len(stack[0, 0, :])):
	    stack_integre[k, l] = stack_integre[k, l] + abs(stack[k, l, m])
print 'min integre ', stack_integre[:, :].min()
print 'max integre ', stack_integre[:, :].max()

stack_sin = np.zeros((nx, ny))
#for i in [10]:
for i in range(nx_sta):
    #for j in [5]:
    for j in range(ny_sta):
	for k in range(nx):
	    for l in range(ny):
		stack_sin[k, l] = stack_sin[k, l] + 1./(nx_sta*ny_sta)*abs(math.sin(math.pi/2 + 2*math.pi*1000/dx*(t[k, l, i, j] - t[(nx - 1)/2, (ny - 1)/2, i, j])))
print 'min sin ', stack_sin[:, :].min()
print 'max sin ', stack_sin[:, :].max()

posx = np.arange(0, nx)
posx = posx*dx
print len(posx), len(stack_integre[:, 0])
fig_stack_int, ax_stack_int = plt.subplots(2, 2)
ax_stack_int[0, 0].set_title('Signal integre en valeur absolue')
ax_stack_int[0, 0].set_xlabel('X (m)')
ax_stack_int[0, 0].set_ylabel('Y (m)')
cax_stack_int1 = ax_stack_int[0, 0].imshow(np.transpose(stack_integre[:, :]), cmap='jet', extent = (0, Lx, 0, Ly), interpolation = 'none', origin = 'lower')
ax_stack_int[0, 0].axhline((ny - 1)/2, color = 'k', linewidth = 2)
ax_stack_int[0, 1].set_title('Signal sinusoidal en valeur abolue')
ax_stack_int[0, 1].set_xlabel('X (m)')
ax_stack_int[0, 1].set_ylabel('Y (m)')
cax_stack_int2 = ax_stack_int[0, 1].imshow(np.transpose(stack_sin[:, :]), cmap='jet', extent = (0, Lx, 0, Ly), interpolation = 'none', origin = 'lower')
ax_stack_int[0, 1].axhline((ny - 1)/2, color = 'k', linewidth = 2)

popt_1, pcov_1 = curve_fit(func_1, posx, np.transpose(stack_integre[:, (ny-1)/2]), bounds=([0.0002, 0.1, 24900, 0.00004],[0.0003, 1, 25100, 0.00005]))
#, bounds=([0.00001, 1e-12, 1e5, 0], [0.1, 0.01, 1e20, 0.001]))
popt_2, pcov_2 = curve_fit(func_2, posx, np.transpose(stack_sin[:, (ny-1)/2]), bounds=([0.00002, 0.0005, 0.4], [0.00003, 0.0007, 0.6]))

ax_stack_int[1, 0].set_title('Coupe')
ax_stack_int[1, 0].set_xlabel('X (m)')
ax_stack_int[1, 0].set_ylabel('Intensite')
ax_stack_int[1, 0].plot(posx, np.transpose(stack_integre[:, (ny-1)/2]))
ax_stack_int[1, 0].plot(posx, popt_1[0]*np.exp(-popt_1[1]*pow(posx, 2) + popt_1[2]) + popt_1[3])
ax_stack_int[1, 1].set_title('Coupe')
ax_stack_int[1, 1].set_xlabel('X (m)')
ax_stack_int[1, 1].set_ylabel('Intensite')
ax_stack_int[1, 1].plot(posx, np.transpose(stack_sin[:, (ny-1)/2]))
ax_stack_int[1, 1].plot(posx, np.sin(popt_2[0]*posx)*np.sin(popt_2[1]*posx) + popt_2[2])
fig_stack_int.savefig('20x20_signaux_int_coupes_fit.pdf')

path = "/home/deleplanque/Documents/back_proj/en_cours/bp_plot"
os.makedirs(path)
os.chdir(path)
time = np.arange(0, 5000)
time = time*dt
for m in range(225):
    n = 2550 + m
    fig_backproj, ax_backproj = plt.subplots(1, 2)
    ax_backproj[0].set_title(str(n*dt))
    ax_backproj[0].set_xlabel('X (m)')
    ax_backproj[0].set_ylabel('Y (m)')
    cax_backproj = ax_backproj[0].imshow(np.transpose(stack[:, :, n]), cmap='bwr', vmax=stack[:, :, :].max(), vmin=stack[:, :, :].min(), extent = (0, Lx, 0, Ly), interpolation='none', origin = "lower")
    ax_backproj[0].axvline(Lx/2, color = 'k', linewidth = 2)
    for l in range(ny):
        ax_backproj[1].plot(time, stack[(nx-1)/2, l, :] + (l-(ny-1)/2)*1.1*stack[:, :, :].max())
    ax_backproj[1].set_xlim(170, 185)
    ax_backproj[1].grid(True, which="both")
    fig_backproj.savefig(str(n) + '.jpg')
