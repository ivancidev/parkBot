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
        """Estaciona un vehículo en el primer espacio disponible más cercano."""
        # Lista de los espacios disponibles y su proximidad
        available_spaces = [i for i in range(self.total_spaces) if self.spaces[i] == 0]
        
        # Ordenar los espacios disponibles por proximidad (espacios más cercanos primero)
        sorted_available_spaces = sorted(available_spaces, key=lambda x: abs(x - (self.total_spaces // 2)))
        
        # Intentamos estacionar el vehículo en el primer espacio disponible más cercano
        for space in sorted_available_spaces:
            if self.spaces[space] == 0:  # Si el espacio está vacío
                self.spaces[space] = vehicle_id  # Marca el espacio con el ID del vehículo
                return space  # Devuelve el índice del espacio ocupado
        return -1  # Si no hay espacios disponibles, devuelve -1

    def park_vehicles(self, num_vehicles):
        """Estaciona múltiples vehículos, priorizando los espacios cercanos."""
        parked_vehicles = 0
        
        for vehicle_id in range(num_vehicles):
            # El agente intenta estacionar el vehículo en el primer espacio disponible más cercano
            parked_space = self.park_vehicle(vehicle_id)
            
            if parked_space != -1:  # Si se estacionó con éxito
                parked_vehicles += 1
            else:
                print("No hay espacio disponible para estacionar más vehículos.")
                break

        return parked_vehicles

    def reset(self):
        """Resetea el estacionamiento."""
        self.spaces = [0] * self.total_spaces
        self.vehicle_positions = []
        self.last_displayed_state = list(self.spaces)  # Resetea el estado mostrado

    def display_parking_lot(self):
        """Muestra el estado del estacionamiento solo si ha cambiado."""
        if self.spaces != self.last_displayed_state:
            print("Estado actual del estacionamiento:")
            for i in range(self.total_spaces):
                print(f"Espacio {i + 1}: {'Ocupado' if self.spaces[i] != 0 else 'Vacío'}")
            print("\n")
            self.last_displayed_state = list(self.spaces)  # Actualizamos el estado mostrado
