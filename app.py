from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return "<h2>Página de Inicio de Sesión</h2>"

@app.route("/registro")
def registro():
    return "<h2>Página de Registro</h2>"

@app.route("/valoraciones")
def valoraciones():
    return "<h2>Página de valoraciones<h2>"

if __name__ == "__main__":
    app.run(debug=True)
