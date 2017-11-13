from networkx.classes.digraph import DiGraph
from math import sqrt

class ts_graph(object):
    """
    Construct transition system graph
    Parameter:
        regions : a partition of work space
        init    : initial state
        edges   : connection between states
        uni_cost: unit cost for weight
    """

    def __init__(self, regions, init, edges, uni_cost):
        self.regions = regions
        self.init = init
        self.edges = edges
        self.uni_cost = uni_cost


    def tsGraph(self):
        """ build graph
        """
        # initialize graph
        self.ts_graph = DiGraph(type='wTS', init=self.init)
        # add node
        self.add_node()
        #add edge
        self.add_edge()

        return self.ts_graph

    def add_node(self):
        """"add nodes
        """
        for (state, label) in iter(self.regions.items()):
            self.ts_graph.add_node(state, label=label)    # ts_graph.node[(0,0,1)] = {'label': {'r', 'r1'}}

    def add_edge(self):
        """ add edges
        """
        # add self loop
        for state in self.ts_graph.nodes:
            self.ts_graph.add_edge(state, state, cost=0)

        # add edges
        for (p_node, c_node) in self.edges:
            dist = self.distance(p_node, c_node)
            self.ts_graph.add_edge(p_node, c_node, cost=dist * self.uni_cost)
            self.ts_graph.add_edge(c_node, p_node, cost=dist * self.uni_cost)

    def distance(self, p_n, c_n):
        """compute distance between states
        """
        return float("{0:.3f}".format(sqrt((p_n[0] - c_n[0]) ** 2 + (p_n[1] - c_n[1]) ** 2)))