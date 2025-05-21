import random
from database import registrar_usuario, iniciar_sesion as db_iniciar_sesion

class Usuario:
    # Clase que representa a un usuario dentro de la plataforma
    def __init__(self, nombre: str, es_comprador: bool = True):
        """
        Constructor de la clase Usuario.
        Parámetros:
        - nombre (str): nombre único del usuario.
        - es_comprador (bool, opcional): indica si es comprador (True) o vendedor (False).
        """
        self.nombre = nombre
        self.es_comprador = es_comprador
        self.historial = []

    def __str__(self):
        """
        Devuelve una representación en string del usuario.
        """
        return f"{self.nombre} ({'Comprador' if self.es_comprador else 'Vendedor'})"

    def agregar_historial(self, vehiculo, tipo_transaccion: str):
        """
        Agrega una entrada al historial del usuario.
        Parámetros:
        - vehiculo (Vehiculo): objeto del vehículo comprado o vendido.
        - tipo_transaccion (str): tipo de transacción ('Compra' o 'Venta').
        """
        self.historial.append(f"{tipo_transaccion} de {vehiculo}")

    def mostrar_historial(self):
        """
        Muestra todas las transacciones del historial del usuario.
        """
        if not self.historial:
            print(f"No hay historial de {self.nombre}")
        else:
            for transaccion in self.historial:
                print(transaccion)


class Vehiculo:
    # Clase que representa un vehículo que puede estar en venta
    def __init__(self, marca: str, modelo: str, matricula: str, precio: float):
        """
        Constructor de la clase Vehiculo.
        Parámetros:
        - marca (str): marca del vehículo.
        - modelo (str): modelo del vehículo.
        - matricula (str): matrícula del vehículo (identificador único).
        - precio (float): precio del vehículo.
        """
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula
        self.precio = precio
        self.id = random.randint(100, 999)

    def __str__(self):
        """
        Devuelve una representación en string del vehículo.
        """
        return f"{self.marca} {self.modelo} {self.matricula} {self.precio}"


class Plataforma:
    def __init__(self):
        """
        Constructor de Plataforma. Inicializa las listas de usuarios y vehículos.
        """
        self.usuarios = [] # Lista de usuarios
        self.vehiculos = [] # Lista de vehículos disponibles en venta

    def registrar_usuario(self, nombre: str, contraseña: str, es_comprador: bool = True):
        """
        Registra un nuevo usuario, tanto en la base de datos como en memoria.
        Parámetros:
        - nombre (str): nombre del nuevo usuario.
        - contraseña (str): contraseña en texto plano (se guarda en hash).
        - es_comprador (bool): True si es comprador, False si es vendedor.
        """
        if registrar_usuario(nombre, contraseña):
            usuario = Usuario(nombre, es_comprador)
            self.usuarios.append(usuario)
            print(f"Usuario registrado: {usuario.nombre}")

    def iniciar_sesion(self, nombre: str, contraseña: str):
        """
        Inicia sesión verificando las credenciales en la base de datos.

        Parámetros:
        - nombre (str): nombre del usuario.
        - contraseña (str): contraseña en texto plano.

        Si las credenciales son correctas, carga el usuario en memoria si no estaba ya.
        """
        if db_iniciar_sesion(nombre, contraseña):
            usuario = next((u for u in self.usuarios if u.nombre == nombre), None)
            if usuario is None:
                usuario = Usuario(nombre)
                self.usuarios.append(usuario)
            print(f"Sesión iniciada: {usuario.nombre}")
            return usuario
        else:
            print("Inicio de sesión fallido.")

    def agregar_vehiculo(self, marca: str, modelo: str, matricula: str, precio: float, vendedor: Usuario):
        """
        Permite a un vendedor agregar un vehículo en venta.
        Parámetros:
        - marca (str): marca del vehículo.
        - modelo (str): modelo del vehículo.
        - matricula (str): matrícula del vehículo.
        - precio (float): precio de venta.
        - vendedor (Usuario): usuario que está intentando vender.
        """
        if not vendedor.es_comprador:
            vehiculo = Vehiculo(marca, modelo, matricula, precio)
            self.vehiculos.append(vehiculo)
            print(f"Vehículo {vehiculo} registrado por {vendedor.nombre}")
        else:
            print("Los compradores no pueden vender vehículos.")

    def mostrar_vehiculos(self):
        """
        Muestra todos los vehículos disponibles en venta.
        """
        if not self.vehiculos:
            print("No hay vehículos disponibles")
        else:
            for v in self.vehiculos:
                print(v)

    def realizar_compra(self, comprador: Usuario, vehiculo: Vehiculo):
        """
       Registra la compra de un vehículo por un comprador.base de datos
       Parámetros:
       - comprador (Usuario): usuario que compra.
       - vehiculo (Vehiculo): vehículo que se desea comprar.
       """
        if vehiculo in self.vehiculos:
            comprador.agregar_historial(vehiculo, 'Compra')
            self.vehiculos.remove(vehiculo)
            print(f"{comprador.nombre} ha comprado el vehículo {vehiculo}")
        else:
            print("El vehículo no está disponible")