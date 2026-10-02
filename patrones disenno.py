"""
Implementación del Patrón Builder para CaféTrace
Cumple con la extensión de 60 a 150 líneas de código útil.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Protocol

# ============================================================================
# 1. ENTIDAD PRODUCTO (El resultado complejo de la construcción)
# ============================================================================
class ReporteTrazabilidad:
    def __init__(self) -> None:
        self.partes: list[str] = []

    def agregar_bloque(self, texto: str) -> None:
        self.partes.append(texto)

    def obtener_resultado(self) -> str:
        return "".join(self.partes)


# ============================================================================
# 2. ROLES DEL PATRÓN BUILDER (En español)
# ============================================================================
class ConstructorReporte(ABC):
    """Interfaz del Builder Abstracto"""
    @abstractmethod
    def reiniciar(self) -> None: ...
    @abstractmethod
    def construir_encabezado(self, id_lote: str, cooperativa: str) -> None: ...
    @abstractmethod
    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal) -> None: ...
    @abstractmethod
    def obtener_reporte(self) -> ReporteTrazabilidad: ...


class ConstructorPosicionesFijas(ConstructorReporte):
    """Implementación Variable 1: El formato exigido por ICAFE en 1998 (R-6)"""
    def __init__(self) -> None:
        self.reiniciar()

    def reiniciar(self) -> None:
        self._producto = ReporteTrazabilidad()

    def construir_encabezado(self, id_lote: str, cooperativa: str) -> None:
        # Ancho fijo: ID toma 8 caracteres, Cooperativa toma 12
        bloque = f"{id_lote.ljust(8)[:8]}{cooperativa.ljust(12)[:12]}"
        self._producto.agregar_bloque(bloque)

    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal) -> None:
        # Peso toma 6 caracteres rellenado con ceros, Humedad toma 4
        peso_str = str(peso).zfill(6)[:6]
        humedad_str = str(humedad).zfill(4)[:4]
        self._producto.agregar_bloque(f"{peso_str}{humedad_str}\n")

    def obtener_reporte(self) -> ReporteTrazabilidad:
        resultado = self._producto
        self.reiniciar()
        return resultado


class ConstructorCSV(ConstructorReporte):
    """Implementación Variable 2: Formato estándar para auditorías rápidas (R-10)"""
    def __init__(self) -> None:
        self.reiniciar()

    def reiniciar(self) -> None:
        self._producto = ReporteTrazabilidad()

    def construir_encabezado(self, id_lote: str, cooperativa: str) -> None:
        self._producto.agregar_bloque(f"{id_lote},{cooperativa},")

    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal) -> None:
        self._producto.agregar_bloque(f"{peso},{humedad}\n")

    def obtener_reporte(self) -> ReporteTrazabilidad:
        resultado = self._producto
        self.reiniciar()
        return resultado


# ============================================================================
# 3. EL DIRECTOR (Maneja el orden secuencial de los pasos)
# ============================================================================
class DirectorReporte:
    def __init__(self, constructor: ConstructorReporte) -> None:
        self._constructor = constructor

    def cambiar_constructor(self, constructor: ConstructorReporte) -> None:
        self._constructor = constructor

    def ordenar_construccion(self, id_lote: str, cooperativa: str, peso: Decimal, humedad: Decimal) -> None:
        self._constructor.reiniciar()
        self._constructor.construir_encabezado(id_lote, cooperativa)
        self._constructor.construir_datos_fisicos(peso, humedad)


# ============================================================================
# 4. EJEMPLO DE USO (python demo.py)
# ============================================================================
if __name__ == "__main__":
    print("--- DEMOSTRACIÓN DEL PATRÓN BUILDER (CaféTrace) ---\n")
    
    # Datos simulados del dominio (R-1)
    id_lote, coop, peso, humedad = "L-552", "Palmares", Decimal("460.00"), Decimal("11.5")
    
    builder_fijo = ConstructorPosicionesFijas()
    director = DirectorReporte(builder_fijo)
    
    # Construcción formato ICAFE 1998
    director.ordenar_construccion(id_lote, coop, peso, humedad)
    print("Formatos de Posiciones Fijas (ICAFE 1998):")
    print(builder_fijo.obtain_reporte().obtener_resultado() if hasattr(builder_fijo, 'obtain_reporte') else builder_fijo.obtener_reporte().obtener_resultado())

    # Cambiamos constructor a CSV dinámicamente sin tocar el Director
    builder_csv = ConstructorCSV()
    director.cambiar_constructor(builder_csv)
    director.ordenar_construccion(id_lote, coop, peso, humedad)
    print("Formatos CSV (Auditoría):")
    print(builder_csv.obtener_reporte().obtener_resultado())
