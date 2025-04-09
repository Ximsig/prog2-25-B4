
import random
from db import registrar_usuario_bd

class Usuario:
    def __init__(self, nombre, apellido, email, es_comprador = True):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.es_comprador = es_comprador
        self.historial = []

    def __str__(self):
        return f"{self.nombre} ({'Comprador' if self.es_comprador else 'Vendedor'})"

    def agregar_historial(self, vehiculo, tipo_transaccion):
        self.historial.append(f" {tipo_transaccion} de {vehiculo}")

    def mostrar_historial(self):
        if not self.historial:
            print("No hay historial de {self.nombre}")
        else:
            for transaccion in self.historial:
                print(transaccion)

class  Vehiculo:
    def __init__(self, marca, modelo, matricula,  precio):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula
        self.precio = precio
        self. id = random.randint(100, 999)  # ID unico para cada vehiculo

    def __str__(self):
        return f" {self.marca} {self.modelo} {self.matricula} {self.precio}"

class Plataforma:
    def __init__(self):
        self.usuarios = []
        self.vehiculos = []

    def registrar_usuario(self, nombre, email, es_comprador = True):
        registrar_usuario_bd(nombre, email, es_comprador)
        nuevo_usuario = Usuario(nombre, email, es_comprador)
        self.usuarios.append(nuevo_usuario)
        print(f" Usuario registrado {nuevo_usuario.nombre}")

    def iniciar_sesion(self, email):
        for usuario in self.usuarios:
            if usuario.email == email:
                return usuario
            else:
                print('Usuario no encontrado')

    def agregar_vehiculo(self, marca, modelo, matricula, precio, vendedor):
        if not vendedor.es_comprador:
            nuevo_vehiculo = Vehiculo(marca, modelo, modelo, precio)
            self.vehiculos.append(nuevo_vehiculo)
            print(f"Vehículo {nuevo_vehiculo} registrado por {vendedor.nombre}")
        else:
            print('El comprador no puede poner vehículos en venta')

    def mostrar_vehiculos(self):
        if not self.vehiculos:
            print("No hay vehiculos disponibles")
        else:
            for vehiculo in self.vehiculos:
                print(vehiculo)

    def realizar_compra(self, comprador, vehiculo):
        if vehiculo in self.vehiculos:
            comprador.agregar_historial(vehiculo, 'Compra')
            self.vehiculos.remove(vehiculo)
            print('f"{comprador.nombre} ha comprado el vehiculo {vehiculo}')
        else:
            print('El vehículo no está disponible')


