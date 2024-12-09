class ParkingLot:
    def __init__(self, total_spaces):
        self.total_spaces = total_spaces
        self.spaces = [0] * total_spaces  # Todos los espacios vacíos
        self.vehicle_types = {}  # Diccionario para asociar vehículos con sus tipos
        # Definir las reglas de estacionamiento para diferentes tipos de vehículos
        self.parking_rules = {
            "pequeño": range(0, total_spaces // 3),
            "mediano": range(total_spaces // 3, 2 * (total_spaces // 3)),
            "grande": range(2 * (total_spaces // 3), total_spaces)  # Solo en espacios grandes
        }
        # Atributo para almacenar los tipos de espacio
        self.space_types = ['pequeño'] * (total_spaces // 3) + \
                           ['mediano'] * (total_spaces // 3) + \
                           ['grande'] * (total_spaces - 2 * (total_spaces // 3))
        self.last_displayed_state = list(self.spaces)  # Resetea el estado mostrado

    def find_empty_space(self):
        """Encuentra el primer espacio vacío."""
        for i, space in enumerate(self.spaces):
            if space == 0:
                return i
        return None

    # Método para estacionar un vehículo en un espacio sugerido
    def park_vehicle(self, vehicle_id, suggested_space, vehicle_type="pequeño"):
        valid_spaces = self.parking_rules.get(vehicle_type, [])
        attempts = 0

        while attempts < self.total_spaces:
            if suggested_space in valid_spaces and self.spaces[suggested_space] == 0:
                self.spaces[suggested_space] = vehicle_id
                self.vehicle_types[vehicle_id] = vehicle_type
                return suggested_space
            else:
                suggested_space = (suggested_space + 1) % self.total_spaces
                attempts += 1

        return -1  # No se pudo estacionar

    def park_vehicles(self, num_vehicles, vehicle_type="pequeño"):
        parked_vehicles = []
        for vehicle_id in range(1, num_vehicles + 1):
            suggested_space = self.find_empty_space()
            if suggested_space is not None:
                parked_space = self.park_vehicle(vehicle_id, suggested_space, vehicle_type)
                parked_vehicles.append(parked_space)
            else:
                print(f"No hay espacio disponible para el vehículo {vehicle_id}.")
        return len(parked_vehicles)

    def reset(self):
        """Resetea el estacionamiento."""
        self.spaces = [0] * self.total_spaces
        self.vehicle_types = {}
        self.last_displayed_state = list(self.spaces)  # Resetea el estado mostrado

    def display_parking_lot(self):
        """Muestra el estado del estacionamiento solo si ha cambiado."""
        if self.spaces != self.last_displayed_state:
            print("Estado actual del estacionamiento:")
            for i in range(self.total_spaces):
                print(f"Espacio {i + 1}: {'Ocupado' if self.spaces[i] != 0 else 'Vacío'}")
            print("\n")
            self.last_displayed_state = list(self.spaces)  # Actualizamos el estado mostrado

    def get_state(self):
        """Devuelve el estado del estacionamiento como una lista."""
        return self.spaces
