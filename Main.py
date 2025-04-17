import pymysql.cursors
from datetime import datetime
from DB import DatabaseConnector
import time  # Import the time module

from gpiozero import Button


class MachineStatusApp2:
    def __init__(self, master, temp):
        # Initialize
        self.master = master
        self.temp = 0
        self.db = None

    def setup_gpio(self, button_pin,temp, time, status, machine_id):
    # def setup_gpio(self, button_pin, temp):
        btn = Button(button_pin)
        if btn.is_pressed and temp == 0:
            print(f"Button on pin {button_pin} is pressed")     
            self.start_run(time, status, machine_id)
            temp = 1
        elif not btn.is_pressed and temp == 1:
            print(f"Button on pin {button_pin} is not pressed")
            self.stop_run(time, status, machine_id)
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

    app = MachineStatusApp2(None, None)
    app.connect()
    # app.dis()
    rodi_green_temp = 0
    rodi_yellow_temp = 0
    rodi_red_temp = 0
    lift_green_temp = 0
    lift_yellow_temp = 0
    lift_red_temp = 0

    if app.is_connected():
        try:
            while True:
                # Check the machine state and update the temp variable accordingly
                #RODI Tank
                rodi_green_temp=  app.setup_gpio(4,rodi_green_temp, datetime.now(), 'Green', 1)
                rodi_yellow_temp =  app.setup_gpio(27, rodi_yellow_temp, datetime.now(), 'Yellow', 1)
                rodi_red_temp =  app.setup_gpio(21, rodi_red_temp, datetime.now(), 'Red', 1)
                #Lifting Tank
                lift_green_temp= app.setup_gpio(13, lift_green_temp, datetime.now(), 'Green', 2)
                lift_yellow_temp = app.setup_gpio(26, lift_yellow_temp, datetime.now(), 'Yellow', 2)
                lift_red_temp = app.setup_gpio(23, lift_red_temp, datetime.now(), 'Yellow', 2)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
