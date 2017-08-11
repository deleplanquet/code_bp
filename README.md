# Plan

1. telecharger les donnees (format ASCII)
2. conversion au format 'SAC'
3. selection des stations a moins de 100km de l'hypocentre
4. faire les pointes des arrivees P et S dans _SAC_ (a la main)
5. transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)
6. filtrage selon differentes bandes de frequences
7. creation d une trace a partir des 3 composantes (toujours positive)
8. obtenir les envelopes
9. estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station
10. selection des stations pour la bp
11. bp des stations selectionnees

# Back projection process

## telecharger les donnees (format ASCII)

- from _http://www.kyoshin.bosai.go.jp_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.kik_

	_/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.knt_

## conversion au format 'SAC'

`python3 tosac.py 'YyyyMmDdHhMmSs'` 
- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_brut/YyyyMmDdHhMmSs.k*_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_

## selection des stations a moins de 100km de l'hypocentre

`python3 select_inf_100km.py 'YyyyMmDdHhMmSs'`
- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km_

## faire les pointes des arrivees P et S dans _SAC_ (a la main)

## transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)

`python3 acc2vel.py 'YyyyMmDdHhMmSs'` 
- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_3comp_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_

## filtrage selon differentes bandes de frequences

`python3 filt_vel.py 'YyyyMmDdHhMmSs'`
- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz_

## creation d une trace a partir des 3 composantes (toujours positive)

`python3 3components.py 'YyyyMmDdHhMmSs'`
- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_3comp_

## obtenir les envelopes

`python3 vel2env.py 'YyyyMmDdHhMmSs'`
- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_02_05Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_05_1Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_1_2Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_2_4Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_4_10Hz_

## estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station

`python3 vitesse_PS.py 'YyyyMmDdHhMmSs'`
- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs_

## selection des stations pour la bp

`python3 selection_station.py 'YyyyMmDdHhMmSs'`
- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_selectP_ et _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_selectS_

## bp des stations selectionnees

`python3 bp_env_E.py 'YyyyMmDdHhMmSs' 'hypothese_ondes' 'stations_selectionnees'`
- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_select*_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_select* _bp_
   - hypothese_ondes: 'P' ou 'S'
   - stations_selectionnees: 'P', 'S' ou 'all'

# Arborescence

Dossier_parent

- Codes
- Data
  - Kumamoto
    - dossiers
      - brut
      - sac
      - sac_inf100km
      - vel
      - vel_env
      - vel_env_selectP
      - vel_env_selectS
      - vel_env_selectP_bp
      - vel_env_selectS_bp
      - acc_env
      - acc_env_selectP
      - acc_env_selectS
      - acc_env_selectP_bp
      - acc_env_selectS_bp












