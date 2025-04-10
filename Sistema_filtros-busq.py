from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

# Clase abstracta para los vehículos
class Vehiculo(ABC):
    @abstractmethod
    def calcular_relevancia(self) -> float:
        """Método abstracto para calcular la relevancia del vehículo.

        Returns:
            float: Valor de relevancia del vehículo.
        """
        pass

# Clase concreta para representar un coche
class Coche(Vehiculo):
    def __init__(self, precio: float, marca: str, modelo: str, anio: int, kilometraje: float,
                 tipo_combustible: str, fecha_publicacion: datetime) -> None:
        """Inicializa un objeto Coche con los atributos especificados.

        Args:
            precio (float): Precio del coche.
            marca (str): Marca del coche.
            modelo (str): Modelo del coche.
            anio (int): Año de fabricación del coche.
            kilometraje (float): Kilometraje del coche.
            tipo_combustible (str): Tipo de combustible del coche.
            fecha_publicacion (datetime): Fecha de publicación del anuncio.

        Raises:
            ValueError: Si los valores de precio, año o kilometraje son inválidos.
        """
        # Validaciones con manejo de excepciones
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if anio < 1900 or anio > datetime.now().year + 1:
            raise ValueError(f"El año debe estar entre 1900 y {datetime.now().year + 1}.")
        if kilometraje < 0:
            raise ValueError("El kilometraje no puede ser negativo.")

        self.precio: float = precio
        self.__marca: str = marca
        self.__modelo: str = modelo
        self.anio: int = anio
        self.kilometraje: float = kilometraje
        self.tipo_combustible: str = tipo_combustible
        self.fecha_publicacion: datetime = fecha_publicacion

    # Getters y setters para los atributos privados
    def get_marca(self) -> str:
        """Obtiene la marca del coche.

        Returns:
            str: Marca del coche.
        """
        return self.__marca

    def set_marca(self, nueva_marca: str) -> None:
        """Establece una nueva marca para el coche.

        Args:
            nueva_marca (str): Nueva marca del coche.

        Raises:
            ValueError: Si la marca está vacía.
        """
        if not nueva_marca.strip():
            raise ValueError("La marca no puede estar vacía.")
        self.__marca = nueva_marca

    def get_modelo(self) -> str:
        """Obtiene el modelo del coche.

        Returns:
            str: Modelo del coche.
        """
        return self.__modelo

    def set_modelo(self, nuevo_modelo: str) -> None:
        """Establece un nuevo modelo para el coche.

        Args:
            nuevo_modelo (str): Nuevo modelo del coche.

        Raises:
            ValueError: Si el modelo está vacío.
        """
        if not nuevo_modelo.strip():
            raise ValueError("El modelo no puede estar vacío.")
        self.__modelo = nuevo_modelo

    # Método para calcular relevancia (para ordenar por relevancia)
    def calcular_relevancia(self) -> float:
        """Calcula la relevancia del coche basada en antigüedad y kilometraje.

        Returns:
            float: Valor de relevancia del coche.
        """
        antiguedad: int = datetime.now().year - self.anio
        return 100 - (antiguedad * 2 + self.kilometraje / 10000)

    def __str__(self) -> str:
        """Devuelve una representación en string del coche.

        Returns:
            str: Representación del coche.
        """
        return (f"Coche(marca={self.__marca}, modelo={self.__modelo}, precio={self.precio}, "
                f"anio={self.anio}, kilometraje={self.kilometraje}, "
                f"tipo_combustible={self.tipo_combustible})")

# Interfaz para el sistema de búsqueda
class SistemaBusqueda(ABC):
    @abstractmethod
    def buscar(self, filtros: Dict[str, Any]) -> List[Vehiculo]:
        """Método abstracto para buscar vehículos según filtros.

        Args:
            filtros (Dict[str, Any]): Diccionario con los filtros de búsqueda.

        Returns:
            List[Vehiculo]: Lista de vehículos que cumplen con los filtros.
        """
        pass

    @abstractmethod
    def ordenar(self, resultados: List[Vehiculo], criterio: str) -> List[Vehiculo]:
        """Método abstracto para ordenar los resultados de búsqueda.

        Args:
            resultados (List[Vehiculo]): Lista de vehículos a ordenar.
            criterio (str): Criterio de ordenamiento ('precio', 'relevancia', 'fecha_publicacion').

        Returns:
            List[Vehiculo]: Lista de vehículos ordenada.
        """
        pass

# Implementación concreta del sistema de búsqueda
class SistemaCoches(SistemaBusqueda):
    def __init__(self, coches: List[Coche]) -> None:
        """Inicializa el sistema de búsqueda con una lista de coches.

        Args:
            coches (List[Coche]): Lista de coches disponibles.
        """
        self.coches: List[Coche] = coches  # Público

    def buscar(self, filtros: Dict[str, Any]) -> List[Vehiculo]:
        """Busca coches aplicando los filtros especificados.

        Args:
            filtros (Dict[str, Any]): Diccionario con los filtros de búsqueda.
                Ejemplo: {'precio_max': 20000, 'marca': 'Toyota', 'anio_min': 2015}

        Returns:
            List[Vehiculo]: Lista de coches que cumplen con los filtros.
        """
        resultados: List[Coche] = self.coches

        # Aplicar filtros
        if 'precio_max' in filtros:
            resultados = [coche for coche in resultados if coche.precio <= filtros['precio_max']]
        if 'precio_min' in filtros:
            resultados = [coche for coche in resultados if coche.precio >= filtros['precio_min']]
        if 'marca' in filtros:
            resultados = [coche for coche in resultados if coche.get_marca().lower() == filtros['marca'].lower()]
        if 'modelo' in filtros:
            resultados = [coche for coche in resultados if coche.get_modelo().lower() == filtros['modelo'].lower()]
        if 'anio_min' in filtros:
            resultados = [coche for coche in resultados if coche.anio >= filtros['anio_min']]
        if 'anio_max' in filtros:
            resultados = [coche for coche in resultados if coche.anio <= filtros['anio_max']]
        if 'kilometraje_max' in filtros:
            resultados = [coche for coche in resultados if coche.kilometraje <= filtros['kilometraje_max']]
        if 'tipo_combustible' in filtros:
            resultados = [coche for coche in resultados if coche.tipo_combustible.lower() == filtros['tipo_combustible'].lower()]

        return resultados

    def ordenar(self, resultados: List[Vehiculo], criterio: str) -> List[Vehiculo]:
        """Ordena los resultados según el criterio especificado.

        Args:
            resultados (List[Vehiculo]): Lista de vehículos a ordenar.
            criterio (str): Criterio de ordenamiento ('precio', 'relevancia', 'fecha_publicacion').

        Returns:
            List[Vehiculo]: Lista de vehículos ordenada.

        Raises:
            ValueError: Si el criterio de ordenamiento no es válido.
        """
        if criterio == "precio":
            return sorted(resultados, key=lambda x: x.precio)
        elif criterio == "relevancia":
            return sorted(resultados, key=lambda x: x.calcular_relevancia(), reverse=True)
        elif criterio == "fecha_publicacion":
            return sorted(resultados, key=lambda x: x.fecha_publicacion, reverse=True)
        else:
            raise ValueError("Criterio de ordenamiento no válido. Use 'precio', 'relevancia' o 'fecha_publicacion'.")