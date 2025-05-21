from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generar_contrato_pdf(comprador, vendedor, vehiculo):
    """
    Genera un contrato de compraventa simple en PDF.
    Parámetros:
    - comprador (Usuario): el que compra.
    - vendedor (Usuario): el que vende.
    - vehiculo (Vehiculo): el vehículo vendido.
    """
    # Crear directorio contratos si no existe
    if not os.path.exists('contratos'):
        os.makedirs('contratos')

    # Generar nombre único para el contrato
    nombre_archivo = f"contratos/contrato_{vehiculo.marca}_{vehiculo.modelo}_{comprador.nombre}.pdf"
    
    c = canvas.Canvas(nombre_archivo)
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "CONTRATO DE COMPRAVENTA DE VEHÍCULO")
    
    # Datos de las partes
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"VENDEDOR: {vendedor.nombre}")
    c.drawString(100, 730, f"COMPRADOR: {comprador.nombre}")
    
    # Datos del vehículo
    c.drawString(100, 680, "DATOS DEL VEHÍCULO:")
    c.drawString(120, 660, f"Marca: {vehiculo.marca}")
    c.drawString(120, 640, f"Modelo: {vehiculo.modelo}")
    c.drawString(120, 620, f"Año: {vehiculo.año}")
    c.drawString(120, 600, f"Kilómetros: {vehiculo.kilometros}")
    c.drawString(120, 580, f"Precio: {vehiculo.precio}€")
    
    # Fecha y firmas
    c.drawString(100, 500, "Fecha: " + datetime.now().strftime("%d/%m/%Y"))
    c.drawString(100, 400, "Firma del vendedor:")
    c.drawString(100, 300, "Firma del comprador:")
    
    c.save()
    print(f"Contrato guardado como {nombre_archivo}")
    return nombre_archivo