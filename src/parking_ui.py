import tkinter as tk
from tkinter import messagebox
import time
from parking_agent import ParkingAgent  # Asegúrate de importar correctamente ParkingAgent

# Dimensiones de la ventana y vehículos
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
VEHICLE_WIDTH = 80
VEHICLE_HEIGHT = 50
wheel_width = 12
wheel_height = 12
window_width = 10
window_height = 10

# Crear una instancia de ParkingAgent (asumiendo que tienes 16 espacios)
agent = ParkingAgent(total_spaces=16)

class ParkingLot:
    def __init__(self, total_spaces):
        self.update_total_spaces(total_spaces)

    def update_total_spaces(self, total_spaces):
        self.spaces = [0] * total_spaces
        self.space_types = ['pequeño'] * (total_spaces // 3) + \
                           ['mediano'] * (total_spaces // 3) + \
                           ['grande'] * (total_spaces - 2 * (total_spaces // 3))

    def park_vehicle(self, vehicle_id, space, vehicle_type):
        if self.spaces[space] == 0 and agent.is_space_compatible(self.space_types[space], vehicle_type):
            self.spaces[space] = vehicle_id
            return space
        return -1


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


# Función para manejar el estacionamiento con el agente inteligente
def update_parking_display():
    for i, (rect, text) in enumerate(parking_buttons):
        if i < len(parking_lot.spaces) and parking_lot.spaces[i] != 0:
            canvas.itemconfig(rect, fill="red")
            canvas.itemconfig(text, text=f"Vehículo {parking_lot.spaces[i]}")
        else:
            space_type = parking_lot.space_types[i]
            color = "lightgreen" if space_type == "pequeño" else "lightblue" if space_type == "mediano" else "orange"
            canvas.itemconfig(rect, fill=color)
            canvas.itemconfig(text, text=f"S{i + 1}")


# Función para redimensionar el lienzo al tamaño de la ventana
def resize_canvas(event):
    canvas.config(width=event.width, height=event.height)
    update_parking_display()


# Función para cambiar el número de espacios de estacionamiento
def change_total_spaces():
    try:
        new_total = int(total_spaces_entry.get())
        if new_total < 1:
            messagebox.showerror("Error", "El número de espacios debe ser mayor que 0.")
            return
        recreate_parking_spaces(new_total)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido.")


# Crear el lienzo principal
def recreate_parking_spaces(new_total):
    global parking_coordinates, parking_buttons

    parking_lot.update_total_spaces(new_total)
    canvas.delete("all")
    parking_coordinates = {}
    parking_buttons = []

    for i in range(new_total):
        if i < new_total // 3:
            x = 50 + (i % 2) * (VEHICLE_WIDTH + 40)
            y = 50 + (i // 2) * (VEHICLE_HEIGHT + 40)
            color = "lightgreen"  # Pequeño
        elif i < 2 * (new_total // 3):
            x = 300 + ((i - new_total // 3) % 2) * (VEHICLE_WIDTH + 40)
            y = 50 + ((i - new_total // 3) // 2) * (VEHICLE_HEIGHT + 40)
            color = "lightblue"  # Mediano
        else:
            x = 600 + ((i - 2 * (new_total // 3)) % 2) * (VEHICLE_WIDTH + 40)
            y = 50 + ((i - 2 * (new_total // 3)) // 2) * (VEHICLE_HEIGHT + 40)
            color = "orange"  # Grande

        rect = canvas.create_rectangle(x, y, x + VEHICLE_WIDTH, y + VEHICLE_HEIGHT, fill=color, tags=f"space{i}")
        text = canvas.create_text(x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2, text=f"S{i + 1}", tags=f"text{i}")
        parking_coordinates[i] = (x + VEHICLE_WIDTH // 2, y + VEHICLE_HEIGHT // 2)
        parking_buttons.append((rect, text))

    update_parking_display()


# Función para manejar el estacionamiento con el agente inteligente
def park_vehicles():
    try:
        num_vehicles = int(vehicle_entry.get())
        vehicle_type = vehicle_type_var.get()

        if num_vehicles <= 0:
            messagebox.showerror("Error", "Por favor, ingresa un número mayor a 0.")
            return

        if num_vehicles > len(parking_lot.spaces):
            messagebox.showerror("Error", f"El número máximo de vehículos es {len(parking_lot.spaces)}.")
            return

        spaces_occupied = 0
        for vehicle_id in range(1, num_vehicles + 1):
            state = parking_lot.spaces
            action = agent.choose_action(state, parking_lot.space_types, vehicle_type)  # Ahora pasa los 3 parámetros

            space = parking_lot.park_vehicle(vehicle_id, action, vehicle_type)
            if space != -1:
                animate_parking(vehicle_id, space)
                spaces_occupied += 1

        update_parking_display()

        if spaces_occupied > 0:
            messagebox.showinfo("Éxito", f"{spaces_occupied} vehículo(s) estacionado(s).")
        else:
            messagebox.showinfo("Lleno", "No hay espacio disponible para estacionar.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido.")


# Crear la ventana principal
root = tk.Tk()
root.title("Simulador de Estacionamiento")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Variables globales
TOTAL_SPACES = 16
parking_lot = ParkingLot(TOTAL_SPACES)
parking_coordinates = {}
parking_buttons = []

# Entrada para tipo de vehículo
vehicle_type_label = tk.Label(root, text="Tipo de vehículo:")
vehicle_type_label.pack()
vehicle_type_var = tk.StringVar(value="pequeño")
vehicle_type_menu = tk.OptionMenu(root, vehicle_type_var, "pequeño", "mediano", "grande")
vehicle_type_menu.pack(pady=5)

# Entrada para el número de vehículos
vehicle_label = tk.Label(root, text="Número de vehículos a estacionar:")
vehicle_label.pack()
vehicle_entry = tk.Entry(root)
vehicle_entry.pack(pady=5)

# Botón para iniciar el estacionamiento
park_button = tk.Button(root, text="Estacionar", command=lambda: park_vehicles())
park_button.pack(pady=10)

# Entrada para modificar el total de espacios
total_spaces_label = tk.Label(root, text="Total de espacios:")
total_spaces_label.pack()
total_spaces_entry = tk.Entry(root)
total_spaces_entry.insert(0, str(TOTAL_SPACES))
total_spaces_entry.pack(pady=5)
update_spaces_button = tk.Button(root, text="Actualizar espacios", command=lambda: change_total_spaces())
update_spaces_button.pack(pady=5)

# Crear el lienzo principal
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

recreate_parking_spaces(TOTAL_SPACES)
root.mainloop()
