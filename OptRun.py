import A
import datetime
def optRun(pba_graph):
    """ find the optimal path  Algorithm3 in Chapter 2 Motion and Task Planning
    """

    start = datetime.datetime.now()

    pre_path = {}
    suf_path = {}
    # prefix path: from initial state to accepting state
    for ini_state in pba_graph.graph['init']:
        for accept_state in pba_graph.graph['accept']:
            p = {(ini_state, accept_state) : A.aStar(pba_graph, ini_state, accept_state, 0)}
            pre_path.update(p)
    # suffix path: from accepting state to accepting
    for accept_state in pba_graph.graph['accept']:
        temp = {}
        for next_state in pba_graph.succ[accept_state]:
            pre_cost = pba_graph.succ[accept_state][next_state]['cost']
            next_path = A.aStar(pba_graph, next_state, accept_state, pre_cost)
            if next_path != None:
                p = {(next_state, accept_state): next_path}
                temp.update(p)
        if temp:
            p = {(accept_state, accept_state): min(temp.values())}
            suf_path.update(p)

    total_path = {}
    for (state, path) in iter(pre_path.items()):
        if not path==None and (state[1], state[1]) in suf_path.keys():
            p = {state: (path[0] + suf_path[(state[1], state[1])][0], (path[1], suf_path[(state[1], state[1])][1] ))}
            total_path.update(p)
    if total_path == {}:
        return 'Planning doesn\'t exist'

    end = datetime.datetime.now()
    print('Time only to find the optimal path:', (end-start).total_seconds(),'s')

    return min(total_path.values())
