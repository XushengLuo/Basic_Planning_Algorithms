from networkx.classes.digraph import DiGraph


class pba_graph(object):
    """ construct product buchi automation graph
    Parameter:
        ts_graph    : transtion system graph
        buchi_graph : buchi automation graph
        alpha       : weight
    """
    
    def __init__(self, ts_graph, buchi_graph, alpha=0):
        self.ts_graph = ts_graph
        self.buchi_graph = buchi_graph
        self.alpha = alpha
        self.pba_graph = DiGraph(type='PBA', init=[], accept=[])

    def pbaGraph(self):
        """ constrcut PBA graph, algorithm 1 in Chapter two Motion and Task Planning
        """
        
        for t_state in self.ts_graph.node:
    
            for b_state in self.buchi_graph.node:
                # new pba graph node
                p_state = (t_state, b_state)
                self.pba_graph.add_node(p_state)
                # initial node
                if t_state in self.ts_graph.graph['init'] and b_state in self.buchi_graph.graph['init']:
                    self.pba_graph.graph['init'].append(p_state)
                # accepting node
                if b_state in self.buchi_graph.graph['accept']:
                    self.pba_graph.graph['accept'].append(p_state)
    
                # succcessor of state
                for t_state_succ in self.ts_graph.succ[t_state]:
                    for b_state_succ in self.buchi_graph.succ[b_state]:
                        p_state_succ = (t_state_succ, b_state_succ)
                        d = self.checkTranB(b_state, self.ts_graph.node[t_state]['label'], b_state_succ)
                        if d >= 0 :
                            self.pba_graph.add_edge(p_state, p_state_succ, cost=self.ts_graph.edges[(t_state, t_state_succ)]['cost'] + self.alpha * d)
    
        return self.pba_graph

    def checkTranB(self, b_state, t_label, b_state_succ,):
        """ decide valid transition
            Algorithm2 in Chapter 2 Motion and Task Planning
        """
        d = -1
        b_label = self.buchi_graph.edges[(b_state, b_state_succ)]['label']
        if self.t_satisfy_b(t_label, b_label):
            d = 0
        return d

    def t_satisfy_b(self, t_label, b_label):
        """ decide whether label of self.ts_graph can satisfy label of self.buchi_graph
        """
        t_s_b = True
        # split label with ||
        b_label = b_label.split('||')
        for label in b_label:
            t_s_b = True
            # spit label with &&
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

