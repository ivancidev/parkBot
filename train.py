import numpy as np
import matplotlib.pyplot as plt
from env import ParkingEnv
from agent import QLearningAgent
from utils import state_to_index
import os

# Función para visualizar estacionamiento final
def visualize_parking(env, num_vehicles):
    """Simula el estacionamiento con vehículos como puntos."""
    plt.figure(figsize=(8, 3))
    # Generar colores según el estado (0 = azul, 1 = rojo)
    colors = ['red' if x == 1 else 'blue' for x in env.state]
    # Crear puntos que representen los vehículos
    plt.scatter(range(env.num_spaces), [1] * env.num_spaces, c=colors, s=200, edgecolor='black')
    # Configuración del gráfico
    plt.title(f"Simulación Final del Estacionamiento ({num_vehicles} vehículos)")
    plt.xticks(range(env.num_spaces), labels=[f"Espacio {i+1}" for i in range(env.num_spaces)])
    plt.yticks([])
    plt.xlabel("Espacios de estacionamiento")
    plt.ylabel("Estado (azul: libre, rojo: ocupado)")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()


# Entrenamiento interactivo
def main():
    

    # Configuración inicial
    while True:
        num_spaces = int(input("Ingrese el número de espacios del estacionamiento: "))
        num_vehicles = int(input("Ingrese el número de vehículos a asignar: "))
        episodes = int(input("Ingrese el número de episodios de entrenamiento: "))
        model_file = f"q_table_{num_spaces}.pkl"
        env = ParkingEnv(num_spaces)
        num_states = 2**num_spaces
        agent = QLearningAgent(num_states=num_states, num_actions=num_spaces)

        # Cargar modelo entrenado si existe
        if os.path.exists(model_file):
           use_saved_model = input("¿Desea cargar el modelo entrenado previamente? (s/n): ").lower()
           if use_saved_model == 's':
              agent.load(model_file)
              print("Modelo cargado.")
           else:
              print("Entrenando un nuevo modelo...")
              agent = QLearningAgent(num_states=num_states, num_actions=num_spaces)



        rewards = []
        moving_avg_rewards = []

        # Entrenamiento
        for episode in range(episodes):
            state = env.reset()
            total_reward = 0
            done = False

            while not done:
                state_idx = state_to_index(state)
                action = agent.choose_action(state_idx)
                next_state, reward, done = env.step(action)
                next_state_idx = state_to_index(next_state)
                agent.update(state_idx, action, reward, next_state_idx)
                state = next_state
                total_reward += reward

                # Visualizar estado actual
                env.render(num_vehicles)

            rewards.append(total_reward)
            moving_avg_rewards.append(np.mean(rewards[-10:]))  # Media móvil
            agent.decay_epsilon()

            # Mostrar progreso del entrenamiento
            print(f"Episodio {episode + 1}/{episodes}, Recompensa: {total_reward}")

        # Guardar modelo entrenado
        agent.save(model_file)
        print("Modelo guardado exitosamente.")

        # Gráficos finales
        plt.figure()
        plt.plot(rewards, label="Recompensas")
        plt.plot(moving_avg_rewards, label="Media Móvil (10)")
        plt.title("Recompensas durante el entrenamiento")
        plt.xlabel("Episodios")
        plt.ylabel("Recompensa acumulada")
        plt.legend()
        plt.show()

        # Simulación final
        visualize_parking(env, num_vehicles)

        # Preguntar si desea realizar otro experimento
        cont = input("¿Desea entrenar con otro número de espacios y vehículos? (s/n): ").lower()
        if cont != 's':
            break

if __name__ == "__main__":
    main()
