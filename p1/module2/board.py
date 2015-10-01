import networkx as nx
from datastructure.csp import Variable


class Board():
    def __init__(self, filename):
        self.read_file(filename)
        self.num_vert = []
        self.num_edge = []

    def read_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read().splitlines()
            temp = content.pop(0).split()

            self.num_vert = int(temp.pop(0))
            self.num_edge = int(temp.pop(0))

            self.graph = nx.Graph()
            self.node_pos = {}

            for _ in range(self.num_vert):

                temp = content.pop(0).split()

                self.graph.add_node(temp[0], x=temp[1], y=temp[2])
                self.node_pos[str(temp[0])] = (float(temp[1]), float(temp[2]))


            self.edge_dic = {}

            for _ in range(self.num_edge):
                temp = content.pop(0).split()
                self.graph.add_edge(temp[0], temp[1])
                self.edge_dic[str(temp[0])] = (int(temp[1]))

            #print("This is edges: ", self.graph.edge)