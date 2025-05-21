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
    print("4. Publicar anuncio")
    print("5. Listar anuncios")
    print("6. Realizar compra")
    print("7. Enviar mensaje")
    print("8. Leer chat")
    print("9. Ver todos tus chats")
    print("10. Estimar valor de reventa")
    print("11. Gestionar historial de vehículo")
    print("12. Buscar vehículos con filtros")
    print("13. Añadir valoración")
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
        respuesta = requests.post(f"{URL}/login", json={"nombre": nombre, "contraseña": contraseña})
        respuesta_json = respuesta.json()

        if "access_token" in respuesta_json:
            token = respuesta_json["access_token"]
            print("✅ Sesión iniciada correctamente")
        else:
            error = respuesta_json.get("error", "Error desconocido")
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

def realizar_compra():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return

    # Primero obtener la lista de anuncios
    try:
        respuesta_anuncios = requests.get(f"{URL}/anuncios")
        if respuesta_anuncios.status_code != 200:
            print("❌ Error al obtener los anuncios.")
            return
        
        anuncios = respuesta_anuncios.json().get("anuncios", [])
        if not anuncios:
            print("No hay anuncios disponibles.")
            return

        # Mostrar anuncios
        for a in anuncios:
            estrella = "⭐" if a.get("destacado") else ""
            print(f"[{a['id']}] Coche: {a['marca']} {a['modelo']} ({a['año']})")
            print(f"     Km: {a['kilometros']} | Precio: {a['precio']}€ | Anunciante: {a['anunciante']} {estrella}")
            print(f"     {a['descripcion']}\n")

        # Pedir ID del vehículo
        id_vehiculo = input("ID del vehículo a comprar: ").strip()
        if not id_vehiculo:
            print("❌ Debes introducir un ID de vehículo.")
            return

        # Realizar la compra
        headers = {"Authorization": f"Bearer {token}"}
        datos = {"id_vehiculo": id_vehiculo}
        respuesta = requests.post(f"{URL}/realizar_compra", json=datos, headers=headers)
        
        if respuesta.status_code == 200:
            datos_respuesta = respuesta.json()
            print("✅ Compra realizada con éxito.")
            
            if datos_respuesta.get("contrato_generado"):
                ruta_contrato = datos_respuesta.get("contrato")
                print(f"📄 Se ha generado el contrato de compraventa en: {ruta_contrato}")
            else:
                print("⚠️ No se pudo generar el contrato:", datos_respuesta.get("error_contrato"))
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"🚨 Error al conectar con el servidor: {e}")

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
            for a in anuncios:
                estrella = "⭐" if a["destacado"] else ""
                print(f"[{a['id']}] Coche: {a['marca']} {a['modelo']} ({a['año']})")
                print(f"     Km: {a['kilometros']} | Precio: {a['precio']}€ | Anunciante: {a['anunciante']} {estrella}")
                print(f"     {a['descripcion']}\n")
        else:
            print(f"❌ Error al obtener anuncios: {respuesta.status_code}")
    except Exception as e:
        print(f"🚨 Error al conectar con el servidor: {e}")


def buscar_vehiculos_filtros():
    """Permite buscar vehículos usando filtros opcionales"""
    print("\n--- Búsqueda de vehículos con filtros ---")
    marca = input("Marca (dejar vacío para cualquier): ").strip()
    modelo = input("Modelo (dejar vacío para cualquier): ").strip()
    año = input("Año (dejar vacío para cualquier): ").strip()
    precio_min = input("Precio mínimo (dejar vacío para cualquier): ").strip()
    precio_max = input("Precio máximo (dejar vacío para cualquier): ").strip()

    filtros = {}
    if marca:
        filtros["marca"] = marca
    if modelo:
        filtros["modelo"] = modelo
    if año.isdigit():
        filtros["año"] = int(año)
    if precio_min.replace('.', '', 1).isdigit():
        filtros["precio_min"] = float(precio_min)
    if precio_max.replace('.', '', 1).isdigit():
        filtros["precio_max"] = float(precio_max)

    try:
        respuesta = requests.get(f"{URL}/buscar_vehiculos", params=filtros)
        if respuesta.status_code == 200:
            resultados = respuesta.json().get("resultados", [])
            if not resultados:
                print("No se encontraron vehículos con esos filtros.")
                return
            print("\nResultados de la búsqueda:")
            for v in resultados:
                print(f"[{v['id']}] {v['marca']} {v['modelo']} ({v['año']}) - {v['kilometros']} km - {v['precio']}€")
                print(f"    {v['descripcion']}")
                print("-" * 40)
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"🚨 Error al conectar con el servidor: {e}")

# Funciones de valoración e historial
def estimar_valor_reventa():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return

    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio = input("Año: ").strip()
    kilometraje = input("Kilómetros: ").strip()

    if not marca or not modelo or not anio.isdigit() or not kilometraje.isdigit():
        print("❌ Datos inválidos. Marca y modelo no vacíos, año y km numéricos.")
        return

    datos = {
        "marca": marca,
        "modelo": modelo,
        "anio": int(anio),
        "kilometraje": int(kilometraje)
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        respuesta = requests.post(f"{URL}/estimar_valor_reventa", json=datos, headers=headers)
        if respuesta.status_code == 200:
            info = respuesta.json()
            print(f"\nValor estimado: ${info['valor_estimado']}")
            print("Reporte:\n" + info['reporte'])
        else:
            print(f"❌ Error: {respuesta.json().get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"🚨 Error de conexión: {e}")

def gestionar_historial_vehiculo():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return

    # Primero mostrar los anuncios disponibles
    try:
        respuesta_anuncios = requests.get(f"{URL}/anuncios")
        if respuesta_anuncios.status_code != 200:
            print("❌ Error al obtener los anuncios.")
            return
        
        anuncios = respuesta_anuncios.json().get("anuncios", [])
        if not anuncios:
            print("No hay vehículos disponibles.")
            return

        # Mostrar anuncios
        print("\nVehículos disponibles:")
        for a in anuncios:
            print(f"[{a['id']}] {a['marca']} {a['modelo']} ({a['año']}) - {a['kilometros']} km")

        # Pedir ID del vehículo
        id_vehiculo = input("\nID del vehículo para gestionar historial: ").strip()
        if not id_vehiculo:
            print("❌ El ID del vehículo no puede estar vacío.")
            return

        # Verificar que el ID existe
        if not any(str(a['id']) == id_vehiculo for a in anuncios):
            print("❌ ID de vehículo no válido.")
            return

        print("\nTipo de registro:")
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

        respuesta = requests.post(f"{URL}/vehiculo/{id_vehiculo}/historial", json=datos, headers=headers)
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


def anadir_valoracion(usuario):
    """Permite al usuario añadir su reseña"""
    try:
        rating = int(input('Cuantas estrellas nos das? (1-5)⭐: '))
        while rating < 1 or rating > 5:
            rating = int(input('Introduce un número del 1-5 ⭐: '))
    except Exception as e:
        return f'Error: {e}, tienes que introducir un valor numérico'
    
    valoracion = input('Comentarios: ')
    fecha = datetime.now().strftime("%Y-%m-%d")

    # leemos el json, si no hay se crea
    try:
        with open("valoraciones.json", "r") as jsonread:
            contenido = json.load(jsonread)
    except FileNotFoundError:
        json.dump({}, open("valoraciones.json", "w"))
        # leemos el archivo creado
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
                    publicar_anuncio()
                case '5':
                    listar_anuncios()
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
                    buscar_vehiculos_filtros()
                case '13':
                    anadir_valoracion(obtener_usuario_actual())
                case '0':
                    print("Cerrando sesión...")
                    token = None
                case _:
                    print("Opción no válida. Intente nuevamente.")
