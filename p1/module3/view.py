
import os
from module3.board import *
from tkinter import *
from util import make_function, generate_permutations
from algorithm.gac import NonogramGAC
from algorithm.astarcsp import AstarCSP
from datastructure.nonograms import CSPState
from datastructure.nonograms import Constraint, Variable


SIZE = 10


class Main(Frame):
    '''
    Class responsible for drawing the graphical interface, and the steps of the algorithm.
    '''


    def __init__(self, parent):
        '''
        Initializes tkinter, and the guis controller.
        '''
        Frame.__init__(self, parent)
        self.parent = parent
        self.width = 600
        self.height = 600
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0, width=self.width, height=self.height)
        self.init_ui()

    def build(self):
        '''
        Builds a graphial representation of a given board.
        '''
        #self.board = board
        print(dir(self.board))
        self.rows = self.board.number_of_columns
        self.columns = self.board.number_of_rows
        if self.rows > self.columns:
            self.square_size = (self.width / self.rows) / 1.5
        else:
            self.square_size = (self.height / self.columns) / 1.5
        for row in reversed(range(self.rows)):
            for column in range(self.columns):
                x1 = row * self.square_size
                y1 = column * self.square_size
                x2 = row * self.square_size + self.square_size
                y2 = column * self.square_size + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2)

        draw_start_x = (self.square_size * self.rows) + self.square_size
        draw_start_y = (self.square_size * self.columns) + self.square_size
        x_count = 0
        y_count = self.square_size / 2
        for row in self.board.rows_info:
            for num in row:
                self.canvas.create_text(draw_start_x + x_count, y_count, text=str(num))
                x_count += 20
            y_count += self.square_size
            x_count = 0

        x_count = self.square_size / 2
        y_count = 0
        for column in self.board.columns_info:
            for num in column:
                self.canvas.create_text(x_count, draw_start_y + y_count, text=str(num))
                y_count += 20
            y_count = 0
            x_count += self.square_size

        self.canvas.pack()

    def draw_square(self, x, y, num):
        '''
        Draws a square from its x and y coordinates, with the given color.
        '''
        x1 = x * self.square_size
        y1 = y * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        if num == 1:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue')
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

#class Main(Frame):
#    def __init__(self, parent):
#            Frame.__init__(self, parent, background='white')
#
#            self.parent = parent
#            self.board = None
#            self.current_file = None
#            self.canvas = None
#            self.view_level = 0
#            self.init_ui()
#            self.node_dict = {}

    def init_ui(self):

        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title('M3')

        optionsmenu = Menu(menubar, tearoff=0)
        boardsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Boards', menu=boardsmenu)

        self.add_boards_to_menu(boardsmenu)

        #self.canvas = Canvas(self, width=800, height=600)
        #self.canvas.config(bg='white')
        #self.canvas.pack(fill=BOTH, expand=1)

        #self.pack(fill=BOTH, expand=1)

        #self.optionsmenu = optionsmenu


    def createmap(self, f=None):

        self.current_file = f

        self.board = Board(f)
        self.build()
        self.run()

#    def draw_map(self):
#        self.canvas.delete('all')
#
#        for y in range(len(self.board.matrix) - 1, -1, -1):
#            for x in range(len(self.board.matrix[y])):
#                coords = (
#                    x * SIZE + 3,
#                    (len(self.board.matrix[y]) - y) * SIZE + 3,
#                    #y * SIZE + 3,
#                    x * SIZE + (SIZE + 2),
#                    (len(self.board.matrix[y]) - y) * SIZE + (SIZE + 2),
#                    #y * SIZE + (SIZE + 2),
#                )
#                self.node_dic[(x, y)] = self.canvas.create_rectangle(*coords,
                                             #fill=self.color_creator(self.board.matrix[y][x]))

#    def color_creator(self, node):
#        if node.one:
#            return "white"
#        if node.zero:
#            return "black"

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
        function = make_function(['x, y'], 'x == y') #x[1][x[0]]
        constraints = {}

        for row in range(len(self.board.rows)):
            constraints[(0, row)] = [(1, x) for x in range(len(self.board.rows))]
            node = Variable((0, row))
            node.domain = generate_permutations(self.board.rows[row], len(self.board.rows))
            nodes[(0, row)] = node

        for col in range(len(self.board.cols)):
            constraints[(1, col)] = [(0, x) for x in range(len(self.board.cols))]
            node = Variable((1, col))
            node.domain = generate_permutations(self.board.cols[col], len(self.board.cols))
            nodes[(1, col)] = node

        print("this is variables: ", nodes)
        for y in constraints:
            print("this is const: ", y)

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


        for r in astar_csp.run():
            if r[0]:
                s = r[0][-1]
                print("This is s: ", s)
