class problemFormulation(object):

    def __init__(self):

        # +----------------------------------------------+
        # |                                              |
        # |                 Problem 1                    |
        # |                                              |
        # +----------------------------------------------+


        # +-----+-----+-----+
        # | r4,r| r5,b| r6,b|
        # +-----+-----+-----+
        # | r1,r| r2,b| r3,r|
        # +-----+-----+-----+

        self.ap = {'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r', 'b'}

        # !! no whitespace in atomic proposation
        self.regions = {   (0, 0, 1): {'r1', 'r'},
                        (1, 0, 1): {'r2', 'b'},
                        (2, 0, 1): {'r3', 'r'},
                        (0, 1, 1): {'r4', 'r'},
                        (1, 1, 1): {'r5', 'b'},
                        (2, 1, 1): {'r6', 'b'}
                        }

        self.init_state = [(0,0,1)]
        self.edges = [   ((0, 0, 1), (1, 0, 1)),
                        ((1, 0, 1), (2, 0, 1)),
                        ((0, 1, 1), (1, 1, 1)),
                        ((1, 1, 1), (2, 1, 1)),
                        ((0, 0, 1), (0, 1, 1)),
                        ((1, 0, 1), (1, 1, 1)),
                        ((2, 0, 1), (2, 1, 1))
                     ]
        self.uni_cost = 0.1

        # #----------------------------------------------#
        # |                                              |
        # |                 Problem 2                    |
        # |                                              |
        # #----------------------------------------------#

        # +-----+-----+-----+
        # | r4,b|r5,rb| r6  |
        # +-----+-----+-----+
        # | c1  | c2  | c3  |
        # +-----+-----+-----+
        # | r1  | r2,b|r3,gb|
        # +-----+-----+-----+

        self.ap = {'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'c1', 'c2', 'c3', 'rb', 'gb', 'b'}

        # !! no whitespace in atomic proposation
        self.regions = {   (0, 0, 1): ['r1'],
                          (1, 0, 1): ['r2', 'b'],
                          (2, 0, 1): ['r3', 'gb'],
                          (0, 1, 1): ['c1'],
                          (1, 1, 1): ['c2'],
                          (2, 1, 1): ['c3'],
                          (0, 2, 1): ['r4', 'b'],
                          (1, 2, 1): ['r5', 'rb'],
                          (2, 2, 1): ['r6']
                          }

        self.init_state = [(0,0,1)]

        self.edges = [
                ((0, 1, 1), (1, 1, 1)),
                ((1, 1, 1), (2, 1, 1)),
                ((0, 0, 1), (0, 1, 1)),
                ((0, 1, 1), (0, 2, 1)),
                ((1, 0, 1), (1, 1, 1)),
                ((1, 1, 1), (1, 2, 1)),
                ((2, 0, 1), (2, 1, 1)),
                ((2, 1, 1), (2, 2, 1))
                ]
        self.uni_cost = 0.1


        """
        +----------------------------+
        |   Propositonal Symbols:    |
        |        true, false         |
        |	    any lowercase string |
        |                            |
        |   Boolean operators:       |
        |       !   (negation)       |
        |       ->  (implication)    |
        |	    <-> (equivalence)    |
        |       &&  (and)            |
        |       ||  (or)             |
        |                            |
        |   Temporal operators:      |
        |       []  (always)         |
        |       <>  (eventually)     |
        |       U   (until)          |
        |       V   (release)        |
        |       X   (next)           |
        +----------------------------+
        """


        #self.formula = '<>(rb && <>b) && <>[]r1'               # \phi 1  pick red ball to one basket and visit r1 infinitely often
        #self.formula =  '<>(rb && <>b) && <>[]r1 && [](rb -> X(!gb U b)) && <>(gb && <>b) && [](gb -> X(!rb U b))'  # \phi 2
        #self.formula = '<>(rb && <>(b && r2)) && <>[]r1 && [](rb -> X(!gb U b)) && <>(gb && <>(b && r4)) && [](gb -> X(!rb U b))'   #\phi 3
        self.formula = '([]<>r4) && ([]<>r3) && ([]<>r6)'     # \phi 4 inspect room r3, r4, r6 infinitely often

    def Formulation(self):
        print('Task specified by LTL formula: ' + self.formula)
        return self.regions, self.init_state, self.edges, self.uni_cost, self.formula