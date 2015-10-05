from datastructure.node import Node
from algorithm.csp import CSP
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
        return self.id == other.id
        #return len(self) == len(other)

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
        self.gac = None

        self.variables = {}
        self.constraints = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.weight = 1
        self.parent = None
        self.kids = []
        self.end = False
        self.hash = str(uuid.uuid1())

    def __str__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __repr__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __hash__(self):
        return hash(self.hash)


    #def generate_kids(self):
    #    for variable in sorted(self.csp.variables):
    #        if len(variable) > 1:
    #            for element in variable.domain:
    #                variable_copy = None

    #                #new_csp = copy.deepcopy(self.csp)
    #                new_csp = CSP()
    #                new_csp.constraints = self.csp.constraints

    #                for n in self.csp.variables:
    #                    new_csp.variables.append(copy.deepcopy(n))
    #                    if n.id == variable.id:
    #                        variable_copy = n
    #                        n.domain = [element]

    #                new_csp.rerun(variable_copy)

    #                # for n in csp_copy.variables:
    #                #     print(n)

    #                if new_csp.is_valid(variable_copy):
    #                    print('POSSIBLE')
    #                    for n in new_csp.variables:
    #                        print(n)
    #                    print('HEURISTIC: ', self.h)
    #                    state = CSPState()
    #                    state.csp = new_csp
    #                    state.parent = self

    #                    if state.csp.is_finished():
    #                        print('POSSIBLE - FINISHED')
    #                        state.end = True

    #                    self.kids.append(state)
    #            break

    def generate_kids(self):
        for variable in sorted(self.variables.values()):
            if len(variable) > 1:
                for domain_element in variable.domain:
                    new_variable = None

                    new_state = CSPState()
                    new_state = str(uuid.uuid1())
                    new_state.gac = self.gac
                    new_state.constraints = self.constraints
                    new_state.variables = copy.deepcopy(self.variables)
                    new_state.variables[variable.id] = [domain_element]

                    new_state.gac.rerun(new_state.variables[variable.id])

                    if new_state.is_valid():
                        print('HEURISTIC: ', self.h)
                        for var in new_state.variable:
                            print(var)
                        new_state.parent = self

                        if new_state.is_finished():
                            print('FINISHED')
                            new_state.end = True

                        self.kids.append(new_state)
                break

    def calculate_heuristic(self, *args):
        heuristic = 0
        for variable in self.csp.variables:
            heuristic += len(variable) - 1
        self.h = heuristic

    def is_finished(self):
        for variable in self.variables:
            if len(variable) != 1:
                return False
        return True

    def is_valid(self, node):
        if len(node.domain) == 1:
            for constraint in self.constraints:
                if node in constraints.variables:
                    var0 = constraints.variables[0]
                    var1 = constraints.variables[0]
                    if var0[0] == var1[0]:
                        print('INVALID - CONSTRAINT NOT MET')
                        return False

        for variable in self.variables:
            if len(variable) == 0:
                print('INVALID - DOMAIN IS TO LITTLE')
                return False
        print('VALID')
        return True
