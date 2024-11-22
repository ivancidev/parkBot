import pickle
def train_agent(agent, parking_lot, num_vehicles):
    total_reward = 0

    for vehicle_id in range(1, num_vehicles + 1):
        state = parking_lot.spaces
        action = agent.choose_action(state)
        parked_space = parking_lot.park_vehicle(vehicle_id, action)
        
        # Ajuste de recompensas
        if parked_space != -1:
            reward = 10  # Recompensa positiva por estacionar correctamente
        else:
            reward = -10  # Penalización negativa si no se estaciona

        next_state = parking_lot.spaces
        agent.update_q_table(action, reward, next_state)
        total_reward += reward

        # Imprimir el estado, acción y recompensa
        print(f"Estado: {state}, Acción: {action}, Recompensa: {reward}")

    parking_lot.display_parking_lot()
    agent.decay_exploration_rate()

    # Imprimir la tabla Q actualizada
    print(f"Tabla Q actualizada:\n{agent.q_table}")

    print(f"Total reward en este episodio: {total_reward}")
    return total_reward

def save_model(agent, filename="parking_agent.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

def load_model(filename="parking_agent.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
