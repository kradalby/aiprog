
class GAC:

    def __init__(self):
        self.queue = []
        self.state = None

    def initialize_queue(self):

        for node_id, constraints in self.state.constraints.items():
            temp_node = self.state.variables[node_id]
            #print("TEMP CONS: ", constraints)
            #print("This is var keys: ", self.state.variables.keys())
            for constraint in constraints:
                self.queue.append((temp_node, self.state.variables[constraint]))
        self.queue.sort(key=lambda tup: tup[0].id)
        #print("This is queue length: ", len(self.queue))
        #print("This queue: ", self.queue)

    def domain_filtering_loop(self):

        while self.queue:
            focal_variable, variable = self.queue.pop(0)

            variable_domain_length = len(variable.domain)

            self.revise(focal_variable, variable)

            if len(variable.domain) != variable_domain_length:
                list_of_neighbor_node = self.state.constraints[variable.id]
                #if shit goes wrong check it!!!
                for node_id in list_of_neighbor_node:
                    self.queue.append((self.state.variables[node_id], variable))

    def revise(self, focal_variable, variable):

        temp_domain = []
        #print("This is focal and variable", focal_variable, variable)
        for x in variable.domain:
            #print("This is x: ", x)
            valid = False
            for y in focal_variable.domain:
                if self.state.constraint.function(x, y):
                    valid = True
                    #print("VALID: ", valid, "x = ", x, "y = ", y)
                    break
            #if shit goes wrong check it!!! is it x or y that needs domain update?
            if valid:
                temp_domain.append(x)
        variable.domain = temp_domain

    def rerun(self, node):

        list_of_neighbor_node = self.state.constraints[node.id]

        for node_id in list_of_neighbor_node:
            self.queue.append((node, self.state.variables[node_id]))
        self.domain_filtering_loop()


class NonogramGAC(GAC):
    def revise(self, focal_variable, variable):

        try:

            temp_domain = []
            #print("This is focal and variable", focal_variable, variable)
            for x in variable.domain:
                #print("PRINT OF x[variable.id[1]]", x)
                z = x[variable.id[1]]
                #print("This is x: ", x)
                valid = False
                for y in focal_variable.domain:
                    q = y[focal_variable.id[1]]
                    if self.state.constraint.function(z, q):
                        valid = True
                        #print("VALID: ", valid, "x = ", x, "y = ", y)
                        break
                #if shit goes wrong check it!!! is it x or y that needs domain update?
                if valid:
                    temp_domain.append(x)
            variable.domain = temp_domain
        except:
            pass
