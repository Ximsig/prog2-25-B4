import sqlite3
import hashlib

def hash_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()


def crear_bd():
    """
    Crea la base de datos si aun no existe.
    """
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()

        # Tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                nombre TEXT,
                contraseña TEXT,
                PRIMARY KEY(nombre)
            )
        """)

        # Tabla chats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id_usuario1 TEXT,
                id_usuario2 TEXT,
                chat TEXT,
                PRIMARY KEY(id_usuario1, id_usuario2),
                FOREIGN KEY(id_usuario1) REFERENCES usuarios(nombre),
                FOREIGN KEY(id_usuario2) REFERENCES usuarios(nombre)
            )
        """)

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()


def registrar_usuario(nombre, contraseña):
    """
    Añade un nuevo usuario

    Parametros:
    nombre(str): unico para cada usuario
    """
    hash = hash_contraseña(contraseña)
    conn = None
    try:
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios VALUES (?, ?)", (nombre, hash))
        conn.commit()
        print('Usuario creado correctamente')
        return True
    except sqlite3.IntegrityError:
        print('Ya hay un usuario con ese nombre, debes usar un nombre único')
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

def iniciar_sesion(nombre, contraseña):
    """
    Verifica si el usuario existe y si la contraseña es correcta.

    Parámetros:
    - nombre (str): nombre del usuario.
    - contraseña (str): contraseña en texto plano, se comparará usando su hash.

    Retorna:
    - True si el inicio de sesión es exitoso.
    - False en caso contrario.
    """
    conn = None
    try:
        if not nombre.strip() or not contraseña.strip():
            raise ValueError("El nombre y la contraseña no pueden estar vacíos.")

        hash_ingresado = hash_contraseña(contraseña)

        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT contraseña FROM usuarios WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()

        if not resultado:
            print("El usuario no existe.")
            return False

        hash_guardado = resultado[0]

        if hash_ingresado == hash_guardado:
            print("Inicio de sesión exitoso.")
            return True
        else:
            print("Contraseña incorrecta.")
            return False
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

def mostrar_usuarios():
    """
    Muestra una lista con todos los nombres de usuario registrados en la base de datos.
    """
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            print("Usuarios registrados:")
            for usuario in usuarios:
                print(f"- {usuario[0]}")
        else:
            print("No hay usuarios registrados.")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
    finally:
        if conn:
            conn.close()