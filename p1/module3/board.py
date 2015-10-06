

class Board():

    def __init__(self, filename):
        self.read_file(filename)


    def read_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read().splitlines()
            self.dimensions = content.pop(0).split()

            self.cols = []
            self.rows = []
            #num_rows = int(self.dimensions.pop(0))
            #num_cols = int(self.dimensions.pop(0))

            self.num_cols = int(self.dimensions.pop(0))
            self.num_rows = int(self.dimensions.pop(0))

            self.matrix = []

            for y in range(self.num_rows):
                self.matrix.append([])
                for x in range(self.num_cols):
                    self.matrix[y].append(0)


            for _ in range(self.num_rows):
                temp = content.pop(0).split()
                print("this is row: ", temp)
                self.rows.append(list(map(lambda x: int(x), temp)))
                    #(int(temp[0]), int(temp[1])))


            for _ in range(self.num_cols):
                temp = content.pop(0).split()
                print("this is col: ", temp)
                self.cols.append(list(map(lambda x: int(x), temp)))

            self.rows.reverse()
