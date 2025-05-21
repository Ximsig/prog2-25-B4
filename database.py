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

        # Tabla historial_vehiculo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_vehiculo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_vehiculo TEXT,
                tipo TEXT,
                fecha TEXT,
                descripcion TEXT,
                valor_estimado REAL
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

def ver_chats(id_usuario):
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats where id_usuario1=? or id_usuario2=?", (id_usuario, id_usuario))
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
    crear_chat(id_emisor, id_receptor)
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

def agregar_registro_historial(id_vehiculo, tipo, fecha, descripcion, valor_estimado=None):
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO historial_vehiculo (id_vehiculo, tipo, fecha, descripcion, valor_estimado)
            VALUES (?, ?, ?, ?, ?)
        """, (id_vehiculo, tipo, fecha, descripcion, valor_estimado))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error agregando historial: {e}")
        return False
    finally:
        if conn:
            conn.close()

def obtener_historial_vehiculo(id_vehiculo):
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tipo, fecha, descripcion, valor_estimado
            FROM historial_vehiculo
            WHERE id_vehiculo = ?
            ORDER BY fecha
        """, (id_vehiculo,))
        rows = cursor.fetchall()
        return [
            {
                "tipo": row[0],
                "fecha": row[1],
                "descripcion": row[2],
                "valor_estimado": row[3]
            } for row in rows
        ]
    except sqlite3.Error as e:
        print(f"Error obteniendo historial: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_historial_usuario(usuario):
    """
    Devuelve un diccionario {id_vehiculo: [registros]} con el historial de todos los vehículos de un usuario.
    """
    # Ejemplo: asume que tienes una función obtener_vehiculos_usuario(usuario)
    # y una función obtener_historial_vehiculo(id_vehiculo)
    historiales = {}
    vehiculos = obtener_vehiculos_usuario(usuario)  # Debe devolver una lista de IDs de vehículos
    for id_vehiculo in vehiculos:
        historial = obtener_historial_vehiculo(id_vehiculo)
        historiales[id_vehiculo] = historial if historial else []
    return historiales

def obtener_vehiculos_usuario(usuario):
    """
    Devuelve una lista de IDs de vehículos asociados a un usuario.
    """
    conn = None
    try:
        conn = sqlite3.connect("compraventa_vehiculos.db")
        cursor = conn.cursor()
        # Ajusta el nombre de la tabla y el campo según tu modelo de datos
        cursor.execute("SELECT id FROM vehiculos WHERE anunciante = ?", (usuario,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        print(f"Error obteniendo vehículos del usuario: {e}")
        return []
    finally:
        if conn:
            conn.close()
