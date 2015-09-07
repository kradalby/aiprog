__author__ = 'Fredrik'


class Node:
    def __init__(self, x, y):
        self.state = "Dont know what this is"
        self.status = ""
        self.weight = 1
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        self.parent = None
        self.kids = []
        self.start = False
        self.end = False
        self.walkable = True

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f

    def __repr__(self):
        return 'Node: {}'.format(str((self.x, self.y)))

    def __str__(self):
        return 'Node: {}'.format(str((self.x, self.y)))

    def __hash__(self):
        return hash(str((self.x, self.y)))

    def calculate_heuristic(self, goal):
        self.h = abs(goal.x - self.x) + abs(goal.y - self.y)

    def calculate_f(self):
        self.f = self.g + self.h

