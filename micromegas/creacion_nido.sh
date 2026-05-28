#!/usr/bin/env bash
#Creación del nido. 
workdir=$(pwd)
cd $workdir/micromegas_5.0.9/
#Esta cantidad va desde 1 hasta 12. 
for i in {1..6}; do
    	ARGUMENTO='idms_'$i #Este es el nombre que le queremos dar a cada una de las carpetas de micromegas. 
    	./newProject $ARGUMENTO
    	#Vamos a utilizar los datos provistos en tools/idms/
    	cp $workdir/tools/idms.tar.xz $ARGUMENTO/work/models
    	cd $workdir/micromegas_5.0.9/$ARGUMENTO/work/models
    	tar -xJf idms.tar.xz 
		cd -
		cd $workdir/micromegas_5.0.9/$ARGUMENTO
		cp -f $workdir/tools/data.dat . #data.dat proviene de idms. 
		cp -f $workdir/tools/main.c . #Esta main.c nos muestra una información muy compacta. 
		make main=main.c
		if ./main data.dat | grep -q "Omega="; then
    		echo "✅ Confirmación: Cálculo de la Densidad de Reliquia (Omega) encontrado."
    		cd $workdir/micromegas_5.0.9/
    	else
	    	echo "❌ Fallo de Confirmación: La palabra 'Omega=' no se encontró en la salida."
	    	exit 1
		fi
	done
