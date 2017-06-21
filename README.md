# Back projection process

## telecharger les donnees (format ASCII)

- from _http://www.kyoshin.bosai.go.jp_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_brut/nom_du_dossier.kik_ and _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_brut/nom_du_dossier.knt_

## conversion au format 'SAC'

`python3 tosac.py 'nom_du_dossier'` 
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_brut/nom_du_dossier.k*_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_sac_

## selection des stations a moins de 100km de l'hypocentre

`python3 select_inf_100km.py 'nom_du_dossier'`
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_sac_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_sac_inf100km_

## faire les pointes des arrivees P et S dans _SAC_ (a la main)

## transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)

`python3 acc2vel.py 'nom_du_dossier'` 
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_sac_inf100km_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_

## obtenir les envelopes

`python3 trace_to_env.py 'nom_du_dossier'`
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_

## estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station

`python3 vitesse_PS.py 'nom_du_dossier'`
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_
- to _/Data/Kumamoto/nom_du_dossier_

## selection des stations pour la bp

`python3 selection_station.py 'nom_du_dossier'`
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_selectP_ et _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_selectS_

## bp des stations selectionnees

`python3 bp_env_E.py 'nom_du_dossier' 'hypothese_ondes' 'stations_selectionnees'`
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_select*_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier_vel_env_select* _bp_
   - hypothese_ondes: 'P' ou 'S'
   - stations_selectionnees: 'P', 'S' ou 'all'

# Arborescence

Codes
Data
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
	 - acc_env_selectS-bp












