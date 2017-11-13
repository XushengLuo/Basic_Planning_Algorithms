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
    optimal_pre.append(ts_graph.node[state[0]]['label'][0])

optimal_suf = [optimal_pre[-1]]
for state in optimal_path[1][1]:
    optimal_suf.append(ts_graph.node[state[0]]['label'][0])

print('The total cost of the path is: ', end='')
print(optimal_path[0])

print('The prefix path is:    ', end='')
for region in optimal_pre[0:-3]:
    print(region + ' -> ', end='')
print(optimal_pre[-3])

print('The suffix path is:    ', end='')
if optimal_suf.__len__() == 2:
    print(optimal_suf[0])
else:
    for region in optimal_suf[0:-3]:
        print(region + ' -> ', end='')
    print(optimal_suf[-3])