.. contents::

.. section-numbering::

telecharger les donnees (format ASCII)
--------------------------------------

- from *http://www.kyoshin.bosai.go.jp*
- to */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs.****

  with *** = *kik* or *knt*

conversion au format 'SAC'
--------------------------

.. code-block:: python3

    python3 tosac.py 'YyyyMmDdHhMmSs'

- from */Data/Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_brut/YyyyMmDdHhMmSs.****

  with *** = *kik* or *knt*

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

  with *** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

creation d une trace a partir des 3 composantes (toujours positive)
-------------------------------------------------------------------

.. code-block:: python3

    python3 3components.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz*

  with *** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp*

  with *** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

obtenir les envelopes
---------------------

.. code-block:: python3

    python3 vel2env.py 'YyyyMmDdHhMmSs'

- from */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp*

  with *** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

- to */Kumamoto/YyyyMmDdHhMmSs/YyyyMmDdHhMmSs_vel_***Hz_3comp_env*

  with *** = *02_05*, *05_1*, *1_2*, *2_4*, *4_8*, *8_16* or *16_30*

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

  with *** = *P* or *S*

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












