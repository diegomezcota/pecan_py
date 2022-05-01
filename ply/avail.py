class Avail:
    def __init__(self):
        self.counter = 0
        self.temp_list = []

    def get_new_temp(self, type):
        self.counter += 1
        temp_tuple = ('t'+str(self.counter), type)
        self.temp_list.append(temp_tuple)
        return temp_tuple
