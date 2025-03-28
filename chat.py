import sqlite3

def crear_bd():
    """
    Crea la base de datos si aun no existe.
    """
    conn = sqlite3.connect("compraventa_vehiculos.db")
    cursor = conn.cursor()

    # Tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER,
            nombre TEXT NOT NULL,
            PRIMARY KEY(id)
        )
    """)

    # Tabla chats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id_usuario1 INTEGER,
            id_usuario2 INTEGER,
            chat TEXT,
            PRIMARY KEY(id_usuario1, id_usuario2),
            FOREIGN KEY(id_usuario1) references usuarios(id),
            FOREIGN KEY(id_usuario2) references usuarios(id)
        )
    """)
    
    conn.commit()
    conn.close()

def agregar_usuario(id, nombre):
    """
    Añade un nuevo usuario

    Parametros:
    id(int): id única para cada usuario
    nombre(str): nombre del usuario
    """
    conn = sqlite3.connect("compraventa_vehiculos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios VALUES (?, ?)", (id, nombre))
    conn.commit()
    conn.close()

def crear_chat(id_usuario1, id_usuario2, chat=''):
    if id_usuario1 > id_usuario2:
        id_usuario1, id_usuario2 = id_usuario2, id_usuario1
    conn = sqlite3.connect("compraventa_vehiculos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats VALUES (?, ?, ?)", (id_usuario1, id_usuario2, chat))
    conn.commit()
    conn.close()
    print('Chat creado correctamente')

def obtener_chat(id_emisor, id_receptor, cursor):
    if id_emisor > id_receptor:
        id_emisor, id_receptor = id_receptor, id_emisor
    cursor.execute(f"""
        SELECT chat FROM chats
        where id_usuario1={id_emisor}
        and id_usuario2={id_receptor}
    """)
    chat = cursor.fetchone()[0]
    return chat
    
    


def enviar_mensaje(id_emisor, id_receptor, mensaje):
    """
    Enviar mensajes entre usuarios

    Parámetros:
    ids usuarios
    mensaje(str): mensaje a enviar
        
    """
    conn = sqlite3.connect("compraventa_vehiculos.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT nombre from usuarios where id={id_emisor}")
    emisor = cursor.fetchone()[0]
    if id_emisor > id_receptor:
        id_emisor, id_receptor = id_receptor, id_emisor
    #chat = obtener_chat(id_emisor, id_receptor, cursor)
    mensaje = f'{emisor}: ' + mensaje + '/s'
    cursor.execute(f"""UPDATE chats set chat=chat || ? 
        where id_usuario1=? and id_usuario2=?""", (mensaje, id_emisor, id_receptor))
    conn.commit()
    conn.close()

def leer_chat(id_emisor, id_receptor):
    if id_emisor > id_receptor:
        id_emisor, id_receptor = id_receptor, id_emisor
    conn = sqlite3.connect("compraventa_vehiculos.db")
    cursor = conn.cursor()
    chat = obtener_chat(id_emisor, id_receptor, cursor)
    conn.close()
    chat = chat.split('/s')
    for linea in chat:
        print(linea)


if __name__ == '__main__':
    # Primera vez, luego cambiar el 1 por 0
    if 1:
        # Creamos bd
        crear_bd()
        #Agregamos tres  usuarios
        agregar_usuario(1, 'Jordi')
        agregar_usuario(2, 'Ximo')
        agregar_usuario(3, 'Linxi')
        # Creamos chats
        crear_chat(1, 2) # Jordi , Ximo
        crear_chat(3, 1) # Linxi , Jordi
    # Mandamos mensajes
    enviar_mensaje(1, 2, 'Hola, cuanto vale?')
    leer_chat(1, 2)
    enviar_mensaje(2, 1, 'Buenas, 2500€')
    leer_chat(2, 1)
    enviar_mensaje(3, 1, 'Cuantos km')
    enviar_mensaje(1, 3, '200mil')
    leer_chat(3, 1)
    leer_chat(1, 3)