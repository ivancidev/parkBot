import random
import numpy as np
class ParkingAgent:
    def __init__(self, total_spaces, learning_rate=0.1, discount_factor=0.9):
        self.total_spaces = total_spaces
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = np.zeros(total_spaces)  # Inicializa una tabla de Q con valores nulos
        self.exploration_rate = 1.0  # Tasa de exploración (comienza explorando mucho)
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.01

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(self.total_spaces))  
        else:
            return np.argmax(self.q_table)  # Explotación: elige el mejor espacio basado en Q

    def update_q_table(self, action, reward, next_state):
        # Actualización de la tabla Q
        best_future_q = np.max(self.q_table[next_state])
        self.q_table[action] = (1 - self.learning_rate) * self.q_table[action] + self.learning_rate * (reward + self.discount_factor * best_future_q)

    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
