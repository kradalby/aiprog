from datastructure.node import Node


class Constraint(Node):

    def __init__(self):
        self.variables = []
        self.function = None

    def __str__(self):
        return str(self.function)

    def __repr__(self):
        return str(self.function)

    def __len__(self):
        return len(self.variables)
