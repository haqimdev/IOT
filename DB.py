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
        try:
            self.connection.close()
            if self.connection:
                self.connection.close()
                print("Success", "Disconnected from the database successfully.")
            else:
                print("Database Error", "No connection to close.")
        except pymysql.Error as e:
            print("Database Connection Error", f"Error: {e}")
            return None

    def check_is_connected(self):
        try:
            if self.connection and self.connection.open:
                return True
            else:
                return False
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False

    def log_insert_to_db(self, start_time, signal_id, machine_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                query = "INSERT INTO machine_log (start_time, signal_id, machine_id) VALUES (%s, %s, %s)"
#                 query = "INSERT INTO machine_status (start_time, signal, status, machine_id) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (start_time, signal_id, machine_id))
                self.connection.commit()
            else:
                print("Database Error", "Failed to connect to the database.")
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False

    def log_update_to_db(self, id, stop_time, signal_id, machine_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                query = "UPDATE machine_log SET stop_time = %s WHERE machine_id = %s AND signal_id = %s AND id = %s"
                cursor.execute(query, ( stop_time,  machine_id, signal_id, id))
                self.connection.commit()
            else:
                print("Database Error", "Failed to connect to the database.")
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False
            
    def status_update_to_db(self, signal_id, status, machine_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                # query = "INSERT INTO machine_status (stop_time, status, machine_id) VALUES (%s, %s, %s)"
                query = "UPDATE machine_status SET status = %s WHERE signal_id = %s AND machine_id = %s"
                # query = "UPDATE machine_status SET status = 5 WHERE signal_id = 4 AND machine_id = 1"
                # cursor.execute()
                cursor.execute(query, (status,signal_id, machine_id))
                # cursor.execute(query)
                self.connection.commit()
            else:
                print("Database Error", "Failed to connect to the database.")
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False

    def get_last_created_id(self, signal_id, machine_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                query = "SELECT id FROM machine_log WHERE signal_id = %s AND machine_id = %s ORDER BY id DESC LIMIT 1"
                cursor.execute(query, (signal_id, machine_id,))
                result = cursor.fetchone()
                return result[0] if result else None
            else:
                print("Database Error", "Failed to connect to the database.")
                return None
        except pymysql.Error as e:
            print("Database Error", f"Error: {e}")
            return False

