
class Node:
    def __init__(self, x, y):
        self.weight = 1
        self.x = x
        self.y = y
        self.g = 0
        self.h = 1
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
        return 'Node: {}, F: {}, G: {}, H: {}'.format(str((self.x, self.y)), self.f, self.g, self.h)

    def __str__(self):
        return 'Node: {}, F: {}, G: {}, H: {}'.format(str((self.x, self.y)), self.f, self.g, self.h)

    def __hash__(self):
        return hash(str((self.x, self.y)))

    def arc_cost(self, node):
        return self.weight

    def calculate_heuristic(self, goal):
        pass

    def calculate_f(self):
        self.f = self.g + self.h

    def generate_kids(self):
        pass
