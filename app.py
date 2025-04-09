from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        return f'Usuario: {usuario}    Contraseña: {contrasena}'
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        confirmar = request.form["confirmar"]
        return f'Usuario: {usuario}    Contraseña: {contrasena}'
    return render_template("registro.html")

@app.route("/valoraciones")
def valoraciones():
    return render_template("valoraciones.html")

if __name__ == "__main__":
    app.run(debug=True)
