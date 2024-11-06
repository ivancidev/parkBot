# Proyecto Python

Este proyecto en Python utiliza un entorno virtual para gestionar sus dependencias.

## Configuración Inicial

Sigue estos pasos para configurar el proyecto desde cero.

### 1. Clona el repositorio


```
git clone https://github.com/ivancidev/parkBot
```

### 2. Crea y activa el entorno virtual

```
python -m venv venv
```

 - En Linux/macOS:
 ```
source venv/bin/activate

 ```

 - En Windows:
 ```
 .\venv\Scripts\activate
 ```

 ### 3. Instala las dependencias
 ```
pip install -r requirements.txt
 ```

 - Instalar paquetes:
 ```
    pip install gym gymnasium stable-baselines3 numpy
 ```
- **Ejecuta con: `python parking.py`**

- Quizas al ejecutar te de error si tienes problemas con shimmy
```
 pip install 'shimmy>=0.2.1'
```

- Si te aaprece segundo error con gymnasium ejecuta el siguiente:
```
pip install gymnasium==0.29.1
```

Con eso deberia correrte y aparecer un ventana de interfaz.
