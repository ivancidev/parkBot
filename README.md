# Instrucciones para Configurar y Ejecutar el Programa

A continuación, encontrarás una guía paso a paso para instalar las dependencias necesarias y ejecutar el programa correctamente.

## Requisitos Previos

### Editor Recomendado:
- Se recomienda usar **Visual Studio Code (VS Code)** como editor de código.
- Si aún no lo tienes instalado, puedes descargarlo desde: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### Versión de Python:
- Asegúrate de tener instalada la versión **Python 3.12 o superior**.
- Puedes verificar tu versión de Python ejecutando el siguiente comando en tu terminal:
  ```bash
  python --version
  ```
- Si necesitas instalar Python, descárgalo desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## Configuración del Entorno Virtual

1. Abre una terminal en tu sistema o en Visual Studio Code.
   - En Visual Studio Code, puedes abrir la terminal integrada con la combinación de teclas:
     **Ctrl + ñ**.

2. Crea un entorno virtual para el proyecto:
   - Ejecuta el siguiente comando en la carpeta raíz del proyecto:
     ```bash
     python -m venv env
     ```
   - Esto creará una carpeta llamada `env`, que contendrá el entorno virtual.

3. Activa el entorno virtual:
   - **En Windows:**
     ```bash
     .\env\Scripts\activate
     ```
   - **En Mac/Linux:**
     ```bash
     source env/bin/activate
     ```

4. Verifica que el entorno virtual esté activo:
   - Deberías ver el prefijo `(env)` al inicio de tu terminal.

---

## Instala las Dependencias

Ejecuta el siguiente comando para instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### Instalar paquetes adicionales:
```bash
pip install gym gymnasium stable-baselines3 numpy
```

---

## Cómo Ejecutar el Programa

1. En la carpeta raíz, navega a la carpeta `src`:
   ```bash
   cd src
   ```

### 1. Para Entrenar el Agente:
- Corre el archivo `main.py` para entrenar al agente con el siguiente comando:
  ```bash
  python main.py
  ```
- Este archivo entrenará al agente y actualizará su modelo, que se guarda en un archivo llamado `parking_agent.pkl`.

### 2. Para Usar la Interfaz y Estacionar Autos:
- Corre el archivo `parking_ui.py` para abrir la interfaz gráfica y estacionar los vehículos:
  ```bash
  python parking_ui.py
  ```
- Una vez que la interfaz esté abierta, puedes interactuar con el simulador y observar cómo el agente toma decisiones para estacionar los vehículos.

---

## Notas Adicionales

### Archivo del Modelo Guardado:
- El archivo `parking_agent.pkl` es donde se guarda el modelo entrenado del agente.
- Si no existe, el programa creará uno nuevo automáticamente al entrenar.

### Reiniciar el Entrenamiento:
- Si deseas reiniciar el entrenamiento desde cero, elimina el archivo `parking_agent.pkl` antes de ejecutar `main.py`.

### Exploración y Aprendizaje del Agente:
- Durante el entrenamiento, el agente ajustará su tabla Q para mejorar su toma de decisiones.
- Puedes revisar la tabla Q cargada o actualizada al ejecutar `main.py`.

---

## Abrir con un Ejecutable:
- Para abrir directamente la interfaz, utiliza el archivo `parking_ui.exe`.
