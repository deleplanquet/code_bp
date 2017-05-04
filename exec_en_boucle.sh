#!/bin/bash

cd
cd ../../media/deleplanque/Lexar/Data/Kumamoto/

liste_dossiers=`ls -d */`

cd
cd Documents/back_proj/en_cours/code/

for dossier in $liste_dossiers; do
	echo $dossier
	if [ ! -e ../../../../../../media/deleplanque/Lexar/Results/Kumamoto/$dossier ]; then
		python3 kumamoto_configuration.py $dossier
	fi
done
