from vehiculo import Vehiculo

class GestorAnuncios:
    def __init__(self, archivo='anuncios.csv'):
        self.archivo = archivo

    def cargar_anuncios(self):
        anuncios = []
        try:
            with open(self.archivo, 'r') as f:
                for linea in f:
                    anuncios.append(Vehiculo.from_csv(linea))
        except FileNotFoundError:
            open(self.archivo, 'w').close()  # Crea archivo vacío si no existe
        return anuncios

    def guardar_anuncios(self, anuncios):
        with open(self.archivo, 'w') as f:
            for v in anuncios:
                f.write(v.to_csv() + '\n')

    def publicar(self, vehiculo):
        anuncios = self.cargar_anuncios()
        anuncios.append(vehiculo)
        self.guardar_anuncios(anuncios)

    def listar(self):
        anuncios = self.cargar_anuncios()
        for i, v in enumerate(anuncios):
            print(f"[{i}] {v}")

    def editar(self, index, nuevo_vehiculo):
        anuncios = self.cargar_anuncios()
        if 0 <= index < len(anuncios):
            anuncios[index] = nuevo_vehiculo
            self.guardar_anuncios(anuncios)
        else:
            print("Índice inválido.")

    def eliminar(self, index):
        anuncios = self.cargar_anuncios()
        if 0 <= index < len(anuncios):
            del anuncios[index]
            self.guardar_anuncios(anuncios)
        else:
            print("Índice inválido.")

    def destacar(self, index):
        anuncios = self.cargar_anuncios()
        if 0 <= index < len(anuncios):
            anuncios[index].destacado = True
            self.guardar_anuncios(anuncios)
        else:
            print("Índice inválido.")