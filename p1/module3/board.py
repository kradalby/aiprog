

class Board():

    def __init__(self, filename):
        self.read_file(filename)

    def read_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read().splitlines()
            self.dimensions = content.pop(0).split()

            self.rows = []
            for _ in range(int(self.dimensions.pop(0))):
                temp = content.pop(0).split()
                self.rows.append(temp)

            self.cols = []
            for _ in range(int(self.dimensions.pop(0))):
                temp = content.pop(0).split()
                self.cols.append(temp)
