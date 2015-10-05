class CSP:

    def __init__(self):
        self.queue = []
        self.variables = []
        self.constraints = []

    def populate_queue(self):
        for constraint in self.constraints:
            for variable in constraint.variables:
                #print('POPULATING QUEUE: VAR - {}, CONS - {}'.format(variable, constraint))
                self.queue.append((variable, constraint))

    def domain_filtering_loop(self):
        #print('QUEUELENGTH: {}'.format(len(self.queue)))
        while self.queue:

            variable, constraint = self.queue.pop(0)

            old_variable_domain = len(variable)

            self.revise(variable, constraint)

            if len(variable) != old_variable_domain:
                for const in self.constraints:
                    if variable in const.variables and const != constraint:
                        for var in constraint.variables:
                            if variable.id != var.id:
                                self.queue.append((var, constraint))

    def revise(self, variable, constraint):
        temp_domain = []

        for domain_element in variable.domain:
            valid = False
            for var in constraint.variables:
                if var.id != variable.id:
                    for var_domain in var.domain:
                        if constraint.function(domain_element, var_domain):
                            valid = True
                            break
            if valid:
                temp_domain.append(domain_element)

        variable.domain = temp_domain

    def rerun(self, variable):
        for constraint in self.constraints:
            if variable in constraint.variables:
                for var in self.variables:
                    if variable.id != var.id:
                        self.queue.append((var, constraint))
        self.domain_filtering_loop()

    def is_finished(self):
        for variable in self.variables:
            if len(variable) != 1:
                return False
        return True

    def is_valid(self, node):
        for variable in self.variables:
            if len(variable) == 0:
                #print('INVALID')
                return False

        for constraint in self.constraints:
            if node in constraint.variables:
                #print("This is constrint variables: ", constraint.variables)
                if len(constraint.variables[0]) == len(constraint.variables[1]):
                    if len(constraint.variables[0]) == 1 and len(constraint.variables[1]) == 1:
                        #print('INVALID Domain')
                        return False
        #print('VALID')
        return True

