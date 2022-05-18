class Quadruples:
    def __init__(self):
        self.counter = 0
        self.list = []

    def generate_quad(self, operator, left_operand, right_operand, result):
        quad = [operator, left_operand, right_operand, result]
        self.list.append(quad)
        self.counter += 1

    def fill_quad(self, quad_to_fill, quad_index, value):
        self.list[quad_to_fill][quad_index] = value
