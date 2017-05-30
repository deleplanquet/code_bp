# codes

Pour back projection:
- telecharger les donnees (format ASCII)
- conversion en format 'SAC':
   - soit un seisme unique avec: **python3 tosac.py "nom_du_dossier"**
   - soit l'ensemble des seismes avec: **./boucle_rosac.sh** (si le dossier d'arrivee existe deja, le seisme correspondant n'est pas traite)
- faire les pointer des arrivees P et S dans 'SAC' (a la main)
- obtenir les envelopes avec: **python3 trace_to_env.py "nom_du_dossier"** (un trim est aussi applique de 5sec avec le pointe P a 45sec apres, duree totale 50sec)
- estimation des vitesses P et S avec: **python3 vitesse_PS.py** (cree un dictionnaire avec le delai correspondant a chaque station)
- selection des stations pour la bp avec: **python3 select_station.py "nom_du_dossier"** (il faut changer dans le dossier si on veut selectionner les P ou les S)
- bp des stations selectionnees avec: **python3 bp_env_E.py "nom_du_dossier"** (il faut changer dans le dossier si on veut utiliser P ou S)
