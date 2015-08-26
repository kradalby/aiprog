__author__ = 'Fredrik'


class Node:

    def __init__(self):
        self.state = "Dont know what this is"
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        self.status = ""
        self.parent = None
        self.kids = []

    def __lt__(self, other):
        return self.f < other.f

    # Todo: this needs to be implemented
    def calculate_heuristic(self):
        self.h = 0

    def calculate_f(self):
        self.f = self.g + self.h