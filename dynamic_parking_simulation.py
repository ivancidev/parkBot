import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def dynamic_parking_simulation(env, num_vehicles):
    """Simula dinámicamente la asignación de vehículos a los espacios."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-1, env.num_spaces)
    ax.set_ylim(-1, 2)
    ax.set_xticks(range(env.num_spaces))
    ax.set_yticks([])
    ax.set_xlabel("Espacios de estacionamiento")
    ax.set_title("Simulación Dinámica del Estacionamiento")

    # Posiciones iniciales (vehículos fuera del estacionamiento)
    vehicle_positions = np.random.uniform(-1, env.num_spaces, num_vehicles)
    occupied_positions = []

    # Gráficos iniciales
    vehicles, = ax.plot(vehicle_positions, [1.5] * num_vehicles, 'bo', label="Vehículos (en movimiento)")
    parking, = ax.plot(range(env.num_spaces), [1] * env.num_spaces, 'ro', label="Espacios (ocupados)")
    ax.legend()

    def update(frame):
        """Actualización de cada cuadro de la animación."""
        nonlocal vehicle_positions
        for i in range(num_vehicles):
            if i < len(occupied_positions):  # Ya estacionado
                continue
            # Determinar el espacio más cercano disponible
            for j in range(env.num_spaces):
                if env.state[j] == 0:  # Espacio libre
                    if abs(vehicle_positions[i] - j) < 0.1:  # Casi estacionado
                        env.state[j] = 1  # Ocupa el espacio
                        occupied_positions.append(i)
                        vehicle_positions[i] = j  # Mover a la posición exacta
                        break
                    else:
                        vehicle_positions[i] += (j - vehicle_positions[i]) * 0.1  # Aproximarse

        # Actualizar colores de los espacios
        parking.set_color(['red' if x == 1 else 'blue' for x in env.state])
        vehicles.set_xdata(vehicle_positions)

    # Animar
    anim = FuncAnimation(fig, update, frames=100, interval=100)
    plt.show()
