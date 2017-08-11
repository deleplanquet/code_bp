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
- to _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS.kik_ and _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS.knt_

## conversion au format 'SAC'

`python3 tosac.py 'YYYYMMDDHHMMSS'` 
- from _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_brut/YYYYMMDDHHMMSS.k*_
- to _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_sac_

## selection des stations a moins de 100km de l'hypocentre

`python3 select_inf_100km.py 'YYYYMMDDHHMMSS'`
- from _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_sac_
- to _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_sac_inf100km_

## faire les pointes des arrivees P et S dans _SAC_ (a la main)

## transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)

`python3 acc2vel.py 'YYYYMMDDHHMMSS'` 
- from _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_3comp_
- to _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_

## filtrage selon differentes bandes de frequences

`python3  'YYYYMMDDHHMMSS'`
- from
- to

## creation d une trace a partir des 3 composantes (toujours positive)

`python3 3components.py 'YYYYMMDDHHMMSS'`
- from _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_sac_inf100km_
- to _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_3comp_

## obtenir les envelopes

`python3 vel2env.py 'YYYYMMDDHHMMSS'`
- from _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_
- to _/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_02_05Hz_

	_/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_05_1Hz_

	_/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_1_2Hz_

	_/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_2_4Hz_

	_/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_4_10Hz_

## estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station

`python3 vitesse_PS.py 'YYYYMMDDHHMMSS'`
- from _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_
- to _/Data/Kumamoto/YYYYMMDDHHMMSS_

## selection des stations pour la bp

`python3 selection_station.py 'YYYYMMDDHHMMSS'`
- from _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_
- to _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_selectP_ et _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_selectS_

## bp des stations selectionnees

`python3 bp_env_E.py 'YYYYMMDDHHMMSS' 'hypothese_ondes' 'stations_selectionnees'`
- from _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_select*_
- to _/Data/Kumamoto/YYYYMMDDHHMMSS/YYYYMMDDHHMMSS_vel_env_select* _bp_
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












