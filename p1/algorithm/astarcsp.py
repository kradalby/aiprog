from datastructure.vc import CSPState
from algorithm.astar import Astar

class AstarCSP:

    def __init__(self):
        self.states = []
        self.astar = Astar(mode='astar')
        self.csp_state = None

    def initialize(self):
        self.csp_state.gac.initialize_queue()
        self.csp_state.gac.domain_filtering_loop()

    def run(self):
        generator = self.astar.astar(self.csp_state)

        #result = [x for x in generator][-1]

        #self.csp_state = list(astar_csp.astar.closed)[-1]

        #print(self.astar.closed)
        #print(self.astar.open)

        return generator
