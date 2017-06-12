# Back projection process

1. telecharger les donnees (format ASCII)
- from _http://www.kyoshin.bosai.go.jp_
- to _/Data/Kumamoto/nom_du_dossier/nom_du_dossier.kik_ and _/Data/Kumamoto/nom_du_dossier/nom_du_dossier.knt_
2. conversion au format 'SAC'

`python3 tosac.py 'nom_du_dossier'` 
- from _/Data/Kumamoto/nom_du_dossier/nom_du_dossier.k*_
- to _/Data/Kumamoto_sac/nom_du_dossier_
3. selection des stations a mpoins de 100km de l'hypocentre

`python3 select_inf_100km.py 'nom_du_dossier'`
- from _/Data/Kumamoto_sac/nom_du_dossier_
- to _/Data/Kumamoto_sac_inf100km/nom_du_dossier_
4. faire les pointes des arrivees P et S dans _SAC_ (a la main)
5. transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)

`python3 acc2vel.py 'nom_du_dossier'` 
- from _/Data/Kumamoto_sac_inf100km/nom_du_dossier_
- to _/Data/Kumamoto_vel/nom_du_dossier_
6. obtenir les envelopes

`python3 trace_to_env.py 'nom_du_dossier'`
- from _/Data/Kumamoto_vel/nom_du_dossier_
- to _/Data/Kumamoto_env/nom_du_dossier_
7. estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station

`python3 vitesse_PS.py 'nom_du_dossier'`
- from _/Data/Kumamoto_env/nom_du_dossier_
- to _/Results/Kumamoto/nom_du_dossier/Velocity_
8. selection des stations pour la bp

`python3 selection_station.py 'nom_du_dossier'`
- from _/Data/Kumamoto_env/nom_du_dossier_
- to _/Data/Kumamoto_env_selectP/nom_du_dossier_ et _/Data/Kumamoto_env_selectS/nom_du_dossier_
9. bp des stations selectionnees

`python3 bp_env_E.py 'nom_du_dossier' 'hypothese_ondes' 'stations_selectionnees'`
- from _/Data/Kumamoto_env_select*/nom_du_dossier_
- to _/Results/Kumamoto/nom_du_dossier_
   - hypothese_ondes: 'P' ou 'S'
   - stations_selectionnees: 'P', 'S' ou 'all'

## Arborescence

Dossier_parent
- Codes
- Data
   - Kumamoto
      - dossiers
   - Kumamoto_sac
      - dossiers
   - Kumamoto_sac_inf100km
      - dossiers
   - Kumamoto_vel
      - dossiers
   - Kumamoto_env
      - dossiers
   - Kumamoto_env_selectP
      - dossiers
   - Kumamoto_env_selectS
      - dossiers
- Results
   - Kumamoto
      - dossiers
