import tkinter as tk
from tkinter import scrolledtext

class ConnectionStatusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connection Status GUI")

        # Connection Status
        self.connection_status_label = tk.Label(root, text="Connection Status:", font=("Arial", 12))
        self.connection_status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.connection_status_value = tk.Label(root, text="Disconnected", font=("Arial", 12), fg="red")
        self.connection_status_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Log Section
        self.log_label = tk.Label(root, text="Log:", font=("Arial", 12))
        self.log_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.log_text = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 10))
        self.log_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # GPIO Status Section
        self.gpio_status_label = tk.Label(root, text="GPIO Status:", font=("Arial", 12))
        self.gpio_status_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Canvas for GPIO Status Circles
        self.gpio_canvas = tk.Canvas(root, width=400, height=200)  # Increased width and height
        self.gpio_canvas.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Create circles for each GPIO pin
        self.gpio_circles = {}
        self.create_gpio_circle("RODI : Power ON", 4, 250, 10)
        self.create_gpio_circle("RODI : Alarm-Siren",27, 250,27)
        self.create_gpio_circle("RODI : Alarm-Revolving Light",21, 250, 44)
        self.create_gpio_circle("Lifting Tank : Power ON",13, 250, 61)
        self.create_gpio_circle("Lifting Tank : Alarm-Siren",26, 250, 78)
        self.create_gpio_circle("Lifting Tank : Alarm-Revolving Light",23, 250, 95)


    def create_gpio_circle(self, name, pin, x, y):
        """Create a circle for a GPIO pin with text on the left side, vertically centered."""
        # Create the circle
        circle = self.gpio_canvas.create_oval(x , y, x + 14, y + 14, fill="red", outline="black")
        self.gpio_circles[pin] = circle

        # Place the text to the left of the circle, vertically centered
        self.gpio_canvas.create_text(20 , y + 7, text=f"{name}" , font=("Arial", 10), anchor="w")
        self.gpio_canvas.create_text(x + 30 , y + 7, text=f"| Pin: {pin}", font=("Arial", 10), anchor="w")

    def update_gpio_status(self, pin, status):
        """Update the color of a GPIO pin circle."""
        color = "green" if status else "red"
        self.gpio_canvas.itemconfig(self.gpio_circles[pin], fill=color)

    def update_connection_status(self, status):
        self.connection_status_value.config(text=status, fg="green" if status == "Connected" else "red")

    def add_log_entry(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
