#!/bin/bash

cd ../Data/Kumamoto

liste_dossiers=`ls -d */`

for dossier in $liste_dossiers; do
	cd /localstorage/deleplanque/Data/Kumamoto/
	dodo=${dossier:0:14}
	echo $dodo
	if [ ! -e /localstorage/deleplanque/Data/Kumamoto_sac/$dodo ]; then
		cd $dodo/
		../../../Codes/tosac.py $dodo.kik
		../../../Codes/tosac.py $dodo.knt
	fi
done
