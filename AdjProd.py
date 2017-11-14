class adj_prod(object):
    """Build adjacency relation of pba graph on the fly
    Parameter:
        pba_graph : current pba graph
        p_state   : state wait for being expanded
        alpha     : weight
    """
    def __init__(self, pba_graph, ts_graph, buchi_graph, alpha=0):
        self.pba_graph = pba_graph
        self.alpha = alpha
        self.ts_graph = ts_graph
        self.buchi_graph = buchi_graph

    def init_accept(self):
        """ Construct inital and accepting state of pba graph"""
        for t_state in self.ts_graph.graph['init']:
            for b_state in self.buchi_graph.graph['init']:
                # new pba graph node
                p_state = (t_state, b_state)
                # initial node
                self.pba_graph.graph['init'].append(p_state)
                self.pba_graph.add_node(p_state, v=False)

        for t_state in self.ts_graph.nodes:
            for b_state in self.buchi_graph.graph['accept']:
                # accepting node
                p_state = (t_state, b_state)
                self.pba_graph.graph['accept'].append(p_state)
                self.pba_graph.add_node(p_state, v=False)


    def adjProd(self, state):
        self.p_state = state
        if self.pba_graph.nodes[self.p_state]['v']:
            # if q is marked with 'visited'
            return self.pba_graph.succ[self.p_state]
        else:
            # new pba graph node
            t_state, b_state = self.p_state
            for t_state_succ in self.ts_graph.succ[t_state]:
                for b_state_succ in self.buchi_graph.succ[b_state]:
                    p_state_succ = (t_state_succ, b_state_succ)

                    if p_state_succ not in self.pba_graph.nodes:
                        # if p_state_succ doesn't exist
                        self.pba_graph.add_node(p_state_succ, v=False)
                        # transition ???
                    d = self.checkTranB(b_state, self.ts_graph.nodes[t_state]['label'], b_state_succ)
                    if d >= 0 :
                        self.pba_graph.add_edge(self.p_state, p_state_succ, cost=self.ts_graph.edges[(t_state, t_state_succ)]['cost'] + self.alpha * d)

            self.pba_graph.nodes[self.p_state]['v'] = True
            return self.pba_graph.succ[self.p_state]

    def checkTranB(self, b_state, t_label, b_state_succ):
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
