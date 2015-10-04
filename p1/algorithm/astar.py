import time


class NotImplemented(Exception):
    pass


class Astar:

    def __init__(self, mode):
        self.mode = mode
        self.open = []
        self.closed = set()

    def generate_path(self, node):
        path = [node]
        #path_dic = {(node.y, node.x): node}

        while node.parent is not None:
            node = node.parent
         #   path_dic[(node.y, node.x)] = node
            path.insert(0, node)

        return path

    def attach_and_evaluate(self, kid, parent, end):
        kid.parent = parent
        kid.g = parent.g + kid.weight
        kid.calculate_heuristic(end)
        kid.calculate_f()

    def propagate_path_improvements(self, node):
        for kid in node.kids:
            if node.g + kid.weight < kid.g:
                kid.parent = node
                kid.g = node.g + kid.weight
                kid.calculate_f()
                self.propagate_path_improvements(kid)


    def astar(self, start, end=None):
        self.open = []

        start.g = 0
        start.calculate_heuristic(end)
        start.calculate_f()
        self.append_node(start)

        print('ASTAR START')

        while self.open:
            current_node = self.next_node()
            current_path = self.generate_path(current_node)
            yield current_path, self.open, self.closed
            self.closed.add(current_node)

            print('ASTAR NODE INFO:', current_node.end)

            if current_node is end or current_node.end:
                print("OPEN:")
                print(self.open)
                print("CLOSED:")
                print(self.closed)
                print('LENGHT: {}'.format(len(current_path)))
                return current_path, self.open, self.closed

            current_node.generate_kids()
            for kid in current_node.kids:

                #if kid in self.closed:
                #    continue

                if kid not in self.open and kid not in self.closed:
                    self.attach_and_evaluate(kid, current_node, end)
                    self.append_node(kid)

                elif current_node.g + kid.weight < kid.g:
                    self.attach_and_evaluate(kid, current_node, end)

                    if kid in self.closed:
                        self.propagate_path_improvements(kid)

        return self.generate_path(current_node)

    def next_node(self):
        if self.mode == "dfs":
            return self.open.pop()
        else:
            node =  self.open.pop(0)
            print("Next node is: ", node, ", H valuse is: ", node.h)
            return node
    def append_node(self, node):
        if self.mode == "astar":
            self.open.append(node)
            self.open.sort()
        else:
            self.open.append(node)
