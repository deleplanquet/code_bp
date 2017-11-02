import os
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

path_origin = os.getcwd()[:-6]
os.chdir(path_origin + '/Kumamoto')
with open('parametres_bin', 'rb') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    param = my_dpck.load()

with open('seismicity.txt', 'r') as my_fch:
    my_dpck = pickle.Unpickler(my_fch)
    

path = path_origin + '/Kumamoto'










