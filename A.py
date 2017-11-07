import queue

class pathFinder(object):
    """ Class pathFinder is specific to the problem.
    including:
    1. """

    def __init__(self,accept_state, uni_cost=0.1):
        """Read the initial state from file
        """
        self.final_state = accept_state
        self.uni_cost = uni_cost

    def genAction(self, state, pba_graph):
        """Generate possible actions for the state
        """
        self.action = pba_graph.node[state].succ

    def heuriCost(self, state):
        """Calculate the heuristic cost
        """

        # state : ((set), 'string')
        return abs(state[0][0] - self.final_state[0][0]) + abs(state[0][1] - self.final_state[0][1])


    def genChild(self, parent_node, child_node, succ, step_cost):
        """Generate childnote according to possible actions of parent_node
        """

        child_node.state = succ
        child_node.parent = parent_node
        child_node.root_cost = parent_node.root_cost + step_cost
        child_node.path_cost = child_node.root_cost + self.uni_cost * self.heuriCost(child_node.state)


class Node(object):
    """Abstract class of node, including three functions:
    1. Initializing the node
    2. Testing whether goal state is reached
    3. Generating the path from current node to the root
    """

    def __init__(self,state=()):
        """Initialize node, including state, parent, root_cost, path_cost
        """

        self.state = state    # such as (0,1,2...,15)
        self.parent = None
        self.root_cost = 0
        self.path_cost = 0

    def testGoal(self, goal_state):
        """Test whether current state equals goal state
        """

        return (self.state == goal_state)

    def Solution(self, node, root_state, pre_cost):
        """ Generate an optimal path from current node to root
        """
        path_cost = node.root_cost
        optimal_path = []

        while node.state != root_state:
            optimal_path.append(node.state[0])
            node = node.parent
        optimal_path.append(root_state[0])
        return (path_cost+pre_cost, optimal_path[::-1])


def aStar(pba_graph, ini_state, accep_state, pre_cost):

    # Request the init and goal state
    path_finder = pathFinder(accep_state)

    # Initializing root node, state type: tuple
    root = Node(ini_state)
    root.path_cost = path_finder.heuriCost(root.state)

    # Initializing frontier
    frontier = queue.PriorityQueue()
    num_node = 1
    # a priority queue ordered by PATH-COST, with node as the only element
    frontier.put((root.path_cost, num_node, root))

    #Initializing explored set  type: set
    exporedSet = set()

    while True:

        # EMPTY?(frontier) then return failure
        if frontier.empty():
            break

        # chooses the lowest-cost node in frontier
        node = Node()
        node.path_cost, _, node = frontier.get()

        # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)

        if node.testGoal(path_finder.final_state):
         #   if not cycle:
              return root.Solution(node, root.state, pre_cost)
         #   else:
        #      cycle = not cycle

        # node with node.state has been expanded
        if node.state in exporedSet:
            continue
        else:
            # add node.STATE to explored
            exporedSet.add(node.state)

        # for each action in problem.ACTIONS(node.STATE) do
        #path_finder.genAction(node.state)
        
        for (succ, cost) in iter(pba_graph.succ[node.state].items()):

            # child CHILD-NODE(problem,node,action)
            child_node =  Node()
            path_finder.genChild(node, child_node, succ, cost['cost'])

            # check if child.STATE is not in explored
            # don't check if child.STATE in frontier, when a node with higher path_cost is popped \
            # out, the node with same state but smaller path_cost will be popped out before it

            if not child_node.state in exporedSet: # or ini_state==succ:
                num_node = num_node + 1
                #frontier.put((child_node.path_cost, num_node, child_node.root_cost, child_node.state, child_node.parent))
                frontier.put((child_node.path_cost, num_node, child_node))










