from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Protocol


#La entidad producto
class ReporteTrazabilidad:

    def __init__(self) -> None:
        self.partes: list[str]= []

    def agregar_bloque(self, texto: str):
        self.partes.append(texto)

    def obtener_resultado(self):
        return "".join(self.partes)


#Roles del patron builder
class ConstructorReporte(ABC):

    @abstractmethod
    def reiniciar(self): ...

    @abstractmethod
    def construir_encabezado(self, id_lote: str, cooperativa: str): ...

    @abstractmethod
    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal): ...

    @abstractmethod
    def obtener_reporte(self): ...


class ConstructorPosicionesFijas(ConstructorReporte): #ICAFE 1998

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self._producto= ReporteTrazabilidad()

    def construir_encabezado(self, id_lote: str, cooperativa: str):
        #Ancho fijo: ID tiene 8 caracteres, cooperativa tiene 12
        bloque= f"{id_lote.ljust(8)[:8]}{cooperativa.ljust(12)[:12]}"
        self._producto.agregar_bloque(bloque)

    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal):
        #Peso tiene 6 digitos rellenando con ceros, humedad tiene 4 digitos
        peso_str= str(peso).zfill(6)[:6]
        humedad_str= str(humedad).zfill(4)[:4]
        self._producto.agregar_bloque(f"{peso_str}{humedad_str}\n")

    def obtener_reporte(self):
        resultado= self._producto
        self.reiniciar()
        return resultado


class ConstructorCSV(ConstructorReporte): #CSV para auditoria rapida

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self._producto= ReporteTrazabilidad()

    def construir_encabezado(self, id_lote: str, cooperativa: str):
        self._producto.agregar_bloque(f"{id_lote},{cooperativa},")

    def construir_datos_fisicos(self, peso: Decimal, humedad: Decimal):
        self._producto.agregar_bloque(f"{peso},{humedad}\n")

    def obtener_reporte(self):
        resultado= self._producto
        self.reiniciar()
        return resultado



#El director
class DirectorReporte:

    def __init__(self, constructor: ConstructorReporte):
        self._constructor= constructor

    def cambiar_constructor(self, constructor: ConstructorReporte):
        self._constructor= constructor

    def ordenar_construccion(self, id_lote: str, cooperativa: str, peso: Decimal, humedad: Decimal):
        self._constructor.reiniciar()
        self._constructor.construir_encabezado(id_lote, cooperativa)
        self._constructor.construir_datos_fisicos(peso, humedad)



#Un ejemplo de uso 

if __name__ == "__main__":
    print("Demostracion del patron builder para CafeTrace\n")
    
    #Datos simulados del dominio
    id_lote, coop, peso, humedad= "L-552", "Palmares", Decimal("460.00"), Decimal("11.5")
    
    builder_fijo= ConstructorPosicionesFijas()
    director= DirectorReporte(builder_fijo)
    
    #Construcción formato ICAFE 1998
    director.ordenar_construccion(id_lote, coop, peso, humedad)
    print("Formatos de Posiciones Fijas (ICAFE 1998):")
    print(builder_fijo.obtain_reporte().obtener_resultado() if hasattr(builder_fijo, 'obtain_reporte') else builder_fijo.obtener_reporte().obtener_resultado())

    #Cambiamos constructor a CSV sin tocar el Director
    builder_csv= ConstructorCSV()
    director.cambiar_constructor(builder_csv)
    director.ordenar_construccion(id_lote, coop, peso, humedad)
    print("Formatos CSV:")
    print(builder_csv.obtener_reporte().obtener_resultado())
