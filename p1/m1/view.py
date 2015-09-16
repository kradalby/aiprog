
import os
import logging
import time

from tkinter import *
from astar import *
from node import *
from board import *

SIZE = 10

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
        self.parent.title('A-Star')

        boardsmenu = Menu(menubar, tearoff=0)
        algorithmmenu = Menu(menubar, tearoff=0)
        speedmenu = Menu(menubar, tearoff=0)
        optionsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Boards', menu=boardsmenu)
        menubar.add_cascade(label='Algorithms', menu=algorithmmenu)
        menubar.add_cascade(label='Speed', menu=speedmenu)
        # menubar.add_cascade(label='Options', menu=optionsmenu)

        algorithmmenu.add_command(label='Astar', command=lambda mode="astar": self.perform_astar(mode))
        algorithmmenu.add_command(label='BFS', command=lambda mode="bfs": self.perform_astar(mode))
        algorithmmenu.add_command(label='DFS', command=lambda mode="dfs": self.perform_astar(mode))

        # optionsmenu.add_command(label='Show trail only', state=DISABLED, command=self.only_show_trail)
        # optionsmenu.add_command(label='Show all states', command=self.show_all_states)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

        self.optionsmenu = optionsmenu

    def createmap(self, f=None):

        logging.debug('Creating map from %s' % os.path.basename(f))
        self.current_file = f

        self.board = Board(f)
        self.draw_map()

    def draw_map(self):
        self.canvas.delete('all')

        for y in range(len(self.board.matrix) - 1, -1, -1):
            for x in range(len(self.board.matrix[y])):
                coords = (
                    x * SIZE + 3,
                    #(len(self.board.matrix[y]) - y) * SIZE + 3,
                    y * SIZE + 3,
                    x * SIZE + (SIZE + 2),
                    #(len(self.board.matrix[y]) - y) * 30 + 32,
                    y * SIZE + (SIZE + 2),
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
                node.x * SIZE + 2 + int((SIZE/4)),
                #(len(self.board.matrix[node.y]) - node.y) * 30 + 2 + 10,
                node.y * SIZE + 2 + int((SIZE/4)),
                node.x * SIZE + (SIZE + 2) - int((SIZE/4)),
                #(len(self.board.matrix[node.y]) - node.y) * 30 + 32 - 10,
                node.y * SIZE + (SIZE + 2) - int((SIZE/4)),
            )
            if icon == 'path':
                self.canvas.create_oval(*coords, fill='cyan', width=0)
            elif icon == 'open':
                self.canvas.create_oval(*coords, fill='black', width=0)
            elif icon == 'closed':
                self.canvas.create_line(*coords)
                self.canvas.create_line(coords[2], coords[1], coords[0], coords[3])

    def perform_astar(self, mode):

        # Do nothing if no board is loaded
        if self.board is None:
            return

        # Clear the canvas and redraw the map
        self.createmap(self.current_file)

        astar = Astar(mode, self.board)
        start, end = self.board.start, self.board.end

        for path, open, closed in astar.astar(start, end):
            self.astar_event_handler(path, open, closed)

        #if self.view_level > 0:
        #    self.draw_markers(openlist, 'open')
        #    for node in trail:
        #        if node in closedlist:
        #            closedlist.remove(node)
        #    self.draw_markers(closedlist, 'closed')

        self.draw_markers(path, 'path')


    def astar_event_handler(self, path, open, closed):
        self.canvas.delete('all')
        self.draw_map()
        self.draw_markers(path, 'path')
        self.draw_markers(open, 'open')
        #self.draw_markers(closed, 'closed')
        self.canvas.update()


    def only_show_trail(self):

        self.optionsmenu.entryconfig(0, state=DISABLED)
        self.optionsmenu.entryconfig(1, state=NORMAL)
        self.view_level = 0

    def show_all_states(self):
        self.optionsmenu.entryconfig(0, state=NORMAL)
        self.optionsmenu.entryconfig(1, state=DISABLED)
        self.view_level = 1
