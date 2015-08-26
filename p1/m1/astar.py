__author__ = 'Fredrik'


class Astar:

    def astar(graph, start, end):

        open = []
        close = []

        start.g = 0
        start.calculate_heuristic()
        start.calculate_f()
        open.append(start)

        while open:
            current_node = open.pop()
            
