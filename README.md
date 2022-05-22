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

## Avance 5: Generación de Código de Funciones

### constants.py
Agregamos la clase Constants que maneja las direcciones virtuales de constantes de tipos atómicos.

### function_directory.py
Agregamos las funciones necesarias para apoyar la creación de cuádruplos para declaración y llamadas de funciones.

### pecan_parser.py
Generación de cuádruplos e implementación de puntos neurálgicos para la definición y llamada a funciones/módulos con sus validaciones pertinentes.

## Avance 6: Mapa de Memoria de Ejecución para la Máquina Virtual y Ejecución de Expresiones Aritméticas y Estatutos Secuenciales

### ovejota.json
Se crea archivo tipo obj como resultado de la compilación con información como directorio de funciones, tabla de constantes y cuádruplos para dar de input a la máquina virtual.

### ovejota_manager.py
Manejador que carga el archivo ovejota.json y administra sus contenidos para la máquina virtual.

### Memory.py
Clase manejadora de memoria de ejecución siguiendo el esquema definido en nuestro archivo avail con las direcciones virtuales de los valores y sus métodos correspondientes de búsqueda y agregación.

### formatter.py
Clase que maneja el casteo de tipos de datos entre Python y PecanPy.

### virtual_machine.py
Archivo que se encarga del manejo de la ejecución de los quádruplos. Para esta entrega se manejan los cuádruplos de estatutos secuenciales y expresiones aritméticas como suma, resta, multiplicación, división, asignación, operadores relacionales, operadores lógicos, escritura y lectura dentro del scope global y main.

