3Dj
=================

3Dj is a SuperCollider library for real-time interactive 3D sound spatialization.

Developed in collaboration with Barcelona Media (http://www.barcelonamedia.org/) as the implementation part of the Master Thesis "Real-Time 3D Audio Spatialization Tools for Interactive Performance", Music Technology Group, Pompeu Fabra University, Barcelona.

Master thesis available here: http://www.andresperezlopez.com/sites/default/files/Andres_Perez_Master_Thesis.pdf

The code can be easily installed through the Quarks system.

=================
FEATURES

Spatial Render:
- 3D source position
- Spatialization techniques: ambisonics, vbap and binaural
- Up to full 3rd order Ambisonics, with different source shapes: punctual, ring, semi-meridian and extended
- SpatDIF compatible
- Log and playback SpatDIF scenes
- Remote performance
- Distance cues
- Jack compatible

Scene Simulator:
- Unlimited number of sound objects
- Source interaction: top-down (absolute objects control) and bottom-up (physical model-based)
- Predefined source motions: orbital, shm, brownian...
- Scene visualization
- SpatDIF compatible

Interaction:
- OSC compatible
- Log and playback user interface gestures

=================
DEPENDENCIES

Spatial Render:
- AmbDec (ambisonics) : http://kokkinizita.linuxaudio.org/linuxaudio/
- SC3 plugins (vbap) : https://github.com/supercollider/sc3-plugins
- ATK: Ambisonics Toolkit (binaural) : http://www.ambisonictoolkit.net/wiki/tiki-index.php

Scene Simulator:
- Quarks: MathLib, redUniverse

Tested for GNU/Linux. It *should* work for OSX,  and maybe partially for Windows.

================
EXTRA

Together with the SuperCollider code, we provide other useful complements:
- Python: scripts for Ambisonics encoding visualization
- Sounds: 4 mono tracks, ready for spatialization!
- Android: a Processing sketch providing sensor data in OSC through the local network, in the OrientationController required format. Ready to compile with Processing-Android.

================
(C) Andrés Pérez López, 2014

All the code is licensed under GPL v3.0

contact [at] andresperezlopez.com // www.andresperezlopez.com
