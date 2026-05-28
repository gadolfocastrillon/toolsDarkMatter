#!/usr/bin/env bash

# --- Archivos de configuración ---
VERSION_FILE="version"
MODELO_FILE="modelo"

# --- Validaciones iniciales ---
if [[ ! -f "$VERSION_FILE" || ! -f "$MODELO_FILE" ]]; then
    echo "❌ Error: Faltan archivos 'version' o 'modelo'."
    exit 1
fi

# --- Carga de variables ---
VERSION_DIR=$(tr -d '[:space:]' < "$VERSION_FILE")
NOMBRE_MODELO=$(tr -d '[:space:]' < "$MODELO_FILE")
workdir=$(pwd)

echo "🛠️  Iniciando preparación de $VERSION_DIR..."

# --- Descompresión de la base de MicrOMEGAs ---
if [[ -d "$workdir/$VERSION_DIR" ]]; then
    echo "⚠️  La carpeta $VERSION_DIR ya existe. Saltando descompresión y make principal."
else
    if [[ -f "$workdir/tools/${VERSION_DIR}.tgz" ]]; then
        echo "📦 Descomprimiendo MicrOMEGAs..."
        tar -xzvf "$workdir/tools/${VERSION_DIR}.tgz"
        
        echo "🏗️  Compilando MicrOMEGAs (esto puede tardar un poco)..."
        cd "$workdir/$VERSION_DIR" || exit
        make
        cd "$workdir"
    else
        echo "❌ Error: No se encontró $workdir/tools/${VERSION_DIR}.tgz"
        exit 1
    fi
fi

# --- Prueba de creación de proyecto ---
cd "$workdir/$VERSION_DIR" || exit

# Usamos 'prueba' como nombre temporal para el test
TEST_DIR="prueba_instalacion"

if [[ -d "$TEST_DIR" ]]; then
    echo "🧹 Limpiando prueba anterior..."
    rm -rf "$TEST_DIR"
fi

echo "🚀 Creando proyecto de prueba: $TEST_DIR"
./newProject "$TEST_DIR"

# --- Copia y descompresión del modelo ---
RUT_MODELO_ORIGEN="$workdir/tools/$NOMBRE_MODELO"

if [[ -f "$RUT_MODELO_ORIGEN" ]]; then
    cp "$RUT_MODELO_ORIGEN" "$TEST_DIR/work/models/"
    if [ $? -eq 0 ]; then
        echo "✅ Éxito: Modelo copiado correctamente."
        cd "$TEST_DIR/work/models/" || exit
        tar -xJf "$NOMBRE_MODELO"
        cd - > /dev/null
    else
        echo "❌ Error: Falló la copia del modelo."
        exit 1
    fi
else
    echo "❌ Error: No se encontró el modelo en $RUT_MODELO_ORIGEN"
    exit 1
fi

# --- Compilación del proyecto de prueba ---
cd "$TEST_DIR" || exit
make # Compila la estructura del proyecto

# Copiar archivos de herramientas
cp -f "$workdir/tools/data.dat" .
cp -f "$workdir/tools/main.c" .

echo "🛠️  Compilando ejecutable de prueba (main.c)..."
make main=main.c > /dev/null

# --- Verificación final ---
echo "🧪 Ejecutando ./main para verificar Omega..."
if ./main data.dat | grep -q "Omega="; then
    echo "✅ Confirmación: Cálculo de la Densidad de Reliquia (Omega) encontrado."
    echo "🎉 MicrOMEGAs está listo para ser usado."
else
    echo "❌ Fallo de Confirmación: No se detectó 'Omega=' en la salida."
    exit 1
fi

# Regresar al directorio original
cd "$workdir"