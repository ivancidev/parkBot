import random
import numpy as np
import pickle
def train_agent(agent, parking_lot, num_vehicles):
    total_reward = 0
    # Asegúrate de que el número de vehículos no sea mayor que el número de espacios
    num_vehicles = min(num_vehicles, parking_lot.total_spaces)

    # Asegura que solo se estacionen los vehículos solicitados
    parked_vehicles = parking_lot.park_vehicles(num_vehicles)

    for vehicle_id in range(parked_vehicles):
        state = parking_lot.spaces
        
        # Verificar si ya hay espacios disponibles
        if parked_vehicles >= parking_lot.total_spaces:
            print("No hay más espacios disponibles.")
            break  # Detener el entrenamiento si no hay más espacio
        
        action = agent.choose_action(state)
        
        # Intentar estacionar el vehículo
        parked_space = parking_lot.park_vehicle(vehicle_id)
        if parked_space != -1:  # Si se estaciona correctamente
            reward = 1  # Recompensa por estacionar con éxito
        else:
            reward = -1  # Penalización si no hay espacio disponible (aunque no debería ocurrir ahora)

        next_state = parking_lot.spaces
        agent.update_q_table(action, reward, next_state)
        total_reward += reward
        parking_lot.display_parking_lot()  # Mostrar estado después de cada vehículo estacionado

    agent.decay_exploration_rate()
    print(f"Total reward en este episodio: {total_reward}")
    return total_reward

def save_model(agent, filename="parking_agent.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

def load_model(filename="parking_agent.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
