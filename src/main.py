from parking_lot import ParkingLot
from parking_agent import ParkingAgent
from training import train_agent, save_model, load_model
import os

def main():
    model_filename = "parking_agent.pkl"
    total_spaces = 16  # Número total de espacios
    
    if os.path.exists(model_filename):
        # Cargar el modelo guardado
        agent = load_model(model_filename)
        print("Modelo cargado exitosamente.")
        print("Tabla Q cargada:", agent.q_table)
    else:
        print(f"El archivo {model_filename} no existe. Creando un nuevo agente...")
        agent = ParkingAgent(total_spaces)  # Crear un nuevo agente
    
    # Crear la instancia de ParkingLot
    parking_lot = ParkingLot(total_spaces)

    # Puedes seguir entrenando el agente cargado
    num_vehicles = min(int(input("Ingrese el número de vehículos a estacionar: ")), total_spaces)

    
    # Entrenar el agente con varios episodios
    for _ in range(10):  # Entrena en 10 episodios
        parking_lot.reset()  # Limpia el estado del estacionamiento
        reward = train_agent(agent, parking_lot, num_vehicles)
        print(f"Total reward en este episodio: {reward}")

    save_model(agent)
    print("Modelo guardado después del entrenamiento.")

if __name__ == "__main__":
    main()
