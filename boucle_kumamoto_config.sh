#!/bin/bash

cd /localstorage/deleplanque/Data/Kumamoto_sac/

liste_dossiers=`ls -d */`

cd /localstorage/deleplanque/Codes/

for dossier in $liste_dossiers; do
	dodo=${dossier:0:14}
	echo $dodo
	if [ ! -e /localstorage/deleplanque/Results/Kumamoto/$dossier/ ]; then
		python3 kumamoto_configuration.py $dossier
	fi
done
