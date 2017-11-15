#!/bin/bash

python3 acc2vel.py
python3 filt_vel.py
python3 3components.py
python3 vel2env.py
python3 env2smooth.py
python3 vitesse_PS.py
python3 select_stat_env.py
python3 select_station_angle.py
