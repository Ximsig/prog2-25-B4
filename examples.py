import requests
import json


URL = "http://127.0.0.1:5050"
token = None



def obtener_usuario_actual():
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}"}
    try:
        respuesta = requests.get(f"{URL}/quien_soy", headers=headers)
        if respuesta.status_code == 200:
            return respuesta.json().get("usuario")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener usuario: {e}")
    except json.JSONDecodeError:
        print(f"Error decodificando respuesta al obtener usuario.")
    return None


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
    if marca:
        params['marca'] = marca
    if modelo:
        params['modelo'] = modelo
    if anio_min_str:
        if anio_min_str.isdigit():
            params['anio_min'] = int(anio_min_str)
        else:
            print("❌ Año mínimo debe ser un número.")
            return
    if anio_max_str:
        if anio_max_str.isdigit():
            params['anio_max'] = int(anio_max_str)
        else:
            print("❌ Año máximo debe ser un número.")
            return
    if precio_min_str:
        try:
            params['precio_min'] = float(precio_min_str)
        except ValueError:
            print("❌ Precio mínimo debe ser un número.")
            return
    if precio_max_str:
        try:
            params['precio_max'] = float(precio_max_str)
        except ValueError:
            print("❌ Precio máximo debe ser un número.")
            return

    respuesta = None
    try:
        respuesta = requests.get(f"{URL}/anuncios", params=params)

        if respuesta.status_code == 200:
            anuncios = respuesta.json().get("anuncios", [])
            if not anuncios:
                print("\nℹ️ No se encontraron vehículos con los filtros especificados.")
                return

            print("\n--- Vehículos Encontrados ---")
            for i, a in enumerate(anuncios):
                estrella = "⭐" if a.get("destacado", False) else ""
                print(f"[{i + 1}] Coche: {a.get('marca', 'N/A')} {a.get('modelo', 'N/A')} ({a.get('año', 'N/A')})")
                print(
                    f"     Km: {a.get('kilometros', 'N/A')} | Precio: {a.get('precio', 'N/A')}€ | Anunciante: {a.get('anunciante', 'N/A')} {estrella}")
                print(f"     {a.get('descripcion', 'N/A')}\n")
        else:
            error_msg = "Error desconocido"
            try:
                error_msg = respuesta.json().get('error', f"Error desconocido (código: {respuesta.status_code})")
            except json.JSONDecodeError:
                # Si respuesta.json() falla, usamos el texto crudo de la respuesta si existe
                if respuesta and hasattr(respuesta, 'text'):
                    error_msg = f"Error en el servidor (código: {respuesta.status_code}), respuesta no es JSON: {respuesta.text[:100]}"
                else:
                    error_msg = f"Error en el servidor (código: {respuesta.status_code}), respuesta no es JSON y no hay texto de respuesta."
            print(f"❌ Error al buscar vehículos: {error_msg}")

    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión al buscar vehículos: {e}")
    except json.JSONDecodeError:  # Este catch es por si respuesta.json() de la sección 200 falla
        if respuesta and hasattr(respuesta, 'text'):
            print(f"🚨 Error decodificando la respuesta del servidor. Respuesta recibida: {respuesta.text[:200]}")
        else:
            print(f"🚨 Error decodificando la respuesta del servidor, y no hay texto de respuesta disponible.")


def mostrar_historial_usuario():
    if token is None:
        print("❌ Debes iniciar sesión para ver tu historial.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    usuario_actual = obtener_usuario_actual()

    if not usuario_actual:
        print("❌ No se pudo obtener la información del usuario actual (asegúrate de estar logueado).")
        return

    respuesta = None
    try:
        respuesta = requests.get(f"{URL}/usuarios/me/anuncios", headers=headers)

        if respuesta.status_code == 200:
            datos_historial = respuesta.json()
            anuncios_publicados = datos_historial.get("anuncios_publicados", [])

            print(f"\n--- Historial de Usuario para {usuario_actual} ---")

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
            error_msg = "Error desconocido"
            try:
                error_msg = respuesta.json().get('error', f"Error desconocido (código: {respuesta.status_code})")
            except json.JSONDecodeError:
                if respuesta and hasattr(respuesta, 'text'):
                    error_msg = f"Error en el servidor (código: {respuesta.status_code}), respuesta no es JSON: {respuesta.text[:100]}"
                else:
                    error_msg = f"Error en el servidor (código: {respuesta.status_code}), respuesta no es JSON y no hay texto de respuesta."
            print(f"❌ Error al obtener el historial de usuario: {error_msg}")

    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión al obtener el historial: {e}")
    except json.JSONDecodeError:  # Este catch es por si respuesta.json() de la sección 200 falla
        if respuesta and hasattr(respuesta, 'text'):
            print(f"🚨 Error decodificando la respuesta del servidor. Respuesta recibida: {respuesta.text[:200]}")
        else:
            print(f"🚨 Error decodificando la respuesta del servidor, y no hay texto de respuesta disponible.")