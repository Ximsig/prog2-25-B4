# Aqui hacemos el menú para que el usuario interactúe con la app.
import requests
import json

URL = "http://127.0.0.1:5050"
token = None  # Para almacenar el token de autenticación

def menu_principal():
    print('\n ---MENÚ PRINCIPAL---')
    print('1. Registrar usuario')
    print('2. Iniciar sesión')
    print('3. Ver valoraciones')
    print('0. Salir')
    return input('Elige opción: ')

def menu_usuario():
    print("\n ---MENÚ USUARIO---")
    print("4. Agregar vehículo (vendedor)")
    print("5. Mostrar vehículos disponibles")
    print("6. Realizar compra")
    print("7. Enviar mensaje")
    print("8. Leer chat")
    print("9. Ver todos tus chats")
    print("10. Estimar valor de reventa")
    print("11. Gestionar historial de vehículo")
    print("12. Publicar anuncio")
    print("13. Listar anuncios")
    print("14. Buscar vehículos con filtros")
    print("15. Mostrar historial de usuario")
    print('0. Cerra sesión')
    return input('Elige opción: ')

# Funciones de autenticación
def registrar_usuario():
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")

    datos = {
        "nombre": nombre,
        "contraseña": contraseña
    }

    try:
        respuesta = requests.post(f"{URL}/registro", json=datos)

        if respuesta.status_code == 201:
            print("✅ Registrado con éxito.")
        else:
            error = respuesta.json().get("error", "Error desconocido")
            print(f"❌ Error: {error}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {error}")

def iniciar_sesion():
    """Inicia sesión y almacena el token"""
    global token
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")

    try:
        respuesta = requests.post(f"{URL}/login", json={"nombre":nombre,"contraseña":contraseña})
        if token:
            token = respuesta.json()["acces_token"]
        if respuesta.status_code == 200:
            print("✅ Sesión iniciada correctamente")
        else:
            error = respuesta.json().get("error", "Error desconocido")
            print(f"❌ Error: {error}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")

def ver_valoraciones():
    with open("valoraciones.json", "r") as reader:
        datos = json.load(reader)

    for nombre, resena in datos.items():
        print('-'*50)
        print(f'{nombre} ({resena['rating']}):\n{resena['valoracion']}')
    print('-'*50)


# Funciones de gestión de vehículos

def agregar_vehiculo():
    """Añade un vehículo nuevo (solo vendedores)"""
    pass

def mostrar_vehiculos():
    """Muestra lista de vehículos disponibles"""
    pass

def realizar_compra():
    """Procesa la compra de un vehículo"""
    pass

# Funciones de chat (Jordi) no tocar.
def enviar_mensaje():
    """Envía un mensaje a un chat , se crea si no existe"""
    pass

def leer_chat():
    """Muestra el contenido de un chat"""
    pass

def ver_chats():
    """Lista todos los chats del usuario"""
    pass


# Funciones de anuncios y búsqueda
def publicar_anuncio():
    """Publica un nuevo anuncio de vehículo"""
    pass

def listar_anuncios():
    """Muestra todos los anuncios disponibles"""
    pass

def buscar_vehiculos_filtros():
    """Busca vehículos aplicando filtros"""
    pass

# Funciones de valoración e historial
def estimar_valor_reventa():
    """Calcula el valor de reventa de un vehículo"""
    pass

def gestionar_historial_vehiculo():
    """Añade entradas al historial de un vehículo"""
    pass

def mostrar_historial_usuario():
    """Muestra el historial de transacciones del usuario"""
    pass

if __name__ == "__main__":
    print('🚀 BIENVENIDO A COMPRAVENTA DE VEHÍCULOS 🚀')
    while True:
        if token is None:  # Menú principal (no autenticado)
            opcion = menu_principal()
            
            match opcion:
                case '1':
                    registrar_usuario()
                case '2':
                    iniciar_sesion()
                case '3':
                    ver_valoraciones()
                case '0':
                    print("Saliendo del sistema...")
                    break
                case _:
                    print("Opción no válida. Intente nuevamente.")
        
        else:  # Menú de usuario (autenticado)
            opcion = menu_usuario()
            
            match opcion:
                case '4':
                    agregar_vehiculo()
                case '5':
                    mostrar_vehiculos()
                case '6':
                    realizar_compra()
                case '7':
                    enviar_mensaje()
                case '8':
                    leer_chat()
                case '9':
                    ver_chats()
                case '10':
                    estimar_valor_reventa()
                case '11':
                    gestionar_historial_vehiculo()
                case '12':
                    publicar_anuncio()
                case '13':
                    listar_anuncios()
                case '14':
                    buscar_vehiculos_filtros()
                case '15':
                    mostrar_historial_usuario()
                case '0':
                    print("Cerrando sesión...")
                    token = None  # Cierra sesión
                case _:
                    print("Opción no válida. Intenta nuevamente.")
