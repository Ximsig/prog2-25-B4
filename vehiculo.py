import random

class Vehiculo:
    def __init__(self, marca, modelo, año, kilometros, precio, descripcion, anunciante, id=None, destacado=False):
        self.id = id if id is not None else random.randint(1000, 9999)
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometros = kilometros
        self.precio = precio
        self.descripcion = descripcion
        self.destacado = destacado
        self.anunciante = anunciante

    def to_csv(self):
        return f"{self.id},{self.marca},{self.modelo},{self.año},{self.kilometros},{self.precio},{self.descripcion},{int(self.destacado)},{self.anunciante}"

    @staticmethod
    def from_csv(linea):
        partes = linea.strip().split(",")
        return Vehiculo(
            marca=partes[1],
            modelo=partes[2],
            año=int(partes[3]),
            kilometros=int(partes[4]),
            precio=float(partes[5]),
            descripcion=partes[6],
            destacado=bool(int(partes[7])),
            anunciante=partes[8],
            id=int(partes[0])
        )
