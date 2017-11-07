# -*- coding: utf-8 -*-

import Buchi
import TS
import PBA
import OptRun
import Problem
"""
    Propositonal Symbols:
        true, false
	    any lowercase string

    Boolean operators:
        !   (negation)
        ->  (implication)
	    <-> (equivalence)
        &&  (and)
        ||  (or)

    Temporal operators:
        []  (always)
        <>  (eventually)
        U   (until) 
        V   (release)
        X   (next)
"""
# construct transition system graph
##############################
# motion FTS
regions, init_state, edges, uni_cost, formula = Problem.problemFormulation()
ts_graph = TS.tsGraph(regions, init_state, edges, uni_cost)
#print(ts_graph.succ)

# construct buchi graph

formula = Buchi.formulaParser(formula)
buchi_str = Buchi.execLtl2ba(formula).decode("utf-8")
buchi_graph = Buchi.buchiGraph(buchi_str)

#print(buchi_str)
# construct product Buchi automaton
pba_graph = PBA.pbaGraph(ts_graph, buchi_graph)

# find the optimal path
optimal_path = OptRun.optRun(pba_graph)
optimal_pre = []
for state in optimal_path[1][0]:
    optimal_pre.append(ts_graph.node[state]['label'][0])

optimal_suf = []
for state in optimal_path[1][1]:
    optimal_suf.append(ts_graph.node[state]['label'][0])
print(optimal_pre)
print(optimal_suf)