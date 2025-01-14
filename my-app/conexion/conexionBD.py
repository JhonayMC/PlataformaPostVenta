
# # Importando Libreria mysql.connector para conectar Python con MySQL

# import pymssql

# def connectionBD():
#     try:
#         connection = pymssql.connect(
#             server='localhost\SQLEXPRESS01',
#             database='master',
#             user='saa',
#             password='1234',
#             as_dict=True  # Configurar el cursor para devolver diccionarios
#         )
#         print("Conexión exitosa a la base de datos SQL Server")
#         return connection  # Configurar el cursor para devolver diccionarios
#     except pymssql.Error as error:
#         print(f"No se pudo conectar: {error}")

# # Llamada a la función para establecer la conexión
# mi_cursor_sql_server = connectionBD()

import pyodbc
import os

def connectionBD():
    try:
        # Leer variables de entorno
        user = os.getenv('SQL_SERVER_USER')
        password = os.getenv('SQL_SERVER_PASSWORD')
        host = os.getenv('SQL_SERVER_HOST')
        database = os.getenv('SQL_SERVER_DATABASE')

        # Establecer conexión con usuario y contraseña
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={host};'
            f'DATABASE={database};'
            f'UID={user};'
            f'PWD={password};'
        )
        print("Conexión exitosa a la base de datos SQL Server")
        
        return connection
    except pyodbc.Error as error:
        print(f"No se pudo conectar: {error}")
        return None


# Configuración de variables de entorno para pruebas
os.environ['SQL_SERVER_USER'] = 'saa'
os.environ['SQL_SERVER_PASSWORD'] = '1234'
os.environ['SQL_SERVER_HOST'] = 'DESKTOP-18DM3IS\\SQLEXPRESS01'
os.environ['SQL_SERVER_DATABASE'] = 'BOT'

# Llamada a la función para establecer la conexión
connection = connectionBD()
