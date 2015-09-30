from datastructure.node import Node
import copy

class CSPStateNode(Node):


    def __init__(self):
        self.csp = None

        self.f = 0
        self.g = 0
        self.h = 0
        self.kids = []
        self.parents = []


    def generate_kids(self):
        kids = []
        node = [x for x in sorted(self.csp.nodes) if len(x)][0]
        print(node)

        if node is None:
            return []

        for element in node.domain:
            node_copy = None
            csp_copy = copy.deepcopy(self.csp)

            for n in csp_copy.nodes:
                if n.id == node.id:
                    node_copy = n
                    n.domain = [element]

            csp_copy.rerun(node_copy)

            if not csp_copy.is_impossibrew():
                state = CSPStateNode()
                state.csp = csp_copy

            if csp_copy.is_finished():
                print('done')

            self.kids.append(state)

    def arc_cost(self):
        return 10

    def calculate_heuristic(self)
        heuristic = 0
        for node in self.csp.nodes:
            heuristic += len(node) # - 1
        return heuristic


