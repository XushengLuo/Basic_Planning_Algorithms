# -*- coding: utf-8 -*-

import subprocess
import os.path
import re
from networkx.classes.digraph import DiGraph

def execLtl2ba(formula):
    """ given formula, exectute the ltl2ba"""

    dirname = os.path.dirname(__file__)
    buchi_str = subprocess.check_output(dirname + "/./ltl2ba -f \"" + formula + "\"", shell=True)
    return buchi_str

def formulaParser(formula):
    indicator = 'FG'

    if [True for i in indicator if i in formula]:
        return formula.replace('F', '<>').replace('G', '[]')

    return formula

def buchiGraph(string):
    """parse the output of ltl2ba"""
    # find state
    state_re = re.compile(r'\n(\w+):\n\t')
    state_group = re.findall(state_re, string)

    # find initial and accepting states
    init = [s for s in state_group if 'init' in s]
    accep = [s for s in state_group if 'accept' in s]

    """
    Format:
        buchi_graph.node = NodeView(('T0_init', 'T1_S1', 'accept_S1'))
        buchi_graph.edges = OutEdgeView([('T0_init', 'T0_init'), ('T0_init', 'T1_S1'),....])
        buchi_graph.succ = AdjacencyView({'T0_init': {'T0_init': {'label': '1'}, 'T1_S1': {'label': 'r3'}}})
    """
    buchi_graph = DiGraph(type='buchi', init=init, accept=accep)
    for state in state_group:
        buchi_graph.add_node(state)
        state_if_fi = re.findall(state + r':\n\tif(.*?)fi', string, re.DOTALL)
        if  state_if_fi:
            relation_group = re.findall(r':: \((.*?)\) -> goto (\w+)\n\t', state_if_fi[0])
            for (label, state_dest) in relation_group:
                buchi_graph.add_edge(state, state_dest, label=label)

    return buchi_graph
