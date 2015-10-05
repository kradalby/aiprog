
import os
from module3.board import *
from tkinter import *
from util import make_function

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
            self.node_dic = {}

    def init_ui(self):

        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title('M3')

        optionsmenu = Menu(menubar, tearoff=0)
        boardsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Boards', menu=boardsmenu)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

        self.optionsmenu = optionsmenu

    def createmap(self, f=None):

        self.current_file = f

        self.board = Board(f)
        self.draw_map()

    def draw_map(self):
        self.canvas.delete('all')

        # for y in range(len(self.board.matrix) - 1, -1, -1):
        #     for x in range(len(self.board.matrix[y])):
        #         coords = (
        #             x * SIZE + 3,
        #             (len(self.board.matrix[y]) - y) * SIZE + 3,
        #             #y * SIZE + 3,
        #             x * SIZE + (SIZE + 2),
        #             (len(self.board.matrix[y]) - y) * SIZE + (SIZE + 2),
        #             #y * SIZE + (SIZE + 2),
        #         )
        #         self.node_dic[(x, y)] = self.canvas.create_rectangle(*coords,
        #                                      fill=self.color_creator(self.board.matrix[y][x]))

    def color_creator(self, node):
        if node.one:
            return "white"
        if node.zero:
            return "black"

    def add_boards_to_menu(self, menu):

        files = [f for f in os.listdir('./module3/boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'module3', 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    def run(self):

        function = make_function(['x, y'], 'x == y') #x[1][x[0]]
        constraints = {}

        for col in self.board.cols:
                constraints[(1, col)] = range(len(self.board.cols))

        for row in self.board.row:
                constraints[(0, row)] = range(len(self.board.row))
