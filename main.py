from database import crear_bd, registrar_usuario, iniciar_sesion, mostrar_usuarios, crear_chat, enviar_mensaje, leer_chat, ver_chats
from usuarios import Usuario, Vehiculo as VehiculoPlataforma, Plataforma
from contratos import generar_contrato_pdf
from estimador import EstimadorValorReventa
from historial import HistorialDelVehiculo
from gestor_anuncios import GestorAnuncios
from vehiculo import Vehiculo as VehiculoAnuncio
from Sistema_filtros_busq import Coche, SistemaCoches
from datetime import datetime

def main():
    # Inicializar componentes
    crear_bd()  # Crear base de datos si no existe
    plataforma = Plataforma()
    gestor_anuncios = GestorAnuncios()
    datos_mercado = {
        "Toyota Corolla": {"valor_base": 20000},
        "Ford Focus": {"valor_base": 18000},
        "BMW Serie 3": {"valor_base": 35000}
    }

    usuario_actual = None

    while True:
        print("\n=== Sistema de Compraventa de Vehículos ===")
        if usuario_actual:
            print(f"Usuario actual: {usuario_actual.nombre} ({'Comprador' if usuario_actual.es_comprador else 'Vendedor'})")
        else:
            print("No has iniciado sesión.")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Mostrar usuarios")
        print("4. Agregar vehículo (vendedor)")
        print("5. Mostrar vehículos disponibles")
        print("6. Realizar compra")
        print("7. Crear chat")
        print("8. Enviar mensaje")
        print("9. Leer chat")
        print("10. Ver todos los chats")
        print("11. Estimar valor de reventa")
        print("12. Gestionar historial de vehículo")
        print("13. Publicar anuncio")
        print("14. Listar anuncios")
        print("15. Buscar vehículos con filtros")
        print("16. Mostrar historial de usuario")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")
                es_comprador = input("¿Es comprador? (s/n): ").lower() == 's'
                plataforma.registrar_usuario(nombre, contraseña, es_comprador)

            elif opcion == "2":
                nombre = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")
                usuario = plataforma.iniciar_sesion(nombre, contraseña)
                if usuario:
                    usuario_actual = usuario

            elif opcion == "3":
                mostrar_usuarios()

            elif opcion == "4":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                elif usuario_actual.es_comprador:
                    print("Solo los vendedores pueden agregar vehículos.")
                else:
                    marca = input("Marca: ")
                    modelo = input("Modelo: ")
                    matricula = input("Matrícula: ")
                    precio = float(input("Precio: "))
                    plataforma.agregar_vehiculo(marca, modelo, matricula, precio, usuario_actual)

            elif opcion == "5":
                plataforma.mostrar_vehiculos()

            elif opcion == "6":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                elif not usuario_actual.es_comprador:
                    print("Solo los compradores pueden realizar compras.")
                else:
                    plataforma.mostrar_vehiculos()
                    matricula = input("Matrícula del vehículo a comprar: ")
                    vehiculo = next((v for v in plataforma.vehiculos if v.matricula == matricula), None)
                    if vehiculo:
                        vendedor = next((u for u in plataforma.usuarios if not u.es_comprador), None)
                        if vendedor:
                            plataforma.realizar_compra(usuario_actual, vehiculo)
                            generar_contrato_pdf(usuario_actual, vendedor, vehiculo)
                        else:
                            print("No hay vendedores disponibles para generar el contrato.")
                    else:
                        print("Vehículo no encontrado.")

            elif opcion == "7":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                else:
                    id_usuario2 = input("Nombre del otro usuario: ")
                    crear_chat(usuario_actual.nombre, id_usuario2)

            elif opcion == "8":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                else:
                    id_receptor = input("Nombre del receptor: ")
                    mensaje = input("Mensaje: ")
                    enviar_mensaje(usuario_actual.nombre, id_receptor, mensaje)

            elif opcion == "9":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                else:
                    id_receptor = input("Nombre del otro usuario: ")
                    leer_chat(usuario_actual.nombre, id_receptor)

            elif opcion == "10":
                ver_chats()

            elif opcion == "11":
                modelo = input("Modelo del vehículo: ")
                anio = int(input("Año: "))
                kilometraje = float(input("Kilometraje: "))
                estimador = EstimadorValorReventa(modelo, anio, kilometraje, datos_mercado)
                print(estimador.generar_reporte_estimacion())

            elif opcion == "12":
                historial = HistorialDelVehiculo()
                while True:
                    print("\n--- Gestionar Historial ---")
                    print("1. Agregar mantenimiento")
                    print("2. Agregar revisión")
                    print("3. Agregar siniestro")
                    print("4. Generar informe de siniestralidad")
                    print("0. Volver")
                    sub_opcion = input("Selecciona una opción: ")

                    if sub_opcion == "1":
                        fecha = input("Fecha (YYYY-MM-DD): ")
                        descripcion = input("Descripción: ")
                        historial.agregar_mantenimiento(fecha, descripcion)
                    elif sub_opcion == "2":
                        fecha = input("Fecha (YYYY-MM-DD): ")
                        descripcion = input("Descripción: ")
                        historial.agregar_revision(fecha, descripcion)
                    elif sub_opcion == "3":
                        fecha = input("Fecha (YYYY-MM-DD): ")
                        descripcion = input("Descripción: ")
                        valor = input("Valor estimado: ")
                        historial.agregar_siniestro(fecha, descripcion, valor)
                    elif sub_opcion == "4":
                        print(historial.generar_informe_siniestralidad())
                    elif sub_opcion == "0":
                        break
                    else:
                        print("Opción inválida.")

            elif opcion == "13":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                else:
                    marca = input("Marca: ")
                    modelo = input("Modelo: ")
                    año = int(input("Año: "))
                    kilometros = int(input("Kilómetros: "))
                    precio = float(input("Precio: "))
                    descripcion = input("Descripción: ")
                    vehiculo = VehiculoAnuncio(marca, modelo, año, kilometros, precio, descripcion)
                    gestor_anuncios.publicar(vehiculo)

            elif opcion == "14":
                gestor_anuncios.listar()

            elif opcion == "15":
                coches = [
                    Coche(20000, "Toyota", "Corolla", 2018, 50000, "Gasolina", datetime(2025, 1, 1)),
                    Coche(18000, "Ford", "Focus", 2017, 60000, "Diésel", datetime(2025, 2, 1)),
                    Coche(35000, "BMW", "Serie 3", 2020, 30000, "Gasolina", datetime(2025, 3, 1))
                ]
                sistema = SistemaCoches(coches)
                filtros = {}
                precio_max = input("Precio máximo (o Enter para omitir): ")
                if precio_max:
                    filtros["precio_max"] = float(precio_max)
                marca = input("Marca (o Enter para omitir): ")
                if marca:
                    filtros["marca"] = marca
                resultados = sistema.buscar(filtros)
                resultados = sistema.ordenar(resultados, "precio")
                for coche in resultados:
                    print(coche)

            elif opcion == "16":
                if not usuario_actual:
                    print("Debes iniciar sesión.")
                else:
                    usuario_actual.mostrar_historial()

            elif opcion == "0":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()