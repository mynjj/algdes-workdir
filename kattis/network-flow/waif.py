from math import inf
from collections import deque

SOURCE_NODE = '__FLOW_GRAPH_SOURCE_NODE'
SINK_NODE = '__FLOW_GRAPH_SINK_NODE'

class Path:
    def __init__(self):
        self.vertices = []
        self.bottleneck = inf
    def append(self, vertex, graph):
        r = Path()
        r.vertices = list(self.vertices)
        if len(self.vertices) == 0:
            r.vertices.append(vertex)
            return r
        r.vertices.append(vertex)
        edge_value = graph.edge(self.vertices[-1], vertex)
        r.bottleneck = min(self.bottleneck, edge_value)
        return r

class WeightedDigraph:
    def __init__(self):
        self.tails = {}

    def add_edge(self, from_node, to_node, value):
        if not from_node in self.tails:
            self.tails[from_node] = {}
        self.tails[from_node][to_node] = value

    def edges_from(self, from_node):
        if from_node not in self.tails:
            return {}
        return self.tails[from_node]

    def bfs_path(self, from_node, to_node):
        """
        Uses BFS to find a path with positive edges from
        from_node to to_node. Returns None if it can't
        be found.
        """
        #path = []
        path = Path()
        possible_paths = deque()
        visited = set()
        possible_paths.append((from_node, path))
        while possible_paths:
            to_visit, path = possible_paths.popleft()
            if to_visit in visited:
                continue
            visited.add(to_visit)
            visiting_path = path.append(to_visit, self)
            if to_visit == to_node:
                return visiting_path
            neighbours = self.edges_from(to_visit)
            for neighbour in neighbours:
                value = neighbours[neighbour]
                if value == 0:
                    continue
                possible_paths.append((neighbour, visiting_path))
        return None
    def edge_traverse(self, callback):
        for from_node in self.tails:
            dests = self.tails[from_node]
            for to_node in dests:
                value = dests[to_node]
                callback(from_node, to_node, value)
    def edge(self, from_node, to_node):
        dests = self.edges_from(from_node)
        if to_node not in dests:
            return None
        return dests[to_node]
    def apply_to_edge(self, u, v, callback):
        self.tails[u][v] = callback(self.tails[u][v])

class Flow(WeightedDigraph):
    """
    Weighted Digraph representing the flow assigned for
    a capacities digraph
    """
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        def create_zero_edge(from_node, to_node, value):
            self.add_edge(from_node, to_node, 0)
        graph.edge_traverse(create_zero_edge)
    def augment(self, graph, residual, path):
        for i in range(len(path.vertices)-1):
            u = path.vertices[i]
            v = path.vertices[i+1]
            if graph.edge(u, v) is not None:
                self.apply_to_edge(u, v, lambda x: x+path.bottleneck)
                residual.apply_to_edge(u, v, lambda x: x-path.bottleneck)
                residual.apply_to_edge(v, u, lambda x: x+path.bottleneck)
            else:
                self.apply_to_edge(v, u, lambda x: x-path.bottleneck)
                residual.apply_to_edge(u, v, lambda x: x+path.bottleneck)
                residual.apply_to_edge(v, u, lambda x: x-path.bottleneck)

class ResidualGraph(WeightedDigraph):
    def __init__(self, graph, flow):
        super().__init__()
        def create_residual_edge(from_node, to_node, value):
            f = flow.edge(from_node, to_node)
            self.add_edge(from_node, to_node, value - f)
            self.add_edge(to_node, from_node, f)
        graph.edge_traverse(create_residual_edge)


def ford_fulkerson(graph):
    flow = Flow(graph)
    residual = ResidualGraph(graph, flow)
    st_path = residual.bfs_path(SOURCE_NODE, SINK_NODE)
    while st_path is not None:
        flow.augment(graph, residual, st_path)
        st_path = residual.bfs_path(SOURCE_NODE, SINK_NODE)
    return flow

def read_vals():
    return input().split()

def read_nums():
    return map(lambda x: int(x), read_vals())

def toy_node_key(key):
    return "Toy "+str(key)

def primed_key(key):
    return str(key) + "'"

n_children, n_toys, n_cats = read_nums()


graph = WeightedDigraph()

uncategorized_toys = set()
for i in range(1, n_children + 1):
    child_id = "Child "+str(i)
    graph.add_edge(SOURCE_NODE, child_id, 1)
    toy_ids = list(map(toy_node_key,read_vals()[1:]))
    for toy_id in toy_ids:
        graph.add_edge(child_id, toy_id, 1)
    uncategorized_toys = uncategorized_toys.union(set(toy_ids))
for i in range(1, n_cats + 1):
    cat_id = "Category "+str(i)
    cat_details = read_vals()[1:]
    max_used = int(cat_details.pop())
    cat_details = list(map(toy_node_key, cat_details))
    for toy_key in cat_details:
        graph.add_edge(toy_key, cat_id, 1)

    graph.add_edge(cat_id, SINK_NODE, max_used) # Restriction: # toys per category
    uncategorized_toys = uncategorized_toys.difference(set(cat_details))


for toy_key in uncategorized_toys:
    graph.add_edge(toy_key, 'UNCATEGORIZED', 1)
graph.add_edge('UNCATEGORIZED', SINK_NODE, inf)

optimal = ford_fulkerson(graph)

s = 0
for k in optimal.tails[SOURCE_NODE]:
    s += optimal.tails[SOURCE_NODE][k]
print(s)

