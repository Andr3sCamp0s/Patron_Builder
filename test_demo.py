from decimal import Decimal
import pytest
from demo import DirectorReporte, ConstructorPosicionesFijas, ConstructorCSV, ConstructorReporte, ReporteTrazabilidad


#Valida que las variaciones en el builder de verdad cambien la salida
def test_las_dos_implementaciones_de_hoy_construyen_diferente():

    id_lote= "L-01"
    coop= "Zarcero"
    peso= Decimal("120")
    hum= Decimal("10")
    
    bf= ConstructorPosicionesFijas()
    director= DirectorReporte(bf)
    director.ordenar_construccion(id_lote, coop, peso, hum)
    salida_fija= bf.obtener_reporte().obtener_resultado()
    
    bc= ConstructorCSV()
    director.cambiar_constructor(bc)
    director.ordenar_construccion(id_lote, coop, peso, hum)
    salida_csv= bc.obtener_reporte().obtener_resultado()
    
    assert salida_fija != salida_csv
    assert "L-01    Zarcero     0001200010\n" == salida_fija
    assert "L-01,Zarcero,120,10\n" == salida_csv



#Se crea un tercer constructor de tipo JSON desde afuera
#El Director lo procesa perfectamente sin condicionales internos 
def test_se_agrega_un_formato_nuevo_sin_modificar_el_director():
    
    class ConstructorJSONDePrueba(ConstructorReporte):

        def reiniciar(self):
            self.p= ReporteTrazabilidad()

        def construir_encabezado(self, id_lote, cooperativa):
            self.p.agregar_bloque(f'{{"id":"{id_lote}","coop":"{cooperativa}"')

        def construir_datos_fisicos(self, peso, humedad):
            self.p.agregar_bloque(f',"peso":{peso},"hum":{humedad}}}')

        def obtener_reporte(self):
            return self.p

    constructor_nuevo= ConstructorJSONDePrueba()
    #Pasamos la nueva estrategia al director original
    director= DirectorReporte(constructor_nuevo)
    
    director.ordenar_construccion("L-99", "Naranjo", Decimal("500"), Decimal("11"))
    resultado= constructor_nuevo.obtener_reporte().obtener_resultado()
    
    #El director fue capaz de construir con una clase que no conocia de antes
    assert resultado== '{"id":"L-99","coop":"Naranjo","peso":500,"hum":11}'
