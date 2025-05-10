from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sql_usuarios import iniciar_sesion, registrar_usuario, crear_bd

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


if __name__ == "__main__":
    app.run(debug=True, port=5050)  
