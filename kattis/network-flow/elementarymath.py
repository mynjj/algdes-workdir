from collections import deque

SOURCE_NODE = '__FLOW_GRAPH_SOURCE_NODE'
SINK_NODE = '__FLOW_GRAPH_SINK_NODE'

class FlowGraph:
    def __init__(self):
        self.tails = {}
        self.residual = {}
        self.flow = 0

    def augmenting_path(self):
        visited = {}
        to_visit = deque()
        to_visit.append((SOURCE_NODE, None))
        while to_visit:
            visiting, from_node = to_visit.popleft()
            if visiting == SINK_NODE:
                return self.traceback_path(visited, from_node)
            if visiting in visited:
                continue
            visited[visiting] = from_node
            if visiting in self.residual:
                reachable = filter(lambda k: self.residual[visiting][k]>0, self.residual[visiting].keys())
                neighbours = map(lambda x: (x, visiting), reachable)
                to_visit.extend(neighbours)
        return None

    def traceback_path(self, visited, from_node):
        """Reversed path on residual graph"""
        path = [SINK_NODE]
        bottleneck = self.residual[from_node][SINK_NODE]
        tracking = from_node
        while tracking is not None:
            path.append(tracking)
            if visited[tracking] is not None:
                bottleneck = min(bottleneck, self.residual[visited[tracking]][tracking])
            tracking = visited[tracking]
        return path, bottleneck

    def dfs_augmenting_path(self):
        visited = {}
        to_visit = [(SOURCE_NODE, None)]
        while to_visit:
            visiting, from_node = to_visit.pop()
            if visiting == SINK_NODE:
                return self.traceback_path(visited, from_node)
            if visiting in visited:
                continue
            visited[visiting] = from_node
            if visiting in self.residual:
                reachable = filter(lambda k: self.residual[visiting][k]>0, self.residual[visiting].keys())
                neighbours = map(lambda x: (x, visiting), reachable)
                to_visit.extend(neighbours)
        return None

    def augment(self, path, bottleneck):
        for i in range(len(path)-1):
            from_node = path[i+1]
            to_node = path[i]
            if from_node in self.tails and to_node in self.tails[from_node]:
                if from_node == SOURCE_NODE:
                    self.flow += bottleneck
                self.tails[from_node][to_node] += bottleneck
            else:
                if from_node == SOURCE_NODE:
                    self.flow -= bottleneck
                self.tails[to_node][from_node] -= bottleneck
            self.residual[from_node][to_node] -= bottleneck
            self.residual[to_node][from_node] += bottleneck

    def add_edge(self, from_node, to_node, cap):
        if not from_node in self.tails:
            self.tails[from_node] = {}
        self.tails[from_node][to_node] = 0

        if not from_node in self.residual:
            self.residual[from_node] = {}
        self.residual[from_node][to_node] = cap

        if not to_node in self.residual:
            self.residual[to_node] = {}
        self.residual[to_node][from_node] = 0



def ford_fulkerson(graph):
    path = graph.augmenting_path()
    while path is not None:
        p, bottleneck = path
        graph.augment(p, bottleneck)
        path = graph.dfs_augmenting_path()

"""
g = FlowGraph()
g.add_edge(SOURCE_NODE, 'a', 16)
g.add_edge(SOURCE_NODE, 'c', 13)
g.add_edge('a', 'c', 10)
g.add_edge('a', 'b', 12)
g.add_edge('c', 'a', 4)
g.add_edge('c', 'd', 14)
g.add_edge('b', 'c', 9)
g.add_edge('b', SINK_NODE, 20)
g.add_edge('d', 'b', 7)
g.add_edge('d', SINK_NODE, 4)

ford_fulkerson(g)
print(g.tails)
print(g.flow)
"""
n = int(input())
graph = FlowGraph()
pairs = []
ops = {}
for i in range(n):
    x, y = input().split()
    vx = int(x)
    vy = int(y)
    pair_id = x+","+y
    pairs.append((x, y))
    if SOURCE_NODE in graph.tails and pair_id in graph.tails[SOURCE_NODE]:
        graph.residual[SOURCE_NODE][pair_id] += 1
        if graph.residual[SOURCE_NODE][pair_id] > len(graph.tails[pair_id]):
            print("impossible")
            exit(0)
        continue
    graph.add_edge(SOURCE_NODE, pair_id, 1)
    r = vx+vy
    graph.add_edge(pair_id, r, 1)
    graph.add_edge(r, SINK_NODE, 1)
    ops[pair_id] = {r: '+'}
    r = vx-vy
    graph.add_edge(pair_id, r, 1)
    graph.add_edge(r, SINK_NODE, 1)
    ops[pair_id][r] = '-'
    r = vx*vy
    graph.add_edge(pair_id, r, 1)
    graph.add_edge(r, SINK_NODE, 1)
    ops[pair_id][r] = '*'

ford_fulkerson(graph)
possible = graph.flow
if possible != n:
    print("impossible")
    exit(0)

for x, y in pairs:
    pair_id = x+","+y
    for r in graph.tails[pair_id]:
        v = graph.tails[pair_id][r]
        if v == 1:
            op = ops[pair_id][r]
            print(f'{x} {op} {y} = {r}')
            graph.tails[pair_id][r] -= 1
            break

