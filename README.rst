.. contents::

.. section-numbering::

telecharger les donnees (format ASCII)
--------------------------------------

- from *http://www.kyoshin.bosai.go.jp*
- to */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.kik*

	_/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.knt_

conversion au format 'SAC'
--------------------------

.. code-block:: python3

    python3 tosac.py 'YyyyMmDdHhMmSs'

- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_brut/YyyyMmDdHhMmSs.kik_

	_/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_brut/YyyyMmDdHhMmSs.knt_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_

selection des stations a moins de 100km de l'hypocentre
-------------------------------------------------------

.. code-block:: python3

    python3 select_inf_100km.py 'YyyyMmDdHhMmSs'

- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km_

faire les pointes des arrivees P et S dans _SAC_ (a la main)
------------------------------------------------------------

transformer les accelerations en vitesses et trimer entre 5sec avant le pointe P et 45sec apres (total 50sec)
-------------------------------------------------------------------------------------------------------------

.. code-block:: python3

    python3 acc2vel.py 'YyyyMmDdHhMmSs' 

- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_sac_inf100km_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_

filtrage selon differentes bandes de frequences
-----------------------------------------------

.. code-block:: python3

    python3 filt_vel.py 'YyyyMmDdHhMmSs'

- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_
- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz_

creation d une trace a partir des 3 composantes (toujours positive)
-------------------------------------------------------------------

.. code-block:: python3

    python3 3components.py 'YyyyMmDdHhMmSs'

- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz

- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz_3comp_

obtenir les envelopes
---------------------

.. code-block:: python3

    python3 vel2env.py 'YyyyMmDdHhMmSs'

- from _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz_3comp_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz_3comp_

- to _/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_02_05Hz_3comp_env_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_05_1Hz_3comp_env_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_1_2Hz_3comp_env_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_2_4Hz_3comp_env_

	_/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_4_10Hz_3comp_env_

estimation des vitesses P et S et creation d'un dictionnaire contenant le delai de starttime pour chaque station
----------------------------------------------------------------------------------------------------------------

.. code-block:: python3

    python3 vitesse_PS.py 'YyyyMmDdHhMmSs'

- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs_

selection des stations pour la bp
---------------------------------

.. code-block:: python3

    python3 selection_station.py 'YyyyMmDdHhMmSs'

- from _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_
- to _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_selectP_ et _/Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_env_selectS_

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












