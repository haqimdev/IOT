import tkinter as tk
from AM import MachineStatusApp
from DB import DatabaseConnector


# class main(MachineStatusApp):
#     def __init__(self):
#         super().__init__()
#         self.db = None
#         self.root = None
#         self.app = None
#         self.periodic_task = None
#         self.main()
def periodic_task(db):
    # Check if the database is connected
    try:
        if db.is_connected():
            #update gpio status here
            #...
            print("Database is connected.")
            db.setup_gpio(23, db.datetime.now(), 'Green', 1)
            db.setup_gpio(24, db.datetime.now(), 'Green', 2)
        else:
            #update gpio status here
            #...
            print("Database is not connected.")
            
    except:
        print("Database is not connected.")
        
    # Schedule the task to run again after 2000ms (2 seconds)
    root.after(2000, lambda: periodic_task(db))
    
def main():
    global root
    root = tk.Tk()
    db = None
    app = MachineStatusApp(root, db)

    periodic_task(db)
    
    root.mainloop()

if __name__ == "__main__":
    main()