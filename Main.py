import pymysql.cursors
from datetime import datetime
from DB import DatabaseConnector
import RPi.GPIO as GPIO  # Import the RPi.GPIO module
import time  # Import the time module
import gpiod
from gpiozero import Button


class MachineStatusApp2:
    def __init__(self, master, temp):
        # Initialize
        self.master = master
        self.temp = temp
        self.db = None
        # GPIO.setmode(GPIO.BCM)  # Use BCM numbering
        # GPIO.setwarnings(False)
        # chip = gpiod.Chip('gpiochip4')

    def setup_gpio(self, button_pin, time, status, machine_id):
        # button_line = chip.get_line(button_pin)
        # button_line.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)
        # self.button_pin = button_pin

        # self.button_pin = 17  # GPIO pin number for the button
        # GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the button pin as input with pull-up resistor
        # GPIO.setup(button_pin, GPIO.IN)  # Set up the button pin as input
        # GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=self.machine_callback, bouncetime=300)  # Add event detection
        # button_state = button_line.get_value()

        # if btn.is_pressed and self.temp == 0:
        #     print("Button pressed")
        #     self.start_run(time, status, machine_id)
        #     self.temp = 1
        # elif button_state == 0 and self.temp == 1:
        #     print("Button released")
        #     self.stop_run(time, status, machine_id)
        #     self.temp = 0
        btn = Button(button_pin)
        if btn.when_pressed:
            print("Button pressed")
        if btn.when_released:
            print("Button Released")

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

    if app.is_connected():
        try:
            while True:
                print('Connected')
                app.setup_gpio(21, datetime.now(), 'Green', 1)
                app.setup_gpio(22, datetime.now(), 'Green', 2)
        except KeyboardInterrupt:
            # print('Diconnected')
            GPIO.cleanup()
            # button_line.release()

