# toolsDarkMatter

Este repositorio contiene un conjunto de herramientas, scripts de automatización y pipelines para la instalación, configuración y ejecución de software científico orientado al estudio de la Materia Oscura.

El objetivo principal es centralizar la infraestructura de simulación para garantizar la reproducibilidad de los entornos de trabajo en sistemas Linux (Ubuntu).

---

## 📁 Estructura del Repositorio

* **`micromegas/`**: Scripts de automatización y flujos de trabajo para el código fenoménico micrOmegas.
    * `instalacion.sh` / `install_micromegas.sh`: Scripts para la descarga y compilación automática del entorno.
    * `check.sh` / `check-DE.sh`: Herramientas de verificación del estado del sistema y dependencias.
    * `modelo`: Archivo de configuración que apunta al identificador del modelo físico activo.
    * `tools/`: Scripts auxiliares de análisis (Python/C) y plantillas esenciales.
    * `versiones_activas/`: Control de versiones locales y configuraciones específicas de ejecución.

---

## 🛠️ Requisitos Previos

Antes de ejecutar los scripts de instalación, asegúrate de contar con las herramientas esenciales de compilación en Linux:


### Para micrOmegas
```bash
sudo apt update
sudo apt install build-essential gfortran make cmake

```

### Para madgraph y maddump
