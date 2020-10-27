from math import inf
import sys

def get_ints(str):
    return [int(x) for x in str.strip().split()]


def bellman_ford(n_nodes, edges, s):
    #distances = {t: inf for t in g.keys()}
    distances = [inf]*n_nodes
    distances[s] = 0
    #predecesors = {}
    #distances[s] = 0
    changed = False
    for i in range(n_nodes-1):
        prev_dists = distances.copy()
        changed = False
        for u, v, w in edges:
            if prev_dists[u]+w < prev_dists[v]:
                changed = True
                distances[v] = prev_dists[u]+w
        if not changed:
            break

        #for u in g:
            #for v in g[u]:
                #print("checking", u, v, prev_dists[u], g[u][v], prev_dists[v])
                #if prev_dists[u]+g[u][v] < prev_dists[v]:
                    #changed = True
                    #distances[v] = prev_dists[u]+g[u][v]
                    #predecesors[v] = u
        #print(i, distances)
        #if not changed:
            #break
    if not changed:
        #print("not changed")
        return distances
    #print("pre-cycles")
    #print(distances)
    negative_cycles_nodes = {}
    for u, v, w in edges:
        if distances[v] == -inf:
            continue
        if distances[u] + w < distances[v]:
            visited = set()
            to_visit = [v]
            while to_visit:
                visiting = to_visit.pop()
                distances[visiting] = -inf
                visited.add(visiting)
                to_visit.extend(v for u, v, w in edges if u==visiting and v not in visited)
    return distances

"""
    for u in g:
        for v in g[u]:
            if distances[v] == -inf:
                continue
            if distances[u]+g[u][v] < distances[v]:
                # v is reachable from a negative cycle
                # DFS from here on...
                visited = set()
                to_visit = [v]
                while to_visit:
                    visiting = to_visit.pop()
                    distances[visiting] = -inf
                    visited.add(visiting)
                    to_visit.extend(k for k in graph[visiting].keys() if k not in visited)

    return distances

"""


data = sys.stdin.readlines()
first = True
while data:
    n_nodes, n_edges, qs, source_index = get_ints(data[0])
    if n_nodes == 0 and n_edges == 0 and qs == 0 and source_index==0:
        break
    if first:
        first = False
    else:
        print()
    #graph = {s: {} for s in range(n_nodes)}
    edges = []
    for i in range(n_edges):
        u, v, w = get_ints(data[i+1])
        edges.append((u, v, w))
        """
        if v in graph[u]: # Taking into account repeated edges
            if graph[u][v] >= w:
                graph[u][v] = w
                continue
        graph[u][v] = w
        """
    distances = bellman_ford(n_nodes, edges, source_index)
    #print(distances)
    for i in range(qs):
        d = distances[int(data[n_edges+i+1])]
        if d == inf:
            print("Impossible")
        elif d == -inf:
            print("-Infinity")
        else:
            print(d)
    data = data[n_edges+qs+1:]
