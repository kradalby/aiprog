#coding=utf8
#Wei Guannan <kiss.kraks@gmail.com>

import copy
import math
import random
from colorama import Fore, Back
from functools import reduce

from ann import ANN
from dump import *
import ai2048demo
import argparse
import time
from gamelogic import *

ann = None

RUN_RANDOM = 0
TILES_RANDOM = []

RUN_ANN = 0
TILES_ANN = []


def prettyPrint(a):
    def color(x):
        if x == 0:    return Fore.RESET + Back.RESET
        if x == 2:    return Fore.RED + Back.RESET
        if x == 4:    return Fore.GREEN + Back.RESET
        if x == 8:    return Fore.YELLOW + Back.RESET
        if x == 16:   return Fore.BLUE + Back.RESET
        if x == 32:   return Fore.MAGENTA + Back.RESET
        if x == 64:   return Fore.CYAN + Back.RESET
        if x == 128:  return Fore.RED + Back.BLACK
        if x == 256:  return Fore.GREEN + Back.BLACK
        if x == 512:  return Fore.YELLOW + Back.BLACK
        if x == 1024: return Fore.BLUE + Back.BLACK
        if x == 2048: return Fore.MAGENTA + Back.BLACK
        if x == 4096: return Fore.CYAN + Back.BLACK
        if x == 8192: return Fore.WHITE + Back.BLACK
    for i in a:
        for j in i:
            print(color(j) + ("%4d" % j) + Fore.RESET + Back.RESET, end=' ')
        print()


def isWin(a):
    return traverse(a, lambda x: x == 2048)

def isFail(a):
    def aux(a):
        for i in a:
            for j in zip(i, i[1:]):
                if j[0] == 0 or j[1] == 0 or j[0] == j[1]: return False
        return True
    return aux(a) and aux(rotate(a))
    
def traverse(a, f):
    for line in a:
        for ele in line:
            if f(ele): return True
    return False

def randomPoint(size):
    x = random.randint(0, size)
    y = random.randint(0, size)
    return (x, y)

def randomInit(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    v = random.randint(0, len(seed)-1)
    a[x][y] = seed[v]

def randomNum(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    if a[x][y] == 0:
        v = random.randint(0, len(seed)-1)
        a[x][y] = seed[v]
    else: randomNum(a)

def get_column(i, m):
    l = []
    for row in m:
        l.append(row[i])
    return l

def valid_move(dir, m):
    """
    Test if a move in the given direction is possible
    U: 0, R: 1: D: 2: L: 3
    :param dir: Direction to check
    :param m: The board to check on
    :return: A boolean telling if a move is valid or not
    """
    size = range(0, 4)
    if dir == 2 or dir == 3:
        for x in size:
            col = m[x]
            for y in size:
                if y < 4 - 1 and col[y] == col[y + 1] and col[y] != 0:
                    return True
                if dir == 3 and y > 0 and col[y] == 0 and col[y - 1] != 0:
                    return True
                if dir == 2 and y < 4 - 1 and col[y] == 0 and col[y + 1] != 0:
                    return True

    if dir == 0 or dir == 1:
        for y in size:
            line = get_column(y, m)
            for x in size:
                if x < 4 - 1 and line[x] == line[x + 1] and line[x] != 0:
                    return True
                if dir == 1 and x > 0 and line[x] == 0 and line[x - 1] != 0:
                    return True
                if dir == 0 and x < 4 - 1 and line[x] == 0 and line[x + 1] != 0:
                    return True
    return False

def convert_map(m):
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] != 0:
                m[y][x] = int(math.log2(m[y][x]))
    return m

def find_best_move(m):
    k = copy.deepcopy(m)
    k = convert_map(k)
    m2 = transform(k)
    move = ann.go(m2)
    move = move[0]
    #print(move)
    if move[0] == move[1] and move[2] == move[3]:
        return random.randint(0,3)
    for i in sorted(move)[::-1]:
        f = move.tolist().index(i)
        legal = valid_move(f, m)
        if legal:
            #print(f)
            #time.sleep(3)
            return move.tolist().index(i)
    return 0

def newGameANN(size):
    global RUN_ANN
    #print("w for move up, a for move left, s for move down, d for move right.")
    #print("q for quit.")
    won = False
    a = newEmpty(size)
    randomInit(a)
    randomInit(a)
    #prettyPrint(a)
    while True:
        b = copy.deepcopy(a)
        key = find_best_move(b)
        if key == 0:   a = reduceUp(a)
        elif key == 2: a = reduceLeft(a)
        elif key == 1: a = reduceDown(a)
        elif key == 3: a = reduceRight(a)
        #elif key == "q": break
        if a == b: 
            pass
            #print("no numbers to be reduce")
        else: randomNum(a)
        #print('-------------------')
        #prettyPrint(a)
        if isWin(a) and not won:
            print("You win")
            won = True
        elif isFail(a):
            #print("You fail")
            max_tile = max([max(x) for x in a])
            #print('-------------------')
            #prettyPrint(a)
            #print(max_tile)
            TILES_ANN.append(max_tile)
            break

def newGameRandom(size):
    global RUN_RANDOM
    #print("w for move up, a for move left, s for move down, d for move right.")
    #print("q for quit.")
    won = False
    a = newEmpty(size)
    randomInit(a)
    randomInit(a)
    #prettyPrint(a)
    while True:
        b = copy.deepcopy(a)
        key = random.randint(0,3)
        if key == 0:   a = reduceUp(a)
        elif key == 2: a = reduceLeft(a)
        elif key == 1: a = reduceDown(a)
        elif key == 3: a = reduceRight(a)
        #elif key == "q": break
        if a == b: 
            pass
            #print("no numbers to be reduce")
        else: randomNum(a)
        #prettyPrint(a)
        if isWin(a) and not won:
            print("You win")
            won = True
        elif isFail(a):
            #print("You fail")
            TILES_RANDOM.append(max([max(x) for x in a]))
            break

def test():
    assert reduceLineLeft([4, 4, 4, 4]) == [8, 8, 0, 0]
    assert reduceLineLeft([0, 0, 0, 0]) == [0, 0, 0, 0]
    assert reduceLineLeft([2, 0, 2, 0]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 0, 0, 2]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 2, 0, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([4, 0, 2, 2]) == [4, 4, 0, 0]
    assert reduceLineLeft([2, 0, 2, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([2, 2, 8, 8]) == [4, 16, 0, 0]
    assert reduceLineRight([2, 2, 0, 2]) == [0, 0, 2, 4]
    assert reduceLineRight([0, 0, 0, 2]) == [0, 0, 0, 2]
    assert reduceLineRight([2, 0, 0, 2]) == [0, 0, 0, 4]
    assert reduceLineRight([4, 4, 2, 2]) == [0, 0, 8, 4]
    assert reduceLineRight([2, 4, 4, 2]) == [0, 2, 8, 2]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='aiprog 2048 NN')

    parser.add_argument('-n', '--trains', action='store', dest='trains', type=int, required=True)
    parser.add_argument('-lr', '--learningrate', action='store', dest='learningrate', type=float, required=True)
    parser.add_argument('-no', '--notation', action='store', dest='notation', type=str, required=True)
    parser.add_argument('-s', '--sizes', nargs='+', type=int)
    parser.add_argument('-t', '--types', nargs='+', type=str)


    args = parser.parse_args()

    trains = args.trains
    learningrate = args.learningrate
    sizes = args.sizes
    types = args.types
    notation = args.notation
    print(trains, learningrate, sizes, types, notation)

    ann = ANN(trains, learningrate, sizes, types, notation, 256)

    RANDOM_AVERAGES = []
    ANN_AVERAGES = []

    scores = []
    for i in range(3):
        print()
        print()
        print()
        print('RUN NUMBER:', i + 1)
        TILES_RANDOM = []
        TILES_ANN = []
        for i in range(50):
            newGameRandom(4)
        #print(RUN_RANDOM)
        #print(TILES_RANDOM)
        #print(len(TILES_RANDOM))

        for i in range(50):
            newGameANN(4)
        #print(RUN_ANN)
        #print(TILES_ANN)
        #print(len(TILES_ANN))

        result = ai2048demo.welch(TILES_RANDOM, TILES_ANN)
        print(result)
        score = 0
        try:
            score = result.split('\n')[3][-3]
        except:
            score = 0
        print(score)
        scores.append(int(score))
        RANDOM_AVERAGE = sum(TILES_RANDOM)/len(TILES_RANDOM)
        ANN_AVERAGE = sum(TILES_ANN)/len(TILES_ANN)
        print('Random average:')
        print(RANDOM_AVERAGE)
        print('ANN average:')
        print(ANN_AVERAGE)
        RANDOM_AVERAGES.append(RANDOM_AVERAGE)
        ANN_AVERAGES.append(ANN_AVERAGE)

    print()
    print()
    print()
    print('=========================================================================')
    print(trains, learningrate, sizes, types, notation)
    print(scores)
    print('avg: ', sum(scores)/len(scores))
    print('Random average:')
    print(sum(RANDOM_AVERAGES)/len(RANDOM_AVERAGES))
    print('ANN average:')
    print(sum(ANN_AVERAGES)/len(ANN_AVERAGES))
    print('=========================================================================')
    print()
    print()
    print()
