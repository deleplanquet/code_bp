.. contents::

.. section-numbering::

Parameters
==========

By running the following code, all the necessary parameters will be asked to
the user.

.. code-block:: python3

    python3 parametres.py

Here is a list of all the parameters that has to be defined.

| **event**: name of the event (earthquake).
| **hypo_min**: minimum of hypocenter distance (in km).
| **hypo_max**: maximum of hypocenter distance (in km).
| **frq_min**: low frequency (in Hz) for the pass-band filter used on the
    velocity waveforms.
| **frq_max**: high frequency (in Hz) for the pass-band filter used on the
    velocity waveforms
| **component**: component [*3cpn*, *hori*, *vert*] used in the study.
| **ratioSP**: selection criteria for the stations depending on the ratio
    between the maximum amplitude of energy of S and P-waves.
| **l_smooth**: length (in s) of the time-window for the smoothing (RMS) of the
    energy waveforms.
| **l_impulse**: length (in s) of the time-window for the selection of
    impulsive stations.
| **angle_min**: minimum of azimuth angle (in deg).
| **angle_max**: maximum of azimuth angle (in deg).
| **vP**: P-waves velocity.
| **vS**: S-waves velocity.
| **selected_waves**: choice of the waves [*P*, *S*] used for the study.
| **strike**: strike direction of the rectangular grid.
| **dip**: dip direction of the rectangular grid.
| **l_grid**: length of the grid (in km) (strike direction).
| **w_grid**: width of the grid (in km) (dip direction).
| **l_grid_step**: length of each subgrid (in km) (strike direction).
| **w_grid_step**: width of each subgrid (in km) (dip direction).
| **bp_samp_rate**: frequency of the back projection images (in Hz).
| **bp_length_time**: duration of the back projection (in s).

Here is the list of all the other parameters that are stored through the run
of parametres.py but not asked to the user:

| **root_folder**: pick the absolute position of the */Codes* directory,
    should be at the same location with the */Kumamoto* directory.
| **R_Earth**: Earth radius equal to 6400 km
| **hypo_interv**: combine **hypo_min** and **hypo_max** inside a string.
| **frq_band**: combine **frq_min** and **frq_max** inside a string.
| **angle**: combine **angle_min** and **angle_max** inside a string.

telecharger les donnees (format ASCII)
======================================

| from *http://www.kyoshin.bosai.go.jp*
| to */Kumamoto/dossier/dossier_brut*

python3 tosac.py
================

.. code-block:: python3

    python3 tosac.py

convertir les traces telechargees au fromat SAC

| from */Kumamoto/dossier/dossier_brut/dossier.****

  with *\**** = *kik* or *knt*

| to */Kumamoto/dossier/dossier_sac*

python3 station_inf_100km.py
============================

.. code-block:: python3

    python3 station_inf_100km.py

| selectionne les stations a moins de 100 km de l'hypocentre
| les distances considerees sont les distances hypocentrales

| from */Kumamoto/dossier/dossier_sac*
| to */Kumamoto/dossier/dossier_sac_inf100km*

faire les pointes des arrivees P et S dans _SAC_ (a la main)
============================================================

| les pointes sont realises dans SAC sur les traces brutes
| les fichiers localises dans */Kumamoto/dossier/dossier_sac_inf100km* sont modifies
| Faire attention si on reprend la procedure du debut

python3 seismicity.py
=====================

.. code-block:: python3

    python3 seismicity.py

| plot la sismicite dans la region du main shock
| affiche le main shock et les deux foreshocks
| le tout sur differentes periodes (avant, apres, entre deux evenements...)

| from */Kumamoto*
| to */Kumamoto*

python3 select_couronne.py
==========================

.. code-block:: python3

    python3 select_couronne.py

| selectionne les stations dans une couronne centree autour de l'hypocentre
| les distances considerees sont les distances hypocentrales

| from */Kumamoto/dossier/dossier_sac_inf100km*
| to */Kumamoto/dossier/dossier_sac_couronne*

python3 acc2vel.py
==================

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
===================

.. code-block:: python3

    python3 filt_vel.py

les differentes etapes sont decrites ci-dessous:

| detrend
| taper hann 0.05
| bandpass dans la bande de frequences definie lors de l'execution de parametres.py, corners = 4, zerophase = false

| from */Kumamoto/dossier/dossier_vel_couronne*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq*

python3 3components.py
======================

.. code-block:: python3

    python3 3components.py

| creation d'une trace a partir des 3 composantes
| cette trace est toujours positive
| A(ti) = sqrt(sum(a(ti)*a(ti)))

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_****

  with *\**** = *3comp*, *hori* or *vert*

python3 vel2env.py
==================

.. code-block:: python3

    python3 vel2env.py

| Produit des traces en energie a partir des velocity waveforms
| E(ti) = A(ti)*A(ti)

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env*

python3 env2smooth.py
=====================

.. code-block:: python3

    python3 env2smooth.py

| fait la RMS des envelopes sur une fenetre de duree **smooth** secondes

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth*

python3 carte_SoverP.py
-----------------------

.. code-block:: python3

    python3 carte_SoverP.py

| fait une carte affichant les stations retenues jusque la avec l'information energie S/P

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth*
| to */Kumamoto/dossier/dossier_results*

python3 vitesse_PS.py
=====================

.. code-block:: python3

    python3 vitesse_PS.py

| calcul les delais entre temps theoriques d'arrivee et les pointes pour les ondes P et S
| les corrections aux stations (delais calcules) sont stockes dans un dictionnaire

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth*
| to */Kumamoto/dossier*

python3 select_stat_env.py
==========================

.. code-block:: python3

    python3 select_stat_env.py

| compare le pic d'energie de l'onde P avec le pic d'energie de l'onde S
| si le rapport S/P est superieur au threshold **ratioSP**, l'onde est selectionnee pour la back projection hypothese S
| si le rapport S/P est inferieur au threshold 1/**ratioSP**, l'onde est selectionee pour la back projection hypothese P

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth_****

  with *\**** = *P* or *S*

python3 select_station_angle.py
===============================

.. code-block:: python3

    python3 select_station_angle.py

| calcul l'azimuth de chaque station par rapport a l'hypocentre
| si l'azimuth de la station est compris entre **angle_min** et **angle_max**, la station est selectionnee pour la back projection
| si l'azimuth de la station est compris entre **angle_min** + 180 et **angle_max** + 180, la station est selectionnee pour la back projection

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth_ondeselect*
| to */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth_ondeselect_angle*

python3 plot_traces.py
----------------------

.. code-block:: python3

    python3 plot_traces.py

| plot

| from
| to

python3 tr_fct_az.py
--------------------

.. code-block:: python3

    python3 tr_fct_az.py

| plot

| from
| to

python3 bp_env_E.py
===================

.. code-block:: python3

    python3 bp_env_E.py

| back projection des stations selectionnees
| enregistre le stack dans un fichier

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth_ondeselect_angle*
| to */Kumamoto/dossier/dossier_results/dossier_vel_couronne_bandfreq*

python3 plot_bp_2d.py
=====================

.. code-block:: python3

    python3 plot_bp_2d.py

| from */Kumamoto/dossier/dossier_results/dossier_vel_couronne_bandfreq*
| to */Kumamoto/dossier/dossier_results/dossier_vel_couronne_bandfreq/pdf*

Arborescence
============

| Codes
| Kumamoto

  | dossier

    | dossier_brut
    | dossier_sac
    | dossier_sac_couronne
    | dossier_vel_couronne
    | dossier_vel_couronne_bandfreq

      | dossier_vel_couronne_bandfreq
      | dossier_vel_couronne_bandfreq_3comp
      | dossier_vel_couronne_bandfreq_hori
      | dossier_vel_couronne_bandfreq_hori_env
      | dossier_vel_couronne_bandfreq_hori_env_smooth
      | dossier_vel_couronne_bandfreq_hori_env_smooth_P
      | dossier_vel_couronne_bandfreq_hori_env_smooth_S
      | dossier_vel_couronne_bandfreq_vert










