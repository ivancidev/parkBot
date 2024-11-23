import numpy as np
import matplotlib.pyplot as plt

class ParkingEnv:
    def __init__(self, num_spaces):
        self.num_spaces = num_spaces
        self.state = np.zeros(num_spaces)
        self.action_space = np.arange(num_spaces)
        self.reset()

    def reset(self):
        """Reinicia el entorno."""
        self.state = np.zeros(self.num_spaces)
        return self.state

    def step(self, action):
        """Ejecuta una acción."""
        if self.state[action] == 0:
            self.state[action] = 1  # Ocupa el espacio
            reward = 10
        else:
            reward = -5  # Penalización
        done = all(self.state)
        return self.state, reward, done

    def render(self, num_vehicles):
        """Visualiza el estacionamiento en tiempo real."""
        plt.clf()
        colors = ['blue' if x == 0 else 'red' for x in self.state]
        plt.bar(range(self.num_spaces), [1] * self.num_spaces, color=colors, edgecolor='black')
        plt.title(f"Estado del estacionamiento ({num_vehicles} vehículos)")
        plt.xlabel("Espacios")
        plt.ylabel("Estado (azul: libre, rojo: ocupado)")
        plt.pause(0.5)
