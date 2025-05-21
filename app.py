from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import *

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


@app.route("/valoraciones", methods=["GET", "POST"])
def valoraciones():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5050)  
