class ParkingLot:
    def __init__(self, total_spaces):
        self.total_spaces = total_spaces
        self.spaces = [0] * total_spaces  # Todos los espacios vacíos

    def find_empty_space(self):
        """Encuentra el primer espacio vacío."""
        for i, space in enumerate(self.spaces):
            if space == 0:
                return i
        return None

    # Método para estacionar un vehículo en un espacio sugerido
    def park_vehicle(self, vehicle_id, suggested_space):
        attempts = 0
        while attempts < self.total_spaces:  # Intenta todos los espacios posibles
            if 0 <= suggested_space < self.total_spaces and self.spaces[suggested_space] == 0:
                self.spaces[suggested_space] = vehicle_id
                return suggested_space
            else:
                suggested_space = (suggested_space + 1) % self.total_spaces
                attempts += 1
        return -1  # No se pudo estacionar




    def park_vehicles(self, num_vehicles):
        parked_vehicles = []
        for vehicle_id in range(1, num_vehicles + 1):
            suggested_space = self.find_empty_space()
            if suggested_space is not None:
                parked_space = self.park_vehicle(vehicle_id, suggested_space)
                parked_vehicles.append(parked_space)
            else:
                print(f"No hay espacio disponible para el vehículo {vehicle_id}.")
        return len(parked_vehicles)

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
