from networkx.classes.digraph import DiGraph

def pbaGraph(ts_graph, buchi_graph, alpha=0):
    """ constrcut PBA graph, algorithm 1 in Chapter two Motion and Task Planning
    """
    pba_graph = DiGraph(type='PBA',init=[],accept=[])
    for t_state in ts_graph.node:

        for b_state in buchi_graph.node:
            # new pba graph node
            p_state = (t_state, b_state)
            pba_graph.add_node(p_state)
            # initial node
            if t_state in ts_graph.graph['init'] and b_state in buchi_graph.graph['init']:
                pba_graph.graph['init'].append(p_state)
            # accept node
            if b_state in buchi_graph.graph['accept']:
                pba_graph.graph['accept'].append(p_state)

            # succcessor of state
            for t_state_succ in ts_graph.succ[t_state]:
                for b_state_succ in buchi_graph.succ[b_state]:
                    p_state_succ = (t_state_succ, b_state_succ)
                    d = checkTranB(b_state, ts_graph.node[t_state]['label'], b_state_succ, buchi_graph)
                    if d >= 0 :
                        pba_graph.add_edge(p_state, p_state_succ, cost=ts_graph.edges[(t_state, t_state_succ)]['cost'] + alpha * d)

    return pba_graph

def checkTranB(b_state, t_label, b_state_succ, buchi_graph):
    """decide valid transition algorithm2 in Chapter 2 Motion and Task Planning
    """
    d = -1
    b_label = buchi_graph.edges[(b_state, b_state_succ)]['label']
    if t_satisfy_b(t_label, b_label):
        d = 0
    return d

def t_satisfy_b(t_label, b_label):
    """ decide whether label of ts_graph can satisfy label of buchi_graph
    """
    t_s_b = True
    # split label with ||
    b_label = b_label.split('||')
    for label in b_label:
        t_s_b = True
        #spit label with &&
        atomic_label = label.split('&&')
        for a in atomic_label:
            a = a.strip()
            if a == '1':
                continue
            # whether ! in an atomic proposition
            if '!' in a:
                if a[1:] in t_label:
                    t_s_b = False
                    break
            else:
                if not a in t_label:
                   t_s_b = False
                   break
    return t_s_b

