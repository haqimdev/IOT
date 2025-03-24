from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql.cursors
from datetime import datetime

class MachineStatusApp:
    def __init__(self, master):
        self.master = master
        master.title("Machine Status Tracker")
        master.geometry("400x400")  # Set the window size to 400x400 pixels

        self.start_time_label = Label(master, text="Start Date:")
        self.start_time_label.pack()

        self.start_date = StringVar()
        self.start_date_entry = DateEntry(master, textvariable=self.start_date, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack()

        self.start_time_label = Label(master, text="Start Time (HH:MM:SS):")
        self.start_time_label.pack()

        self.start_hour = StringVar()
        self.start_hour_entry = ttk.Combobox(master, textvariable=self.start_hour, values=[f"{i:02d}" for i in range(24)])
        self.start_hour_entry.pack()

        self.start_minute = StringVar()
        self.start_minute_entry = ttk.Combobox(master, textvariable=self.start_minute, values=[f"{i:02d}" for i in range(60)])
        self.start_minute_entry.pack()

        self.start_second = StringVar()
        self.start_second_entry = ttk.Combobox(master, textvariable=self.start_second, values=[f"{i:02d}" for i in range(60)])
        self.start_second_entry.pack()

        self.stop_time_label = Label(master, text="Stop Date:")
        self.stop_time_label.pack()

        self.stop_date = StringVar()
        self.stop_date_entry = DateEntry(master, textvariable=self.stop_date, date_pattern='yyyy-mm-dd')
        self.stop_date_entry.pack()

        self.stop_time_label = Label(master, text="Stop Time (HH:MM:SS):")
        self.stop_time_label.pack()

        self.stop_hour = StringVar()
        self.stop_hour_entry = ttk.Combobox(master, textvariable=self.stop_hour, values=[f"{i:02d}" for i in range(24)])
        self.stop_hour_entry.pack()

        self.stop_minute = StringVar()
        self.stop_minute_entry = ttk.Combobox(master, textvariable=self.stop_minute, values=[f"{i:02d}" for i in range(60)])
        self.stop_minute_entry.pack()

        self.stop_second = StringVar()
        self.stop_second_entry = ttk.Combobox(master, textvariable=self.stop_second, values=[f"{i:02d}" for i in range(60)])
        self.stop_second_entry.pack()

        self.status_label = Label(master, text="Status:")
        self.status_label.pack()

        self.status = StringVar()
        self.status_entry = Entry(master, textvariable=self.status)
        self.status_entry.pack()
        
        self.machine_id_label = Label(master, text="Machine ID:")
        self.machine_id_label.pack()

        self.machine_id = StringVar()
        self.machine_id_entry = Entry(master, textvariable=self.machine_id)
        self.machine_id_entry.pack()

        self.duration_label = Label(master, text="Duration:")
        self.duration_label.pack()

        self.duration = StringVar()
        self.duration_display = Label(master, textvariable=self.duration)
        self.duration_display.pack()

        self.submit_button = Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        start_date = self.start_date.get()
        start_time = f"{self.start_hour.get()}:{self.start_minute.get()}:{self.start_second.get()}"
        stop_date = self.stop_date.get()
        stop_time = f"{self.stop_hour.get()}:{self.stop_minute.get()}:{self.stop_second.get()}"
        status = self.status.get()
        machine_id = self.machine_id.get()

        if not start_date or not start_time or not stop_date or not stop_time or not status or not machine_id:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            start_dt = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M:%S')
            stop_dt = datetime.strptime(f"{stop_date} {stop_time}", '%Y-%m-%d %H:%M:%S')
            duration = stop_dt - start_dt
            self.duration.set(str(duration))

            self.save_to_database(f"{start_date} {start_time}", f"{stop_date} {stop_time}", status, machine_id)
            messagebox.showinfo("Success", "Machine status recorded successfully.")
            self.start_date.set("")
            self.start_hour.set("")
            self.start_minute.set("")
            self.start_second.set("")
            self.stop_date.set("")
            self.stop_hour.set("")
            self.stop_minute.set("")
            self.stop_second.set("")
            self.status.set("")
            self.machine_id.set("")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS.")
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def save_to_database(self, start_time, stop_time, status, machine_id):
        connection = pymysql.connect(
            host='172.17.0.1',
            database='sensor_data',
            user='root',
            password='IOtSt4ckToorMariaDb'
        )
        cursor = connection.cursor()
        query = "INSERT INTO status (start_time, stop_time, status, machine_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (start_time, stop_time, status, machine_id))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == "__main__":
    root = Tk()
    app = MachineStatusApp(root)
    root.mainloop()