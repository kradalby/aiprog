import pickle
import numpy as np


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
