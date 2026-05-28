#!/bin/bash

# Salir inmediatamente si algún comando falla
set -e

URL_MICROMEGAS="https://lapth.cnrs.fr/micromegas/downloadarea/code/micromegas_5.0.9.tgz"
CARPETA_TOOLS="tools"
ARCHIVO_TGZ="micromegas_5.0.9.tgz"

echo "================================================="
echo " Creando entorno e instalando micrOmegas 5.0.9 "
echo "================================================="

mkdir -p "$CARPETA_TOOLS"

echo "-> Descargando micrOmegas desde la fuente oficial..."
wget -O "$CARPETA_TOOLS/$ARCHIVO_TGZ" "$URL_MICROMEGAS"