from reportlab.pdfgen import canvas

def generar_contrato_pdf(comprador, vendedor, vehiculo):
    """
    Genera un contrato de compraventa simple en PDF.
    Parámetros:
    - comprador (Usuario): el que compra.
    - vendedor (Usuario): el que vende.
    - vehiculo (Vehiculo): el vehículo vendido.
    """
    nombre_archivo = f"contrato_{vehiculo.matricula}.pdf"
    c = canvas.Canvas(nombre_archivo)

    c.drawString(100, 800, "CONTRATO DE COMPRAVENTA")

    c.drawString(100, 760, f"Comprador: {comprador.nombre}")
    c.drawString(100, 740, f"Vendedor: {vendedor.nombre}")

    c.drawString(100, 700, "Datos del vehículo:")
    c.drawString(120, 680, f"Marca: {vehiculo.marca}")
    c.drawString(120, 660, f"Modelo: {vehiculo.modelo}")
    c.drawString(120, 640, f"Matrícula: {vehiculo.matricula}")
    c.drawString(120, 620, f"Precio: {vehiculo.precio} €")

    c.drawString(100, 580, "Ambas partes acuerdan la compraventa del vehículo en las condiciones descritas.")

    c.drawString(100, 520, "Firma del comprador: ____________________")
    c.drawString(100, 500, "Firma del vendedor: _____________________"

    c.save()
    print(f"Contrato guardado como {nombre_archivo}")
