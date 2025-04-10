import sqlite3
import hashlib

'''

CÓDIGO AUXILIAR PROBAR USUARIOS API

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
    Muestra todos los usuarios de la bd.
    """
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        consulta = cursor.fetchall()
        
        if not consulta:
            print("No hay usuarios registrados")
            return []
            
        for idx, usuario in enumerate(consulta):
            print(f'Usuario {idx}: {usuario[0]}')
        return [usuario[0] for usuario in consulta]
    except sqlite3.Error as e:
        print(f"Error al mostrar usuarios: {e}")
        return []
    finally:
        if conn:
            conn.close()
'''

############
# Mi parte #
############
def crear_chat(id_usuario1, id_usuario2):
    conn = None
    try:
        if id_usuario1 == id_usuario2:
            raise ValueError("No puedes crear un chat contigo mismo")
            
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        
        # Verificar que los usuarios existen
        cursor.execute("SELECT 1 FROM usuarios WHERE nombre=?", (id_usuario1,))
        if not cursor.fetchone():
            raise ValueError(f"El usuario {id_usuario1} no existe")
            
        cursor.execute("SELECT 1 FROM usuarios WHERE nombre=?", (id_usuario2,))
        if not cursor.fetchone():
            raise ValueError(f"El usuario {id_usuario2} no existe")
        
        id_usuario1, id_usuario2 = sorted([id_usuario1, id_usuario2])  # Ordenamos para evitar problemas con la clave primaria

        cursor.execute("SELECT 1 FROM chats WHERE id_usuario1=? AND id_usuario2=?", (id_usuario1, id_usuario2))
        if cursor.fetchone():
            print("Ya teneis un chat.")
            return False
        else:
            cursor.execute("INSERT INTO chats VALUES (?, ?, ?)", (id_usuario1, id_usuario2, ''))
            conn.commit()
            print("Chat creado correctamente.")
            return True
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

def ver_chats():
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats")
        consulta = cursor.fetchall()
        
        if not consulta:
            print("No hay chats creados")
            return []
            
        for idx, chat in enumerate(consulta):
            print(f'Chat {idx}: {chat[0]} - {chat[1]}')
        return consulta
    except sqlite3.Error as e:
        print(f"Error al ver chats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_chat(id_emisor, id_receptor, cursor):
    try:
        cursor.execute("""
            SELECT chat FROM chats
            WHERE id_usuario1 = ? AND id_usuario2 = ?
        """, (id_emisor, id_receptor))
        chat = cursor.fetchone()
        return chat[0] if chat else ""  # Evitamos errores si el chat no existe
    except sqlite3.Error as e:
        print(f"Error al obtener chat: {e}")
        return ""

def enviar_mensaje(id_emisor, id_receptor, mensaje):
    """
    Enviar mensajes entre usuarios

    Parámetros:
    ids usuarios
    mensaje(str): mensaje a enviar
    """
    conn = None
    try:
        if not mensaje.strip():
            raise ValueError("El mensaje no puede estar vacío")
            
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM usuarios WHERE nombre = ?", (id_emisor,))
        emisor = cursor.fetchone()
        if not emisor:
            raise ValueError("El usuario emisor no existe.")
        emisor = emisor[0]  # Extraer el nombre
        
        cursor.execute("SELECT nombre FROM usuarios WHERE nombre = ?", (id_receptor,))
        if not cursor.fetchone():
            raise ValueError("El usuario receptor no existe.")

        mensaje_formateado = f'{emisor}: {mensaje}\n'
        
        # Verificamos si existe el chat
        id_usuario1, id_usuario2 = sorted([id_emisor, id_receptor])
        cursor.execute("SELECT 1 FROM chats WHERE id_usuario1=? AND id_usuario2=?", (id_usuario1, id_usuario2))
        if not cursor.fetchone():
            raise ValueError("No existe un chat entre estos usuarios")
        
        cursor.execute("""
            UPDATE chats SET chat = chat || ?
            WHERE id_usuario1 = ? AND id_usuario2 = ?
        """, (mensaje_formateado, id_usuario1, id_usuario2))

        conn.commit()
        print("Mensaje enviado correctamente")
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

def leer_chat(id_emisor, id_receptor):
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        
        # Verificar que los usuarios existen
        cursor.execute("SELECT 1 FROM usuarios WHERE nombre=?", (id_emisor,))
        if not cursor.fetchone():
            raise ValueError(f"El usuario {id_emisor} no existe")
            
        cursor.execute("SELECT 1 FROM usuarios WHERE nombre=?", (id_receptor,))
        if not cursor.fetchone():
            raise ValueError(f"El usuario {id_receptor} no existe")
        
        id_usuario1, id_usuario2 = sorted([id_emisor, id_receptor])
        cursor.execute("SELECT chat FROM chats WHERE id_usuario1=? AND id_usuario2=?", (id_usuario1, id_usuario2))
        chat = cursor.fetchone()

        if not chat:
            raise ValueError("No existe un chat entre estos usuarios")
            
        chat = chat[0]
        if not chat.strip():
            print("No hay mensajes en este chat.")
            return []
            
        chat_lineas = chat.strip().split("\n")
        for linea in chat_lineas:
            print(linea)
        return chat_lineas
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except sqlite3.Error as e:
        print(f"Error al leer chat: {e}")
        return []
    finally:
        if conn:
            conn.close()
