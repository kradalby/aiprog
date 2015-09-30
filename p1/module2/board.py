from ast import literal_eval
import networkx as nx
import matplotlib.pyplot as plt


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

            for _ in range(self.num_edge):
                temp = content.pop(0).split()
                self.graph.add_edge(temp.pop(0), temp.pop(0))

        print(self.node_pos)

        nx.draw(self.graph, self.node_pos)
        plt.show()



