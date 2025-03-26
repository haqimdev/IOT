# Description: This file contains the DatabaseConnector class which is responsible for connecting to the database and saving data to the database.
import pymysql.cursors
from datetime import datetime


class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Success", "Connected to the database successfully.")
            return self.connection
        except pymysql.Error as e:
            print("Database Connection Error", f"Error: {e}")
            return None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Success", "Disconnected from the database successfully.")
        else:
            print("Database Error", "No connection to close.")

    def save_to_database(self, start_time, status, machine_id):
        if self.connection:
            cursor = self.connection.cursor()
            query = "INSERT INTO machine_status (start_time, status, machine_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (start_time, status, machine_id))
            self.connection.commit()
        else:
            print("Database Error", "Failed to connect to the database.")
            
    def update_to_database(self, stop_time, status, machine_id,id):
        if self.connection:
            cursor = self.connection.cursor()
            # query = "INSERT INTO machine_status (stop_time, status, machine_id) VALUES (%s, %s, %s)"
            query = "UPDATE machine_status SET stop_time = %s, status = %s WHERE machine_id = %s AND id = %s"
            # cursor.execute()
            cursor.execute(query, (stop_time, status, machine_id,id))
            self.connection.commit()
        else:
            print("Database Error", "Failed to connect to the database.")
    
    def get_last_created_id(self, machine_id):
        if self.connection:
            cursor = self.connection.cursor()
            query = "SELECT id FROM machine_status WHERE machine_id = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(query, (machine_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        else:
            print("Database Error", "Failed to connect to the database.")
            return None
    def is_connected(self):
        try:
            if self.connection and self.connection.open:
                return True
            else:
                return False
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False
            