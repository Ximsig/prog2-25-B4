class Vehiculo:
    def __init__(self, marca, modelo, año, kilometros, precio, descripcion, destacado=False):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometros = kilometros
        self.precio = precio
        self.descripcion = descripcion
        self.destacado = destacado

    def __str__(self):
        estrella = " ⭐" if self.destacado else ""
        return f"{self.marca} {self.modelo} ({self.año}) - {self.kilometros}km - {self.precio}€{estrella}\n  {self.descripcion}"

    def to_csv(self):
        return f"{self.marca},{self.modelo},{self.año},{self.kilometros},{self.precio},{self.descripcion},{int(self.destacado)}"

    @staticmethod
    def from_csv(linea):
        try:
            partes = linea.strip().split(",")
            return Vehiculo(partes[0], partes[1], int(partes[2]), int(partes[3]), float(partes[4]), partes[5], bool(int(partes[6])))
        except Exception as e:
            raise ValueError("Línea inválida en el archivo de vehículos.") from e
