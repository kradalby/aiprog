import os
import logging
import random

from tkinter import *
from module2.board import *
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from algorithm.gac import GAC
from algorithm.astarcsp import AstarCSP
from datastructure.vc import Constraint, Variable, CSPState
from util import make_function

class Main():

    BLACK = '#000000'
    COLORS = [BLACK, '#ffcc80', '#99ff80', '#80ffff', '#9980ff', '#ff80cc', '#e5ff80', '#80b3ff', '#e680ff']

    def __init__(self, parent):

        self.parent = parent
        self.board = None
        self.current_file = None
        self.k = 4
        self.init_ui()

    def init_ui(self):

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        boardsmenu = Menu(menubar, tearoff=0)
        kmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Boards', menu=boardsmenu)
        menubar.add_cascade(label='K', menu=kmenu)

        self.add_boards_to_menu(boardsmenu)
        self.add_k_to_menu(kmenu)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)



    def createmap(self, f=None):
        logging.debug('Creating map from %s' % os.path.basename(f))
        self.current_file = f
        self.board = Board(f)
        self.draw_map()
        self.run()

    def add_boards_to_menu(self, menu):
        files = [f for f in os.listdir('./module2/boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'module2', 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    def set_k(self, k):
        self.k = k

    def add_k_to_menu(self, menu):
        for k in range(1, 15+1):
            menu.add_command(label=str(k), command=lambda x=k: self.set_k(x))

    def draw_map(self):
        nx.draw(self.board.graph, self.board.node_pos, ax=self.ax, node_color=[Main.BLACK for x in range(len(self.board.graph))])
        #nx.draw_networkx_nodes(self.board.graph, self.board.node_pos, nodelist=[('0'), ('1')], node_color='b')
        self.canvas.draw()

    def redraw_nodes_with_color(self, state):
        self.ax.clear()
        color_list = []
        for node_id in self.board.node_pos.keys():
            for node in state.variables.values():
                if node.id == node_id:
                    color_list.append(Main.COLORS[node.domain[0] if len(node.domain) == 1 else 0])
        #print('GRAPH: ', color_list)

        #nx.draw(self.board.graph, self.board.node_pos, ax=self.ax, node_color=[Main.COLORS[random.randint(1,4)] for x in range(len(self.board.graph))])
        nx.draw(self.board.graph, self.board.node_pos, ax=self.ax, node_color=color_list)

        self.canvas.draw()

    def run(self):

        print('K VALUE: ', self.k)
        domain = [x for x in range(1, self.k + 1)]
        function = make_function(['x, y'], 'x != y')
        gac = GAC()
        nodes = {}
        constraints = {}

        for node in sorted(self.board.graph.nodes()):
            id = str(node)
            var = Variable(id)
            nodes[id] = var
            var.domain = domain
#            gac.variables.append(var)

        for key in nodes.keys():
            constraints[key] = self.board.graph.neighbors(key)

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
                self.redraw_nodes_with_color(s)
                #self.color_node(s.colored_node)

                unsatisfied = [(len(x.domain)-1) for x in gac.state.variables.values()]
                without_assignments = [1 for x in gac.state.variables.values() if  len(x.domain) > 1]
                print('UNSATISFIED CONSTRAINTS: {}'.format(sum(unsatisfied)))
                print('Vertices without assignments: {}'.format(sum(without_assignments)))
                print('Nodes in seachtree: {}'.format(len(r[1])))
                print('Number of expanded: {}'.format(len(r[2])))
