import requests
import json
from datetime import datetime

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
    print("16. Añadir valoración")
    print('0. Cerrar sesión')
    return input('Elige opción: ')

def menu_historial():
    print("\n--- MENÚ HISTORIAL DE VEHÍCULO ---")
    print("1. Añadir registro")
    print("2. Ver historial")
    print("0. Volver")
    return input("Elige opción: ")

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
        print(f"❌ Error: {e}")

def iniciar_sesion():
    global token
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")

    try:
        respuesta = requests.post(f"{URL}/login", json={"nombre":nombre,"contraseña":contraseña})
        if "acces_token" in respuesta.json():
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
        print(f'{nombre} ({resena["rating"]}):\n{resena["valoracion"]}')
    print('-'*50)

# Funciones de gestión de vehículos
def agregar_vehiculo():
    pass

def mostrar_vehiculos():
    pass

def realizar_compra():
    pass

def enviar_mensaje():
    receptor = input("Nombre del usuario: ")
    mensaje = input("Mensaje: ")

    headers = {"Authorization": f"Bearer {token}"}
    datos = {"receptor": receptor, "mensaje": mensaje}

    try:
        respuesta = requests.post(
            f"{URL}/enviar_mensaje",
            json=datos,
            headers=headers
        )
        if respuesta.status_code == 200:
            print("✅ Mensaje enviado")
        else:
            print(f"❌ Error: {respuesta.json().get('error')}")
    except Exception as e:
        print(f"🚨 Error: {e}")

def leer_chat():
    receptor = input("Nombre del receptor: ")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.get(
            f"{URL}/leer_chat/{receptor}",
            headers=headers
        )
        if respuesta.status_code == 200:
            mensajes = respuesta.json().get("mensajes", [])
            for msg in mensajes:
                print(msg)
        else:
            print(f"❌ Error: {respuesta.json().get('error')}")
    except Exception as e:
        print(f"🚨 Error: {e}")

def ver_chats():
    headers = {"Authorization": f"Bearer {token}"}
    try:
        respuesta = requests.get(f"{URL}/ver_chats", headers=headers)
        if respuesta.status_code == 200:
            chats = respuesta.json().get("chats", [])
            for chat in chats:
                print(f"Chat de: {chat[0]} y {chat[1]}")
        else:
            print(f"❌ Error: {respuesta.json().get('error')}")
    except Exception as e:
        print(f"🚨 Error: {e}")

# Funciones de anuncios y búsqueda
def publicar_anuncio():
    """Envía un nuevo anuncio al backend autenticado"""
    headers = {"Authorization": f"Bearer {token}"}

    marca = input("Marca: ")
    modelo = input("Modelo: ")
    año = input("Año: ")
    kilometros = input("Kilómetros: ")
    precio = input("Precio: ")
    descripcion = input("Descripción: ")

    datos = {
        "marca": marca,
        "modelo": modelo,
        "año": int(año),
        "kilometros": int(kilometros),
        "precio": float(precio),
        "descripcion": descripcion
    }

    try:
        respuesta = requests.post(
            f"{URL}/publicar_anuncio",
            json=datos,
            headers=headers
        )

        if respuesta.status_code == 201:
            print("✅ Anuncio publicado correctamente.")
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")

    except Exception as e:
        print(f"🚨 Error al conectar con el servidor: {e}")


def listar_anuncios():
    try:
        respuesta = requests.get(f"{URL}/anuncios")
        if respuesta.status_code == 200:
            anuncios = respuesta.json().get("anuncios", [])
            for i, a in enumerate(anuncios):
                estrella = "⭐" if a["destacado"] else ""
                print(f"[{i}] Coche: {a['marca']} {a['modelo']} ({a['año']})")
                print(f"     Km: {a['kilometros']} | Precio: {a['precio']}€ | Anunciante: {a['anunciante']} {estrella}")
                print(f"     {a['descripcion']}\n")
        else:
            print(f"❌ Error al obtener anuncios: {respuesta.status_code}")
    except Exception as e:
        print(f"🚨 Error al conectar con el servidor: {e}")

def buscar_vehiculos_filtros():
    pass

# Funciones de valoración e historial
def estimar_valor_reventa():
    pass


def gestionar_historial_vehiculo():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return

    id_vehiculo = input("ID del vehículo: ").strip()
    if not id_vehiculo:
        print("❌ El ID del vehículo no puede estar vacío.")
        return

    print("Tipo de registro:")
    print("1. Mantenimiento")
    print("2. Revisión")
    print("3. Siniestro")
    tipo_opcion = input("Elige tipo (1-3): ").strip()

    tipos_validos = {'1': 'mantenimiento', '2': 'revision', '3': 'siniestro'}

    if tipo_opcion not in tipos_validos:
        print("❌ Tipo inválido.")
        return

    tipo = tipos_validos[tipo_opcion]

    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    # Validar formato fecha
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        print("❌ Fecha inválida. Usa formato YYYY-MM-DD.")
        return

    descripcion = input("Descripción: ").strip()
    if not descripcion:
        print("❌ La descripción no puede estar vacía.")
        return

    valor_estimado = None
    if tipo == 'siniestro':
        valor_estimado_str = input("Valor estimado (numérico): ").strip()
        try:
            valor_estimado = float(valor_estimado_str)
            if valor_estimado < 0:
                print("❌ El valor estimado no puede ser negativo.")
                return
        except ValueError:
            print("❌ Valor estimado inválido.")
            return

    datos = {
        "tipo": tipo,
        "fecha": fecha,
        "descripcion": descripcion
    }

    if valor_estimado is not None:
        datos["valor_estimado"] = valor_estimado

    headers = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.post(
            f"{URL}/vehiculo/{id_vehiculo}/historial",
            json=datos,
            headers=headers
        )
        if respuesta.status_code == 201:
            print("✅ Registro añadido correctamente al historial.")
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"🚨 Error de conexión: {e}")

def mostrar_historial_vehiculo():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return

    id_vehiculo = input("ID del vehículo: ")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.get(
            f"{URL}/vehiculo/{id_vehiculo}/historial",
            headers=headers
        )
        if respuesta.status_code == 200:
            historial = respuesta.json().get("historial", [])
            if not historial:
                print("No hay registros en el historial para este vehículo.")
                return

            print(f"\nHistorial del vehículo {id_vehiculo}:")
            for idx, registro in enumerate(historial, 1):
                print(f"{idx}. Tipo: {registro['tipo'].capitalize()}")
                print(f"   Fecha: {registro['fecha']}")
                print(f"   Descripción: {registro['descripcion']}")
                if registro['tipo'] == 'siniestro':
                    print(f"   Valor estimado: {registro['valor_estimado']}")
                print("-" * 40)
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"🚨 Error de conexión: {e}")

def mostrar_historial_usuario():
    pass

def anadir_valoracion(usuario):
    """Permite al usuario añadir su reseña"""
    try:
        rating = int(input('Cuantas estrellas nos das(1-5)⭐? '))
    except Exception as e:
        return f'Error: {e}, tienes que introducir un valor numérico'
    valoracion = input('Comentarios: ')
    fecha = datetime.now().strftime("%Y-%m-%d")

    # leemos el json
    with open("valoraciones.json", "r") as jsonread:
        contenido = json.load(jsonread)

    # añadir / modificar valoración
    contenido[usuario] = {
        'rating' : '⭐'*rating, 
        'valoracion' : valoracion, 
        'fecha' : fecha
        }

    with open("valoraciones.json", 'w') as file:
        json.dump(contenido, file)

def obtener_usuario_actual():
    headers = {"Authorization": f"Bearer {token}"}
    try:
        respuesta = requests.get(f"{URL}/quien_soy", headers=headers)
        if respuesta.status_code == 200:
            return respuesta.json().get("usuario")
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
    return None

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
                    while True:
                        opcion_historial = menu_historial()
                        if opcion_historial == '1':
                            gestionar_historial_vehiculo()
                        elif opcion_historial == '2':
                            mostrar_historial_vehiculo()
                        elif opcion_historial == '0':
                            break
                        else:
                            print("Opción no válida.")
                case '12':
                    publicar_anuncio()
                case '13':
                    listar_anuncios()
                case '14':
                    buscar_vehiculos_filtros()
                case '15':
                    mostrar_historial_usuario()
                case '16':
                    anadir_valoracion(obtener_usuario_actual())
                case '0':
                    print("Cerrando sesión...")
                    token = None  # Cierra sesión
                case _:
                    print("Opción no válida. Intente nuevamente.")
