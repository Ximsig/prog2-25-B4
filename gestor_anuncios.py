from vehiculo import Vehiculo

class GestorAnuncios:
    def __init__(self, archivo='anuncios.csv', plataforma=None):
        self.archivo = archivo
        self.plataforma = plataforma 

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
            
    def obtener_usuario_por_nombre(self, nombre):
        return next((u for u in self.plataforma.usuarios if u.nombre == nombre), None)

    def realizar_compra(self, comprador_nombre, id_vehiculo):
        # Primero buscar el vehículo
        vehiculo = self.buscar_vehiculo_por_id(id_vehiculo)
        if not vehiculo:
            return False, "Vehículo no encontrado"

        # Asegurarse de que el vendedor exista
        vendedor_nombre = vehiculo.anunciante
        if not vendedor_nombre:
            return False, "Vendedor no especificado"

        # Crear vendedor si no existe
        vendedor = self.obtener_usuario_por_nombre(vendedor_nombre)
        if vendedor is None:
            from usuarios import Usuario
            vendedor = Usuario(vendedor_nombre)
            self.plataforma.usuarios.append(vendedor)

        # Obtener o crear comprador
        comprador = self.obtener_usuario_por_nombre(comprador_nombre)
        if comprador is None:
            from usuarios import Usuario
            comprador = Usuario(comprador_nombre)
            self.plataforma.usuarios.append(comprador)

        # Realizar la compra
        anuncios = self.cargar_anuncios()
        index = next((i for i, v in enumerate(anuncios) if str(v.id) == str(id_vehiculo)), -1)
        
        if index == -1:
            return False, "Vehículo no encontrado"

        # Actualizar historial
        comprador.agregar_historial(vehiculo, "Compra")
        vendedor.agregar_historial(vehiculo, "Venta")

        # Eliminar anuncio
        del anuncios[index]
        self.guardar_anuncios(anuncios)

        return True, None

    def buscar_vehiculo_por_id(self, id_vehiculo):
        anuncios = self.cargar_anuncios()
        for a in anuncios:
            if str(a.id) == str(id_vehiculo):
                return a
        return None
