from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import *
from gestor_anuncios import GestorAnuncios
from vehiculo import Vehiculo
from estimador import EstimadorValorReventa

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "39vnv03+$^4"
jwt = JWTManager(app)



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
            "marca": anuncio_obj.marca,
            "modelo": anuncio_obj.modelo,
            "año": anuncio_obj.año,
            "kilometros": anuncio_obj.kilometros,
            "precio": anuncio_obj.precio,
            "descripcion": anuncio_obj.descripcion,
            "destacado": anuncio_obj.destacado,
            "anunciante": anuncio_obj.anunciante
        })

    return jsonify({"anuncios": anuncios_serializados}), 200

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
                "marca": anuncio_obj.marca,
                "modelo": anuncio_obj.modelo,
                "año": anuncio_obj.año,
                "kilometros": anuncio_obj.kilometros,
                "precio": anuncio_obj.precio,
                "descripcion": anuncio_obj.descripcion,
                "destacado": anuncio_obj.destacado,
                "anunciante": anuncio_obj.anunciante
            })

    return jsonify({"anuncios_publicados": mis_anuncios_publicados_serializados}), 200


if __name__ == "__main__":
    crear_bd()
    app.run(debug=True, port=5050)