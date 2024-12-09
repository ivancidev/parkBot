# Instrucciones para Configurar y Ejecutar el Programa

## Requisitos Previos

### Editor Recomendado

Se recomienda usar **Visual Studio Code (VS Code)** como editor de código.
- Si aún no lo tienes instalado, puedes descargarlo desde: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### Versión de Python

- Asegúrate de tener instalada la versión **Python 3.12** o superior.
- Puedes verificar tu versión de Python ejecutando el siguiente comando en tu terminal:

```bash
python --version
```

- Si necesitas instalar Python, descárgalo desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## Instalación de Dependencias

1. Abre una nueva terminal en tu editor de código o en tu sistema operativo.
   - En Visual Studio Code, puedes abrir la terminal integrada con `Ctrl + \`` (combinación de teclas).

2. Ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
pip install numpy
```

Esto instalará la biblioteca **NumPy**, que es necesaria para el funcionamiento del programa. Todas las demás bibliotecas requeridas vienen preinstaladas con Python.

---

## Cómo Ejecutar el Programa

### 1. Para Entrenar el Agente

Corre el archivo `main.py` para entrenar al agente con el siguiente comando:

```bash
python main.py
```

Este archivo entrenará al agente y actualizará su modelo, que se guarda en un archivo llamado `parking_agent.pkl`.

### 2. Para Usar la Interfaz y Estacionar Autos

Corre el archivo `parking_ui.py` para abrir la interfaz gráfica y estacionar los vehículos:

```bash
python parking_ui.py
```

Una vez que la interfaz esté abierta, puedes interactuar con el simulador y observar cómo el agente toma decisiones para estacionar los vehículos.

### 3. Abrir con un Ejecutable

Ejecuta el archivo `parking_ui.exe` directamente para abrir la interfaz gráfica sin necesidad de usar la terminal.

---

## Notas Adicionales

### Archivo del Modelo Guardado

- El archivo `parking_agent.pkl` es donde se guarda el modelo entrenado del agente. Si no existe, el programa creará uno nuevo automáticamente al entrenar.

### Reiniciar el Entrenamiento

- Si deseas reiniciar el entrenamiento desde cero, elimina el archivo `parking_agent.pkl` antes de ejecutar `main.py`.

### Exploración y Aprendizaje del Agente

- Durante el entrenamiento, el agente ajustará su tabla Q para mejorar su toma de decisiones.
- Puedes revisar la tabla Q cargada o actualizada al ejecutar `main.py`.
