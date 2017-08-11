import pickle
import matplotlib.pyplot as plt
import sys
import os

dossier = sys.argv[1]
frq = sys.argv[2]
sttn = sys.argv[3]

path = os.getcwd()[:-6] + '/Kumamoto/' + dossier

os.chdir(path)

with open(dossier + '_mat_vel_ampli_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    my_dct = my_dpck.load()

print(my_dct[frq][sttn])

fig, ax = plt.subplots(1, 1)
ax.plot(my_dct[frq][sttn])
plt.show()
