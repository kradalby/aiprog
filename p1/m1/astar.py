__author__ = 'Fredrik'


class NotImplemented(Exception):
    pass


class Astar:
    def generate_path(self, node):
        path = [node]

        while node.parent is not None:
            node = node.parent
            path.insert(0, node)

        return path

    def attach_and_evaluate(self, kid, parent, end):
        kid.g = parent.g + kid.weight
        kid.calculate_heuristic(end)
        kid.calculate_f()
        kid.parent = parent

    def propagate_path_improvements(self, node):
        for kid in node.kids:
            if node.g + kid.weight < kid.g:
                kid.parent = node
                kid.g = node.g + kid.weight
                kid.calculate_f()
                self.propagate_path_improvements(kid)


    def astar(self, start, end):

        open_list = []
        close_list = set()

        start.calculate_heuristic(end)
        start.calculate_f()
        open_list.append(start)

        while open_list:
            print(open_list)
            current_node = open_list.pop(0)
            close_list.add(current_node)

            current_path = self.generate_path(current_node)
            if current_node is end:
                return current_path

            for kid in current_node.kids:

                if kid in close_list:
                    continue

                if kid not in open_list:
                    self.attach_and_evaluate(kid, current_node, end)
                    open_list.append(kid)
                    open_list.sort()

                elif current_node.g + kid.weight < kid.g:
                    self.attach_and_evaluate(kid, current_node, end)
                    #open_list.add(kid)

                    if kid in close_list:
                        propagate_path_improvements(kid)


        print("Open: {}".format(open_list))
        print("Closed: {}".format(close_list))

        return generate_path(current_node)
