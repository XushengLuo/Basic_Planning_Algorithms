# -*- coding: utf-8 -*-

from Buchi import buchi_graph
from TS import ts_graph
from PBA import pba_graph
from OptRun import opt_path
from Problem import problemFormulation

# +------------------------------------------+
# |     construct transition system graph    |
# +------------------------------------------+

regions, init_state, edges, uni_cost, formula = problemFormulation().Formulation()
ts_graph = ts_graph(regions, init_state, edges, uni_cost).tsGraph()


# +------------------------------------------+
# |            construct buchi graph         |
# +------------------------------------------+

buchi = buchi_graph(formula)
buchi.formulaParser()
buchi.execLtl2ba()
buchi_graph = buchi.buchiGraph()


# +------------------------------------------+
# |     construct product Buchi automaton    |
# +------------------------------------------+

pba_graph = pba_graph(ts_graph, buchi_graph).pbaGraph()

# +------------------------------------------+
# |          find the optimal path           |
# +------------------------------------------+

optimal_path = opt_path(pba_graph)
optimal_path.optRun()
optimal_path.printOptPath(ts_graph)
