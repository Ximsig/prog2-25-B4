class HistorialDelVehiculo:
    def __init__(self):
        # Listas para almacenar los registros
        self.registro_mantenimiento = []
        self.registro_revisiones = []
        self.registro_siniestros = []

    def agregar_mantenimiento(self, fecha, descripcion):

        self.registro_mantenimiento.append({
            'fecha': fecha,
            'descripcion': descripcion
        })

    def agregar_revision(self, fecha, descripcion):

        self.registro_revisiones.append({
            'fecha': fecha,
            'descripcion': descripcion
        })

    def agregar_siniestro(self, fecha, descripcion, valor_estimado):

        self.registro_siniestros.append({
            'fecha': fecha,
            'descripcion': descripcion,
            'valor_estimado': valor_estimado
        })

    def generar_informe_siniestralidad(self):

        lineas = []
        lineas.append("Informe de Siniestralidad del Vehículo")
        lineas.append("=" * 40)
        
        if not self.registro_siniestros:
            lineas.append("No se han registrado siniestros.")
        else:
            for indice, siniestro in enumerate(self.registro_siniestros, start=1):
                lineas.append(f"{indice}. Fecha: {siniestro['fecha']}")
                lineas.append(f"   Descripción: {siniestro['descripcion']}")
                lineas.append(f"   Valor Estimado: {siniestro['valor_estimado']}")
                lineas.append("-" * 40)
        
        return "\n".join(lineas)
