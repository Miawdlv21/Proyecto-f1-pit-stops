# Proyecto Integrador: Análisis de Pit Stops en F1 (2011-2024)

Este repositorio contiene el código y la estructura para el proyecto integrador de 5to semestre de Ciencia de Datos. El objetivo es analizar cómo la eficiencia y variabilidad en las paradas en boxes afectan el éxito de las escuderías en el Campeonato de Constructores.

## Estructura del Proyecto

* `data/`: Contiene los datos originales y procesados.
* `scripts/`: Scripts de Python y notebooks para el pipeline ETL, análisis y Machine Learning.
* `requirements.txt`: Lista de librerías necesarias para ejecutar el proyecto.

## Guía de Instalación para Colaboradores

Para evitar conflictos de versiones, trabajaremos estrictamente con un **entorno virtual**. Sigue estos pasos para configurar tu entorno local:

### Paso 1: Clonar el repositorio
Abre tu terminal y clona este repositorio en tu máquina:
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DE_LA_CARPETA]

### Paso 2: Crear el entorno virtual
Ejecuta el siguiente comando para crear un entorno virtual llamado `.venv`:
python -m venv .venv

### Paso 3: Activar el entorno virtual
* **En Windows:**
  .venv\Scripts\activate
* **En Mac/Linux:**
  source .venv/bin/activate

*(Sabrás que está activado porque verás `(.venv)` al principio de la línea de tu terminal).*

### Paso 4: Instalar las dependencias
Con el entorno activado, instala todas las librerías necesarias ejecutando:
pip install -r requirements.txt

---
**Nota para el equipo:** Si instalas una nueva librería durante el desarrollo (por ejemplo, `pip install seaborn`), recuerda actualizar el archivo de dependencias ejecutando:
`pip freeze > requirements.txt` y sube ese cambio a GitHub.