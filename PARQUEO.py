import numpy as np
import gym
from gym import spaces
from stable_baselines3 import DQN
import tkinter as tk
from PIL import Image, ImageTk
import random
import time

class UrbanParkingEnv(gym.Env):
    def __init__(self, num_spaces=44, max_time=10):
        super(UrbanParkingEnv, self).__init__()
        self.num_spaces = num_spaces
        self.max_time = max_time
        self.available_spaces = np.ones(self.num_spaces)
        self.time_remaining = np.zeros(self.num_spaces)

        self.action_space = spaces.Discrete(self.num_spaces)
        self.observation_space = spaces.Box(low=0, high=1, shape=(num_spaces,), dtype=np.float32)

    def reset(self):
        self.available_spaces = np.ones(self.num_spaces)
        self.time_remaining = np.zeros(self.num_spaces)
        return self.available_spaces

    def step(self, action):
        reward = 0
        done = False
        if self.available_spaces[action] == 0:
            reward = -1
        else:
            self.available_spaces[action] = 0
            self.time_remaining[action] = random.randint(1, self.max_time)
            reward = 1

        for i in range(self.num_spaces):
            if self.time_remaining[i] > 0:
                self.time_remaining[i] -= 1
            if self.time_remaining[i] == 0:
                self.available_spaces[i] = 1

        if np.sum(self.available_spaces) == 0:
            done = True

        return self.available_spaces, reward, done, {}

# Crear el entorno y el modelo DQN
env = UrbanParkingEnv(num_spaces=44)
model = DQN("MlpPolicy", env, verbose=0)

# Coordenadas de cada espacio de estacionamiento en el canvas (11 columnas x 4 filas)
space_positions = [
    # Primera fila
    (90, 38), (140, 38), (320, 38), (370, 38),
    
    (90, 64), (140, 64), (320, 64), (370, 64),
    
    (90, 90), (140, 90), (320, 90), (370, 90),

    (90, 114), (140, 114), (320, 114), (370, 114),

    (90, 139), (140, 139), (320, 139), (370, 139),

    (90, 165), (140, 165), (320, 165), (370, 165),

    (90, 190), (140, 190), (320, 190), (370, 190),

    (90, 216), (140, 216), (320, 216), (370, 216),

    (90, 242), (140, 242), (320, 242), (370, 242),

    (90, 267), (140, 267), (320, 267), (370, 267),

    (90, 293), (140, 293), (320, 293), (370, 293),
]

# Función para actualizar la interfaz de los espacios
def update_parking_spaces():
    if len(parking_rectangles) != env.num_spaces:
        print("Error: No coinciden los espacios de estacionamiento con las posiciones definidas.")
        return
    for i, space in enumerate(env.available_spaces):
        color = "green" if space == 1 else "red"
        canvas.itemconfig(parking_rectangles[i], fill=color)

# Función para mostrar la ruta en el canvas
def show_route_to_space(space_index):
    # Limpiar la ruta anterior
    canvas.delete("route")
    
    start_x, start_y = 250, 300  # Punto de inicio (centro de la imagen)
    end_x, end_y = space_positions[space_index]  # Punto de destino (espacio escogido)

    # Dibujar puntos de la ruta hacia el espacio escogido
    steps = 10  # Número de puntos en la ruta
    for i in range(steps + 1):
        x = start_x + (end_x - start_x) * i / steps
        y = start_y + (end_y - start_y) * i / steps
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="blue", tags="route")

# Función para buscar un espacio de estacionamiento y entrenar el modelo
def find_parking():
    obs = env.available_spaces
    done = False

    # Entrenar el modelo por refuerzo para que aprenda
    model.learn(total_timesteps=1, reset_num_timesteps=False)

    # Realizar una predicción y ejecutar una acción
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)

    if reward == 1:  # Si encontró un espacio libre
        stay_time = env.time_remaining[action]
        car_specs = f"Auto estacionado:\nEspacio escogido: {action + 1}\n"
        car_specs += f"Tiempo de permanencia: {stay_time} horas\n"
        specs_label.config(text=car_specs)
        print(f"Auto estacionado en el espacio {action + 1} por {stay_time} horas")

        # Mostrar la ruta hacia el espacio escogido
        show_route_to_space(action)
    else:
        specs_label.config(text="Espacio ocupado, intente de nuevo.")
        print("El espacio estaba ocupado, intente nuevamente.")

    # Actualizar la interfaz de los espacios
    update_parking_spaces()

# Crear la interfaz de usuario
root = tk.Tk()
root.title("Simulador de Estacionamiento Urbano")

# Cargar y mostrar la imagen del estacionamiento
image = Image.open("estacionamiento.jpg")
image = image.resize((500, 300))  # Ajusta el tamaño de la imagen si es necesario
parking_image = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=500, height=300)
canvas.create_image(0, 0, anchor="nw", image=parking_image)
canvas.grid(row=0, column=0, columnspan=5, pady=10)

# Crear rectángulos para representar cada espacio de estacionamiento
parking_rectangles = []
for x, y in space_positions:
    rect = canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="green", tags="parking_space")
    parking_rectangles.append(rect)

evaluate_button = tk.Button(root, text="Buscar Estacionamiento", command=find_parking)
evaluate_button.grid(row=1, column=0, columnspan=5, pady=10)

# Etiqueta para mostrar las especificaciones del auto
specs_label = tk.Label(root, text="Especificaciones del auto:", anchor="w", justify="left")
specs_label.grid(row=0, column=6, padx=10, rowspan=5)

update_parking_spaces()
root.mainloop()
