from datastructure.node import Node
import math
from itertools import product


class BoardNode(Node):
    def __init__(self, x, y, board):
        self.board = board
        super(BoardNode, self).__init__(x, y)

    def calculate_heuristic(self, goal):
        e = math.sqrt(((self.x - goal.x) ** 2) + ((self.y - goal.y) ** 2))
        self.h = abs(goal.x - self.x) + abs(goal.y - self.y)
        self.h += 0.001 * e

    def generate_kids(self):
        top = 0
        left = 0
        right = len(self.board.matrix[0]) - 1
        bottom = len(self.board.matrix) - 1

        x = self.x
        y = self.y

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
                if not self.board.matrix[y+j][x+i].walkable:
                    continue
            except IndexError:
                continue

            self.kids.append(self.board.matrix[y+j][x+i])

