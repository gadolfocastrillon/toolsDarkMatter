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
VERSION_DIR=$(tr -d '[:space:]' < "$VERSION_FILE")

PREFIX=$(sed -n '1p' "$CONFIG_FILE")
# (Las líneas 2 y 3 no se usan aquí, pero mantenemos la estructura)
START=$(sed -n '4p' "$CONFIG_FILE")
END=$(sed -n '5p' "$CONFIG_FILE")

echo "--- Checking logs in $VERSION_DIR ---"

for (( i=$START; i<=$END; i++ )); do
    ARGUMENTO="${PREFIX}${i}"
    LOG_FILE="$VERSION_DIR/$ARGUMENTO/nohup.out"
    
    echo "Checking $ARGUMENTO..."
    
    # Verificar si el archivo nohup.out existe antes de hacer grep
    if [[ -f "$LOG_FILE" ]]; then
        # Buscamos "sltns" en el archivo de log
        grep "sltns" "$LOG_FILE"
    else
        echo "No nohup.out file found in $ARGUMENTO"
    fi
    
    sleep 0.02
done

echo "--- Check complete ---"