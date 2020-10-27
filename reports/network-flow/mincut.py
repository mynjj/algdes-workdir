from fordfulkerson import printGraph, Algorithm, Edge
import sys, re

def printMinCut(a):
    (g, _) = a.get()
    visited = a.mincut
    # select the edges of the vertices leaving this cut:
    eids       = sum(list(map(lambda n: g['n'][n], visited)),[])
    edges      = list(map(lambda eid: g['e'][abs(eid)], eids))
    validEdges = filter(lambda e: e.t not in visited, edges)
    # count total outgoing flow of s:
    total_flow = sum(list(map(lambda eid: g['e'][eid].f, g['n'][0])))

    # print the information (sorted)
    for ef in validEdges:
        e = g['e'][abs(ef.id)]
        print(f'{e.s} {e.t} {e.f}')

    # print
    print (f'total = {total_flow}')
