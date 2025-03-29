from vehiculo import Vehiculo
from gestor_anuncios import GestorAnuncios

gestor = GestorAnuncios()

def menu():
    ejecutando = True

    while ejecutando:
        print("\n--- GESTOR DE ANUNCIOS DE VEHÍCULOS ---")
        print("1. Publicar nuevo vehículo")
        print("2. Ver anuncios")
        print("3. Editar anuncio")
        print("4. Eliminar anuncio")
        print("5. Destacar anuncio")
        print("0. Salir")

        opcion = input("Opción: ")

        try:
            if opcion == '1':
                datos = input("Marca, Modelo, Año, KM, Precio, Descripción: ").split(",")
                vehiculo = Vehiculo(
                    datos[0].strip(), datos[1].strip(), int(datos[2]),
                    int(datos[3]), float(datos[4]), datos[5].strip()
                )
                gestor.publicar(vehiculo)

            elif opcion == '2':
                gestor.listar()

            elif opcion == '3':
                gestor.listar()
                idx = int(input("Índice a editar: "))
                datos = input("Nueva info (Marca, Modelo, Año, KM, Precio, Descripción): ").split(",")
                nuevo = Vehiculo(
                    datos[0].strip(), datos[1].strip(), int(datos[2]),
                    int(datos[3]), float(datos[4]), datos[5].strip()
                )
                gestor.editar(idx, nuevo)

            elif opcion == '4':
                gestor.listar()
                idx = int(input("Índice a eliminar: "))
                gestor.eliminar(idx)

            elif opcion == '5':
                gestor.listar()
                idx = int(input("Índice a destacar: "))
                gestor.destacar(idx)

            elif opcion == '0':
                print("Saliendo del gestor...")
                ejecutando = False

            else:
                print("Opción inválida. Intenta otra vez.")

        except Exception as e:
            print(f"⚠️ Error: {e}")

menu()
