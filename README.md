# Patrón Builder aplicado a CaféTrace

Implementación mínima del patrón de diseño **Builder** para construir reportes
de trazabilidad de café en representaciones diferentes. El ejemplo usa los
mismos datos y la misma secuencia de construcción para producir un archivo de
posiciones fijas para el ICAFE y una salida CSV para auditorías.

El objetivo no es construir un sistema completo. El código busca mostrar cómo
separar dos responsabilidades:

- `DirectorReporte` decide **qué pasos se ejecutan y en qué orden**.
- Cada constructor concreto decide **cómo se representa cada paso**.

Gracias a esta separación, se puede incorporar otro formato sin agregar
condicionales al Director ni cambiar su algoritmo de construcción.

## Requisitos

- Python 3.10 o posterior.
- `pytest` para ejecutar las pruebas.

El ejemplo solamente utiliza módulos de la biblioteca estándar de Python. Si
`pytest` no está instalado, se puede instalar con:

```bash
python -m pip install pytest
```

## Archivos del proyecto

```text
Patron_Builder/
├── demo.py       Implementación del patrón y ejemplo ejecutable.
├── test_demo.py  Dos pruebas centradas en la estructura del patrón.
└── README.md     Instrucciones y explicación del ejemplo.
```

## Roles del patrón

| Rol de Builder | Clase del ejemplo | Responsabilidad |
|---|---|---|
| Producto | `ReporteTrazabilidad` | Acumula los bloques del reporte y entrega el texto final. |
| Builder abstracto | `ConstructorReporte` | Define los pasos que todo formato debe implementar. |
| Builder concreto | `ConstructorPosicionesFijas` | Aplica anchos y rellenos para el formato heredado del ICAFE. |
| Builder concreto | `ConstructorCSV` | Separa los valores con comas para producir una salida CSV. |
| Director | `DirectorReporte` | Ejecuta los pasos de construcción en el orden correcto. |
| Cliente | Bloque principal de `demo.py` | Elige el constructor, inicia el proceso y solicita el producto. |

## Cómo ejecutar el ejemplo

Desde la carpeta raíz del repositorio, ejecute:

```bash
python demo.py
```

La salida esperada es semejante a esta:

```text
Demostracion del patron builder para CafeTrace

Formatos de Posiciones Fijas (ICAFE 1998):
L-552   Palmares    460.0011.5

Formatos CSV:
L-552,Palmares,460.00,11.5
```

## Qué ocurre paso por paso

1. El cliente crea un `ConstructorPosicionesFijas` y se lo entrega a
   `DirectorReporte`.
2. El cliente llama a `ordenar_construccion()` con los datos del lote.
3. El Director solicita al constructor que reinicie su producto para evitar
   mezclarlo con una construcción anterior.
4. El Director ordena construir el encabezado con el identificador del lote y
   el nombre de la cooperativa.
5. Después ordena construir los datos físicos con el peso y la humedad.
6. El constructor de posiciones fijas aplica los anchos y rellenos propios del
   formato del ICAFE y agrega cada bloque a `ReporteTrazabilidad`.
7. El cliente llama a `obtener_reporte()` y recibe el producto terminado. El
   constructor queda preparado para fabricar el siguiente reporte.
8. El cliente crea un `ConstructorCSV` y usa `cambiar_constructor()` para
   entregárselo al mismo Director.
9. El Director repite exactamente los mismos pasos. Esta vez, el constructor
   concreto representa los bloques mediante valores separados por comas.

El Director nunca pregunta qué tipo de constructor recibió y no contiene
condicionales para distinguir posiciones fijas de CSV.

## Cómo ejecutar las pruebas

Ejecute las dos pruebas con:

```bash
python -m pytest -q
```

El resultado esperado es:

```text
..                                                                       [100%]
2 passed
```

### Prueba 1: dos constructores producen representaciones diferentes

`test_las_dos_implementaciones_de_hoy_construyen_diferente` entrega los mismos
datos a `ConstructorPosicionesFijas` y `ConstructorCSV`. Comprueba tanto que
las salidas son diferentes como que cada una coincide exactamente con su
formato esperado.

Esta prueba demuestra que el punto variable está en los constructores
concretos. Fallaría si ambos constructores aplicaran la misma representación,
si el Director omitiera un paso o si alguno formateara incorrectamente los
datos.

### Prueba 2: un formato nuevo no requiere modificar el Director

`test_se_agrega_un_formato_nuevo_sin_modificar_el_director` declara dentro de
la propia prueba un tercer constructor llamado `ConstructorJSONDePrueba`. Este
constructor no aparece en `demo.py` y el Director no lo conoce previamente.

La prueba entrega ese nuevo constructor al `DirectorReporte` existente y
verifica que puede producir JSON mediante la misma secuencia. Demuestra que el
sistema está abierto a nuevas representaciones sin modificar el Director.
Fallaría si el Director dependiera de nombres o tipos concretos, o si usara
condicionales que solo reconocieran los formatos originales.

## Contrato central

- **Precondición:** el Director recibe un objeto que cumple la interfaz
  `ConstructorReporte` y datos válidos del lote.
- **Poscondición:** el constructor contiene un reporte con encabezado y datos
  físicos, agregados en ese orden y con la representación seleccionada.
- **Invariante:** la secuencia del Director no depende del constructor concreto.

## Qué demuestra el ejemplo

Builder compra independencia entre el proceso de construcción y la
representación del producto. Lo paga con más clases, un producto temporal y la
necesidad de mantener sincronizado el contrato de todos los constructores.

Para un único formato sencillo, una función directa sería más clara. Builder
resulta útil cuando la construcción tiene varios pasos que deben conservar su
orden y esos mismos pasos necesitan producir representaciones diferentes.
