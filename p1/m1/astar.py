__author__ = 'Fredrik'


class Astar:


    def generate_path(self, node):
        path = [node]

        while node.parent is not None:
            node = node.parent
            path.insert(0, node)

        return path

    def astar(self, graph, start, end):

        open_list = []
        close_list = []

        start.g = 0
        start.calculate_heuristic()
        start.calculate_f()
        open_list.append(start)

        while open_list:
            current_node = open_list.pop()
            close_list.append(current_node)

            current_path = self.generate_path(current_node)
            if current_node is end:
                return current_path

        