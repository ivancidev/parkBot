import pickle
def train_agent(agent, parking_lot, num_vehicles, vehicle_type="pequeño"):
    total_reward = 0

    for vehicle_id in range(1, num_vehicles + 1):
        state = parking_lot.spaces
        action = agent.choose_action(state, parking_lot.space_types, vehicle_type)
        parked_space = parking_lot.park_vehicle(vehicle_id, action, vehicle_type)
        
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

    parking_lot.display_parking_lot()  # Asegúrate de que este método existe en ParkingLot
    agent.decay_exploration_rate()

    print(f"Total reward en este episodio: {total_reward}")
    return total_reward


def save_model(agent, filename="parking_agent.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)
    print(f"Modelo guardado en {filename}.")

def load_model(filename="parking_agent.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
