
import os
import logging
import time

from tkinter import *
from astar import *
from node import *
from board import *


class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')

        self.parent = parent
        self.board = None
        self.current_file = None
        self.canvas = None
        self.view_level = 0
        self.init_ui()

    def init_ui(self):

        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title(u'A-Star')

        boardsmenu = Menu(menubar, tearoff=0)
        algorithmmenu = Menu(menubar, tearoff=0)
        optionsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label=u'Boards', menu=boardsmenu)
        menubar.add_cascade(label=u'Algorithms', menu=algorithmmenu)
        menubar.add_cascade(label=u'Options', menu=optionsmenu)

        algorithmmenu.add_command(label=u'Astar', command=self.perform_astar)
        #algorithmmenu.add_command(label=u'BFS', command=self.perform_bfs)

        optionsmenu.add_command(label=u'Show trail only', state=DISABLED, command=self.only_show_trail)
        optionsmenu.add_command(label=u'Show all states', command=self.show_all_states)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

        self.optionsmenu = optionsmenu

    def createmap(self, f=None):

        logging.debug('Creating map from %s' % os.path.basename(f))
        self.current_file = f

        self.board = Board(f)

        self.canvas.delete('all')

        for y in range(len(self.board.matrix) - 1, -1, -1):
            print(y)
            for x in range(len(self.board.matrix[y])):
                coords = (
                    x * 30 + 3,
                    (len(self.board.matrix[y]) - y) * 30 + 3,
                    x * 30 + 32,
                    (len(self.board.matrix[y]) - y) * 30 + 32,
                )
                self.canvas.create_rectangle(*coords,
                                             fill=self.color_creator(self.board.matrix[y][x]))

    def color_creator(self, node):

        if node.end:
            return "yellow"
        if node.start:
            return "black"
        if node.walkable:
            return "white"
        if not node.walkable:
            return "red"

    def add_boards_to_menu(self, menu):

        files = [f for f in os.listdir('./boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    def draw_markers(self, nodes, icon):

        for node in nodes:
            coords = (
                node.x * 30 + 2 + 10,
                node.y * 30 + 2 + 10,
                node.x * 30 + 32 - 10,
                node.y * 30 + 32 - 10,
            )
            if icon == 'path':
                self.canvas.create_oval(*coords, fill='cyan', width=0)
            elif icon == 'open':
                self.canvas.create_oval(*coords, fill='black', width=0)
            elif icon == 'closed':
                self.canvas.create_line(*coords)
                self.canvas.create_line(coords[2], coords[1], coords[0], coords[3])

    def perform_astar(self):

        # Do nothing if no board is loaded
        if self.board is None:
            return

        logging.debug('Start %s' % self.board.get_start())
        logging.debug('Dest %s' % self.board.get_goal())

        # Clear the canvas and redraw the map
        self.createmap(self.current_file)

        trail, openlist, closedlist = a_star(self.board.graph, self.board.get_start(), self.board.get_goal())

        if self.view_level > 0:
            self.draw_markers(openlist, 'open')
            for node in trail:
                if node in closedlist:
                    closedlist.remove(node)
            self.draw_markers(closedlist, 'closed')

        self.draw_markers(trail, 'path')

    def only_show_trail(self):

        self.optionsmenu.entryconfig(0, state=DISABLED)
        self.optionsmenu.entryconfig(1, state=NORMAL)
        self.view_level = 0

    def show_all_states(self):
        self.optionsmenu.entryconfig(0, state=NORMAL)
        self.optionsmenu.entryconfig(1, state=DISABLED)
        self.view_level = 1
