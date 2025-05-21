class EstimadorValorReventa:
    def __init__(self, marca, modelo, anio, kilometraje, datos_mercado):
        self.marca = marca
        self.modelo = modelo
        self.anio = int(anio)
        self.kilometraje = kilometraje
        self.datos_mercado = datos_mercado

    def calcular_valor_reventa(self):
        valor_base = self.datos_mercado.get(self.marca, {}).get(self.modelo, {}).get('valor_base', 0)

        anio_actual = 2025
        años_uso = anio_actual - self.anio

        factor_anual = 1 - (0.10 * años_uso)
        factor_anual = max(factor_anual, 0)

        factor_km = 1 - (0.05 * (self.kilometraje / 10000))
        factor_km = max(factor_km, 0)

        valor_estimado = valor_base * factor_anual * factor_km

        if años_uso == 0 and self.kilometraje == 0:
            valor_estimado -= 3500
            if valor_estimado < 0:
                valor_estimado = 0

        return round(valor_estimado, 2)

    def generar_reporte_estimacion(self):
        reporte = []
        reporte.append("\nReporte de Estimación de Valor de Reventa")
        reporte.append("=" * 50)
        reporte.append(f"Marca: {self.marca}")
        reporte.append(f"Modelo: {self.modelo}")
        reporte.append(f"Año: {self.anio}")
        reporte.append(f"Kilometraje: {self.kilometraje} km")

        valor_base = self.datos_mercado.get(self.marca, {}).get(self.modelo, {}).get('valor_base', 'N/D')
        reporte.append(f"Valor de mercado base: ${valor_base}")

        valor_est = self.calcular_valor_reventa()
        reporte.append(f"Valor Estimado de Reventa: ${valor_est}")
        reporte.append("=" * 50)
        return "\n".join(reporte)
