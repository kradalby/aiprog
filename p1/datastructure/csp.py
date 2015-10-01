from datastructure.node import Node


class Variable(Node):

    def __init__(self, id):
        self.id = id
        self.domain = []
        self.f = 0
        self.kids = []

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __len__(self):
        return len(self.domain)


class Constraint(Node):

    def __init__(self):
        self.f = 0
        self.variables = []
        self.function = None

    def __str__(self):
        return str(self.variables)

    def __repr__(self):
        return str(self.variables)

    def __len__(self):
        return len(self.variables)
