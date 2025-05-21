# [Compramos_Tu_Coche]
[//]: # (Incluid aquí la descripción de vuestra aplicación. Por cierto, así se ponen comentarios en Markdown)

## Autores

* (Coordinador)[Joaquín Sigüenza Chilar](https://github.com/Ximsig)
* [Juan Carlos Valentin Pérez](https://github.com/alumno1)
* [Sandra Crevillen Contreras](https://github.com/alumno3)
* [Jorge Soto Tripiana](https://github.com/alumno4)
* [NIcolás Sanchez Saura](https://github.com/alumno5)

## Profesor
[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
[//]: # (Indicad aquí los requisitos de vuestra aplicación, así como el alumno responsable de cada uno de ellos)
* Registro de usuarios (compradores y vendedores), base de datos y generación de contratos (Sandra)
* Publicación del producto (creación, edición y eliminación de anuncios, así como la posibilidad de destacarlos mediante pago) (Nicolás)
* Historial completo del vehículo (informe de siniestralidad y mantenimientos), herramienta de estimación de valor de reventa (Joaquín)
* Sistema de búsqueda y ordenación (con filtros por precio, marca, modelo, año, kilometraje, etc.) (Juan Carlos)
* Chat entre compradores y vendedores y valoraciones y reseñas de los usuarios (Jorge)
* Integración de la API (entre todos)

## Instrucciones de instalación y ejecución
[//]: # (Indicad aquí qué habría que hacer para ejecutar vuestra aplicación)
Instalación
Clona o descarga el repositorio del proyecto en tu máquina local.

Abre una terminal y navega a la carpeta raíz del proyecto.

(Opcional pero recomendado) Crea un entorno virtual y actívalo:

bash
Copiar
python -m venv env
# Windows
env\Scripts\activate
# Linux / macOS
source env/bin/activate
Instala las dependencias necesarias:

bash
Copiar
pip install -r requirements.txt
Si no tienes un archivo requirements.txt, instala manualmente:

bash
Copiar
pip install flask flask-jwt-extended requests
(Agrega otras librerías que uses en el proyecto.)

Ejecución del servidor API
En la terminal, asegúrate de estar en la carpeta raíz del proyecto y con el entorno virtual activado.

Ejecuta el servidor Flask con:

bash
Copiar
python app.py
El servidor correrá por defecto en http://127.0.0.1:5050/

Verifica que esté corriendo abriendo en el navegador http://127.0.0.1:5050/ — debería mostrar un mensaje de bienvenida.

Uso del cliente (ejemplo de interacción)
En otra terminal, con entorno virtual activado, ejecuta:

bash
Copiar
python examples.py

# Sigue el menú interactivo para:

Registrar usuarios

Iniciar sesión

Publicar anuncios

Comprar vehículos

Enviar mensajes, etc.

Notas adicionales
La base de datos se crea automáticamente la primera vez que arrancas la API.

Las rutas y funcionalidades están definidas en app.py.

El cliente examples.py se comunica con la API vía HTTP.

Para producción, cambia la clave JWT en app.py por una segura.

## Resumen de la API
[//]: # Esta es una API web básica construida con Flask que permite a los usuarios registrarse, iniciar sesión y acceder a diferentes secciones como valoraciones. Incluye manejo de sesiones, validaciones simples y estructura inicial para expandir funcionalidades como creación y visualización de anuncios.
La API incluye las siguientes rutas:
  / — Página principal e inicialización de la base de datos.
  /login — Página de inicio de sesión.
  /registro — Página de registro de nuevos usuarios.
  /valoraciones — Sección de valoraciones.
