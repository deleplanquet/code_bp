.. contents::

.. section-numbering::

definir les parametres
----------------------

.. code-block:: python3

    python3 parametres.py
-------------------------

list of parameters:
- path_origin: va chercher la position absolue du dossier */Codes* (qui est au meme niveau que le dossier */Kumamoto* contenant les data)
  n'est pas demande a l'utilisateur
- dossier: demande le nom du dossier (seisme) qui doit etre traite au format est *YYYYMMDDHHMMSS*
- R_Earth: fixe a 6400
  n'est pas demande a l'utilisateur
- dist_min: hypocenter distance minimale pour que la station soit traite (en km)
- dist_max: hypocenter distance maximale pour que la station soit traite (en km)
- couronne: associe *dist_min* et *dist_max* pour creer un string et faciliter la creation des fichiers et dossiers
  n'est pas demande a l'utilisateur
- freq_min: frequence basse pour le filtre passe bande utilise sur les velocity waveforms
- freq_max: frequence haute pour le filtre passe bande utilise sur les velocity waveforms
- band_freq: associe *freq_min* et *freq_max* pour creer un string et faciliter la creation des fichiers et dossiers
  n'est pas demande a l'utilisateur
- composante: demande un string parmi [3comp/hori/vert] pour definir celles qu'ils faut traiter
- ratioSP: critere de selection des stations sur le rapport de maximum d'amplitude de l'energie S sur P
- smooth: longueur (en s) de la fenetre glissante sur laquelle on fait la RMS
- impulse: longueur (en s) de la fenetre dans laquelle au mois 80% de l'energie doit etre pour que la station soit traitee dans la back projection (l'energie est celle de l'onde defini [P/S])
- angle_min: angle minimal pour la selection azimuthale des stations
- angle_max: angle maximal pour la selection azimuthale des stations
  pour les angles, deux zones sont definies, la premiere entre *angle_min* et *angle_max*, la seconde entre *angle_min* + 180 et *angle_max* + 180. C'est pour cela que les angles sont compris entre 0 et 180
- angle: associe *angle_min* et *angle_max* pour creer un string et faciliter la creation des fichiers et dossiers
  n'est pas demande a l'utilisateur
- vP: vitesse des ondes P utilisee pour calculer les temps de trajet des ondes P entre chaque subfault et chaque station
- vS: vitesse des ondes S utilisee pour calculer les temps de trajet des ondes S entre chaque subfault et chaque station
- ondes_select: demande un string parmi [P/S] pour savoir si l'hypothese de back projection est les ondes P ou les ondes S
- strike: direction du strike de la faille rectangulaire
- dip: direction du dip de la faille rectangulaire
- l_fault: longueur de la faille (en km) (direction du strike)
- w_fault: largeur de la faille (en km) (direction du dip)
- pas_l: longueur de chaque subfault dans la direction du strike (en km)
- pas_w: longueur de chaque subfault dans la direction du dip (en km)
- samp_rate: frequeuce de production des figures de back projection (Hz)
- length_t: duree de la back projection (en s) en sachant que le depart est toujours 5 sec avant le debut de la rupture

telecharger les donnees (format ASCII)
--------------------------------------

- from *http://www.kyoshin.bosai.go.jp*
- to */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.****

  with *\**** = *kik* or *knt*

conversion au format 'SAC'
--------------------------

.. code-block:: python3

    python3 tosac.py 'YyyyMmDdHhMmSs'

- from */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_brut/YyyyMmDdHhMmSs.****

  with *\**** = *kik* or *knt*

- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac*

selection des stations a moins de 100km de l'hypocentre
-------------------------------------------------------

.. code-block:: python3

    python3 select_inf_100km.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac*
- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km*

faire les pointes des arrivees P et S dans _SAC_ (a la main)
------------------------------------------------------------

transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)
-------------------------------------------------------------------------------------------------------------

.. code-block:: python3

    python3 acc2vel.py 'YyyyMmDdHhMmSs' 

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km*
- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel*

filtrage selon differentes bandes de frequences
-----------------------------------------------

.. code-block:: python3

    python3 filt_vel.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel*
- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz*

  with *\**** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

creation d une trace a partir des 3 composantes (toujours positive)
-------------------------------------------------------------------

.. code-block:: python3

    python3 3components.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz*

  with *\**** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp*

  with *\**** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

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












