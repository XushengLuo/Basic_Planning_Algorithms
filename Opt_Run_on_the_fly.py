import A_on_the_fly
import datetime


class opt_path_on_the_fly(object):
    """ find the optimal path
    Parameter:
        start      : beginning time of path searching algorithm
        pre_path   : prefix path
        suf_path   : suffix path
        total_path : prefix + suffix path
        pba_graph: : product buchi automation graph
    """

    def __init__(self, ts_graph, buchi_graph, pba):

        self.pre_path = {}
        self.suf_path = {}
        self.total_path = {}
        self.ts_graph = ts_graph
        self.buchi_graph = buchi_graph
        self.pba = pba

    def prePath(self):
        """prefix path: from each initial state to each accepting state
        """
        for ini_state in self.pba.pba_graph.graph['init']:
            for accept_state in self.pba.pba_graph.graph['accept']:
                path, self.pba = A_on_the_fly.aStar(ini_state, accept_state, 0, self.pba)   # update self.pba for future calling
                p = {(ini_state, accept_state): path}
                self.pre_path.update(p)

    def sufPath(self):
        """suffix path: from one accepting state to itself
        """
        for accept_state in self.pba.pba_graph.graph['accept']:
            temp = {}
            # find the optimal path from each succsseor of a given accepting state to itself
            for next_state in self.pba.pba_graph.succ[accept_state]:
                pre_cost = self.pba.pba_graph.succ[accept_state][next_state]['cost']
                next_path, self.pba = A_on_the_fly.aStar(next_state, accept_state, pre_cost, self.pba)   # update self.pba for future calling
                # if one path from given succ of a given accepting state to itself exists
                if next_path != None:
                    p = {(next_state, accept_state): next_path}
                    temp.update(p)
            # if path from several succ of a given accepting state to itself exists, find the minimum one
            if temp:
                p = {(accept_state, accept_state): min(temp.values())}
                self.suf_path.update(p)

    def optRun(self):
        """ find the optimal path  Algorithm3 in Chapter 2 Motion and Task Planning
        """
        self.start = datetime.datetime.now()
        # prefix path: from initial state to accepting state
        self.prePath()
        # suffix path: from accepting state to accepting
        self.sufPath()

        for (state, path) in iter(self.pre_path.items()):
            # if the path from initial state to one accepting state exists
            if not path == None and (state[1], state[1]) in self.suf_path.keys():
                p = {state: (
                path[0] + self.suf_path[(state[1], state[1])][0], (path[1], self.suf_path[(state[1], state[1])][1]))}
                self.total_path.update(p)
        if self.total_path == {}:
            return 'Planning doesn\'t exist'

        end = datetime.datetime.now()
        print('Time only to find the optimal path:', (end - self.start).total_seconds(), 's')
        # fing the minimum path from inital state to accepting state
        self.optimal_path = min(self.total_path.values())

    def printOptPath(self):
        """ print out optimal path
            Parameter
                ts_graph : transition system, mapping state to regions
        """
        optimal_pre = []
        for state in self.optimal_path[1][0]:
            optimal_pre.append(self.ts_graph.nodes[state[0]]['label'][0])

        optimal_suf = [optimal_pre[-1]]
        for state in self.optimal_path[1][1]:
            optimal_suf.append(self.ts_graph.nodes[state[0]]['label'][0])

        # print path cost
        print('The total cost of the path is: ', end='')
        print(self.optimal_path[0])

        # print prefix path
        print('The prefix path is:    ', end='')
        for region in optimal_pre[0:-3]:
            print(region + ' -> ', end='')
        print(optimal_pre[-3])

        # print suffix path
        print('The suffix path is:    ', end='')
        if optimal_suf.__len__() == 2:
            print(optimal_suf[0])
        else:
            for region in optimal_suf[0:-3]:
                print(region + ' -> ', end='')
            print(optimal_suf[-3])


