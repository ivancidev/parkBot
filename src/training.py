import pickle
def train_agent(agent, parking_lot, num_vehicles):
    total_reward = 0

    for vehicle_id in range(1, num_vehicles + 1):  # Iterar desde 1 hasta num_vehicles
        state = parking_lot.spaces
        action = agent.choose_action(state)  # El agente selecciona un espacio

        parked_space = parking_lot.park_vehicle(vehicle_id, action)  # Proporcionar 'action' como espacio sugerido
        if parked_space != -1:
            reward = 1  # Recompensa por estacionar correctamente
        else:
            reward = -1  # Penalización si no puede estacionar
        
        next_state = parking_lot.spaces
        agent.update_q_table(action, reward, next_state)
        total_reward += reward

    parking_lot.display_parking_lot()
    agent.decay_exploration_rate()
    print(f"Total reward en este episodio: {total_reward}")
    return total_reward

def save_model(agent, filename="parking_agent.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

def load_model(filename="parking_agent.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
