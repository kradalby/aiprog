class CSP:

    def __init__(self):
        self.queue = []
        self.variables = []
        self.constraints = []

    def populate_queue(self):
        for constraint in self.constraints:
            print('C', constraint)
            for variable in self.variables:
                print('V', variable)
                self.queue.append((variable, constraint))

    def domain_filtering_loop(self):
        while self.queue:

            variable, constraint = self.queue.pop(0)

            old_variable_domain = len(variable.domain)

            self.revise(variable, constraint)

            if len(variable) != old_variable_domain:
                for const in self.constraints:
                    if variable in const.variables and const != constraint:
                        for var in constraint.variables:
                            if variable != var:
                                self.queue.append((var, constraint))

    def revise(self, variable, constraint):
        #temp_domain = []

        #for domain_element in variable.domain:
        #    valid = False
        #    for var in self.variables:
        #        if var != variable:
        #            for domain in var:
        #                print(domain_element, domain)
        #                if constraint.function(domain_element, domain):
        #                    valid = True
        #                    break
        #    if valid:
        #        temp_domain.append(domain_element)

        #variable.domain = temp_domain

        temp_domain = []
        for x in variable.domain:
            valid = False
            for var in self.variables:
                if var.id != variable.id:
                    for y in var.domain:
                        if constraint.function(x, y):
                            print(x, y)
                            valid = True
                            break
            if valid:
                temp_domain.append(x)

        variable.domain = temp_domain

    def rerun(self, variable):
        for const in self.constraints:
            if variable in const:
                for var in self.variables:
                    if variable != var:
                        self.queue.append((var, constraint))

    def is_finished(self):
        for variable in self.variables:
            if len(variable) > 1:
                return False
        return True

    def is_impossibrew(self):
        for variable in self.variables:
            if len(variable) == 0:
                return True
        return False


if __name__ == '__main__':
    from util import make_function
    from module2.constraint import Constraint
    from module2.variable import Variable

    x = Variable(1)
    y = Variable(2)
    z = Variable(3)

    x.domain = [0, 1, 2, 3]
    y.domain = [0, 1, 2, 3, 4, 5]
    z.domain = [4, 5, 6, 7]

    c1 = Constraint()
    c2 = Constraint()

    c1.function = make_function(['x', 'y'], 'x > y')
    c2.function = make_function(['x', 'y', 'z'], 'x + y > z')

    csp = CSP()

    csp.variables.append(x)
    csp.variables.append(y)
    csp.variables.append(z)
    csp.constraints.append(c1)
    #csp.constraints.append(c2)

    csp.populate_queue()
    print(csp.queue)
    csp.domain_filtering_loop()

    print(csp.variables)

