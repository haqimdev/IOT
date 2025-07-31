import pymysql.cursors
from datetime import datetime
from DB import DatabaseConnector
from GUI import ConnectionStatusGUI
import time  # Import the time module

from gpiozero import Button

import tkinter as tk
from tkinter import scrolledtext

class MachineStatusApp2:
    def __init__(self, master, temp):
        # Initialize
        self.master = master
        self.temp = 0
        self.db = None

    def setup_gpio(self, button_pin,temp, time, machine_id):
    # def setup_gpio(self, button_pin, temp):
        btn = Button(button_pin)
        if btn.is_pressed and temp == 0:
            print(f"Button on pin {button_pin} is pressed")     
            self.start_run(time, 1, machine_id)
            temp = 1
        elif not btn.is_pressed and temp == 1:
            print(f"Button on pin {button_pin} is not pressed")
            self.stop_run(time, 0, machine_id)
            temp = 0
        return temp
        

    def connect(self):
        self.db = DatabaseConnector('172.20.10.2', 'root', 'IOtSt4ckToorMariaDb', 'sensor_data')
        self.db.connect()
        return self.db.connection

    def start_run(self, start_time, status, machine_id):
        # Get the current time
        # start_time = datetime.now()
        # status = "Green"
        # machine_id = 1
        self.db.save_to_database(start_time, status, machine_id)

    def stop_run(self, stop_time, status, machine_id):
        # Get the current time
        # stop_time = datetime.now()
        # status = "Green"
        # machine_id = 1
        id = self.db.get_last_created_id(machine_id)
        print(f"The last created ID for machine_id {machine_id} is: {id}")
        self.db.update_to_database(stop_time, status, machine_id, id)

    def is_connected(self):
        if self.db.check_is_connected():
            print('Database Is Connected')
            return True
        else:
            print('Database Is NOT Connected')
            return False

    def dis(self):
        self.db.disconnect()

    


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    gui = ConnectionStatusGUI(root)

    app = MachineStatusApp2(None, None)
    if app.connect():
        gui.update_connection_status("Connected")
        gui.add_log_entry("Database connection established.")
    else:
        gui.update_connection_status("Disconnected")
        gui.add_log_entry("Failed to connect to the database.")

    rodi_power_on_temp = 0
    rodi_siren_temp = 0
    rodi_revolving_light_temp = 0
    lift_power_on_temp = 0
    lift_siren_temp = 0
    lift_revolving_light_temp = 0

    if app.is_connected():
        try:
            # while True:
            # Check GPIO pins and update GUI
            rodi_power_on_temp = app.setup_gpio(4, rodi_power_on_temp, datetime.now(), 1)
            gui.update_gpio_status(4, rodi_power_on_temp)

            rodi_siren_temp = app.setup_gpio(27, rodi_siren_temp, datetime.now(), 1)
            gui.update_gpio_status(27, rodi_siren_temp)

            rodi_revolving_light_temp = app.setup_gpio(21, rodi_revolving_light_temp, datetime.now(), 1)
            gui.update_gpio_status(21, rodi_revolving_light_temp)

            lift_power_on_temp = app.setup_gpio(13, lift_power_on_temp, datetime.now(), 2)
            gui.update_gpio_status(13, lift_power_on_temp)

            lift_siren_temp = app.setup_gpio(26, lift_siren_temp, datetime.now(), 2)
            gui.update_gpio_status(26, lift_siren_temp)
# 
            lift_revolving_light_temp = app.setup_gpio(23, lift_revolving_light_temp, datetime.now(), 2)
            gui.update_gpio_status(23, lift_revolving_light_temp)

            time.sleep(1)  # Add a delay to avoid excessive CPU usage
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
            gui.add_log_entry("Program interrupted by user. Exiting...")
            app.dis()
            gui.update_connection_status("Disconnected")
            gui.add_log_entry("Database disconnected.")
    else:
        gui.add_log_entry("Database is not connected.")

    root.mainloop()
