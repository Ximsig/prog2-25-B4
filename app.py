from flask import Flask, render_template, request, flash, session, url_for, redirect
from sql_usuarios import iniciar_sesion, registrar_usuario, crear_bd # sql_usuarios.py en la rama de registros


app = Flask(__name__)
app.secret_key = "183buc80y01c91ñ21z$%//$Cc12%"
@app.route("/")
def index():
    crear_bd()
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form["usuario"]
        contraseña = request.form["contrasena"]
        
        if iniciar_sesion(nombre, contraseña):  # Esta es tu función propia
            session["usuario"] = nombre
            return 'Implementar esta parte. Ver anuncios, crear anuncios, buscar...'  # O a donde quieras llevar al usuario
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login"))
        
    return render_template("login.html") 

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"]
        confirmar = request.form["confirmar"]

        # Validación de campos vacíos
        if not usuario or not contrasena or not confirmar:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for("registro"))

        # Verificación de contraseñas
        if contrasena != confirmar:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for("registro"))

        # Intentar registrar al usuario
        creado = registrar_usuario(usuario, contrasena)
        if creado:
            flash("Registrado correctamente, por favor, inicie sesión")
            return redirect(url_for("login"))
        else:
            flash("No se pudo registrar el usuario. Es posible que ya exista.")
            return redirect(url_for("registro"))

    return render_template("registro.html")


@app.route("/valoraciones")
def valoraciones():
    return render_template("valoraciones.html")

if __name__ == "__main__":
    app.run(debug=True)
