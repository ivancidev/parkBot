from parking_lot import ParkingLot
from parking_agent import ParkingAgent
from training import train_agent, save_model, load_model
import os

def main():
    model_filename = "parking_agent.pkl"
    total_spaces = 16  
    
    if os.path.exists(model_filename):
        agent = load_model(model_filename)
        print("Modelo cargado exitosamente.")
        print("Tabla Q cargada:", agent.q_table)
    else:
        print(f"El archivo {model_filename} no existe. Creando un nuevo agente...")
        agent = ParkingAgent(total_spaces)  
    
    parking_lot = ParkingLot(total_spaces)

    num_vehicles = min(int(input("Ingrese el número de vehículos a estacionar: ")), total_spaces)

    episodes = 10  #
    for episode in range(episodes):
        print(f"Comenzando episodio {episode + 1}")
        parking_lot.reset()  
        total_reward = train_agent(agent, parking_lot, num_vehicles)
        print(f"Total reward en este episodio: {total_reward}")

    # Guardar el modelo entrenado
    save_model(agent, model_filename)
    print("Modelo guardado después del entrenamiento.")

if __name__ == "__main__":
    main()
