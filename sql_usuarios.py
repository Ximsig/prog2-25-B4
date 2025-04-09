import random
from db import registrar_usuario_bd

def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Nuestro usuario de MySQL
            password='tu_contraseña',  # Nuestra contraseña
            database='plataforma_vehiculos'
        )
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Funciones para registrar usuario, agregar vehículo, etc.

def registar_usuario_bd(nombre, apellido, email, es_comprador):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(nombre, apellido, email, es_comprador)
        conn.commit()
        print(f"Usuario {nombre} {apellido} registrado exitosamente.")
    except Error as e:
        print(f"Error al registrar usuario: {e}")
    finally:
        cursor.close()
        conn.close()
