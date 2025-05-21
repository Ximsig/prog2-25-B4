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
        comprador = self.obtener_usuario_por_nombre(comprador_nombre)
        if comprador is None:
            return False, "Usuario comprador no encontrado"
        # Ya no chequeamos es_comprador, porque todos pueden comprar


        vehiculo_con_index = [(i, v) for i, v in enumerate(self.cargar_anuncios()) if str(getattr(v, 'id', '')) == str(id_vehiculo)]
        if not vehiculo_con_index:
            return False, "Vehículo no encontrado"

        index, vehiculo = vehiculo_con_index[0]

        vendedor = self.obtener_usuario_por_nombre(vehiculo.anunciante)
        if vendedor is None:
            return False, "Vendedor no encontrado"

        # Actualizar historial, eliminar anuncio
        comprador.agregar_historial(vehiculo, "Compra")
        vendedor.agregar_historial(vehiculo, "Venta")

        anuncios = self.cargar_anuncios()
        del anuncios[index]
        self.guardar_anuncios(anuncios)

        return True, None
