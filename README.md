# PecanPy

Para esta entrega este proyecto tiene la estructura de dos fólders 
principales, los cuales son descritos a continuación.

## Avance 0: Documentación
Este tiene el documento del Avance #0, que contiene:
- Lista de Tokens
- Diagramas de Sintaxis
- Gramática Formal
- Las principales consideraciones semánticas

## Avance 1: PLY
En este directorio se tienen todos los archivos en el que desarrollamos
el análisis léxico y sintáctico de PecanPy. Cuenta con la siguiente
estructura:

### tests/
Se definen los tests para asegurarnos que se reconozcan tanto los tókens
(carpeta lexer) como las reglas gramaticales (carpeta parser)

### lexer_tests.py, parser_tests.py
Archivos a correr para probar el lexer y el parser, respectivamente.

### lexer.py, pecan_parser.py
Archivos que utilizan PLY para definir los tókens y reglas gramaticales de PecanPy.
pecan_parser.py utiliza la gramática formal descrita en documentación/.

## Avance 2: Semántica Básica

### function_directory.py, pecan_parser.py
Se trabajó en la estructura e implementación del directorio de funciones así como su integración con la gramática.

### semantic_cube.py
Se trabajó en el diseño e implementación del cubo semántico.
