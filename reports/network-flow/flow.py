from fordfulkerson import printGraph, Algorithm, Edge
from mincut import printMinCut
import sys, re
# helper functions:
def read(): return re.sub(r'\r\n', '', sys.stdin.readline())
def readInts(): return list(map(int, read().split()))
def readInt(): return int(read())

# input regarding nodes:
n = readInt(); nodes = {}
# setup algorithm:
alg = Algorithm(0,n - 1)
# skip s node:
read()
# get all nodes inbetween:
for i in range(1, n - 1): # s[...]t
    alg.addNode(i)
    read()

# skip t node:
read()

# input regarding edges:
e = readInt(); edges = {}; eid = 1
for i in range(e):
    einfo = readInts()
    cap = einfo[2]
    if cap < 0: # ensure that -1 -> infinity
        cap = float('inf')
    # add an edge both ways:
    alg.addEdge(eid, einfo[0], einfo[1], cap)
    alg.addEdge(eid + 1, einfo[1], einfo[0], cap)
    eid += 2

# run the algorithm:
alg.run()

printMinCut(alg)
