from datastructure.node import Node
import copy
import uuid


class Variable(Node):

    def __init__(self, id):
        self.id = id
        self.domain = []
        self.f = 0
        self.kids = []
        self.color = 0

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __len__(self):
        return len(self.domain)


class Constraint(Node):

    def __init__(self):
        self.f = 0
        self.variables = []
        self.function = None

    def __str__(self):
        return str(self.variables)

    def __repr__(self):
        return str(self.variables)

    def __len__(self):
        return len(self.variables)


class CSPState(Node):


    def __init__(self):
        self.csp = None

        self.f = 0
        self.g = 0
        self.h = 0
        self.weight = 10
        self.parent = None
        self.kids = []
        self.goal = False

    def __str__(self):
        return str(self.csp)

    def __repr__(self):
        return str(self.csp)

    def __hash__(self):
        return hash(str(uuid.uuid1()))


    def generate_kids(self):
        kids = []
        variable = [x for x in sorted(self.csp.variables) if len(x) != 0][-1]

        if variable is None:
            return []

        for element in variable.domain:
            print(element)
            variable_copy = None
            csp_copy = copy.deepcopy(self.csp)

            for n in csp_copy.variables:
                if n.id == variable.id:
                    variable_copy = n
                    n.domain = [element]
                    n.color = element

            csp_copy.rerun(variable_copy)

            for n in csp_copy.variables:
                print(n.domain)

            if not csp_copy.is_impossibrew():
                state = CSPState()
                state.csp = csp_copy
                state.parent = self
                self.kids.append(state)

                if csp_copy.is_finished():
                    self.goal = True

    def arc_cost(self):
        return 10

    def calculate_heuristic(self, *args):
        heuristic = 0
        for variable in self.csp.variables:
            heuristic += len(variable) # - 1
        return heuristic
