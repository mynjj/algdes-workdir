import sys
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




def get_ints(line):
    return map(lambda x: int(x), line.split())
def get_floats(line):
    return map(lambda x: float(x), line.split())

data = sys.stdin.readlines()
while data:
    gophers, holes, time_limit, vel = get_ints(data[0])
    reachable = time_limit*time_limit*vel*vel
    graph = FlowGraph()

    for j in range(gophers+1, gophers+holes+1):
        data[j] = list(get_floats(data[j]))

    for i in range(1, gophers+1):
        g_added = False
        x, y = get_floats(data[i])
        for j in range(gophers+1, gophers+holes+1):
            h = 'H'+str(j-gophers)
            xp, yp = data[j]
            if (xp-x)**2+(yp-y)**2 <= reachable:
                if not g_added:
                    g = 'G'+str(i)
                    graph.add_edge(SOURCE_NODE,  g, 1)
                    g_added = True
                graph.add_edge(g, h, 1)
                graph.add_edge(h, SINK_NODE, 1)
    ford_fulkerson(graph)
    print(gophers-graph.flow)
    data = data[gophers+holes+1:]