import time


class NotImplemented(Exception):
    pass


class Astar:

    def __init__(self, mode, astar_event_handler):
        self.mode = mode
        self.astar_event_handler = astar_event_handler
        self.open = []

    def generate_path(self, node):
        path = [node]

        while node.parent is not None:
            node = node.parent
            path.insert(0, node)

        return path

    def attach_and_evaluate(self, kid, parent, end):
        kid.parent = parent
        kid.g = parent.g + kid.weight
        kid.calculate_heuristic(end)
        kid.calculate_f()
        print(kid)

    def propagate_path_improvements(self, node):
        for kid in node.kids:
            if node.g + kid.weight < kid.g:
                kid.parent = node
                kid.g = node.g + kid.weight
                print(kid.g)
                kid.calculate_f()
                self.propagate_path_improvements(kid)


    def astar(self, start, end):
        self.open = []
        close_list = set()

        start.g = 0
        start.calculate_heuristic(end)
        start.calculate_f()
        self.append_node(start)

        while self.open:
            current_node = self.next_node()
            current_path = self.generate_path(current_node)
            self.astar_event_handler(current_path, self.open, close_list)
            close_list.add(current_node)

            if current_node is end:
                print("OPEN:")
                print(self.open)
                print("CLOSED:")
                print(close_list)
                return current_path

            for kid in current_node.kids:

                #if kid in close_list:
                #    continue

                if kid not in self.open and kid not in close_list:
                    self.attach_and_evaluate(kid, current_node, end)
                    self.append_node(kid)

                elif current_node.g + kid.weight < kid.g:
                    self.attach_and_evaluate(kid, current_node, end)

                    if kid in close_list:
                        print('prop')
                        self.propagate_path_improvements(kid)

            time.sleep(0.2)
        print("OPEN:")
        print(self.open)
        print("CLOSED:")
        print(close_list)
        return self.generate_path(current_node)

    def next_node(self):
        if self.mode == "dfs":
            return self.open.pop()
        else:
            return self.open.pop(0)

    def append_node(self, node):
        if self.mode == "astar":
            self.open.append(node)
            self.open.sort()
        else:
            self.open.append(node)
