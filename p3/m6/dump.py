import pickle
import numpy as np
from itertools import product
import copy
import math


class Dump:
    def __init__(self, move, board):
        self.move = move
        self.board = board

def convert_txt_to_dump(txtfile, dumpfile):
    lines = None
    with open(txtfile, 'r') as t:
        lines = t.read().split('\n')

    print(lines)
    with open(dumpfile, 'wb') as d:
        for line in lines:
            board, move = line.split('Direction')
            board = eval(board)
            move = move.split('}')[-1]
            if move == 'DOWN':
                move = 0
            elif move == 'UP':
                move = 1
            elif move == 'LEFT':
                move = 2
            elif move == 'RIGTH':
                move = 3

            board = convert_map(board)

            pickle.dump(Dump(move, board), d)

def convert_map(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] != 0:
                m[y][x] = int(math.log2(m[y][x]))
    return m



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

def transform_all_boards(filename):
    dumps = []
    for dump in read_dump(filename):
        dump.board = transform(dump.board)
        if dump.move in [0, 1, 2, 3]:
            dumps.append(dump)

    return list(load_all_boards_flat(dumps)), list(load_all_moves_flat(dumps))


def transform_2048board_to_neighbour_score(board):

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

    return np.asarray(kids)

def transform_2048board_to_neighbour_gradiant(board):

    weight = [
        [4, 3, 2, 1],
        [5, 4, 3, 2],
        [6, 5, 4, 3],
        [7, 6, 5, 4]
    ]

    c = copy.deepcopy(board)

    result = []

    for i in range(1):
        grad = np.dot(weight, c).flatten()
        grad = grad/max(grad)
        result.append(grad)
        weight = np.rot90(weight)

    return result


def transform_2048board_to_neighbour_snake(board):

    weight = [[16, 15, 14, 13],
             [9, 10, 11, 12],
             [8, 7, 6, 5],
             [1, 2, 3, 4]]

    c = copy.deepcopy(board)

    result = []

    for i in range(4):
        grad = np.dot(weight, c).flatten()
        grad = grad/max(grad)
        result.append(grad)
        weight = np.rot90(weight)

    return result

def transform(board):
    result = []

    b = np.asarray(board).flatten()
    result.append(b/max(b))
    result.append(transform_2048board_to_neighbour_score(board))
    for r in transform_2048board_to_neighbour_gradiant(board):
        result.append(r)
    #for r in transform_2048board_to_neighbour_snake(board):
    #    result.append(r)

    return np.asarray(result).flatten()
