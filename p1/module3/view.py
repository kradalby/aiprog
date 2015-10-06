
import os
from module3.board import *
from tkinter import *
from util import make_function, generate_permutations
from algorithm.gac import NonogramGAC
from algorithm.astarcsp import AstarCSP
from datastructure.nonograms import CSPState
from datastructure.nonograms import Constraint, Variable
from pprint import pprint


SIZE = 30


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

    def generate_matrix(self, state):

        matrix = [None for x in range(self.board.num_rows)]
        for var in state.variables.values():
            if var.id[0] == 0:
                matrix[var.id[1]] = var.domain[0]
        self.board.matrix = matrix

        for x in matrix:
            print(x)
        print('---------------------------------')
        for y in state.variables.values():
            if y.id[0] == 1:
                print(y.domain[0])

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
        self.run()

    def draw_map(self):
        self.canvas.delete('all')

        for y in range(len(self.board.matrix)):
            for x in range(len(self.board.matrix[y])):
                coords = (
                    x * SIZE + 3,
                    #(len(self.board.matrix[y]) - y) * SIZE + 3,
                    y * SIZE + 3,
                    x * SIZE + (SIZE + 2),
                    #(len(self.board.matrix[y]) - y) * SIZE + (SIZE + 2),
                    y * SIZE + (SIZE + 2),
                )
                color = 'pink' if self.board.matrix[y][x] else 'white'
                self.node_dic[(x, y)] = self.canvas.create_rectangle(*coords,
                                             fill= color)

    def update_map(self):
        for y in range(len(self.board.matrix)):
            #print("this is y:", self.board.matrix[y])
            for x in range(len(self.board.matrix[y])):
                if self.board.matrix[y][x]:
                    #print("Render cores", y, ":", x)
                    #self.canvas.itemconfig(self.node_dic[(x, y)], fill='white')
                    self.canvas.itemconfig(self.node_dic[(x, y)], fill='pink')

    def add_boards_to_menu(self, menu):

        files = [f for f in os.listdir('./module3/boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'module3', 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    def run(self):

        gac = NonogramGAC()
        nodes = {}
        function = make_function(['x', 'y'], 'x == y') #x[1][x[0]]
        constraints = {}

        for row in range(len(self.board.rows)):
            constraints[(0, row)] = [(1, x) for x in range(len(self.board.cols))]
            node = Variable((0, row))
            node.domain = generate_permutations(self.board.rows[row], len(self.board.cols))
            print("xxxxx", self.board.rows[row])
            print(node.domain)
            nodes[(0, row)] = node

        for col in range(len(self.board.cols)):
            constraints[(1, col)] = [(0, x) for x in range(len(self.board.rows))]
            node = Variable((1, col))
            node.domain = generate_permutations(self.board.cols[col], len(self.board.rows))
            nodes[(1, col)] = node


        constraint = Constraint()
        constraint.function = function
        state = CSPState()
        state.constraints = constraints
        state.constraint = constraint
        state.variables = nodes
        state.gac = gac
        gac.state = state
        astar_csp = AstarCSP()
        astar_csp.csp_state = state
        astar_csp.initialize()
        pprint(state.constraints)


        for r in astar_csp.run():
            if r[0]:
                s = r[0][-1]
                self.generate_matrix(s)
                self.draw_map()
                #self.update_map()
                print("This is s: ", s)
