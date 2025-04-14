class EstimadorValorReventa:
    def __init__(self, modelo, anio, kilometraje, datos_mercado):

        self.modelo = modelo
        self.anio = int(anio)
        self.kilometraje = kilometraje
        self.datos_mercado = datos_mercado

    def calcular_valor_reventa(self):

        # Obtener el valor base del modelo desde los datos de mercado
        modelo_info = self.datos_mercado.get(self.modelo, {})
        valor_base = modelo_info.get('valor_base', 0)
        
        # Suponemos el año actual como 2025 para fines de la estimación
        anio_actual = 2025
        años_uso = anio_actual - self.anio
        
        # Cálculo de depreciación por año (10% anual)
        factor_anual = 1 - (0.10 * años_uso)
        factor_anual = max(factor_anual, 0)  # Evitar que el factor sea negativo
        
        # Cálculo de depreciación por kilometraje (5% por cada 10,000 km)
        factor_km = 1 - (0.05 * (self.kilometraje / 10000))
        factor_km = max(factor_km, 0)
        
        # Valor de reventa estimado
        valor_estimado = valor_base * factor_anual * factor_km
        return round(valor_estimado, 2)

    def generar_reporte_estimacion(self):
 
        reporte = []
        reporte.append("Reporte de Estimación de Valor de Reventa")
        reporte.append("=" * 50)
        reporte.append(f"Modelo: {self.modelo}")
        reporte.append(f"Año: {self.anio}")
        reporte.append(f"Kilometraje: {self.kilometraje} km")
        
        modelo_info = self.datos_mercado.get(self.modelo, {})
        valor_base = modelo_info.get('valor_base', 'N/D')
        reporte.append(f"Valor de mercado base: ${valor_base}")
        
        valor_est = self.calcular_valor_reventa()
        reporte.append(f"Valor Estimado de Reventa: ${valor_est}")
        reporte.append("=" * 50)
        return "\n".join(reporte)


# Ejemplo de uso
if __name__ == "__main__":
    # Datos de mercado simulados para distintos modelos
    datos_mercado = {
        "ModeloA": {"valor_base": 30000},
        "ModeloB": {"valor_base": 25000},
        "ModeloC": {"valor_base": 40000}
    }
    
    # Crear instancia del estimador para un vehículo específico
    estimador = EstimadorValorReventa("ModeloA", 2020, 50000, datos_mercado)
    
    # Generar y mostrar el reporte de estimación
    reporte = estimador.generar_reporte_estimacion()
    print(reporte)
