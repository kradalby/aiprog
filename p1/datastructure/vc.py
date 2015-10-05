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


class Constraint():

    def __init__(self):
        self.function = None


class CSPState(Node):


    def __init__(self):
        self.gac = None

        self.variables = {}
        self.constraints = {}
        self.constraint = None
        self.f = 0
        self.g = 0
        self.h = 0
        self.weight = 1
        self.parent = None
        self.kids = []
        self.end = False
        self.hash = str(uuid.uuid1())
        self.gac = None

    def __str__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __repr__(self):
        return 'CSPState: end: {}, H: {}, F: {}'.format(self.end, self.h, self.f)

    def __hash__(self):
        return hash(self.hash)

    def generate_kids(self):
        for variable in sorted(self.variables.values()):
            if len(variable) > 1:
                for domain_element in variable.domain:
                    new_variable = None

                    new_state = CSPState()
                    new_state.hash = str(uuid.uuid1())
                    new_state.gac = self.gac
                    new_state.gac.state = new_state
                    new_state.constraints = self.constraints
                    new_state.constraint = self.constraint
                    new_state.variables = copy.deepcopy(self.variables)
                    new_state.variables[variable.id].domain = [domain_element]
                    new_variable = new_state.variables[variable.id]

                    new_state.gac.rerun(new_state.variables[variable.id])

                    if new_state.is_valid(new_variable):
                        #print('HEURISTIC: ', self.h)
                        # for var in new_state.variables.values():
                        #     print(var)
                        new_state.parent = self

                        if new_state.is_finished():
                            #print('FINISHED')
                            new_state.end = True

                        self.kids.append(new_state)
                break

    def calculate_heuristic(self, *args):
        heuristic = 0
        for variable in self.variables.values():
            heuristic += len(variable) - 1
        self.h = heuristic

    def is_finished(self):
        for variable in self.variables.values():
            if len(variable) != 1:
                return False
        return True

    def is_valid(self, node):
        #if len(node.domain) == 1:
        #    for constraint in self.constraints:
        #        if node in constraints.variables:
        #            var0 = constraints.variables[0]
        #            var1 = constraints.variables[0]
        #            if var0[0] == var1[0]:
        #                print('INVALID - CONSTRAINT NOT MET')
        #                return False

        for variable in self.variables.values():
            if len(variable) == 0:
                #print('INVALID - DOMAIN IS TO LITTLE')
                return False
        #print('VALID')
        return True
