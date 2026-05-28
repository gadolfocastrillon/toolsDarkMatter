#!/bin/bash
#Define la ruta
CARPETA_TOOLS="tools"
NOMBRE_COMPRIMIDO="funciones_python.tar.xz" #nombre del archivo

echo "================================================="
echo " Generando archivo comprimido: $NOMBRE_COMPRIMIDO "
echo "================================================="

# Verifica si la carpeta tools existe
if [ ! -d "$CARPETA_TOOLS" ]; then
    echo "❌ Error: La carpeta $CARPETA_TOOLS no existe."
    exit 1
fi

# Entra a la carpeta para que el tar no guarde rutas completas
cd "$CARPETA_TOOLS"

# Verifica que los archivos .py existan antes de comprimir
if [ ! -f "funcion_l.py" ] || [ ! -f "main_limit_Ms2.py" ]; then
    echo "❌ Error: No se encontró 'funcion_l.py' o 'main_limit_Ms2.py' en tools/."
    exit 1
fi

echo "-> Comprimiendo archivos en formato XZ (máxima compresión)..."

# Crea el archivo .tar.xz
tar -cJvf "$NOMBRE_COMPRIMIDO" funcion_l.py main_limit_Ms2.py

echo "================================================="
echo " ¡Archivo creado con éxito en $CARPETA_TOOLS/$NOMBRE_COMPRIMIDO! "
echo "================================================="