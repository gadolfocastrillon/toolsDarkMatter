# toolsDarkMatter

Este repositorio contiene un conjunto de herramientas, scripts de automatización y pipelines para la instalación, configuración y ejecución de software científico orientado al estudio de la Materia Oscura.

El objetivo principal es centralizar la infraestructura de simulación para garantizar la reproducibilidad de los entornos de trabajo en sistemas Linux (Ubuntu).

---

## 📁 Estructura del Repositorio

* **`micromegas/`**: Scripts de automatización y flujos de trabajo para el código en micrOmegas.
    * `descarga.sh`: Descarga la versión 5.0.9 de micrOmegas.
    * `install_micromegas.sh`: Despues de la descargar, descomprime micrOmegas y ejecuta una prueba de funcionamiento 
    * `modelo`: Archivo de configuración que apunta al identificador del modelo físico activo.
    * `version`: Tiene la versión de micrOmegas utilizada.
    * `tools/`: Scripts auxiliares de análisis (Python/C) y plantillas esenciales.
    * `creacion_funciones_python.sh`: Hace uso de dos programa de python funcion_l.py y main_limit_Ms2.py para comprimirlo y crear un archivo .tar necesario para ejecutar los programas.
    * `creacion_nido.sh`: Crea diferentes carpetas de micrOmegas con el fin de ejecutar el modelo objetivo en varios núcleos.
    * `newmain.sh` / `setup.sh`: Ejecuta el codigo necesario para correr el programa dentro de micrOmegas para todos los nidos.
    * `config.txt`: Tiene la información de cómo se van a llamar las carpetas dentro del nido y cuantas carpetas voy a crear en el mismo.
    * `check.sh`: Se encarga de verificar si termino de corer el programa.
    * `collet.sh`: Recopila la información de las carpetas creadas para el modelo. 

---

## 🛠️ Requisitos Previos

Antes de ejecutar los scripts de instalación, asegúrate de contar con las herramientas esenciales de compilación en Linux:


### Para micrOmegas
```bash
sudo apt update
sudo apt install build-essential gfortran make cmake python
sudo pip install numpy pandas 

```

### Para madgraph y maddump
