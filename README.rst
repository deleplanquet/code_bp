.. contents::

.. section-numbering::

python3 parametres.py
---------------------

.. code-block:: python3

    python3 parametres.py

Definir les parametres ci-dessous:

| **path_origin**: va chercher la position absolue du dossier */Codes* (qui est au meme niveau que le dossier */Kumamoto* contenant les data)::

    n'est pas demande a l'utilisateur
| **dossier**: demande le nom du dossier (seisme) qui doit etre traite au format *YYYYMMDDHHMMSS*
| **R_Earth**: fixe a 6400::

    n'est pas demande a l'utilisateur
| **dist_min**: hypocenter distance minimale pour que la station soit traite (en km)
| **dist_max**: hypocenter distance maximale pour que la station soit traite (en km)
| **couronne**: associe **dist_min** et **dist_max** pour creer un string et faciliter la creation des fichiers et dossiers::

    n'est pas demande a l'utilisateur
| **freq_min**: frequence basse pour le filtre passe bande utilise sur les velocity waveforms
| **freq_max**: frequence haute pour le filtre passe bande utilise sur les velocity waveforms
| **band_freq**: associe **freq_min** et **freq_max** pour creer un string et faciliter la creation des fichiers et dossiers::

    n'est pas demande a l'utilisateur
| **composante**: demande un string parmi [3comp/hori/vert] pour definir celles qu'ils faut traiter
| **ratioSP**: critere de selection des stations sur le rapport de maximum d'amplitude de l'energie S sur P
| **smooth**: longueur (en s) de la fenetre glissante sur laquelle on fait la RMS
| **impulse**: longueur (en s) de la fenetre dans laquelle au mois 80% de l'energie doit etre pour que la station soit traitee dans la back projection (l'energie est celle de l'onde defini [P/S])
| **angle_min**: angle minimal pour la selection azimuthale des stations
| **angle_max**: angle maximal pour la selection azimuthale des stations::

    pour les angles, deux zones sont definies, la premiere entre **angle_min** et **angle_max**, la seconde entre **angle_min** + 180 et **angle_max** + 180. C'est pour cela que les angles sont compris entre 0 et 180
| **angle**: associe **angle_min** et **angle_max** pour creer un string et faciliter la creation des fichiers et dossiers::

   n'est pas demande a l'utilisateur
| **vP**: vitesse des ondes P utilisee pour calculer les temps de trajet des ondes P entre chaque subfault et chaque station
| **vS**: vitesse des ondes S utilisee pour calculer les temps de trajet des ondes S entre chaque subfault et chaque station
| **ondes_select**: demande un string parmi [P/S] pour savoir si l'hypothese de back projection est les ondes P ou les ondes S
| **strike**: direction du strike de la faille rectangulaire
| **dip**: direction du dip de la faille rectangulaire
| **l_fault**: longueur de la faille (en km) (direction du strike)
| **w_fault**: largeur de la faille (en km) (direction du dip)
| **pas_l**: longueur de chaque subfault dans la direction du strike (en km)
| **pas_w**: longueur de chaque subfault dans la direction du dip (en km)
| **samp_rate**: frequeuce de production des figures de back projection (Hz)
| **length_t**: duree de la back projection (en s) en sachant que le depart est toujours 5 sec avant le debut de la rupture

telecharger les donnees (format ASCII)
--------------------------------------

| from *http://www.kyoshin.bosai.go.jp*
| to */Kumamoto/dossier/dossier_brut*

python3 tosac.py
----------------

.. code-block:: python3

    python3 tosac.py

convertir les traces telechargees au fromat SAC

| from */Kumamoto/dossier/dossier_brut/dossier.****

  with *\**** = *kik* or *knt*

| to */Kumamoto/dossier/dossier_sac*

python3 select_couronne.py
--------------------------

.. code-block:: python3

    python3 select_couronne.py

| selectionne les stations dans une couronne centree autour de l'hypocentre
| les distances considerees sont les distances hypocentrales

| from */Kumamoto/dossier/dossier_sac*
| to */Kumamoto/dossier/dossier_sac_couronne*

faire les pointes des arrivees P et S dans _SAC_ (a la main)
------------------------------------------------------------

| les pointes sont realises dans SAC sur les traces brutes
| les fichiers localises dans */Kumamoto/dossier/dossier_sac_couronne* sont modifies
| Faire attention si on reprend la procedure du debut

python3 acc2vel.py
------------------

.. code-block:: python3

    python3 acc2vel.py

les differentes etapes sont decrites ci-dessous:

| detrend
| taper hann 0.05
| highpass 20 s
| trim 5 s avant pointe P - 45 s apres pointe P (fenetre de 50 s)
| taper hann 0.05
| fft
| division by 2iPif
| ifft

| from */Kumamoto/dossier/dossier_sac_couronne*
| to */Kumamoto/dossier/dossier_vel_couronne*

python3 filt_vel.py
------------------

.. code-block:: python3

    python3 filt_vel.py

les differentes etapes sont decrites ci-dessous:

| detrend
| taper hann 0.05
| bandpass dans la bande de frequences definie lors de l'execution de parametres.py, corners = 4, zerophase = false

| from */Kumamoto/dossier/dossier_vel_couronne*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq*

python3 3components.py
----------------------

.. code-block:: python3

    python3 3components.py

| creation d'une trace a partir des 3 composantes
| cette trace est toujours positive
| A(ti) = sqrt(sum(a(ti)*a(ti)))

- from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq*
- to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_****

  with *\**** = *3comp*, *hori* or *vert*

obtenir les envelopes
---------------------

.. code-block:: python3

    python3 vel2env.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp*

  with *\**** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp_env*

  with *\**** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station
----------------------------------------------------------------------------------------------------------------

.. code-block:: python3

    python3 vitesse_PS.py 'YyyyMmDdHhMmSs'

- from */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env*
- to */Data/Kumamoto/YyyyMmDdHhMmSs*

selection des stations pour la bp
---------------------------------

.. code-block:: python3

    python3 selection_station.py 'YyyyMmDdHhMmSs'

- from */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env*
- to */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_select****

  with *\**** = *P* or *S*

bp des stations selectionnees
-----------------------------

.. code-block:: python3

    python3 bp_env_E.py 'YyyyMmDdHhMmSs' 'hypothese_ondes' 'stations_selectionnees'

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












