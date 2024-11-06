import numpy as np
import gym
from gym import spaces
from stable_baselines3 import DQN
import tkinter as tk
import random

class UrbanParkingEnv(gym.Env):
    def __init__(self, num_spaces=10, max_time=10):
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
env = UrbanParkingEnv(num_spaces=10)
model = DQN("MlpPolicy", env, verbose=0)

# Función para entrenar el modelo
def train_model():
    model.learn(total_timesteps=10000)
    print("Entrenamiento completo.")

# Función para actualizar la interfaz de los espacios
def update_parking_spaces():
    for i, space in enumerate(env.available_spaces):
        if space == 1:
            parking_buttons[i].config(bg="green", text=f"Libre {i+1}")
        else:
            parking_buttons[i].config(bg="red", text=f"Ocupado {i+1}")

# Función para buscar un espacio de estacionamiento
def find_parking():
    obs = env.available_spaces
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        if reward == 1:  # Encontró un espacio libre
            print(f"Carrito estacionado en el espacio {action + 1}")
            update_parking_spaces()
            break

# Crear la interfaz de usuario
root = tk.Tk()
root.title("Simulador de Estacionamiento Urbano")

train_button = tk.Button(root, text="Entrenar Modelo", command=train_model)
train_button.grid(row=0, column=0, columnspan=5, pady=10)

evaluate_button = tk.Button(root, text="Buscar Estacionamiento", command=find_parking)
evaluate_button.grid(row=1, column=0, columnspan=5, pady=10)

# Crear botones para representar los espacios de estacionamiento
parking_buttons = []
for i in range(env.num_spaces):
    button = tk.Button(root, text=f"Libre {i+1}", width=10, height=2, bg="green")
    button.grid(row=(i // 5) + 2, column=i % 5, padx=5, pady=5)
    parking_buttons.append(button)

update_parking_spaces()
root.mainloop()
