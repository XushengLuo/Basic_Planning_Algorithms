from networkx.classes.digraph import DiGraph
from math import sqrt


def distance(p_n, c_n):
    return float("{0:.3f}".format(sqrt((p_n[0]-c_n[0])**2 + (p_n[1]-c_n[1])**2)))

def tsGraph(regions, init, edges, uni_cost):
    """constrcut transition system graph"""

    ts_graph = DiGraph(type='wTS', init=init)

    # add nodes
    for (state, label) in iter(regions.items()):
        ts_graph.add_node(state, label=label)    # ts_graph.node[(0,0,1)] = {'label': {'r', 'r1'}}


    # add self loop
    for state in ts_graph.node:
        ts_graph.add_edge(state, state, cost=0)

    # add edges
    for (p_node, c_node) in edges:
        dist = distance(p_node, c_node)
        ts_graph.add_edge(p_node, c_node, cost=dist * uni_cost)
        ts_graph.add_edge(c_node, p_node, cost=dist * uni_cost)



    return ts_graph