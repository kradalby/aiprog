import pickle
import numpy as np
from itertools import product


class Dump:
    def __init__(self, move, board):
        self.move = move
        self.board = board

def read_dump(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

def load_all_boards_flat(dumps):
    for dump in dumps:
        board = np.asarray(dump.board).flatten()
        yield board


def load_all_moves_flat(dumps):
    for dump in dumps:
        arr = np.zeros(4)
        arr.put(dump.move, 1)
        yield arr

def load_all(filename):
    dumps = []
    for dump in read_dump(filename):
        if dump.move in [0, 1, 2, 3]:
            dumps.append(dump)

    return list(load_all_boards_flat(dumps)), list(load_all_moves_flat(dumps))

def transforme_all_boards(filename):
    dumps = []
    for dump in read_dump(filename):
        dump.board = transforme_2048board_to_neighbour_score(dump.board)
        if dump.move in [0, 1, 2, 3]:
            dumps.append(dump)

    return list(load_all_boards_flat(dumps)), list(load_all_moves_flat(dumps))


def transforme_2048board_to_neighbour_score(board):

    top = 0
    left = 0
    right = len(board[0]) - 1
    bottom = len(board) - 1
    kids = []

    # Make a cartesian product of adjacent Nodes.
    # Ignores self, out of bounds, diagonals and non-walkables
    for y in range(len(board)):
        for x in range(len(board[y])):
            temp = []
            for i, j in product([-1, 0, 1], [-1, 0, 1]):
                if i == 0 and j == 0:
                    continue
                if not (left <= (x + i) <= right):
                    continue
                if not (top <= (y + j) <= bottom):
                    continue
                if abs(i) + abs(j) > 1:
                    continue
                temp.append(board[y+j][x+i])

            count = 0
            me = board[y][x]
            score = 0
            for number in temp:
                if number == me:
                    count += 1
                score = (float(count)/float(len(temp)))
            kids.append(score)

    return kids
