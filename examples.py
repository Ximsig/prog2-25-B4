import requests
import json
from datetime import datetime
from types import SimpleNamespace
from contratos import generar_contrato_pdf

# --- DEFINICIONES GLOBALES ---
URL = "http://127.0.0.1:5050"
token = None


# -----------------------------

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
    print("13. Mostrar historial de usuario")
    print("14. Añadir valoración")
    print('0. Cerrar sesión')
    return input('Elige opción: ')


def menu_historial():
    print("\n--- MENÚ HISTORIAL DE VEHÍCULO ---")
    print("1. Añadir registro")
    print("2. Ver historial")
    print("0. Volver")
    return input("Elige opción: ")


def registrar_usuario():
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")
    datos = {"nombre": nombre, "contraseña": contraseña}
    try:
        respuesta = requests.post(f"{URL}/registro", json=datos)
        if respuesta.status_code == 201:
            print("✅ Registrado con éxito.")
        else:
            error = respuesta.json().get("error", "Error desconocido")
            print(f"❌ Error: {error}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except json.JSONDecodeError:
        print(f"❌ Error decodificando respuesta del servidor.")


def iniciar_sesion():
    global token
    nombre = input("Nombre: ")
    contraseña = input("Contraseña: ")
    try:
        respuesta = requests.post(f"{URL}/login", json={"nombre": nombre, "contraseña": contraseña})
        if respuesta.status_code == 200 and "acces_token" in respuesta.json():
            token = respuesta.json()["acces_token"]
            print("✅ Sesión iniciada correctamente")
        else:
            error = respuesta.json().get("error", "Error desconocido al iniciar sesión")
            print(f"❌ Error: {error}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        print(f"🚨 Error decodificando respuesta del servidor.")


def ver_valoraciones():
    try:
        with open("valoraciones.json", "r") as reader:
            datos = json.load(reader)
        if not datos:
            print("ℹ️ No hay valoraciones para mostrar.")
            return
        for nombre, resena in datos.items():
            print('-' * 50)
            print(f'{nombre} ({resena["rating"]}):\n{resena["valoracion"]}')
        print('-' * 50)
    except FileNotFoundError:
        print("ℹ️ Aún no hay valoraciones guardadas.")
    except json.JSONDecodeError:
        print("❌ Error al leer el archivo de valoraciones.")


def obtener_usuario_actual():
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_quiensoy = None
    try:
        respuesta_quiensoy = requests.get(f"{URL}/quien_soy", headers=headers)
        if respuesta_quiensoy.status_code == 200:
            return respuesta_quiensoy.json().get("usuario")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener usuario: {e}")
    except json.JSONDecodeError:
        if respuesta_quiensoy and hasattr(respuesta_quiensoy, 'text'):
            print(f"Error decodificando respuesta al obtener usuario: {respuesta_quiensoy.text[:100]}")
        else:
            print(f"Error decodificando respuesta al obtener usuario.")
    return None


def publicar_anuncio():
    if token is None:
        print("❌ Debes iniciar sesión primero.")
        return
    headers = {"Authorization": f"Bearer {token}"}
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    año_str = input("Año: ")
    kilometros_str = input("Kilómetros: ")
    precio_str = input("Precio: ")
    descripcion = input("Descripción: ")

    try:
        año = int(año_str)
        kilometros = int(kilometros_str)
        precio = float(precio_str)
    except ValueError:
        print("❌ Año, kilómetros y precio deben ser numéricos.")
        return

    datos = {
        "marca": marca, "modelo": modelo, "año": año,
        "kilometros": kilometros, "precio": precio, "descripcion": descripcion
    }
    respuesta_anuncio = None
    try:
        respuesta_anuncio = requests.post(f"{URL}/publicar_anuncio", json=datos, headers=headers)
        if respuesta_anuncio.status_code == 201:
            print("✅ Anuncio publicado correctamente.")
        else:
            error_msg = "Error desconocido"
            try:
                error_msg = respuesta_anuncio.json().get('error', f"Error {respuesta_anuncio.status_code}")
            except json.JSONDecodeError:
                if respuesta_anuncio and hasattr(respuesta_anuncio, 'text'):
                    error_msg = f"Error {respuesta_anuncio.status_code}, respuesta no JSON: {respuesta_anuncio.text[:100]}"
            print(f"❌ Error publicando anuncio: {error_msg}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_anuncio and hasattr(respuesta_anuncio, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_anuncio.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def listar_anuncios_para_cliente(params=None):
    """Lista anuncios, opcionalmente con filtros, y devuelve la lista si tiene éxito."""
    respuesta_lista = None
    try:
        respuesta_lista = requests.get(f"{URL}/anuncios", params=params)
        if respuesta_lista.status_code == 200:
            anuncios = respuesta_lista.json().get("anuncios", [])
            if not anuncios:
                if params:
                    print("\nℹ️ No se encontraron vehículos con los filtros especificados.")
                else:
                    print("ℹ️ No hay anuncios disponibles en este momento.")
                return None  # Importante para que realizar_compra sepa que no hay nada

            print("\n--- Anuncios ---")
            for i, a in enumerate(anuncios):
                estrella = "⭐" if a.get("destacado", False) else ""
                print(f"[{i}] Coche: {a.get('marca', 'N/A')} {a.get('modelo', 'N/A')} ({a.get('año', 'N/A')})")
                print(
                    f"     Km: {a.get('kilometros', 'N/A')} | Precio: {a.get('precio', 'N/A')}€ | Anunciante: {a.get('anunciante', 'N/A')} {estrella}")
                print(f"     {a.get('descripcion', 'N/A')}\n")
            return anuncios
        else:
            error_msg = "Error desconocido"
            try:
                error_msg = respuesta_lista.json().get('error', f"Error {respuesta_lista.status_code}")
            except json.JSONDecodeError:
                if respuesta_lista and hasattr(respuesta_lista, 'text'):
                    error_msg = f"Error {respuesta_lista.status_code}, respuesta no JSON: {respuesta_lista.text[:100]}"
            print(f"❌ Error al obtener anuncios: {error_msg}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión al obtener anuncios: {e}")
        return None
    except json.JSONDecodeError:
        if respuesta_lista and hasattr(respuesta_lista, 'text'):
            print(f"🚨 Error decodificando respuesta del servidor al listar anuncios: {respuesta_lista.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor al listar anuncios.")
        return None


def listar_anuncios():  # Función original para la opción 5 del menú
    listar_anuncios_para_cliente()  # Reutiliza la lógica


def realizar_compra():
    if token is None:
        print("❌ Debes iniciar sesión para realizar una compra.")
        return
    print("\n--- Realizar Compra ---")
    anuncios_disponibles = listar_anuncios_para_cliente()
    if not anuncios_disponibles:
        return

    seleccion_idx_str = input("Ingresa el número del anuncio que deseas comprar: ")
    try:
        seleccion_idx = int(seleccion_idx_str)
    except ValueError:
        print("❌ Selección inválida. Debes ingresar un número.")
        return

    if not (0 <= seleccion_idx < len(anuncios_disponibles)):
        print("❌ Número de anuncio fuera de rango.")
        return

    anuncio_seleccionado = anuncios_disponibles[seleccion_idx]
    confirmar = input(
        f"¿Confirmas la compra de: {anuncio_seleccionado['marca']} {anuncio_seleccionado['modelo']} por {anuncio_seleccionado['precio']}€? (s/n): ").lower()
    if confirmar != 's':
        print("ℹ️ Compra cancelada.")
        return

    datos_compra = {
        "marca": anuncio_seleccionado["marca"], "modelo": anuncio_seleccionado["modelo"],
        "año": anuncio_seleccionado["año"], "anunciante": anuncio_seleccionado["anunciante"],
        "precio": anuncio_seleccionado["precio"]
    }
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_api = None
    try:
        respuesta_api = requests.post(f"{URL}/comprar_vehiculo", json=datos_compra, headers=headers)
        if respuesta_api.status_code == 200:
            datos_respuesta = respuesta_api.json()
            print(f"✅ {datos_respuesta.get('mensaje', 'Compra realizada con éxito.')}")

            comprador_nombre = obtener_usuario_actual() or "Comprador Desconocido"
            vendedor_nombre = datos_respuesta.get("vendedor_nombre", "Vendedor Desconocido")
            vehiculo_comprado_info = datos_respuesta.get("vehiculo_comprado", {})

            vehiculo_para_contrato = SimpleNamespace(
                marca=vehiculo_comprado_info.get('marca', 'N/A'),
                modelo=vehiculo_comprado_info.get('modelo', 'N/A'),
                matricula=vehiculo_comprado_info.get('matricula',
                                                     f"ID-{vehiculo_comprado_info.get('marca', '')}-{vehiculo_comprado_info.get('modelo', '')}"),
                precio=vehiculo_comprado_info.get('precio', 0.0)
            )
            comprador_obj_contrato = SimpleNamespace(nombre=comprador_nombre)
            vendedor_obj_contrato = SimpleNamespace(nombre=vendedor_nombre)
            try:
                generar_contrato_pdf(comprador_obj_contrato, vendedor_obj_contrato, vehiculo_para_contrato)
            except Exception as e_contrato:
                print(f"⚠️ No se pudo generar el contrato PDF: {e_contrato}")
        else:
            final_error_message = f"Error desconocido durante la compra (código: {respuesta_api.status_code})"
            try:
                json_response = respuesta_api.json()
                final_error_message = json_response.get('error', final_error_message)
            except json.JSONDecodeError:
                if respuesta_api and hasattr(respuesta_api, 'text') and respuesta_api.text:
                    final_error_message = f"Error en el servidor (código: {respuesta_api.status_code}), respuesta no es JSON: {respuesta_api.text[:100]}"
            print(f"❌ Error al realizar la compra: {final_error_message}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión durante la compra: {e}")
    except json.JSONDecodeError:  # Para el caso de que respuesta_api.json() falle en la parte del 200
        if respuesta_api and hasattr(respuesta_api, 'text'):
            print(f"🚨 Error decodificando respuesta del servidor: {respuesta_api.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor durante la compra.")
    except Exception as e:
        print(f"🚨 Ocurrió un error inesperado en realizar_compra: {e}")


def enviar_mensaje():
    if token is None: print("❌ Debes iniciar sesión."); return
    receptor = input("Nombre del usuario: ")
    mensaje = input("Mensaje: ")
    headers = {"Authorization": f"Bearer {token}"}
    datos = {"receptor": receptor, "mensaje": mensaje}
    respuesta_msg = None
    try:
        respuesta_msg = requests.post(f"{URL}/enviar_mensaje", json=datos, headers=headers)
        if respuesta_msg.status_code == 200:
            print("✅ Mensaje enviado")
        else:
            print(f"❌ Error: {respuesta_msg.json().get('error', 'Error al enviar mensaje')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_msg and hasattr(respuesta_msg, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_msg.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def leer_chat():
    if token is None: print("❌ Debes iniciar sesión."); return
    receptor = input("Nombre del receptor: ")
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_chat = None
    try:
        respuesta_chat = requests.get(f"{URL}/leer_chat/{receptor}", headers=headers)
        if respuesta_chat.status_code == 200:
            mensajes = respuesta_chat.json().get("mensajes", [])
            if mensajes:
                for msg in mensajes: print(msg)
            else:
                print("ℹ️ No hay mensajes en este chat.")
        else:
            print(f"❌ Error: {respuesta_chat.json().get('error', 'Error al leer chat')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_chat and hasattr(respuesta_chat, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_chat.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def ver_chats():
    if token is None: print("❌ Debes iniciar sesión."); return
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_vchat = None
    try:
        respuesta_vchat = requests.get(f"{URL}/ver_chats", headers=headers)
        if respuesta_vchat.status_code == 200:
            chats = respuesta_vchat.json().get("chats", [])
            if chats:
                for chat in chats: print(f"Chat de: {chat[0]} y {chat[1]}")
            else:
                print("ℹ️ No tienes chats activos.")
        else:
            print(f"❌ Error: {respuesta_vchat.json().get('error', 'Error al ver chats')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_vchat and hasattr(respuesta_vchat, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_vchat.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def estimar_valor_reventa():
    if token is None: print("❌ Debes iniciar sesión primero."); return
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio_str = input("Año: ").strip()
    kilometraje_str = input("Kilómetros: ").strip()

    if not marca or not modelo or not anio_str.isdigit() or not kilometraje_str.isdigit():
        print("❌ Datos inválidos. Marca y modelo no vacíos, año y km numéricos.")
        return
    datos = {"marca": marca, "modelo": modelo, "anio": int(anio_str), "kilometraje": int(kilometraje_str)}
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_est = None
    try:
        respuesta_est = requests.post(f"{URL}/estimar_valor_reventa", json=datos, headers=headers)
        if respuesta_est.status_code == 200:
            info = respuesta_est.json()
            print(f"\nValor estimado: ${info['valor_estimado']}\nReporte:\n{info['reporte']}")
        else:
            print(f"❌ Error: {respuesta_est.json().get('error', 'Error estimando valor')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_est and hasattr(respuesta_est, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_est.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def gestionar_historial_vehiculo():
    if token is None: print("❌ Debes iniciar sesión primero."); return
    id_vehiculo = input("ID del vehículo: ").strip()
    if not id_vehiculo: print("❌ El ID del vehículo no puede estar vacío."); return

    print("Tipo de registro: 1. Mantenimiento 2. Revisión 3. Siniestro")
    tipo_opcion = input("Elige tipo (1-3): ").strip()
    tipos_validos = {'1': 'mantenimiento', '2': 'revision', '3': 'siniestro'}
    if tipo_opcion not in tipos_validos: print("❌ Tipo inválido."); return
    tipo = tipos_validos[tipo_opcion]

    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        print("❌ Fecha inválida. Usa formato YYYY-MM-DD.");
        return

    descripcion = input("Descripción: ").strip()
    if not descripcion: print("❌ La descripción no puede estar vacía."); return

    valor_estimado_siniestro = None
    if tipo == 'siniestro':
        valor_estimado_str = input("Valor estimado (numérico): ").strip()
        try:
            valor_estimado_siniestro = float(valor_estimado_str)
            if valor_estimado_siniestro < 0: print("❌ El valor estimado no puede ser negativo."); return
        except ValueError:
            print("❌ Valor estimado inválido.");
            return

    datos_hist = {"tipo": tipo, "fecha": fecha, "descripcion": descripcion}
    if valor_estimado_siniestro is not None: datos_hist["valor_estimado"] = valor_estimado_siniestro
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_ghist = None
    try:
        respuesta_ghist = requests.post(f"{URL}/vehiculo/{id_vehiculo}/historial", json=datos_hist, headers=headers)
        if respuesta_ghist.status_code == 201:
            print("✅ Registro añadido correctamente al historial.")
        else:
            print(f"❌ Error: {respuesta_ghist.json().get('error', 'Error añadiendo historial')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_ghist and hasattr(respuesta_ghist, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_ghist.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def mostrar_historial_vehiculo():
    if token is None: print("❌ Debes iniciar sesión primero."); return
    id_vehiculo = input("ID del vehículo: ")
    headers = {"Authorization": f"Bearer {token}"}
    respuesta_mhist = None
    try:
        respuesta_mhist = requests.get(f"{URL}/vehiculo/{id_vehiculo}/historial", headers=headers)
        if respuesta_mhist.status_code == 200:
            historial = respuesta_mhist.json().get("historial", [])
            if not historial: print("No hay registros en el historial para este vehículo."); return
            print(f"\nHistorial del vehículo {id_vehiculo}:")
            for idx, registro in enumerate(historial, 1):
                print(
                    f"{idx}. Tipo: {registro['tipo'].capitalize()}\n   Fecha: {registro['fecha']}\n   Descripción: {registro['descripcion']}")
                if registro['tipo'] == 'siniestro': print(f"   Valor estimado: {registro['valor_estimado']}")
                print("-" * 40)
        else:
            print(f"❌ Error: {respuesta_mhist.json().get('error', 'Error mostrando historial')}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except json.JSONDecodeError:
        if respuesta_mhist and hasattr(respuesta_mhist, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_mhist.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def buscar_vehiculos_filtros():
    print("\n--- Buscar Vehículos con Filtros ---")
    print("Deja el campo en blanco si no deseas aplicar ese filtro.")
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio_min_str = input("Año mínimo (ej: 2015): ").strip()
    anio_max_str = input("Año máximo (ej: 2020): ").strip()
    precio_min_str = input("Precio mínimo (€): ").strip()
    precio_max_str = input("Precio máximo (€): ").strip()

    params = {}
    if marca: params['marca'] = marca
    if modelo: params['modelo'] = modelo
    if anio_min_str:
        try:
            params['anio_min'] = int(anio_min_str)
        except ValueError:
            print("❌ Año mínimo debe ser un número."); return
    if anio_max_str:
        try:
            params['anio_max'] = int(anio_max_str)
        except ValueError:
            print("❌ Año máximo debe ser un número."); return
    if precio_min_str:
        try:
            params['precio_min'] = float(precio_min_str)
        except ValueError:
            print("❌ Precio mínimo debe ser un número."); return
    if precio_max_str:
        try:
            params['precio_max'] = float(precio_max_str)
        except ValueError:
            print("❌ Precio máximo debe ser un número."); return

    listar_anuncios_para_cliente(params=params)


def mostrar_historial_usuario():
    if token is None: print("❌ Debes iniciar sesión para ver tu historial."); return
    headers = {"Authorization": f"Bearer {token}"}
    usuario_actual_nombre = obtener_usuario_actual()
    if not usuario_actual_nombre: print("❌ No se pudo obtener la información del usuario actual."); return

    respuesta_uhist = None
    try:
        respuesta_uhist = requests.get(f"{URL}/usuarios/me/anuncios", headers=headers)
        if respuesta_uhist.status_code == 200:
            datos_historial = respuesta_uhist.json()
            anuncios_publicados = datos_historial.get("anuncios_publicados", [])
            print(f"\n--- Historial de Usuario para {usuario_actual_nombre} ---")
            if anuncios_publicados:
                print("\n== Anuncios Publicados por ti ==")
                for i, a in enumerate(anuncios_publicados):
                    estrella = "⭐" if a.get("destacado", False) else ""
                    print(
                        f"  [{i + 1}] Coche: {a.get('marca', 'N/A')} {a.get('modelo', 'N/A')} ({a.get('año', 'N/A')})")
                    print(f"       Km: {a.get('kilometros', 'N/A')} | Precio: {a.get('precio', 'N/A')}€ {estrella}")
                    print(f"       {a.get('descripcion', 'N/A')}\n")
            else:
                print("ℹ️ No has publicado ningún anuncio.")
        else:
            final_error_message = f"Error desconocido obteniendo historial (código: {respuesta_uhist.status_code})"
            try:
                json_response = respuesta_uhist.json()
                final_error_message = json_response.get('error', final_error_message)
            except json.JSONDecodeError:
                if respuesta_uhist and hasattr(respuesta_uhist, 'text') and respuesta_uhist.text:
                    final_error_message = f"Error en el servidor (código: {respuesta_uhist.status_code}), respuesta no es JSON: {respuesta_uhist.text[:100]}"
            print(f"❌ Error al obtener el historial de usuario: {final_error_message}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión al obtener el historial: {e}")
    except json.JSONDecodeError:
        if respuesta_uhist and hasattr(respuesta_uhist, 'text'):
            print(f"🚨 Error decodificando respuesta: {respuesta_uhist.text[:100]}")
        else:
            print(f"🚨 Error decodificando respuesta del servidor.")


def anadir_valoracion(usuario_valorado):
    if not usuario_valorado:
        print("❌ No se pudo determinar el usuario para la valoración.")
        return
    try:
        rating_str = input('Cuantas estrellas nos das? (1-5)⭐: ')
        rating = int(rating_str)
        while not (1 <= rating <= 5):
            rating_str = input('Introduce un número del 1-5 ⭐: ')
            rating = int(rating_str)
    except ValueError:
        print('Error: tienes que introducir un valor numérico para las estrellas.')
        return

    comentario_valoracion = input('Comentarios: ')
    fecha_valoracion = datetime.now().strftime("%Y-%m-%d")

    contenido_valoraciones = {}
    try:
        with open("valoraciones.json", "r") as jsonread:
            contenido_valoraciones = json.load(jsonread)
    except FileNotFoundError:
        pass  # Si el archivo no existe, se creará
    except json.JSONDecodeError:
        print("⚠️ El archivo valoraciones.json está corrupto. Se creará uno nuevo.")

    contenido_valoraciones[usuario_valorado] = {
        'rating': '⭐' * rating,
        'valoracion': comentario_valoracion,
        'fecha': fecha_valoracion
    }
    try:
        with open("valoraciones.json", 'w') as file_valoraciones:
            json.dump(contenido_valoraciones, file_valoraciones, indent=4)
        print("✅ Valoración añadida con éxito.")
    except IOError:
        print("❌ Error al guardar la valoración en el archivo.")


if __name__ == "__main__":
    print('🚀 BIENVENIDO A COMPRAVENTA DE VEHÍCULOS 🚀')
    while True:
        if token is None:
            opcion_principal = menu_principal()
            if opcion_principal == '1':
                registrar_usuario()
            elif opcion_principal == '2':
                iniciar_sesion()
            elif opcion_principal == '3':
                ver_valoraciones()
            elif opcion_principal == '0':
                print("Saliendo del sistema..."); break
            else:
                print("Opción no válida. Intente nuevamente.")
        else:
            opcion_usuario = menu_usuario()
            if opcion_usuario == '4':
                publicar_anuncio()
            elif opcion_usuario == '5':
                listar_anuncios()
            elif opcion_usuario == '6':
                realizar_compra()
            elif opcion_usuario == '7':
                enviar_mensaje()
            elif opcion_usuario == '8':
                leer_chat()
            elif opcion_usuario == '9':
                ver_chats()
            elif opcion_usuario == '10':
                estimar_valor_reventa()
            elif opcion_usuario == '11':
                while True:
                    opcion_historial_veh = menu_historial()
                    if opcion_historial_veh == '1':
                        gestionar_historial_vehiculo()
                    elif opcion_historial_veh == '2':
                        mostrar_historial_vehiculo()
                    elif opcion_historial_veh == '0':
                        break
                    else:
                        print("Opción no válida.")
            elif opcion_usuario == '12':
                buscar_vehiculos_filtros()
            elif opcion_usuario == '13':
                mostrar_historial_usuario()
            elif opcion_usuario == '14':
                usuario_actual_para_valorar = obtener_usuario_actual()
                if usuario_actual_para_valorar:
                    anadir_valoracion(usuario_actual_para_valorar)
                else:
                    print("❌ Debes estar logueado para añadir una valoración.")
            elif opcion_usuario == '0':
                print("Cerrando sesión..."); token = None
            else:
                print("Opción no válida. Intente nuevamente.")