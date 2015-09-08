from ast import literal_eval
from itertools import product
from node import Node
from astar import Astar

class Board():
    def __init__(self, filename):
        self.read_file(filename)
        self.create_board_matrix()

    def read_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read().split()
            self.dimensions = literal_eval(content.pop(0))
            self.start = literal_eval(content.pop(0))
            self.goal = literal_eval(content.pop(0))
            self.barriers = [literal_eval(x) for x in content]

    def blocked_cordinates(self, block):
        x = block[0]
        y = block[1]
        width = block[2]
        height = block[3]

        cordinates = []

        for temp_x in range(width):
            for temp_y in range(height):
                cordinates.append((temp_x + x, temp_y + y))

        return cordinates

    def create_board_matrix(self):
        self.matrix = []
        for y in range(self.dimensions[1]):
            self.matrix.append([])
            for x in range(self.dimensions[0]):
                self.matrix[y].append(Node(x, y))

        self.matrix[self.start[1]][self.start[0]].start = True
        self.matrix[self.goal[1]][self.goal[0]].end = True

        for barriers in self.barriers:
            for barrier in self.blocked_cordinates(barriers):
                self.matrix[barrier[1]][barrier[0]].walkable = False

    def create_graph(self):
        top = 0
        left = 0
        right = len(self.matrix[0]) - 1
        bottom = len(self.matrix) - 1

        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                node = self.matrix[y][x]

                # If it is not walkable, just ignore it
                if not node.walkable:
                    continue

                # Make a cartesian product of adjacent Nodes.
                # Ignores self, out of bounds, diagonals and non-walkables
                for i, j in product([-1, 0, 1], [-1, 0, 1]):
                    if i == 0 and j == 0:
                        continue
                    if not (left <= (x + i) <= right):
                        continue
                    if not (top <= (y + j) <= bottom):
                        continue
                    if abs(i) + abs(j) > 1:
                        continue
                    try:
                        if not self.matrix[y+j][x+i].walkable:
                            continue
                    except IndexError:
                        continue

                    node.kids.append(self.matrix[y+j][x+i])

        start = self.matrix[self.start[1]][self.start[0]]
        end = self.matrix[self.goal[1]][self.goal[0]]

        return start, end


if __name__ == '__main__':
    b = Board('testmap1.txt')
    s, e = b.create_graph()
    print(s.start, s.end)

    a = Astar('bfs')
    print(a.astar(s, e))

