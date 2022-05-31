# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# quadruples.py
# Estructura para manejar los cuadruplos de la compilacion
class Quadruples:
    def __init__(self):
        # contador de cuadruplos - representa el indice del siguiente cuadruplo a generar
        self.counter = 0
        self.list = []  # lista de cuadruplos

    # funcion para generar un nuevo cuadruplo, gregarlo a la lista y actualizar contador
    # entradas: operador, operando izquierdo, operando derecho y resultado (direccion virtual donde se guarda)
    def generate_quad(self, operator, left_operand, right_operand, result):
        quad = [operator, left_operand, right_operand, result]
        self.list.append(quad)
        self.counter += 1

    # funcion para completar el indice de un cuadruplo previamente creado utilizado normalmente en los gotof, gotot, goto, etc
    # entradas: cuadruplo a completar, el indice que se completara y el valor a agregar
    def fill_quad(self, quad_to_fill, quad_index, value):
        self.list[quad_to_fill][quad_index] = value
