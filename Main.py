import pymysql.cursors
from datetime import datetime
from DB import DatabaseConnector
import time
import tkinter as tk
from tkinter import scrolledtext
from gpiozero import Button
from gpiozero.exc import GPIOPinInUse
from threading import Thread
import numpy as np

# --- Theme Colors ---
BG_MAIN = "#181818"        # Deep blackish background
BG_FRAME = "#232323"       # Dark grey for frames
BG_INDICATOR = "#333333"   # Slightly lighter grey for indicators
FG_TEXT = "#E0E0E0"        # Light grey for text
FG_LABEL = "#B0B0B0"       # Soft grey for labels
GREEN_ON = "#43FF43"       # Neon green for ON
RED_ON = "#FF4242"         # Bright red for alarms
BRIGHT_BLUE = "#1EC8FF"    # Bright blue for canvas border/accent
GREY_OFF = "#5A5A5A"       # Medium grey for OFF
WHITE = "#FFFFFF"

class MachineStatusApp2:
    def __init__(self, root):
        self.temp = 0
        self.db = None
        self.gui = None
        self.rodi_power_on_temp = 0
        self.rodi_siren_temp = 0
        self.rodi_revolving_light_temp = 0
        self.lift_power_on_temp = 0
        self.lift_siren_temp = 0
        self.lift_revolving_light_temp = 0
        self.connected = False

        self.time_last = 0
        self.timer_on = False

        self.alarm_power_rodi = False
        self.alarm_rodi = False
        self.alarm_power_lift = False
        self.alarm_lift = False


        self.last_rodi_power_on = None
        self.last_rodi_siren = None
        self.last_rodi_revolving_light = None
        self.last_lift_power_on = None
        self.last_lift_siren = None
        self.last_lift_revolving_light = None

        self.input_signal = {
            4: False,
            27: False,
            21: False,
            13: False,
            26: False,
            23: False
        }
        self.input_temp_signal = {
            4: tk.BooleanVar(),
            27: tk.BooleanVar(),
            21: tk.BooleanVar(),
            13: tk.BooleanVar(),
            26: tk.BooleanVar(),
            23: tk.BooleanVar()
        }
        self.tk_Connection_status = tk.StringVar()

        self.thread = Thread(target=self.RunMain)
        self.thread.daemon = True
        self.thread.start()

        self.root = root
        self.root.configure(bg=BG_MAIN)
        self.root.title("Connection Status GUI")

        # Connection Status
        self.connection_status_label = tk.Label(root, text="Connection Status:", font=("Arial", 12), bg=BG_MAIN, fg=FG_LABEL)
        self.connection_status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.connection_status_value = tk.Label(root, text="Disconnected", font=("Arial", 12), bg=BG_MAIN, fg=RED_ON)
        self.connection_status_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Log Section
        self.log_label = tk.Label(root, text="Log:", font=("Arial", 12), bg=BG_MAIN, fg=FG_LABEL)
        self.log_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.log_text = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 10), bg=BG_FRAME, fg=FG_TEXT, insertbackground=WHITE, borderwidth=2, highlightbackground=BRIGHT_BLUE, highlightcolor=BRIGHT_BLUE)
        self.log_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Machine Status Frames
        self.machine_status_frame = tk.Frame(root, bg=BG_MAIN)
        self.machine_status_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # RODI Status Interface
        self.rodi_status_frame = tk.LabelFrame(self.machine_status_frame, text="RODI Machine Status", font=("Arial", 12),
                                               bg=BG_MAIN, fg=FG_LABEL, bd=2, relief=tk.GROOVE, highlightbackground=BG_MAIN, highlightcolor=BG_MAIN, highlightthickness=2)
        self.rodi_status_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.rodi_power_indicator = tk.Canvas(self.rodi_status_frame, width=30, height=30, bg=BG_MAIN, highlightthickness=2, highlightbackground=BG_MAIN)
        self.rodi_power_indicator.grid(row=0, column=0, padx=5)
        self.rodi_power_circle = self.rodi_power_indicator.create_oval(5, 5, 25, 25, fill=GREY_OFF, outline=GREY_OFF, width=2)
        tk.Label(self.rodi_status_frame, text="Power Supply", font=("Arial", 10), bg=BG_MAIN, fg=FG_LABEL).grid(row=0, column=1, padx=5)
        self.rodi_alarm_indicator = tk.Canvas(self.rodi_status_frame, width=30, height=30, bg=BG_MAIN, highlightthickness=2, highlightbackground=BG_MAIN)
        self.rodi_alarm_indicator.grid(row=0, column=2, padx=5)
        self.rodi_alarm_circle = self.rodi_alarm_indicator.create_oval(5, 5, 25, 25, fill=GREY_OFF, outline=GREY_OFF, width=2)
        tk.Label(self.rodi_status_frame, text="Alarm", font=("Arial", 10), bg=BG_MAIN, fg=FG_LABEL).grid(row=0, column=3, padx=5)

        # Lifting Tank Status Interface
        self.lift_status_frame = tk.LabelFrame(self.machine_status_frame, text="Lifting Tank Machine Status", font=("Arial", 12),
                                               bg=BG_MAIN, fg=FG_LABEL, bd=2, relief=tk.GROOVE, highlightbackground=BG_MAIN, highlightcolor=BG_MAIN, highlightthickness=2)
        self.lift_status_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.lift_power_indicator = tk.Canvas(self.lift_status_frame, width=30, height=30, bg=BG_MAIN, highlightthickness=2, highlightbackground=BG_MAIN)
        self.lift_power_indicator.grid(row=0, column=0, padx=5)
        self.lift_power_circle = self.lift_power_indicator.create_oval(5, 5, 25, 25, fill=GREY_OFF, outline=GREY_OFF, width=2)
        tk.Label(self.lift_status_frame, text="Power Supply", font=("Arial", 10), bg=BG_MAIN, fg=FG_LABEL).grid(row=0, column=1, padx=5)
        self.lift_alarm_indicator = tk.Canvas(self.lift_status_frame, width=30, height=30, bg=BG_MAIN, highlightthickness=2, highlightbackground=BG_MAIN)
        self.lift_alarm_indicator.grid(row=0, column=2, padx=5)
        self.lift_alarm_circle = self.lift_alarm_indicator.create_oval(5, 5, 25, 25, fill=GREY_OFF, outline=GREY_OFF, width=2)
        tk.Label(self.lift_status_frame, text="Alarm", font=("Arial", 10), bg=BG_MAIN, fg=FG_LABEL).grid(row=0, column=3, padx=5)

        # GPIO Status Section
        self.gpio_status_label = tk.Label(root, text="GPIO Status:", font=("Arial", 12), bg=BG_MAIN, fg=FG_LABEL)
        self.gpio_status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Canvas for GPIO Status Circles
        self.gpio_canvas = tk.Canvas(root, width=400, height=200, bg=BG_FRAME, highlightthickness=3, highlightbackground=BRIGHT_BLUE)
        self.gpio_canvas.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.gpio_circles = {}
        self.create_gpio_circle("RODI : Power ON", 4, 250, 10)
        self.create_gpio_circle("RODI : Alarm-Siren",27, 250,27)
        self.create_gpio_circle("RODI : Alarm-Revolving Light",21, 250, 44)
        self.create_gpio_circle("Lifting Tank : Power ON",13, 250, 61)
        self.create_gpio_circle("Lifting Tank : Alarm-Siren",26, 250, 78)
        self.create_gpio_circle("Lifting Tank : Alarm-Revolving Light",23, 250, 95)

        # For Alarm Blinking
        self.alarm_blink_state = {"rodi": False, "lift": False}
        self.blink_interval = 500  # ms

    def setup_gpio(self, input_pin, temp, last_active_time, machine_id):
        try:
            if not self.input_signal[input_pin]:
                self.input_signal[input_pin] = Button(input_pin)

            current_time = time.time()

            if self.input_signal[input_pin].is_active and temp == 0:
                if last_active_time is None:
                    last_active_time = current_time
                elif current_time - last_active_time >= 1:
                    self.start_run(datetime.now(), input_pin, machine_id)
                    temp = 1
                    self.input_temp_signal[input_pin].set(temp)
                    self.update_gpio_status(input_pin, temp)
            elif not self.input_signal[input_pin].is_active and temp == 1:
                self.stop_run(datetime.now(), input_pin , machine_id)
                temp = 0
                self.input_temp_signal[input_pin].set(temp)
                self.update_gpio_status(input_pin, temp)
                last_active_time = None
        except GPIOPinInUse:
            print(f"GPIO pin {input_pin} is already in use. Skipping...")
        return temp, last_active_time
    
    def start_run(self, start_time, signal_id, machine_id):
        self.db.log_insert_to_db(start_time, signal_id, machine_id)
        self.db.status_update_to_db(signal_id, 1 ,machine_id)

    def stop_run(self, stop_time, signal_id, machine_id):
        id = self.db.get_last_created_id(signal_id, machine_id)
        self.db.log_update_to_db(id,stop_time, signal_id, machine_id)
        self.db.status_update_to_db(signal_id, 0 , machine_id)

    def connect(self):
        ip_addresses = ['172.20.10.2', '172.17.0.1','10.154.245.1']
        for ip in ip_addresses:
            try:
                print(f"Attempting to connect to database at {ip}...")
                self.add_log_entry(f"Attempting to connect to database at {ip}...")
                self.db = DatabaseConnector(ip, 'root', 'IOtSt4ckToorMariaDb', 'sensor_data')
                self.db.connect()
                if self.db.check_is_connected():
                    print(f"Successfully connected to database at {ip}")
                    self.add_log_entry(f"Successfully connected to database at {ip}")
                    return self.db.connection
            except Exception as e:
                print(f"Failed to connect to database at {ip}: {e}")
                self.add_log_entry(f"Failed to connect to database at {ip}: {e}")
        print("All connection attempts failed.")
        return None

    def is_connected(self):
        if self.db and self.db.check_is_connected():
            return True
        else:
            return False

    def dis(self):
        if self.db:
            self.db.disconnect()

    def create_gpio_circle(self, name, pin, x, y):
        # Use blue outline for all circles
        circle = self.gpio_canvas.create_oval(x, y, x + 14, y + 14, fill=GREY_OFF, outline=GREY_OFF, width=2)
        self.gpio_circles[pin] = circle
        self.gpio_canvas.create_text(20, y + 7, text=f"{name}", font=("Arial", 10), anchor="w", fill=FG_LABEL)
        self.gpio_canvas.create_text(x + 30, y + 7, text=f"| Pin: {pin}", font=("Arial", 10), anchor="w", fill=FG_LABEL)

    def update_gpio_status(self, pin, status):
        # Power pins: green when ON, grey when OFF. Alarm pins: bright blue when ON, grey when OFF.
        power_pins = [4, 13]
        alarm_pins = [27, 21, 26, 23]
        if pin in power_pins:
            color = GREEN_ON if status else GREY_OFF
        else:
            color = GREEN_ON if status else GREY_OFF
        self.gpio_canvas.itemconfig(self.gpio_circles[pin], fill=color,outline=color)
        # self.add_log_entry(f"Pin {pin} : {status}")

    def update_connection_status(self, status):
        self.tk_Connection_status.set(status)
        fg_color = GREEN_ON if status == "Connected" else RED_ON
        self.connection_status_value.config(text=status, fg=fg_color)

    def add_log_entry(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def Timer(self, trigger, timer_time):    
        if trigger:
            if not self.timer_on:               
                self.time_last = time.time() + timer_time
                self.timer_on = True
            else:
                time_elapsed = int(self.time_last - time.time())
                if time.time() >= self.time_last:
                    self.timer_on = False
                    return True
            return False
        else:
            return False

    def update_machine_status(self):
        if self.rodi_power_on_temp == 0 :
            self.rodi_power_indicator.itemconfig(self.rodi_power_circle, fill=RED_ON , outline=RED_ON)   
            if not self.alarm_power_rodi:
                self.add_log_entry(f"RODI NO POWER!")
                self.alarm_power_rodi = True
        elif self.rodi_power_on_temp == 1 :
            if self.alarm_power_rodi:
                self.rodi_power_indicator.itemconfig(self.rodi_power_circle, fill=GREEN_ON, outline=GREEN_ON)      
                self.add_log_entry(f"RODI POWER RESTORED!")
                self.alarm_power_rodi = False

        if (self.rodi_siren_temp == 1 or self.rodi_revolving_light_temp == 1) and not self.alarm_rodi:
            self.rodi_alarm_indicator.itemconfig(self.rodi_alarm_circle, fill=RED_ON  ,outline=RED_ON )  
            self.add_log_entry(f"RODI ALARM ACTIVE!")
            self.alarm_rodi = True
        elif (self.rodi_siren_temp == 0 and self.rodi_revolving_light_temp == 0) and self.alarm_rodi:
            self.rodi_alarm_indicator.itemconfig(self.rodi_alarm_circle, fill=GREY_OFF,outline=GREY_OFF)  
            self.add_log_entry(f"RODI ALARM CLEARED!")
            self.alarm_rodi = False
        
        if self.lift_power_on_temp == 0 :
            self.lift_power_indicator.itemconfig(self.lift_power_circle, fill=RED_ON , outline=RED_ON)   
            if not self.alarm_power_lift:
                self.add_log_entry(f"LIFTING TANK NO POWER!")
                self.alarm_power_lift = True
        elif self.lift_power_on_temp == 1 :
            if self.alarm_power_lift:
                self.lift_power_indicator.itemconfig(self.lift_power_circle, fill=GREEN_ON, outline=GREEN_ON)      
                self.add_log_entry(f"LIFTING TANK POWER RESTORED!")
                self.alarm_power_lift = False

        if (self.lift_siren_temp == 1 or self.lift_revolving_light_temp == 1) and not self.alarm_lift:
            self.lift_alarm_indicator.itemconfig(self.lift_alarm_circle, fill=RED_ON  ,outline=RED_ON )  
            self.add_log_entry(f"LIFTING TANK ALARM ACTIVE!")
            self.alarm_lift = True
        elif (self.lift_siren_temp == 0 and self.lift_revolving_light_temp == 0) and self.alarm_lift:
            self.lift_alarm_indicator.itemconfig(self.lift_alarm_circle, fill=GREY_OFF,outline=GREY_OFF)  
            self.add_log_entry(f"LIFTING TANK ALARM CLEARED!")
            self.alarm_lift = False

    def RunMain(self):
        last_active_times = {4: None, 27: None, 21: None, 13: None, 26: None, 23: None}
        try:
            while True:
                if self.connected:
                    if self.Timer(True, 9):
                        if self.is_connected():
                            self.update_connection_status("Connected")
                        else:
                            self.update_connection_status("Disconnected")
                            self.add_log_entry("Database disconnected. Retrying connection...")
                            self.connected = False

                    self.rodi_power_on_temp, last_active_times[4] = self.setup_gpio(
                        4, self.rodi_power_on_temp, last_active_times[4], 1
                    )
                    self.rodi_siren_temp, last_active_times[27] = self.setup_gpio(
                        27, self.rodi_siren_temp, last_active_times[27], 1
                    )
                    self.rodi_revolving_light_temp, last_active_times[21] = self.setup_gpio(
                        21, self.rodi_revolving_light_temp, last_active_times[21], 1
                    )
                    self.lift_power_on_temp, last_active_times[13] = self.setup_gpio(
                        13, self.lift_power_on_temp, last_active_times[13], 2
                    )
                    self.lift_siren_temp, last_active_times[26] = self.setup_gpio(
                        26, self.lift_siren_temp, last_active_times[26], 2
                    )
                    self.lift_revolving_light_temp, last_active_times[23] = self.setup_gpio(
                        23, self.lift_revolving_light_temp, last_active_times[23], 2
                    )

                    self.update_machine_status()
                   
                else:
                    self.update_connection_status("Disconnected")
                    self.add_log_entry("Not connected to the database. Waiting for connection...")
                    if self.connect():
                        self.update_connection_status("Connected")
                        self.add_log_entry("Database connection established.")                                                   
                        self.stop_run(datetime.now(), 4, 1)
                        self.stop_run(datetime.now(), 27, 1)
                        self.stop_run(datetime.now(), 21, 1)
                        self.stop_run(datetime.now(), 13, 2)
                        self.stop_run(datetime.now(), 26, 2)
                        self.stop_run(datetime.now(), 23, 2)
                        self.connected = True
                    else:
                        print("Failed to connect to the database. Retrying in 10 seconds...")
                        self.update_connection_status("Disconnected")
                        self.add_log_entry("Failed to connect to the database. Retrying in 10 seconds...")
                        time.sleep(5)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
            self.add_log_entry("Program interrupted by user. Exiting...")
            self.dis()
            self.update_connection_status("Disconnected")
            self.add_log_entry("Database disconnected.")

root = tk.Tk()
app = MachineStatusApp2(root)
root.mainloop()