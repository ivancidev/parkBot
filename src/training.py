import pickle
def train_agent(agent, parking_lot, num_vehicles, start_position=0):
    total_reward = 0

    for vehicle_id in range(1, num_vehicles + 1):
        state = parking_lot.spaces
        action = agent.choose_action(state, start_position)
        parked_space = parking_lot.park_vehicle(vehicle_id, action)

        if parked_space != -1:
            reward = 10 - abs(start_position - parked_space)  # Mayor recompensa por espacios más cercanos
        else:
            reward = -10

        next_state = parking_lot.spaces
        agent.update_q_table(action, reward, next_state)
        total_reward += reward

        print(f"Estado: {state}, Acción: {action}, Recompensa: {reward}")

    parking_lot.display_parking_lot()
    agent.decay_exploration_rate()

    print(f"Recompensa total: {total_reward}")
    return total_reward

def save_model(agent, filename="parking_agent.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

def load_model(filename="parking_agent.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
