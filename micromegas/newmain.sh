#!/usr/bin/env bash

# --- Archivos de configuración ---
CONFIG_FILE="config.txt"
VERSION_FILE="version"

# --- Validaciones de existencia ---
if [[ ! -f "$CONFIG_FILE" || ! -f "$VERSION_FILE" ]]; then
    echo "Error: Falta config.txt o el archivo version."
    exit 1
fi

# --- Cargar datos de los archivos ---
# Leer el nombre de la versión (limpiando espacios)
VERSION_DIR=$(tr -d '[:space:]' < "$VERSION_FILE")

# Leer parámetros de configuración
PREFIX=$(sed -n '1p' "$CONFIG_FILE")
ARCHIVO=$(sed -n '2p' "$CONFIG_FILE")
NAME=$(sed -n '3p' "$CONFIG_FILE")
START=$(sed -n '4p' "$CONFIG_FILE")
END=$(sed -n '5p' "$CONFIG_FILE")

workdir=$(pwd)

echo "--- Iniciando proceso para $VERSION_DIR ---"

for (( i=$START; i<=$END; i++ )); do
    DIRECTORY="${PREFIX}${i}"
    
    # Construcción de la ruta usando la variable de versión
    TARGET_DIR="$workdir/$VERSION_DIR/$DIRECTORY"

    if [[ -d "$TARGET_DIR" ]]; then
        echo "Processing $DIRECTORY..."

        # Copiar herramientas
        cp "$workdir/tools/$ARCHIVO" "$TARGET_DIR/"

        # Entrar al directorio
        cd "$TARGET_DIR" || { echo "Error al entrar a $TARGET_DIR"; continue; }

        # Limpiar y Descomprimir
        rm -f nohup.out ard_results.csv
        tar -xJf "$ARCHIVO"
        
        # Ejecución en segundo plano
        nohup python "$NAME" > /dev/null 2>&1 &
        
        # Volver a la raíz del proyecto
        cd "$workdir"
    else
        echo "Saltando: $DIRECTORY (No existe en $VERSION_DIR)"
    fi

    sleep 0.05
done

echo "Done. Todos los procesos han sido lanzados en segundo plano."