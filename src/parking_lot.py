import random
import numpy as np
import pickle

class ParkingLot:
    def __init__(self, total_spaces):
        self.total_spaces = total_spaces
        self.spaces = [0] * total_spaces  # 0: vacío, 1: ocupado
        self.vehicle_positions = []
        self.last_displayed_state = list(self.spaces)  # Estado anterior para comparación

    def park_vehicle(self, vehicle_id):
        for i in range(len(self.spaces)):
            if self.spaces[i] == 0:  # Espacio vacío
                self.spaces[i] = 1  # Marca el espacio como ocupado
                self.vehicle_positions.append((vehicle_id, i))  # Guarda la posición del vehículo
                return i  # Retorna el espacio donde se estacionó el vehículo
        return -1  # No hay espacio disponible

    def park_vehicles(self, num_vehicles):
        # Asegura que solo se estacionen los vehículos solicitados
        parked_vehicles = 0
        for vehicle_id in range(num_vehicles):
            parked_space = self.park_vehicle(vehicle_id)
            if parked_space != -1:
                parked_vehicles += 1
            else:
                break  # Si no hay más espacio, sale del bucle
        return parked_vehicles

    def reset(self):
        # Resetea el estacionamiento
        self.spaces = [0] * self.total_spaces
        self.vehicle_positions = []
        self.last_displayed_state = list(self.spaces)  # Resetea el estado mostrado

    def display_parking_lot(self):
        # Muestra el estado del estacionamiento solo si ha cambiado
        if self.spaces != self.last_displayed_state:
            print("Estado actual del estacionamiento:")
            for i in range(self.total_spaces):
                print(f"Espacio {i + 1}: {'Ocupado' if self.spaces[i] == 1 else 'Vacío'}")
            print("\n")
            self.last_displayed_state = list(self.spaces)  # Actualizamos el estado mostrado
