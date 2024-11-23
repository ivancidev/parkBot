import random
import numpy as np
class ParkingAgent:
    def __init__(self, total_spaces, learning_rate=0.1, discount_factor=0.9):
        self.total_spaces = total_spaces
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = np.zeros(total_spaces)
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.01
        
    def calculate_distances(self, state, start_position):
        """Calcula las distancias desde el punto inicial a los espacios vacíos."""
        distances = []
        for i, space in enumerate(state):
            if space == 0:  # Solo considerar espacios vacíos
                distance = abs(start_position - i)
                distances.append((distance, i))
        return sorted(distances)  # Ordenar por distancia

    def choose_action(self, state, start_position=0):
        """Selecciona un espacio basado en distancia o exploración."""
        if random.uniform(0, 1) < self.exploration_rate:
            # Explorar: Elegir aleatoriamente entre los más cercanos
            distances = self.calculate_distances(state, start_position)
            return distances[0][1] if distances else -1
        else:
            # Explotar: Elegir el mejor espacio basado en Q
            return np.argmax(self.q_table)

    def update_q_table(self, action, reward, next_state):
        if reward == -1:  # Penalización para acciones inválidas
            print(f"Penalizando acción inválida: {action}")
        best_future_q = np.max(self.q_table[next_state])
        self.q_table[action] = (1 - self.learning_rate) * self.q_table[action] + \
                           self.learning_rate * (reward + self.discount_factor * best_future_q)

    def print_q_table(self):
        print("Tabla Q:")
        for i, q_value in enumerate(self.q_table):
            print(f"Espacio {i + 1}: Q-value = {q_value:.2f}")


    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
