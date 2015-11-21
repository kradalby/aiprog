#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Help the user achieve a high score in a real game of 2048 by using a move searcher. '''

from __future__ import print_function
import ctypes
import math
import random
import time
import os
from ann import ANN
from dump import *

ann = ANN(10, 0.001, [64, 32, 16, 4], ['rect', 'rect', 'soft'], "derp")

def to_c_board(m):
    board = 0
    i = 0
    for row in m:
        for c in row:            
            board |= c << (4*i)
            i += 1
    return board

def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()

def _to_val(c):
    if c == 0: return 0
    return 2**c

def to_val(m):
    return [[_to_val(c) for c in row] for row in m]

def _to_score(c):
    if c <= 1:
        return 0
    return (c-1) * (2**c)

def to_score(m):
    return [[_to_score(c) for c in row] for row in m]

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
    print(move)
    if move[0] == move[1] and move[2] == move[3]:
        return random.randint(0,3)
    for i in sorted(move)[::-1]:
        legal = valid_move(move.tolist().index(i), m)
        if legal:
            return move.tolist().index(i)
    return 0

def movename(move):
    return ['up', 'down', 'left', 'right'][move]

def play_game(gamectrl):
    moveno = 0
    start = time.time()
    while 1:
        state = gamectrl.get_status()
        if state == 'ended':
            break
        elif state == 'won':
            time.sleep(0.75)
            gamectrl.continue_game()

        moveno += 1
        board = gamectrl.get_board()
        move = find_best_move(board)
        if move < 0:
            break
        print("%010.6f: Score %d, Move %d: %s" % (time.time() - start, gamectrl.get_score(), moveno, movename(move)))
        gamectrl.execute_move(move)

    score = gamectrl.get_score()
    board = gamectrl.get_board()
    maxval = max(max(row) for row in to_val(board))
    print("Game over. Final score %d; highest tile %d." % (score, maxval))

def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-p', '--port', help="Port number to control on (default: 32000 for Firefox, 9222 for Chrome)", type=int)
    parser.add_argument('-b', '--browser', help="Browser you're using. Only Firefox with the Remote Control extension, and Chrome with remote debugging, are supported right now.", default='firefox', choices=('firefox', 'chrome'))
    parser.add_argument('-k', '--ctrlmode', help="Control mode to use. If the browser control doesn't seem to work, try changing this.", default='hybrid', choices=('keyboard', 'fast', 'hybrid'))

    return parser.parse_args(argv)

def main(argv):
    args = parse_args(argv)

    if args.browser == 'firefox':
        from ffctrl import FirefoxRemoteControl
        if args.port is None:
            args.port = 32000
        ctrl = FirefoxRemoteControl(args.port)
    elif args.browser == 'chrome':
        from chromectrl import ChromeDebuggerControl
        if args.port is None:
            args.port = 9222
        ctrl = ChromeDebuggerControl(args.port)

    if args.ctrlmode == 'keyboard':
        from gamectrl import Keyboard2048Control
        gamectrl = Keyboard2048Control(ctrl)
    elif args.ctrlmode == 'fast':
        from gamectrl import Fast2048Control
        gamectrl = Fast2048Control(ctrl)
    elif args.ctrlmode == 'hybrid':
        from gamectrl import Hybrid2048Control
        gamectrl = Hybrid2048Control(ctrl)

    if gamectrl.get_status() == 'ended':
        gamectrl.restart_game()

    play_game(gamectrl)

if __name__ == '__main__':
    import sys
    exit(main(sys.argv[1:]))
