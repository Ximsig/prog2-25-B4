from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import *
from gestor_anuncios import GestorAnuncios
from vehiculo import Vehiculo
from estimador import EstimadorValorReventa
from usuarios import Plataforma
import requests
from examples import listar_anuncios
from contratos import generar_contrato_pdf  # Añade esta importación al inicio

plataforma = Plataforma()
gestor = GestorAnuncios(plataforma=plataforma)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "39vnv03+$^4"  # ¡Usa una clave segura en producción!
jwt = JWTManager(app)
crear_bd()


@app.route("/")
def index():
    return 'API Compraventa Coches'
    


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    if not datos or "nombre" not in datos or "contraseña" not in datos:
        return {"error": "Nombre y contraseña son obligatorios"}, 400

    nombre = datos["nombre"]
    contraseña = datos["contraseña"]

    if iniciar_sesion(nombre, contraseña):
        token = create_access_token(identity=nombre)

        usuario = next((u for u in plataforma.usuarios if u.nombre == nombre), None)
        if usuario is None:
            from usuarios import Usuario
            plataforma.usuarios.append(Usuario(nombre))

        return {"access_token": token}, 200 
    else:
        return {"error": "El usuario no existe o credenciales incorrectas"}, 401


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json() # datos de la peticion del usuario

    if not datos or 'nombre' not in datos or 'contraseña' not in datos:
        return {"error": "Nombre y contraseña son obligatorios"}, 400 
    nombre = datos['nombre']
    contraseña = datos['contraseña']

    if registrar_usuario(nombre, contraseña):
        return {"mensaje": "Usuario registrado exitosamente"}, 201 
    else:
        return {"error": "El usuario ya existe o datos inválidos"}, 409

@app.route("/enviar_mensaje", methods=["POST"])
@jwt_required()
def api_enviar_mensaje():
    datos = request.get_json()
    id_emisor = get_jwt_identity()
    id_receptor = datos.get("receptor")
    mensaje = datos.get("mensaje")

    if not id_receptor or not mensaje:
        return {"error": "Receptor y mensaje son obligatorios"}, 400
    
    if enviar_mensaje(id_emisor, id_receptor, mensaje):
        return {"mensaje": "Mensaje enviado"}, 200
    else:
        return {"error": "Error al enviar el mensaje"}, 400

@app.route("/ver_chats", methods=["GET"])
@jwt_required()
def api_ver_chats():
    usuario_actual = get_jwt_identity()
    chats = ver_chats(usuario_actual)  
    return {"chats": chats}, 200

@app.route("/leer_chat/<id_receptor>", methods=["GET"])
@jwt_required()
def api_leer_chat(id_receptor):
    id_emisor = get_jwt_identity()
    mensajes = leer_chat(id_emisor, id_receptor)
    return {"mensajes": mensajes}, 200



@app.route("/vehiculo/<id_vehiculo>/historial", methods=["POST"])
@jwt_required()
def agregar_historial(id_vehiculo):
    datos = request.get_json()
    if not datos or "tipo" not in datos or "fecha" not in datos or "descripcion" not in datos:
        return {"error": "Faltan datos"}, 400

    tipo = datos["tipo"]
    fecha = datos["fecha"]
    descripcion = datos["descripcion"]
    valor_estimado = datos.get("valor_estimado") if tipo == "siniestro" else None

    if tipo not in ["mantenimiento", "revision", "siniestro"]:
        return {"error": "Tipo no válido"}, 400

    exito = agregar_registro_historial(id_vehiculo, tipo, fecha, descripcion, valor_estimado)
    if exito:
        return {"mensaje": "Registro añadido correctamente"}, 201
    else:
        return {"error": "Error al añadir el registro"}, 500

@app.route("/vehiculo/<id_vehiculo>/historial", methods=["GET"])
@jwt_required()
def ver_historial(id_vehiculo):
    historial = obtener_historial_vehiculo(id_vehiculo)
    return {"historial": historial}, 200
    
# funcion para obtener usuario
@app.route("/quien_soy", methods=["GET"])
@jwt_required()
def quien_soy():
    return {"usuario": get_jwt_identity()}, 200


@app.route("/anuncios", methods=["GET"])
def obtener_anuncios():
    gestor = GestorAnuncios()
    anuncios = gestor.cargar_anuncios()
    return {
        "anuncios": [
            {
                "id": a.id,
                "marca": a.marca,
                "modelo": a.modelo,
                "año": a.año,
                "kilometros": a.kilometros,
                "precio": a.precio,
                "descripcion": a.descripcion,
                "destacado": getattr(a, "destacado", False),  # <-- Añade esto
                "anunciante": a.anunciante
            }
            for a in anuncios
        ]
    }, 200

@app.route("/publicar_anuncio", methods=["POST"])
@jwt_required()
def publicar_anuncio():
    datos = request.get_json()
    anunciante = get_jwt_identity()

    # Asegúrate de que el anunciante está en la plataforma
    usuario = next((u for u in plataforma.usuarios if u.nombre == anunciante), None)
    if usuario is None:
        from usuarios import Usuario
        plataforma.usuarios.append(Usuario(anunciante))

    try:
        vehiculo = Vehiculo(
            marca=datos["marca"],
            modelo=datos["modelo"],
            año=int(datos["año"]),
            kilometros=int(datos["kilometros"]),
            precio=float(datos["precio"]),
            descripcion=datos["descripcion"],
            anunciante=anunciante
        )

        gestor = GestorAnuncios()
        gestor.publicar(vehiculo)

        return {"mensaje": "Anuncio publicado correctamente"}, 201

    except KeyError as e:
        return {"error": f"Falta el campo: {e}"}, 400
    except Exception as e:
        return {"error": f"Error al publicar anuncio: {str(e)}"}, 500
   
@app.route("/estimar_valor_reventa", methods=["POST"])
@jwt_required()
def estimar_valor_reventa_api():
    datos = request.get_json()
    marca = datos.get("marca")
    modelo = datos.get("modelo")
    anio = datos.get("anio")
    kilometraje = datos.get("kilometraje")

    if not marca or not modelo or anio is None or kilometraje is None:
        return {"error": "Faltan datos: marca, modelo, año y kilometraje son obligatorios"}, 400

    try:
        gestor = GestorAnuncios()
        anuncios = gestor.cargar_anuncios()

        # Construir datos_mercado como dict {marca: {modelo: {'valor_base': precio_promedio}}}
        datos_mercado = {}
        for a in anuncios:
            m = a.marca.lower()
            mo = a.modelo.lower()
            if m not in datos_mercado:
                datos_mercado[m] = {}
            if mo not in datos_mercado[m]:
                datos_mercado[m][mo] = {"precios": []}
            datos_mercado[m][mo]["precios"].append(a.precio)

        # Calcular promedio de precios para cada marca-modelo
        for m in datos_mercado:
            for mo in datos_mercado[m]:
                precios = datos_mercado[m][mo]["precios"]
                datos_mercado[m][mo] = {"valor_base": sum(precios) / len(precios)}

        # Usar claves en minúscula para buscar
        marca_key = marca.lower()
        modelo_key = modelo.lower()

        if marca_key not in datos_mercado or modelo_key not in datos_mercado[marca_key]:
            return {"error": f"No se encontraron anuncios para {marca} {modelo}"}, 404

        est = EstimadorValorReventa(marca_key, modelo_key, int(anio), int(kilometraje), datos_mercado)
        valor = est.calcular_valor_reventa()
        reporte = est.generar_reporte_estimacion()
        return jsonify({"valor_estimado": valor, "reporte": reporte}), 200

    except Exception as e:
        return {"error": f"Error calculando valor de reventa: {str(e)}"}, 500
    


@app.route("/realizar_compra", methods=["POST"])
@jwt_required()
def api_realizar_compra():
    comprador_nombre = get_jwt_identity()
    datos = request.get_json()
    id_vehiculo = datos.get("id_vehiculo")

    if not id_vehiculo:
        return {"error": "ID del vehículo es obligatorio"}, 400

    # Buscar el vehículo antes de realizar la compra
    vehiculo = gestor.buscar_vehiculo_por_id(id_vehiculo)
    if not vehiculo:
        return {"error": "Vehículo no encontrado"}, 404

    exito, error = gestor.realizar_compra(comprador_nombre, id_vehiculo)
    if exito:
        try:
            from usuarios import Usuario
            comprador = Usuario(comprador_nombre)
            vendedor = Usuario(vehiculo.anunciante)
            ruta_contrato = generar_contrato_pdf(comprador, vendedor, vehiculo)
            return {
                "mensaje": "Compra realizada con éxito",
                "contrato": ruta_contrato,
                "contrato_generado": True
            }, 200
        except Exception as e:
            return {
                "mensaje": "Compra realizada con éxito",
                "error_contrato": str(e),
                "contrato_generado": False
            }, 200
    else:
        return {"error": error}, 400
    
@app.route("/buscar_vehiculos", methods=["GET"])
def buscar_vehiculos():
    marca = request.args.get("marca", "").lower()
    modelo = request.args.get("modelo", "").lower()
    año = request.args.get("año")
    precio_min = request.args.get("precio_min")
    precio_max = request.args.get("precio_max")

    gestor = GestorAnuncios()
    anuncios = gestor.cargar_anuncios()

    resultados = []
    for a in anuncios:
        if marca and a.marca.lower() != marca:
            continue
        if modelo and a.modelo.lower() != modelo:
            continue
        if año and str(a.año) != str(año):
            continue
        if precio_min and a.precio < float(precio_min):
            continue
        if precio_max and a.precio > float(precio_max):
            continue
        resultados.append({
            "id": a.id,
            "marca": a.marca,
            "modelo": a.modelo,
            "año": a.año,
            "kilometros": a.kilometros,
            "precio": a.precio,
            "descripcion": a.descripcion,
            "anunciante": a.anunciante
        })

    return jsonify({"resultados": resultados}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050)




