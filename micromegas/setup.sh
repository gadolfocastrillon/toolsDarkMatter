#!/usr/bin/env bash

# --- Definición de archivos de configuración ---
CONFIG_FILE="config.txt"
VERSION_FILE="version"
MODELO_FILE="modelo"

# --- Validaciones iniciales ---
if [[ ! -f "$CONFIG_FILE" || ! -f "$VERSION_FILE" || ! -f "$MODELO_FILE" ]]; then
    echo "❌ Error: Faltan archivos de configuración (config.txt, version o modelo)."
    exit 1
fi

# --- Carga de variables ---
# Usamos tr para limpiar espacios y sed para líneas específicas
VERSION_DIR=$(tr -d '[:space:]' < "$VERSION_FILE")
NOMBRE_MODELO=$(tr -d '[:space:]' < "$MODELO_FILE")

PREFIX=$(sed -n '1p' "$CONFIG_FILE")
# Línea 2 y 3 se usan en el script de ejecución, aquí las cargamos por consistencia
START=$(sed -n '4p' "$CONFIG_FILE")
END=$(sed -n '5p' "$CONFIG_FILE")

workdir=$(pwd)

# --- Entrada al directorio base de MicrOMEGAs ---
if [[ -d "$workdir/$VERSION_DIR" ]]; then
    cd "$workdir/$VERSION_DIR" || exit 1
else
    echo "❌ Error: El directorio base $VERSION_DIR no existe."
    exit 1
fi

echo "🚀 Iniciando configuración en: $VERSION_DIR"
echo "📦 Modelo a utilizar: $NOMBRE_MODELO"
echo "🔢 Rango: $START hasta $END"

# --- Bucle principal ---
for (( i=$START; i<=$END; i++ )); do
    ARGUMENTO="${PREFIX}${i}"
    
    echo "------------------------------------------"
    echo "⚙️  Procesando: $ARGUMENTO"

    # --- VALIDACIÓN: Evitar duplicados ---
    if [[ -d "$ARGUMENTO" ]]; then
        echo "⚠️  El directorio $ARGUMENTO ya existe. Saltando creación y descompresión."
    else
        # Crear el nuevo proyecto
        if [[ -f "./newProject" ]]; then
            ./newProject "$ARGUMENTO"
        else
            echo "❌ Error: No se encontró el ejecutable ./newProject"
            exit 1
        fi

        # Copiar y descomprimir el modelo
        RUT_MODELO_ORIGEN="$workdir/tools/$NOMBRE_MODELO"
        
        if [[ -f "$RUT_MODELO_ORIGEN" ]]; then
            mkdir -p "$ARGUMENTO/work/models/"
            cp "$RUT_MODELO_ORIGEN" "$ARGUMENTO/work/models/"
            
            cd "$ARGUMENTO/work/models" || exit
            echo "📦 Descomprimiendo $NOMBRE_MODELO en $ARGUMENTO..."
            tar -xJf "$NOMBRE_MODELO"
            cd - > /dev/null
        else
            echo "❌ Error: No se encontró el archivo $RUT_MODELO_ORIGEN"
            continue
        fi
    fi

    # --- Compilación y Test (Siempre se verifica) ---
    if [[ -d "$ARGUMENTO" ]]; then
        cd "$ARGUMENTO" || continue
        
        # Copiar archivos necesarios desde tools
        cp -f "$workdir/tools/data.dat" .
        cp -f "$workdir/tools/main.c" .

        echo "🛠️  Compilando main.c en $ARGUMENTO..."
        make main=main.c > /dev/null 2>&1

        # Ejecutar y verificar salida
        if [[ -f "./main" ]]; then
            if ./main data.dat | grep -q "Omega="; then
                echo "✅ Confirmación: 'Omega=' detectado correctamente."
            else
                echo "❌ Fallo: 'Omega=' no encontrado en la ejecución."
                exit 1
            fi
        else
            echo "❌ Error: No se pudo generar el ejecutable 'main'."
            exit 1
        fi

        # Regresar al nivel de la versión
        cd "$workdir/$VERSION_DIR"
    fi
done

echo "------------------------------------------"
echo "✨ ¡Proceso completado con éxito!" 