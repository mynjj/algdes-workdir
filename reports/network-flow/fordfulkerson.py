import math

class Edge:
    def __init__(self, id, s, t, c):
        self.s = s
        self.t = t
        self.f = 0
        self.c = c
        self.id = id

class Algorithm:
    def __init__(self, s, t):
        # setup G and Gf:
        self.g = {'n': {}, 'e': {}}
        self.gf = {'n': {}, 'e': {}}
        self.mincut = set() # after running the algorithm this will contain the mincut
        # setup s and t:
        self.s = s; self.t = t
        self.addNode(s); self.addNode(t)

    def addNode(self, n):
        self.g['n'][n] = []; self.gf['n'][n] = []

    def addEdge(self, id, s, t, c):
        '''Given an edge info we construct the edge '''
        e = self.g['e'][id] = Edge(id, s, t, c)
        self.g['n'][s].append(id)
        # append to residual graph:
        self.gf['n'][s].append(id)
        self.gf['n'][t].append(-id)
        self.updateResidiualEdges(e) # construct proper edges

    def edgesOf(self, n): return list(map(lambda eid: self.gf['e'][eid], self.gf['n'][n]))

    def dfs(self):
        '''returns the set of edges pointing to t from s'''
        discovered = set()
        def rec(v):
            discovered.add(v)
            if v == self.t:
                return []
            edges = filter(lambda e: (e.t not in discovered) and
                                      e.c > 0,
                                      self.edgesOf(v))
            for e in edges:
                tmp = rec(e.t)
                if tmp is not None:
                    tmp.append(e) # order will be reversed, but this is irrelevant
                    return tmp
            return None
        self.mincut = discovered # will at the end of the algorithm be the mincut
        return rec(self.s)

    def bottleneck(self, p):
        return min(list(map(lambda e: e.c, p)))

    def updateResidiualEdges(self, e):
        self.gf['e'][e.id]  = Edge(e.id, e.s, e.t, e.c - e.f);
        self.gf['e'][-e.id] = Edge(-e.id, e.t, e.s, e.f);

    def augment(self, p):
        cf = self.bottleneck(p)
        for i in range(len(p)):
            ef = p[i] #residual edge
            e = self.g['e'][abs(ef.id)] # original edge
            # if forward edge, positive id, otherwise it is backwards:
            if ef.id > 0:
                e.f += cf
            else:
                e.f -= cf
            self.updateResidiualEdges(e)

    def run(self):
        p = self.dfs()
        while p:
            self.augment(p)
            p = self.dfs()

    def get(self): return (self.g, self.gf)


def printGraph(g):
    for eid, e in g['e'].iteritems():
        print ('{}: {} -- ({} / {}) --> {}').format(eid,e.s,e.f,e.c,e.t)

# # test case, taken from kevin wayne's slides
# s = 0
# t = 5
#
# a = Algorithm(s, t)
#
# for i in range(1,5):
#     a.addNode(i)
#
# a.addEdge(1, 0,1,10)
# a.addEdge(2, 0,2,10)
# a.addEdge(3, 1,2,2)
# a.addEdge(4, 1,3,4)
# a.addEdge(5, 1,4,8)
# a.addEdge(6, 2,4,9)
# a.addEdge(7, 4,3,6)
# a.addEdge(8, 3,5,10)
# a.addEdge(9, 4,5,10)
#
# a.run()
# (g, gf) = a.get()
#
# printGraph(g)
