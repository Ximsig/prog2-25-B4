from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import crear_bd, registrar_usuario, iniciar_sesion, mostrar_usuarios, crear_chat, enviar_mensaje, leer_chat, ver_chats, agregar_registro_historial, obtener_historial_vehiculo


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
    contraseña = datos['contraseña']

    if iniciar_sesion(nombre, contraseña):
        token = create_access_token(identity=nombre)
        return {"acces_token": token}, 200 
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

@app.route("/valoraciones")
def valoraciones():
    pass

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


if __name__ == "__main__":
    app.run(debug=True, port=5050)  
