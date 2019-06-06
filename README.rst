.. contents::

.. section-numbering::

Parameters
==========

By running ``parametres.py``, all the necessary parameters will be asked to the
user.

Here is a list of all the parameters that has to be defined.

+-----------------------+---------------------------------------------------+
| **Parameters**        | Description                                       |
+=======================+===================================================+
| **event**             | name of the event (earthquake)                    |
+-----------------------+---------------------------------------------------+
| **hypo_min**          | minimum of hypocenter distance (in km)            |
+-----------------------+---------------------------------------------------+
| **hypo_max**          | maximum of hypocenter distance (in km)            |
+-----------------------+---------------------------------------------------+
| **frq_min**           | low frequency (in Hz) for the pass-band filter    |
|                       | used on the velocity waveforms                    |
+-----------------------+---------------------------------------------------+
| **frq_max**           | high frequency (in Hz) for the pass-band filter   |
|                       | used on the velocity waveforms                    |
+-----------------------+---------------------------------------------------+
| **component**         | component [*3cpn*, *hori*, *vert*] used in the    |
|                       | study                                             |
+-----------------------+---------------------------------------------------+
| **ratioSP**           | ratio between the maximum amplitude of energy of S|
|                       | and P-waves                                       |
+-----------------------+---------------------------------------------------+
| **l_smooth**          | length (in s) of the time-window for the smoothing|
|                       | (RMS) of the energy waveforms                     |
+-----------------------+---------------------------------------------------+
| **l_impulse**         | length (in s) of the time-window for the selection|
|                       | of impulsive stations                             |
+-----------------------+---------------------------------------------------+
| **angle_min**         | minimum of azimuth angle (in deg)                 |
+-----------------------+---------------------------------------------------+
| **angle_max**         | maximum of azimuth angle (in deg)                 |
+-----------------------+---------------------------------------------------+
| **vP**                | P-waves velocity                                  |
+-----------------------+---------------------------------------------------+
| **vS**                | S-waves velocity                                  |
+-----------------------+---------------------------------------------------+
| **selected_waves**    | choice of the waves [*P*, *S*] used for the study |
+-----------------------+---------------------------------------------------+
| **strike**            | strike direction of the rectangular grid          |
+-----------------------+---------------------------------------------------+
| **dip**               | dip direction of the rectangular grid             |
+-----------------------+---------------------------------------------------+
| **l_grid**            | length of the grid (in km) (strike direction)     |
+-----------------------+---------------------------------------------------+
| **w_grid**            | width of the grid (in km) (dip direction)         |
+-----------------------+---------------------------------------------------+
| **l_grid_step**       | length of each subgrid (in km) (strike direction) |
+-----------------------+---------------------------------------------------+
| **w_grid_step**       | width of each subgrid (in km) (dip direction)     |
+-----------------------+---------------------------------------------------+
| **bp_samp_rate**      | frequency of the back projection images (in Hz)   |
+-----------------------+---------------------------------------------------+
| **bp_length_time**    | duration of the back projection (in s)            |
+-----------------------+---------------------------------------------------+

Here is the list of all the other parameters that are stored through the run
of ``parametres.py`` but not asked to the user:

+-----------------------+---------------------------------------------------+
| **Parameters**        | Description                                       |
+=======================+===================================================+
| **root_folder**       | pick the absolute position of the */Codes*        |
|                       | directory, should be at the same location with the|
|                       | */Kumamoto* directory                             |
+-----------------------+---------------------------------------------------+
| **R_Earth**           | Earth radius equal to 6400 km                     |
+-----------------------+---------------------------------------------------+
| **hypo_interv**       | combine **hypo_min** and **hypo_max** inside a    |
|                       | string                                            |
+-----------------------+---------------------------------------------------+
| **frq_band**          | combine **frq_min** and **frq_max** inside a      |
|                       | string                                            |
+-----------------------+---------------------------------------------------+
| **angle**             | combine **angle_min** and **angle_max** inside a  |
|                       | string                                            |
+-----------------------+---------------------------------------------------+

::

    Kumamoto                            *OUTPUT* named as current_parameters.txt
    ├── parameters_history              *OUTPUT* named as parametres_creationtime.txt
    └── event
        └── results
            └── general
                └── hypo_interv_selected_waves_angle
                    └── parameters      *OUTPUT* named as parametres_creationtime.txt

Tree view
=========

::

    Codes
    Kumamoto
    ├── parameters_history
    └── event
        ├── brut
        ├── acc 
        │   ├── brut
        │   ├── inf100km
        │   └── inf100km_copy
        ├── vel
        │   ├── brut
        │   ├── frq_band
        │   └── frq_band_component
        ├── vel_env
        │   ├── frq_band_component
        │   └── frq_band_component_smooth
        ├── vel_env_selection
        │   ├── frq_band_component_smooth_hypo_interv
        │   ├── frq_band_component_smooth_hypo_interv_selected_waves
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle
        ├── vel_env_bpinv
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle
        │       └── iteration-i
        │           ├── brut
        │           └── smooth
        ├── vel_env_modifed
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle
        │       └── iteration-i
        └── results
            ├── general
            └── vel_env_frq_band_component_smooth
                ├── hypo_interv_selected_waves_angle
                │   ├── parameters
                │   ├── brut
                │   │   ├── pdf
                │   │   └── png
                │   ├── iteration-i
                │   │   ├── pdf
                │   │   └── png
                │   └── others
                └── others

Data
====

ASCII format
------------

Data are downloaded from `http://www.kyoshin.bosai.go.jp` provided by National
Reasearch Institute for Earth Science and Disaster Resilience (NIED) for
research use only here.

::

    Kumamoto
    └── event
        └── brut    *DOWLOAD + UNZIP*

Do not forget to unzip the original files.

SAC format
----------

``tosac.py`` converts the original data into SAC files.

::

    Kumamoto
    └── event
        ├── brut        *INPUT*
        └── acc
            └── brut    *OUTPUT*

Picking
=======

"Local" stations (hypocenter distance < 100 km)
-----------------------------------------------

``station_inf_100km.py`` selects the stations with hypocenter distance less
than 100 km. This is to prevent too high variability among the records.

::

    Kumamoto
    └── event
        └── acc
            ├── brut        *INPUT*
            └── inf100km    *OUTPUT*

Hand picking of P and S-waves arrival time
------------------------------------------

The files should be copied/pasted from */Kumamoto/event/acc/inf_100km* to
*/Kumamoto/event/acc/inf_100km_copy* before any picking. This is to prevent the
loss of the picking by running the previous codes again.

Then each file is opened to pick the waves arrival time (the three components
at same time). The picking is intentionally done on UD component and then
applied on every component through further code.

By following these steps, files localised at */Kumamoto/event/acc/inf_100km*
do not have any picking information, but files localised at
*/Kumamoto/event/acc/inf_100km_copy* are modified and contain the picking
information (again, at this step, only UD component file contain the picking
information).

::

    Kumamoto
    └── event
        └── acc
            ├── inf100km        *COPY*
            └── inf100km_copy   *PASTE + MODIFY*

Velocity waveforms
==================

From acceleration to velocity waveforms
---------------------------------------

By running ``acc2vel.py``, the records (acceleregrams) are converted to
velocity waveforms.

::

    Kumamoto
    └── event
        ├── acc
        │   └── inf100km_copy   *INPUT*
        └── vel
            └── brut            *OUTPUT*

The process of conversion is done in spectral domain (FFT/IFFT). To prevent any
frequency content issue, the following steps are performed:

* Remove of the average mean value to prevent high energy content in very low
  frequency domain
* Remove very low frequencies (< 1/20 Hz)
* Consider only 50 sec of the trace, from 5 sec before picked P-arrival time to
  45 sec after
* Smoothly bring to 0 the beginning and the end of the trace to prevent
  apparent discontinuity and high energy content in high frequency domain
* Change the value for picked P and S-arrival time (necessary because of the
  cut of the trace)

Then the conversion itself can be done properly.

It can be note that the source directory is
*/Kumamoto/event/acc/inf100km_copy*. The code can not be runned if the picking
has not been done in the expected directory.

Filtering
---------

``filt_vel.py`` is filtering each component of the velocity waveforms with
a pass-band filter between **frq_min** and **frq_max** defined by user through
the run of ``parametres.py``.

::

    Kumamoto
    └── event
        └── vel
            ├── brut        *INPUT*
            └── frq_band    *OUTPUT*

Combination of the components
-----------------------------

By running ``3components.py``, three different combinations among the
components for each station will be done.

* Firt one is combining the three components all together to have the '3D'
  velocity waveform.
* Second one is combining both EW and UD components to have the 'horizontal'
  component of the velocity.
* And the last one is just keeping the UD component to consider it as the
  'vertical' component of the velocity.

Here, we are aware of the positivity of the '3D' and 'horizontal' velocity
waveforms. On purpose we don't deal with the sign because the study is not
using velocity waveforms directly as we can see after.

::

    Kumamoto
    └── event
        └── vel
            ├── frq_band            *INPUT*
            └── frq_band_component  *OUTPUT*

Envelopes
=========

From velocity waveforms to envelopes
------------------------------------

``vel2env.py`` will convert the velocity waveforms into envelopes by simply
squarring the velocity waveforms.

::

    Kumamoto
    └── event
        ├── vel
        │   └── frq_band_component  *INPUT*
        └── vel_env
            └── frq_band_component  *OUTPUT*

Smoothing
---------

``env2smooth.py`` smooths the envelopes (RMS) with a time-window of length
**l_smooth** defined by the user through the run of ``parametres.py``

::

    Kumamoto
    └── event
        └── vel_env
            ├── frq_band_component          *INPUT*
            └── frq_band_component_smooth   *OUTPUT*

Stations selection
==================

Distance selection
------------------

Through the run of ``select_couronne.py``, stations will be selected according
to their hypocenter distance. The stations selected are inside a ring defined
by the **hypo_min** and **hypo_max** values.

::

    Kumamoto
    └── event
        ├── vel_env
        │   └── frq_band_component_smooth               *INPUT*
        └── vel_env_selection
            └── frq_band_component_smooth_hypo_interv   *OUTPUT*

Energy distribution-based selection
-----------------------------------

By running ``select_stat_env.py``, stations will be sorted depending on their
P and S-waves energy ratio. More precisely, the maxima of energy for both P and
S-waves are checked. Their ratio (S/P) is compared to the parameter **ratioSP**
given by the user through the run of ``parametres.py``.

::

    Kumamoto
    └── event
        └── vel_env_selection
            ├── frq_band_component_smooth_hypo_interv                   *INPUT*
            └── frq_band_component_smooth_hypo_interv_selected_waves    *OUTPUT*

Azimuth-based selection
-----------------------

``select_station_angle.py`` is sorting stations depending on their relative
azimuth to the hypocenter of the studied event. Stations with azimuth between
**angle_min** and **angle_max** OR between **angle_min** + 180 and
**angle_max** + 180 are selected.

::

    Kumamoto
    └── event
        └── vel_env_selection
            ├── frq_band_component_smooth_hypo_interv_selected_waves        *INPUT*
            └── frq_band_component_smooth_hypo_interv_selected_waves_angle  *OUTPUT*

Station corrections
===================

``vitesse_PS.py`` is calculating station corrections, that is the delay between
the picked arrival time (for both P and S-waves) and the expected arrival time
of geometrical calculation.

::

    Kumamoto
    └── event
        ├── vel
        │   └── brut    *INPUT*
        └── results
            └── general *OUTPUT*

Back projection
===============

Building back projection cube
-----------------------------

By running ``bp_env_E.py``, a 4D cube will be created and stored in a
dictionnary. The 4 dimensions are the followings:

* 2 dimensions in space to explore the grid
* 1 dimension in time representing the duration of application of the back
  projection process (longer than duration of the event to not miss anything)
* 1 dimension for the stations, that is the envelopes are back projected but
  not stacked yet. The stack can be quickly done later among all the stations
  or just part of them without running the ``bp_env_E.py`` code again (which is
  the most time consuming code)

::

    Kumamoto
    └── event
        ├── vel_env
        │   └── frq_band_component_smooth       *INPUT*
        └── results
            ├── general                         *INPUT & OUTPUT*
            └── vel_env_frq_band_component_smooth
                └── others                      *OUTPUT*

The travel time matrix and absolute travel time cube will also be stored for
faster further use.

Summation among stations
------------------------

``prestack2stack.py`` is reducing the dimension of the 4D cube to 3 dimensions
by summing for the stations each subgrid at each time. The stations considered
are the ones remaining after distance, energy and azimuth selections.

::

    Kumamoto
    └── event
        ├── vel_env_selection
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle      *INPUT*
        └── results
            └── vel_env_frq_band_component_smooth
                ├── hypo_interv_selected_waves_angle
                │   └── others                                                  *OUTPUT*
                └── others                                                      *INPUT*

Plotting back projection images
-------------------------------

``plot_bp.py`` is creating images from the 3D cube of back projection. There
are as many images as time step in the back projection process. They reveal the
coherent information among the network at the corresponding studied parameters.

::

    Kumamoto
    └── event
        └── results
            └── vel_env_frq_band_component_smooth
                └── hypo_interv_selected_waves_angle
                    ├── pdf             *OUTPUT*
                    ├── png             *OUTPUT*
                    └── others          *INPUT*

Source extraction
=================

Creation of inverse traces
--------------------------

The run of ``bpinv_trace.py`` will read the back projection cube and assume
every subgrid as a source with an intensity equal to the value of the cube at
the corresponding time and position. Then traces will be created for each
station as if all the back projection cube was radiating. Finally traces will
be smoothed.

::

    Kumamoto
    └── event
        ├── vel_env_selection
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle      *INPUT*
        ├── vel_env_bpinv
        │   └── frq_band_component_smooth_hypo_interv_selected_waves_angle
        │       ├── brut                                                        *OUTPUT*
        │       └── smooth                                                      *OUTPUT*
        └── results
            ├── general                                                         *INPUT*
            └── vel_env_frq_band_component_smooth
                └── hypo_interv_selected_waves_angle
                    └── others                                                  *INPUT*

Iteration of back projection method
-----------------------------------

As explained in **Back projection** chapter, the three steps are done here
again by running the following codes:

* ``bp_env_E_patch_secondaire.py``
* ``prestack2stack.py``
* ``plot_bp_patch_secondaire.py``

Secondary codes
===============

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

python3 seismicity.py
---------------------

.. code-block:: python3

    python3 seismicity.py

| plot la sismicite dans la region du main shock
| affiche le main shock et les deux foreshocks
| le tout sur differentes periodes (avant, apres, entre deux evenements...)

| from */Kumamoto*
| to */Kumamoto*

python3 carte_SoverP.py
-----------------------

.. code-block:: python3

    python3 carte_SoverP.py

| fait une carte affichant les stations retenues jusque la avec l'information energie S/P

| from */Kumamoto/dossier/dossier_vel_couronne_bandfreq/dossier_vel_couronne_bandfreq_composante_env_smooth*
| to */Kumamoto/dossier/dossier_results*




