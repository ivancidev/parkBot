from parking_lot import ParkingLot
from training import load_model 
import tkinter as tk
from tkinter import messagebox
import time

TOTAL_SPACES = 12 

agent = load_model("parking_agent.pkl")  # Cambia la ruta si guardaste el modelo en otro lugar

# Función para actualizar la matriz visual
def update_parking_display():
    for i in range(6):
        color = "red" if parking_lot.spaces[i] != 0 else "green"
        left_buttons[i].config(bg=color, text=f"L{i + 1}" if parking_lot.spaces[i] == 0 else f"Vehículo {parking_lot.spaces[i]}")

    for i in range(6, TOTAL_SPACES):
        color = "red" if parking_lot.spaces[i] != 0 else "green"
        right_buttons[i - 6].config(bg=color, text=f"R{i - 5}" if parking_lot.spaces[i] == 0 else f"Vehículo {parking_lot.spaces[i]}")

# Función para manejar el estacionamiento con el agente inteligente
def park_vehicles():
    try:
        num_vehicles = int(vehicle_entry.get()) 
        if num_vehicles <= 0:
            messagebox.showerror("Error", "Por favor, ingresa un número mayor a 0.")
            return

        spaces_occupied = 0 
        for vehicle_id in range(1, num_vehicles + 1):
            state = parking_lot.spaces  
            action = agent.choose_action(state)  
            
            space = parking_lot.park_vehicle(vehicle_id, action)
            if space != -1:
                animate_parking(vehicle_id, space) 
                reward = 1  
                spaces_occupied += 1
            else:
                reward = -1 
            
            # Actualizar la tabla Q del agente
            next_state = parking_lot.spaces
            agent.update_q_table(action, reward, next_state)
            
            time.sleep(0.5)  # Esperar un poco para la animación

        if spaces_occupied > 0:
            messagebox.showinfo("Éxito", f"{spaces_occupied} vehículo(s) estacionado(s).")
        else:
            messagebox.showinfo("Lleno", "No hay espacio disponible para estacionar.")

        update_parking_display()  # Actualizar la visualización
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido.")


# Función de animación para mover los vehículos
def animate_parking(vehicle_id, space):
    """Animar el proceso de estacionamiento moviendo los vehículos."""
    # Si el vehículo está en la parte izquierda
    if space < 6:
        button = left_buttons[space]
    else:
        button = right_buttons[space - 6]

    # Cambiar el color del botón para simular que el vehículo llega al espacio
    button.config(bg="blue", text=f"Vehículo {vehicle_id}")
    
    # Simular el "movimiento" hacia el espacio
    for i in range(6):
        if space < 6:  # Si es un espacio izquierdo
            left_buttons[i].config(bg="green")
        else:  # Si es un espacio derecho
            right_buttons[i].config(bg="green")
        time.sleep(0.1)  # Hacer una pausa para simular movimiento

    # Cambiar el color final cuando el vehículo ha llegado
    button.config(bg="blue", text=f"Vehículo {vehicle_id}")
    
# Crear la ventana principal
root = tk.Tk()
root.title("Simulador de Estacionamiento")
root.geometry("600x400")

parking_lot = ParkingLot(TOTAL_SPACES)

# Título
title_label = tk.Label(root, text="Simulador de Estacionamiento", font=("Arial", 16))
title_label.pack(pady=10)

# Entrada para el número de vehículos
vehicle_label = tk.Label(root, text="Número de vehículos a estacionar:")
vehicle_label.pack()
vehicle_entry = tk.Entry(root)
vehicle_entry.pack(pady=5)

# Botón para iniciar el estacionamiento
park_button = tk.Button(root, text="Estacionar", command=park_vehicles)
park_button.pack(pady=10)

# Crear el marco principal para las áreas de estacionamiento
parking_frame = tk.Frame(root)
parking_frame.pack(pady=20)

# Área izquierda (2 columnas × 3 filas)
left_frame = tk.Frame(parking_frame)
left_frame.grid(row=0, column=0, padx=20)

left_buttons = []
for i in range(6):
    button = tk.Button(left_frame, text=f"L{i + 1}", width=10, height=2, bg="green")
    button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
    left_buttons.append(button)

# Área derecha (2 columnas × 3 filas)
right_frame = tk.Frame(parking_frame)
right_frame.grid(row=0, column=2, padx=20)

right_buttons = []
for i in range(6):
    button = tk.Button(right_frame, text=f"R{i + 1}", width=10, height=2, bg="green")
    button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
    right_buttons.append(button)

# Inicializar la visualización
update_parking_display()

# Ejecutar la aplicación
root.mainloop()
