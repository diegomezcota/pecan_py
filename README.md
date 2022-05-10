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

## Avance 3: Semántica, Generación de Código de Expresiones y Estatutos Lineales

### pecan_parser.py
Generación de cuádruplos para expresiones y estatutos lineales. Manejamos la lógica de type matching, administración de temporales, las filas de operandos y operadores.

### semantic_cube.py
Agregamos el type matching para estatutos de asignación.

### avail.py
Diseño e implementación de la estructura Avail (temporales).

### quadruples.py
Diseño e implementación de estructura y creación de cuádruplos.

## Avance 4: Generación de Código de Estatutos Condicionales y Cíclicos

### avail.py
Agregamos implementación de direcciones de memoria virtuales para constantes y variables globales, locales y temporales.

### function_directory.py
Agregamos chequeos de existencia de scopes y variables.

### lexer.py
Modificación de palabras reservadas para soportar el ciclo for en nuestra gramática.

### pecan_parser.py
Generación de cuádruplos para condicionales if e if else y ciclos while, do while y for.
Administración de memoria virtual para variables y constantes.

