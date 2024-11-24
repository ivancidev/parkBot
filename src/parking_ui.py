from parking_lot import ParkingLot
from training import load_model 
import tkinter as tk
from tkinter import messagebox
import time

TOTAL_SPACES = 16
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
VEHICLE_WIDTH = 50
VEHICLE_HEIGHT = 30
wheel_width = 12  
wheel_height = 12
window_width = 10
window_height = 10  
agent = load_model("parking_agent.pkl")  # Cambia la ruta si guardaste el modelo en otro lugar


root = tk.Tk()
root.title("Simulador de Estacionamiento")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

parking_lot = ParkingLot(TOTAL_SPACES)

# Entrada para tipo de vehículo
vehicle_type_label = tk.Label(root, text="Tipo de vehículo:")
vehicle_type_label.pack()
vehicle_type_var = tk.StringVar(value="pequeño")
vehicle_type_menu = tk.OptionMenu(root, vehicle_type_var, "pequeño", "mediano", "grande")
vehicle_type_menu.pack(pady=5)

# Título
title_label = tk.Label(root, text="Simulador de Estacionamiento", font=("Arial", 16))
title_label.pack(pady=10)

# Entrada para el número de vehículos
vehicle_label = tk.Label(root, text="Número de vehículos a estacionar:")
vehicle_label.pack()
vehicle_entry = tk.Entry(root)
vehicle_entry.pack(pady=5)

# Botón para iniciar el estacionamiento
park_button = tk.Button(root, text="Estacionar", command=lambda: park_vehicles())
park_button.pack(pady=10)

# Crear un lienzo principal
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
canvas.pack()

# Crear las coordenadas de los espacios y dibujar los botones
parking_coordinates = {}
parking_buttons = []

for i in range(6):
    x = 50 + (i % 2) * (VEHICLE_WIDTH + 20)
    y = 50 + (i // 2) * (VEHICLE_HEIGHT + 20)
    rect = canvas.create_rectangle(x, y, x + VEHICLE_WIDTH, y + VEHICLE_HEIGHT, fill="green", tags=f"space{i}")
    text = canvas.create_text(x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2, text=f"L{i + 1}", tags=f"text{i}")
    parking_coordinates[i] = (x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2)
    parking_buttons.append((rect, text))

for i in range(6, TOTAL_SPACES):
    x = 300 + ((i - 6) % 2) * (VEHICLE_WIDTH + 20)
    y = 50 + ((i - 6) // 2) * (VEHICLE_HEIGHT + 20)
    rect = canvas.create_rectangle(x, y, x + VEHICLE_WIDTH, y + VEHICLE_HEIGHT, fill="green", tags=f"space{i}")
    text = canvas.create_text(x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2, text=f"R{i - 5}", tags=f"text{i}")
    parking_coordinates[i] = (x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2)
    parking_buttons.append((rect, text))


# Función para manejar el estacionamiento con animación
def update_parking_display():
    for i, (rect, text) in enumerate(parking_buttons):
        if parking_lot.spaces[i] != 0:
            canvas.itemconfig(rect, fill="red")
            canvas.itemconfig(text, text=f"Vehículo {parking_lot.spaces[i]}")
        else:
            canvas.itemconfig(rect, fill="green")
            canvas.itemconfig(text, text=f"L{i + 1}" if i < 6 else f"R{i - 5}")


# Función para manejar el estacionamiento con el agente inteligente
def park_vehicles():
    try:
        num_vehicles = int(vehicle_entry.get())
        vehicle_type = vehicle_type_var.get()  # Tipo seleccionado

        if num_vehicles <= 0:
            messagebox.showerror("Error", "Por favor, ingresa un número mayor a 0.")
            return

        if num_vehicles > TOTAL_SPACES:
            messagebox.showerror("Error", f"El número máximo de vehículos es {TOTAL_SPACES}.")
            return

        spaces_occupied = 0
        for vehicle_id in range(1, num_vehicles + 1):
            state = parking_lot.spaces
            action = agent.choose_action(state)
            
            space = parking_lot.park_vehicle(vehicle_id, action, vehicle_type)
            if space != -1:
                animate_parking(vehicle_id, space)
                reward = 1
                spaces_occupied += 1
            else:
                reward = -1

            next_state = parking_lot.spaces
            agent.update_q_table(action, reward, next_state)

        update_parking_display()

        if spaces_occupied > 0:
            messagebox.showinfo("Éxito", f"{spaces_occupied} vehículo(s) estacionado(s).")
        else:
            messagebox.showinfo("Lleno", "No hay espacio disponible para estacionar.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido.")


# Función de animación para mover los vehículos
def animate_parking(vehicle_id, space, start_position=(0, 300)):
    x_start, y_start = start_position
    x_dest, y_dest = parking_coordinates[space]
    
    car_body = canvas.create_rectangle(x_start, y_start, x_start + VEHICLE_WIDTH, y_start + VEHICLE_HEIGHT, fill="orange")
    front_wheel = canvas.create_oval(x_start + 5, y_start + VEHICLE_HEIGHT - wheel_height / 2, x_start + 5 + wheel_width, y_start + VEHICLE_HEIGHT + wheel_height / 2, fill="black")
    rear_wheel = canvas.create_oval(x_start + VEHICLE_WIDTH - wheel_width - 5, y_start + VEHICLE_HEIGHT - wheel_height / 2, x_start + VEHICLE_WIDTH - 5, y_start + VEHICLE_HEIGHT + wheel_height / 2, fill="black")
    window1 = canvas.create_rectangle(x_start + 10, y_start + 5, x_start + 10 + window_width, y_start + 5 + window_height, fill="lightblue")
    window2 = canvas.create_rectangle(x_start + window_width + 15, y_start + 5, x_start + 2 * window_width + 15, y_start + 5 + window_height, fill="lightblue")
    window3 = canvas.create_rectangle(x_start + 2 * window_width + 20, y_start + 5, x_start + 3 * window_width + 20, y_start + 5 + window_height, fill="lightblue")

    vehicle_parts = [car_body, front_wheel, rear_wheel, window1, window2, window3]
    step = 5

    while x_start < x_dest or y_start > y_dest:
        if x_start < x_dest:
            for part in vehicle_parts:
                canvas.move(part, step, 0)
            x_start += step
        elif y_start > y_dest:
            for part in vehicle_parts:
                canvas.move(part, 0, -step)
            y_start -= step
        root.update()
        time.sleep(0.05)

    for part in vehicle_parts:
        canvas.delete(part)
 

update_parking_display()
root.mainloop()
