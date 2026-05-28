#!/usr/bin/env bash

# --- Archivos de configuración ---
CONFIG_FILE="config.txt"
VERSION_FILE="version"

# --- Validaciones ---
if [[ ! -f "$CONFIG_FILE" || ! -f "$VERSION_FILE" ]]; then
    echo "Error: Falta config.txt o el archivo version."
    exit 1
fi

# --- Cargar datos ---
VERSION_DIR=$(tr -d '[:space:]' < "$VERSION_FILE")
PREFIX=$(sed -n '1p' "$CONFIG_FILE")
START=$(sed -n '4p' "$CONFIG_FILE")
END=$(sed -n '5p' "$CONFIG_FILE")

# Nombre del archivo de salida
OUTPUT_FILE="slts-scan-${PREFIX%_}.txt"

# Eliminar el archivo de resultados previo si existe para empezar de cero
rm -f "$OUTPUT_FILE"

echo "--- Consolidating results from $VERSION_DIR ---"

for (( i=$START; i<=$END; i++ )); do
    DIRECTORY="${PREFIX}${i}"
    # Ruta al archivo de resultados de cada carpeta
    RESULT_FILE="$VERSION_DIR/$DIRECTORY/ard_results.txt"
    
    echo "Collecting from $DIRECTORY..."
    
    # Verificar si el archivo existe antes de intentar concatenar
    if [[ -f "$RESULT_FILE" ]]; then
        # Añadir una cabecera opcional o solo el contenido
        cat "$RESULT_FILE" >> "$OUTPUT_FILE"
    else
        echo "Warning: $RESULT_FILE not found."
    fi
    
    sleep 0.02
done

echo "--- Process complete. Results saved in: $OUTPUT_FILE ---"