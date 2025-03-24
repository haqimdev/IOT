class MachineStatus:
    def __init__(self, start_time, stop_time, status, machine_id):
        self.start_time = start_time
        self.stop_time = stop_time
        self.status = status
        self.machine_id = machine_id

    def __repr__(self):
        return f"MachineStatus(start_time={self.start_time}, stop_time={self.stop_time}, status='{self.status}, machine_id='{self.machine_id}')"