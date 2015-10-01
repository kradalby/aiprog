from datastructure.csp import CSPState
from algorithm.astar import Astar

class AstarCSP:

    def __init__(self):
        self.states = []
        self.astar = Astar(mode='astar')
        self.csp_state = None

    def initialize(self):
        self.csp_state.csp.populate_queue()
        self.csp_state.csp.domain_filtering_loop()

    def run(self):
        generator = self.astar.astar(self.csp_state)

        return generator
