import tkinter as tk
from gui import MachineStatusApp

def main():
    root = tk.Tk()
    app = MachineStatusApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()