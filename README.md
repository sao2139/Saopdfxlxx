# SaoPdfxlxx Enterprise

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?logo=windows&logoColor=white) ![Version](https://img.shields.io/badge/Version-1.0.0-555555)

## Descripción General

**SaoPdfxlxx Enterprise** es una solución de escritorio desarrollada para la automatización de procesos ETL (Extracción, Transformación y Carga) de documentos no estructurados. El sistema está diseñado específicamente para procesar lotes masivos de archivos PDF, extrayendo información crítica (entidades nominadas, direcciones y fechas) mediante algoritmos de coincidencia de patrones (Regex) y exportando los resultados a formatos estructurados (Excel/.xlsx).

La arquitectura del software implementa procesamiento asíncrono (multithreading) para garantizar la estabilidad de la interfaz gráfica y la gestión eficiente de memoria durante cargas de trabajo intensivas.

## Especificaciones Técnicas

### Arquitectura del Sistema
El proyecto sigue una arquitectura modular desacoplada:
* **Core Engine:** Lógica de extracción pura separada de la interfaz.
* **UI Layer:** Interfaz gráfica basada en `customtkinter` para renderizado de alta DPI.
* **Config Module:** Centralización de patrones de expresiones regulares para mantenimiento escalable.

### Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Motor de Extracción:** `pdfplumber` (Análisis de layout y texto).
* **Manipulación de Datos:** `pandas` (Dataframes y serialización Excel).
* **Interfaz Gráfica:** `customtkinter` (Thread-safe GUI).
* **Compilación:** PyInstaller (Generación de binarios).
* **Empaquetado:** Inno Setup (Creación de instalador Windows).

## Requisitos de Instalación

### Para Usuario Final (Entorno de Producción)
El software se distribuye mediante un instalador ejecutable para sistemas Windows de 64 bits.

1.  Descargar el archivo `Instalador_SaoPdfxlxx_v1.0.exe` desde la sección de **Releases**.
2.  Ejecutar el asistente de instalación con privilegios estándar (no requiere administrador).
3.  El sistema desplegará los binarios y creará los accesos directos correspondientes.

### Para Desarrolladores (Código Fuente)

Clonar el repositorio y establecer el entorno virtual:

```bash
git clone [https://github.com/TU_USUARIO/SaoPdf_Enterprise.git](https://github.com/TU_USUARIO/SaoPdf_Enterprise.git)
cd SaoPdf_Enterprise
pip install -r requirements.txt