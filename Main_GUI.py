from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter import ttk
# from tkcalendar import DateEntry
import pymysql.cursors
from datetime import datetime
from DB import DatabaseConnector
# import RPi.GPIO as GPIO  # Import the RPi.GPIO module
import time  # Import the time module
        
class MachineStatusApp:
    def __init__(self, master):
        # Initialize 
        self.master = master
        master.title("Machine Status Tracker")
        master.geometry("400x400")  # Set the window size to 400x400 pixels
        
        # Initialize your GUI components here
        # ...
        self.db_host_label = Label(master, text="Database Host:")
        self.db_host_label.pack()
        
        self.db_host = StringVar()
        self.db_host_entry = Entry(master, textvariable=self.db_host)
        self.db_host_entry.pack()
        
        self.db_user_label = Label(master, text="Database User:")
        self.db_user_label.pack()
        
        self.db_user = StringVar()
        self.db_user_entry = Entry(master, textvariable=self.db_user)
        self.db_user_entry.pack()
        
        self.db_password_label = Label(master, text="Database Password:")
        self.db_password_label.pack()
        
        self.db_password = StringVar()
        self.db_password_entry = Entry(master, textvariable=self.db_password, show = '*')
        self.db_password_entry.pack()
        
        self.db_name_label = Label(master, text="Database Name:")
        self.db_name_label.pack()
        
        self.db_name = StringVar()
        self.db_name_entry = Entry(master, textvariable=self.db_name)
        self.db_name_entry.pack()
             
        self.connect_button = Button(master, text="Connect", command=self.connect,  foreground="#ff0000",
                   activeforeground="#FFA500")
        # self.connect_button.place(x=250, y=50)
        self.connect_button.pack()
 
        self.check_button = Button(master, text="Check Connection", command= self.is_connected,  foreground="#ff0000",
                   activeforeground="#FFA500")
        # self.connect_button.place(x=250, y=50)
        self.check_button.pack()       
        
        ##machine run and stop simulation
        self.rodi_run_button = Button(master, text="RODI Running", command=lambda : self.start_run(datetime.now(), 'Green', 1), foreground="#ff0000",
            activeforeground="#FFA500")
        # self.submit_button.place(x=50, y=50)
        self.rodi_run_button.pack()
        
        self.rodi_stop_button = Button(master, text="RODI Stopped", command=lambda : self.stop_run(datetime.now(), 'Green', 1), foreground="#ff0000",
            activeforeground="#FFA500")
        # self.submit_button.place(x=50, y=50)
        self.rodi_stop_button.pack()
        
        ##machine run and stop simulation
        self.lift_run_button = Button(master, text="Lift Tank Running", command=lambda : self.start_run(datetime.now(), 'Green', 2), foreground="#ff0000",
            activeforeground="#FFA500")
        # self.submit_button.place(x=50, y=50)
        self.lift_run_button.pack()
        
        self.lift_stop_button = Button(master, text="Lift Tank Stopped", command=lambda : self.stop_run(datetime.now(), 'Green', 2), foreground="#ff0000",
            activeforeground="#FFA500")
        # self.submit_button.place(x=50, y=50)
        self.lift_stop_button.pack()
        
        
    def connect(self):
        host = self.db_host.get()
        user = self.db_user.get()
        password = self.db_password.get()
        database = self.db_name.get()
        self.db = DatabaseConnector(host, user, password, database)
        try:
            self.db.connect()
            return self.db.connection

        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False
        
        
    def start_run(self, start_time, status, machine_id):
        self.db.save_to_database(start_time, status, machine_id)
        
    def stop_run(self, stop_time, status, machine_id):
        id  = self.db.get_last_created_id(machine_id)
        print(f"The last created ID for machine_id {machine_id} is: {id}")
        self.db.update_to_database(stop_time, status, machine_id, id)
    
    def is_connected(self):
        try:
            if self.db.check_is_connected():
                print('Database Is Connected')
            else:
                print('Database Is NOT Connected')
        except:
            print('Database Is NOT Connected')
        

# Example usage
if __name__ == "__main__":
    root = Tk()
    app = MachineStatusApp(root)
    root.mainloop()
