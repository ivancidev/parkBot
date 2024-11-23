import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.99):
        self.q_table = np.zeros((num_states, num_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def choose_action(self, state_idx):
        """Elige una acción basada en la política ε-greedy."""
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.q_table.shape[1])
        return np.argmax(self.q_table[state_idx])

    def update(self, state_idx, action, reward, next_state_idx):
        """Actualiza la Q-table."""
        best_next_action = np.argmax(self.q_table[next_state_idx])
        td_target = reward + self.gamma * self.q_table[next_state_idx][best_next_action]
        self.q_table[state_idx][action] += self.alpha * (td_target - self.q_table[state_idx][action])

    def decay_epsilon(self):
        """Reduce el valor de epsilon."""
        self.epsilon *= self.epsilon_decay

    def save(self, filename):
        """Guarda la Q-table en un archivo."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filename):
        """Carga la Q-table desde un archivo."""
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
