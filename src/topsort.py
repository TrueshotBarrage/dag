def add_list_to_dict(d, k, v):
    if k in d:
        d[k].append(v)
    else:
        d[k] = [v]
    
    return d

def init_dict(keys):
    return {k: [] for k in keys}

class Graph:
    def __init__(self, rels_input=None, debug=False):
        self.debug = debug
        
        self.graph = None
        self.relationships = None
        self.nodes = None
        
        if rels_input is None:
            user_input = input("Enter the relationships: ")
            self._load_graph(user_input)
        else:
            self._load_graph(rels_input)

    def _print_debug(self, fstr):
        if self.debug:
            print(f"[DEBUG] {fstr}")
    
    def _load_graph(self, input):
        if input == "":
            self.relationships = []
            self.nodes = set()
            self.graph = {}
            self.deps = {}
            return
        
        # Generate the relationships and list of nodes from the graph input
        self.relationships  = [x.strip() for x in input.split(",")]
        self.nodes = Graph.rels_to_nodes(">".join(self.relationships))

        # With these, derive the adjacency list for the graph
        adj_graph = init_dict(self.nodes)
        rev_adj_graph = init_dict(self.nodes)
        for rel in self.relationships:
            chd, par = rel.split(">")
            adj_graph = add_list_to_dict(adj_graph, par, chd)
            rev_adj_graph = add_list_to_dict(rev_adj_graph, chd, par)
        
        self.graph = adj_graph
        self.deps = rev_adj_graph

    def rels_to_nodes(rels):
        return {x.strip() for x in rels.split(">")}
    
    def pp(self):
        print(f"Relationships: {self.relationships}")
        print(f"Nodes: {self.nodes}")
        print(f"Adjacency Graph: {self.graph}")
        print(f"Dependency (Reverse Adjacency Graph): {self.deps}")

    def nodes_without_inc_edges(self, G, ):
        return [n for n in self.nodes if not G[n]]

    def topsort(self):
        # See the pseudocode algorithm in topsort_algo.md.
        L = []
        S = self.nodes_without_inc_edges(self.graph)
        while S:
            n = S.pop()
            L.append(n)
            self._print_debug(f"Adding {n} to plan")
            for m in self.deps[n]:
                self.graph[m].remove(n)
                self._print_debug(f"Removing {n}>{m}")
                if not self.graph[m]:
                    S.append(m)
            self.deps[n] = []
        
        assert self.graph == self.deps, \
            f"Cycle detected in the graph:\n{self.deps}"
        assert len(self.graph.values()) == len(self.deps.values()), \
            f"Cycle detected in the graph:\n{self.deps}"

        return L


def main():
    g = Graph(debug=True)
    # g = Graph(rels_input="A>B,B>C,B>D,D>E,C>E", debug=True)
    g.pp()

    ex_order = g.topsort()
    print(ex_order)


if __name__ == "__main__":
    main()