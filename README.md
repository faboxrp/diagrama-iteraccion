# Calculadora de Diagrama de Interacción para Muros de Mampostería

Esta aplicación web, desarrollada con FastAPI (Python), permite calcular y graficar el diagrama de interacción de Carga Axial (Pr) y Momento Resistente (Mr) para muros de mampostería. La interfaz facilita la introducción de parámetros de geometría, materiales y acero de refuerzo, generando resultados de manera dinámica.

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación y Ejecución

Sigue los pasos a continuación para ejecutar el proyecto en tu entorno local.

### 1. Clona o descarga el repositorio

Descarga los archivos del proyecto en una carpeta local.

### 2. Crea un entorno virtual (recomendado)

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Crear el entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### 3. Instala las dependencias

Con el entorno virtual activado, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### 4. Inicia el servidor web

Utiliza Uvicorn para lanzar la aplicación. El siguiente comando iniciará un servidor local con recarga automática al detectar cambios en el código fuente:

```bash
uvicorn main:app --reload
```

### 5. Accede a la aplicación

Cuando el servidor esté en ejecución, abre tu navegador y visita:

```
http://127.0.0.1:8000
```

¡Listo! Ahora puedes interactuar con la aplicación desde tu navegador.