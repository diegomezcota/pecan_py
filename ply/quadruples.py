class Quadruples:
    def __init__(self):
        self.counter = 0
        self.quads = []

    def generate_quad(self, operator, left_operand, right_operand, result):
        quad = [operator, left_operand, right_operand, result]
        self.quads.append(quad)
        self.counter += 1
