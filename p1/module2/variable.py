from datastructure.node import Node


class Variable(Node):

    def __init__(self, id):
        self.id = id
        self.domain = []
        self.f = 0

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __str__(self):
        return str(self.domain)

    def __repr__(self):
        return str(self.domain)

    def __len__(self):
        return len(self.domain)
