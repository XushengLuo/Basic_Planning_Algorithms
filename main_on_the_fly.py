# -*- coding: utf-8 -*-

from Buchi import buchi_graph
from TS import ts_graph
from Problem import problemFormulation
from AdjProd import adj_prod
from networkx.classes.digraph import DiGraph
from OptRun_on_the_fly import opt_path_on_the_fly
import datetime

start = datetime.datetime.now()
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
# |          find the optimal path           |
# +------------------------------------------+

pba = adj_prod(DiGraph(type='PBA', init=[], accept=[]), ts_graph, buchi_graph)
pba.init_accept()

optimal_path = opt_path_on_the_fly(ts_graph, buchi_graph, pba)
optimal_path.optRun()
optimal_path.printOptPath()

print((datetime.datetime.now() - start).total_seconds())