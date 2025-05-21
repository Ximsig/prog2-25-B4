# app.py

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import (
    crear_bd, registrar_usuario as db_registrar_usuario,
    iniciar_sesion as db_iniciar_sesion,
    enviar_mensaje as db_enviar_mensaje,
    ver_chats as db_ver_chats,
    leer_chat as db_leer_chat,
    agregar_registro_historial,
    obtener_historial_vehiculo
)
from gestor_anuncios import GestorAnuncios
from vehiculo import Vehiculo
from estimador import EstimadorValorReventa

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "39vnv03+$^4"
jwt = JWTManager(app)


@app.route("/")
def index():
    return 'API Compraventa Coches'


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    if not datos or "nombre" not in datos or "contraseña" not in datos:
        return jsonify({"error": "Nombre y contraseña son obligatorios"}), 400
    nombre = datos["nombre"]
    contraseña = datos['contraseña']

    if db_iniciar_sesion(nombre, contraseña):
        access_token = create_access_token(identity=nombre)
        return jsonify(acces_token=access_token), 200
    else:
        return jsonify({"error": "El usuario no existe o credenciales incorrectas"}), 401


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Nombre y contraseña son obligatorios"}), 400
    nombre = datos['nombre']
    contraseña = datos['contraseña']

    if db_registrar_usuario(nombre, contraseña):
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    else:
        return jsonify({"error": "El usuario ya existe o datos inválidos"}), 409


@app.route("/enviar_mensaje", methods=["POST"])
@jwt_required()
def api_enviar_mensaje():
    datos = request.get_json()
    id_emisor = get_jwt_identity()
    id_receptor = datos.get("receptor")
    mensaje = datos.get("mensaje")

    if not id_receptor or not mensaje:
        return jsonify({"error": "Receptor y mensaje son obligatorios"}), 400

    if db_enviar_mensaje(id_emisor, id_receptor, mensaje):
        return jsonify({"mensaje": "Mensaje enviado"}), 200
    else:
        return jsonify({"error": "Error al enviar el mensaje"}), 400


@app.route("/ver_chats", methods=["GET"])
@jwt_required()
def api_ver_chats():
    usuario_actual = get_jwt_identity()
    chats = db_ver_chats(usuario_actual)
    return jsonify({"chats": chats}), 200


@app.route("/leer_chat/<id_receptor>", methods=["GET"])
@jwt_required()
def api_leer_chat(id_receptor):
    id_emisor = get_jwt_identity()
    mensajes = db_leer_chat(id_emisor, id_receptor)
    return jsonify({"mensajes": mensajes}), 200


@app.route("/vehiculo/<id_vehiculo>/historial", methods=["POST"])
@jwt_required()
def agregar_historial(id_vehiculo):
    datos = request.get_json()
    if not datos or "tipo" not in datos or "fecha" not in datos or "descripcion" not in datos:
        return jsonify({"error": "Faltan datos: tipo, fecha, descripción son obligatorios"}), 400

    tipo = datos["tipo"]
    fecha = datos["fecha"]
    descripcion = datos["descripcion"]
    valor_estimado = datos.get("valor_estimado") if tipo == "siniestro" else None

    if tipo not in ["mantenimiento", "revision", "siniestro"]:
        return jsonify({"error": "Tipo de historial no válido"}), 400

    exito = agregar_registro_historial(id_vehiculo, tipo, fecha, descripcion, valor_estimado)
    if exito:
        return jsonify({"mensaje": "Registro añadido correctamente al historial del vehículo"}), 201
    else:
        return jsonify({"error": "Error al añadir el registro al historial del vehículo"}), 500


@app.route("/vehiculo/<id_vehiculo>/historial", methods=["GET"])
@jwt_required()
def ver_historial(id_vehiculo):
    historial = obtener_historial_vehiculo(id_vehiculo)
    return jsonify({"historial": historial}), 200


@app.route("/quien_soy", methods=["GET"])
@jwt_required()
def quien_soy():
    return jsonify({"usuario": get_jwt_identity()}), 200


@app.route("/anuncios", methods=["GET"])
def obtener_anuncios():
    gestor = GestorAnuncios()
    anuncios_todos_obj = gestor.cargar_anuncios()

    marca_filtro = request.args.get('marca', default=None, type=str)
    modelo_filtro = request.args.get('modelo', default=None, type=str)
    anio_min_filtro = request.args.get('anio_min', default=None, type=int)
    anio_max_filtro = request.args.get('anio_max', default=None, type=int)
    precio_min_filtro = request.args.get('precio_min', default=None, type=float)
    precio_max_filtro = request.args.get('precio_max', default=None, type=float)

    anuncios_serializados = []
    for anuncio_obj in anuncios_todos_obj:
        if marca_filtro and marca_filtro.lower() not in anuncio_obj.marca.lower():
            continue
        if modelo_filtro and modelo_filtro.lower() not in anuncio_obj.modelo.lower():
            continue
        if anio_min_filtro and anuncio_obj.año < anio_min_filtro:
            continue
        if anio_max_filtro and anuncio_obj.año > anio_max_filtro:
            continue
        if precio_min_filtro and anuncio_obj.precio < precio_min_filtro:
            continue
        if precio_max_filtro and anuncio_obj.precio > precio_max_filtro:
            continue

        anuncios_serializados.append({
            "marca": anuncio_obj.marca, "modelo": anuncio_obj.modelo, "año": anuncio_obj.año,
            "kilometros": anuncio_obj.kilometros, "precio": anuncio_obj.precio,
            "descripcion": anuncio_obj.descripcion, "destacado": anuncio_obj.destacado,
            "anunciante": anuncio_obj.anunciante
        })
    return jsonify({"anuncios": anuncios_serializados}), 200


@app.route("/publicar_anuncio", methods=["POST"])
@jwt_required()
def publicar_anuncio():
    datos = request.get_json()
    anunciante = get_jwt_identity()

    try:
        vehiculo_nuevo = Vehiculo(
            marca=datos["marca"], modelo=datos["modelo"], año=int(datos["año"]),
            kilometros=int(datos["kilometros"]), precio=float(datos["precio"]),
            descripcion=datos["descripcion"], anunciante=anunciante
        )
        gestor = GestorAnuncios()
        gestor.publicar(vehiculo_nuevo)
        return jsonify({"mensaje": "Anuncio publicado correctamente"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta el campo: {e}"}), 400
    except ValueError:
        return jsonify({"error": "Datos inválidos para año, kilómetros o precio. Deben ser numéricos."}), 400
    except Exception as e:
        return jsonify({"error": f"Error al publicar anuncio: {str(e)}"}), 500


@app.route("/estimar_valor_reventa", methods=["POST"])
@jwt_required()
def estimar_valor_reventa_api():
    datos = request.get_json()
    marca = datos.get("marca")
    modelo = datos.get("modelo")
    anio = datos.get("anio")
    kilometraje = datos.get("kilometraje")

    if not all([marca, modelo, anio is not None, kilometraje is not None]):
        return jsonify({"error": "Faltan datos: marca, modelo, año y kilometraje son obligatorios"}), 400

    try:
        gestor_anuncios = GestorAnuncios()
        anuncios = gestor_anuncios.cargar_anuncios()
        datos_mercado = {}
        for a in anuncios:
            m_key = a.marca.lower()
            mo_key = a.modelo.lower()
            if m_key not in datos_mercado:
                datos_mercado[m_key] = {}
            if mo_key not in datos_mercado[m_key]:
                datos_mercado[m_key][mo_key] = {"precios": []}
            datos_mercado[m_key][mo_key]["precios"].append(a.precio)

        for m_key in datos_mercado:
            for mo_key in datos_mercado[m_key]:
                precios = datos_mercado[m_key][mo_key]["precios"]
                if precios:
                    datos_mercado[m_key][mo_key] = {"valor_base": sum(precios) / len(precios)}
                else:
                    datos_mercado[m_key][mo_key] = {"valor_base": 0}

        marca_key_req = marca.lower()
        modelo_key_req = modelo.lower()

        if marca_key_req not in datos_mercado or modelo_key_req not in datos_mercado[marca_key_req]:
            return jsonify({"error": f"No se encontraron suficientes datos de mercado para {marca} {modelo}."}), 404

        estimador = EstimadorValorReventa(marca_key_req, modelo_key_req, int(anio), int(kilometraje), datos_mercado)
        valor = estimador.calcular_valor_reventa()
        reporte = estimador.generar_reporte_estimacion()
        return jsonify({"valor_estimado": valor, "reporte": reporte}), 200
    except ValueError:
        return jsonify({"error": "Año o kilometraje deben ser numéricos."}), 400
    except Exception as e:
        return jsonify({"error": f"Error calculando valor de reventa: {str(e)}"}), 500


@app.route("/usuarios/me/anuncios", methods=["GET"])
@jwt_required()
def obtener_mis_anuncios_publicados():
    usuario_actual = get_jwt_identity()
    gestor = GestorAnuncios()
    todos_los_anuncios_obj = gestor.cargar_anuncios()

    mis_anuncios_publicados_serializados = []
    for anuncio_obj in todos_los_anuncios_obj:
        if anuncio_obj.anunciante == usuario_actual:
            mis_anuncios_publicados_serializados.append({
                "marca": anuncio_obj.marca, "modelo": anuncio_obj.modelo, "año": anuncio_obj.año,
                "kilometros": anuncio_obj.kilometros, "precio": anuncio_obj.precio,
                "descripcion": anuncio_obj.descripcion, "destacado": anuncio_obj.destacado,
                "anunciante": anuncio_obj.anunciante
            })
    return jsonify({"anuncios_publicados": mis_anuncios_publicados_serializados}), 200


@app.route("/comprar_vehiculo", methods=["POST"])
@jwt_required()
def api_comprar_vehiculo():
    datos_solicitud = request.get_json()
    if not datos_solicitud:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    comprador_actual_id = get_jwt_identity()
    marca_req = datos_solicitud.get("marca")
    modelo_req = datos_solicitud.get("modelo")
    año_req = datos_solicitud.get("año")
    anunciante_req = datos_solicitud.get("anunciante")

    if not all([marca_req, modelo_req, año_req is not None, anunciante_req]):
        return jsonify({"error": "Faltan identificadores del vehículo (marca, modelo, año, anunciante)"}), 400

    if comprador_actual_id == anunciante_req:
        return jsonify({"error": "No puedes comprar tu propio anuncio."}), 400

    try:
        año_req_int = int(año_req)
    except ValueError:
        return jsonify({"error": "El año del vehículo debe ser un número."}), 400

    gestor = GestorAnuncios()
    anuncios_actuales = gestor.cargar_anuncios()
    anuncio_a_comprar = None
    indice_anuncio_a_comprar = -1

    for i, anuncio in enumerate(anuncios_actuales):
        if (anuncio.marca == marca_req and
                anuncio.modelo == modelo_req and
                anuncio.año == año_req_int and
                anuncio.anunciante == anunciante_req):
            anuncio_a_comprar = anuncio
            indice_anuncio_a_comprar = i
            break

    if anuncio_a_comprar is None:
        return jsonify({"error": "El vehículo seleccionado no está disponible o no se encontró."}), 404

    try:
        vehiculo_comprado_detalles = {
            "marca": anuncio_a_comprar.marca, "modelo": anuncio_a_comprar.modelo,
            "año": anuncio_a_comprar.año, "kilometros": anuncio_a_comprar.kilometros,
            "precio": anuncio_a_comprar.precio, "descripcion": anuncio_a_comprar.descripcion,
            "anunciante": anuncio_a_comprar.anunciante
        }

        anuncios_actuales.pop(indice_anuncio_a_comprar)
        gestor.guardar_anuncios(anuncios_actuales)

        return jsonify({
            "mensaje": "Compra realizada con éxito. El anuncio ha sido retirado.",
            "vendedor_nombre": anuncio_a_comprar.anunciante,
            "vehiculo_comprado": vehiculo_comprado_detalles
        }), 200
    except Exception as e:
        app.logger.error(f"Error al procesar la compra en backend: {e}")
        return jsonify({"error": f"Error interno al procesar la compra."}), 500


if __name__ == "__main__":
    crear_bd()
    app.run(debug=True, port=5050)