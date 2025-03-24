import pymysql.cursors
# from pymysql.cursors import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = pymysql.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MariaDB successful")
    except pymysql.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except pymysql.Error as e:
        print(f"The error '{e}' occurred")

def insert_machine_status(connection, start_time, stop_time, status,machine_id):
    query = """
    INSERT INTO status (start_time, stop_time, status, machine_id)
    VALUES (%s, %s, %s, %s)
    """
    data = (start_time, stop_time, status, machine_id)
    execute_query(connection, query, data)