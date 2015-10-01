import os
import logging

from tkinter import *
from module2.board import *
import matplotlib.pyplot as plt
import networkx as nx

from algorithm.csp import CSP
from algorithm.astarcsp import AstarCSP
from datastructure.csp import Constraint, Variable, CSPState
from util import make_function

class Main():
    def __init__(self, parent):

        self.parent = parent
        self.board = None
        self.current_file = None
        self.init_ui()

    def init_ui(self):

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        boardsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Boards', menu=boardsmenu)

        self.add_boards_to_menu(boardsmenu)

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

    def draw_map(self):
        plt.clf()
        nx.draw(self.board.graph, self.board.node_pos)
        #nx.draw_networkx_nodes(self.board.graph, self.board.node_pos, nodelist=[('0'), ('1')], node_color='b')
        plt.ion()
        plt.show()

    def run(self):

        domain = [1, 2, 3, 4]
        function = make_function(['x, y'], 'x != y')
        COLORS = ['w', 'r', 'b', 'g', 'y', 'p', '', '', '']

        csp = CSP()
        edges = self.board.graph.edges()

        for node in self.board.graph.nodes():
            var = Variable(str(node))
            var.domain = domain
            csp.variables.append(var)

            c = Constraint()
            c.function = function
            c.variables.append(self.board.graph.neighbors(node))
            csp.constraints.append(c)

        print("this is conts:!!! ::: : :", csp.constraints)


        # edges = self.board.graph.edges()
        # for i in range(len(edges)):
        #     c = Constraint()
        #     c.function = function
        #     c.variables.append(csp.variables[int(edges[i][0])])
        #     c.variables.append(csp.variables[int(edges[i][1])])
        #     csp.constraints.append(c)


        csp.populate_queue()


        csp.domain_filtering_loop()

        state = CSPState()

        state.csp = csp

        astar_csp = AstarCSP()

        astar_csp.csp_state = state
        astar_csp.initialize()
        while astar_csp.csp_state.csp.is_finished():
            for node in astar_csp.csp_state.variables:
                nx.draw_networkx_nodes(self.board.graph, self.board.node_pos, nodelist=[(node.id)], node_color=COLORS[node.color])
