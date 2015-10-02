from datastructure.node import Node
import copy
import uuid
import time


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
        return 'VARIABLE - ID: {}, D: {}'.format(self.id, self.domain)

    def __repr__(self):
        return 'VARIABLE - ID: {}, D: {}'.format(self.id, self.domain)

    def __len__(self):
        return len(self.domain)


class Constraint(Node):

    def __init__(self):
        self.f = 0
        self.variables = []
        self.function = None

    def __str__(self):
        return 'CONSTRAINT - VARS: {}'.format(self.variables)

    def __repr__(self):
        return 'CONSTRAINT - VARS: {}'.format(self.variables)

    def __len__(self):
        return len(self.variables)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class CSPState(Node):


    def __init__(self):
        self.csp = None

        self.f = 0
        self.g = 0
        self.h = 0
        self.weight = 1
        self.parent = None
        self.kids = []
        self.colored_node = None
        self.end = False

    def __str__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __repr__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __hash__(self):
        return hash(str(uuid.uuid1()))


    def generate_kids(self):
        kids = []
        print('CSP variables: ',self.csp.variables)
        variable = [x for x in sorted(self.csp.variables) if len(x) != 0][-1]
        print('CSP var after filt: ', variable)

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
                    self.colored_node = n

            csp_copy.rerun(variable_copy)

            # for n in csp_copy.variables:
            #     print(n)

            if csp_copy.is_valid():
                time.sleep(1.5)
                print('POSSIBLE')
                for n in csp_copy.variables:
                    print(n)
                print('HEURISTIC: ', self.h)
                state = CSPState()
                state.csp = csp_copy
                state.parent = self
                self.kids.append(state)

                if csp_copy.is_finished():
                    print('POSSIBLE - FINISHED')
                    self.end = True

    def calculate_heuristic(self, *args):
        heuristic = 0
        for variable in self.csp.variables:
            heuristic += len(variable) #- 1
        self.h = heuristic
