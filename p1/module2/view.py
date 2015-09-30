import os
import logging

from tkinter import *
from module2.board import *
import matplotlib.pyplot as plt




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
        self.parent.title('M2')

        boardsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Boards', menu=boardsmenu)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=1200, height=1200)
        self.canvas.config(bg='white')
        #self.canvas.configure(scrollregion=(-300, -300, 300, 300))
        self.canvas.pack(fill=BOTH, expand=1)
        self.pack(fill=BOTH, expand=1)

    def createmap(self, f=None):
        logging.debug('Creating map from %s' % os.path.basename(f))
        self.current_file = f
        self.board = Board(f)
     #   self.draw_map()

    def add_boards_to_menu(self, menu):

        files = [f for f in os.listdir('./module2/boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'module2', 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    # def draw_map(self):
    #     self.canvas.delete('all')
    #
    #     for node in self.board.graph:
    #
    #         x = float(node[0]) * SIZE
    #         y = float(node[1]) * SIZE
    #         coords = (
    #             x + 5, y + 5, x + 15, y + 15,
    #         )
    #         self.canvas.create_oval(*coords, outline="black", width=2)

