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

    def choose_action(self, state, space_types, vehicle_type):
        if random.uniform(0, 1) < self.exploration_rate:
            # Elegir aleatoriamente entre espacios vacíos compatibles con el tipo de vehículo
            available_spaces = [i for i, space in enumerate(state) if space == 0 and self.is_space_compatible(space_types[i], vehicle_type)]
            return random.choice(available_spaces) if available_spaces else -1
        else:
            # Explotar la mejor acción basada en Q
            return np.argmax(self.q_table)

    def is_space_compatible(self, space_type, vehicle_type):
        if vehicle_type == "pequeño":
            return space_type in ["pequeño", "mediano", "grande"]
        elif vehicle_type == "mediano":
            return space_type in ["mediano", "grande"]
        elif vehicle_type == "grande":
            return space_type == "grande"
        return False

    def update_q_table(self, action, reward, next_state):
        if reward == -1:  # Penalización para acciones inválidas
            print(f"Penalizando acción inválida: {action}")
        best_future_q = np.max(self.q_table[next_state])
        self.q_table[action] = (1 - self.learning_rate) * self.q_table[action] + \
                               self.learning_rate * (reward + self.discount_factor * best_future_q)

    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
