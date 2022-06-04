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

## Avance 7: Generación de Código de Arreglos/Tipos estructurados. Máquina Virtual: Ejecución de Estatutos Condicionales

### pecan_parser.py, function_directory.py
Generación de código intermedio y chequeos semánticos para arreglos y matrices cuyo límite inferior de indexación es 0 (tipo C), así como funciones de ayuda del directorio de funciones. Generación de código intermedio y chequeos semánticos para la declaración y la llamada de funciones, así como guardar la información de ayuda pertinente (cuádruplo de inicio, tipo de retorno, pedir variable global, entre otros). 

### avail.py
Añadición de métodos de ayuda para separar bloques contiguos de memoria.

### virtual_machine.py
Implementación de función para pointers que nos ayuda a hacer el indexamiento indirecto. Ejecución de los códigos de operación de funciones, apoyándonos con un stack de memoria.

## Avance 8: Avance de Documentación y Ejecución de aplicación particular

### pecan_parser.py, function_directory.py
Generación de código intermedio y chequeos semánticos para soportar toda la funcionalidad de objetos. Manejo de scopes, salvar workspaces de memoria necesaria y creación de cuádruplos específicos que nos ayudaron a hacer el direccionamiento correcto para el futuro acceso y modificación en la memoria de ejecución.

### virtual_machine.py, Memory.py
Ejecución de código de objetos, resolver cuádruplos de constructores globales, métodos específicos de redireccionamiento de memoria de un objeto entre scopes, chequeos que preveen errores de ejecución como stack overflow.
