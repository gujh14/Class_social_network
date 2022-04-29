import operator, networkx as nx, pandas as pd

def pagerank(csv_file_path, scaling=0.85, iterations=30, directed=False):
    '''
    csv_file_path: File path of a csv file. It should not have a header row.
        suitable csv_file_path example: 'https://raw.githubusercontent.com/timothyasp/PageRank/master/data/dolphins.csv'
    scaling: A float number between [0, 1].
        if scaling == 1, then it is just basic PageRank(with no teleport)
    iterations: Number of iterations
    directed: Set this parameter True if the graph and csv file is directed.
    '''
    if directed: # directed graph
        graph = nx.DiGraph()
    else: # undirected graph
        graph = nx.Graph()
        
    data = pd.read_csv(csv_file_path, header=None)
    
    nodes = set(data[0]).union(set(data[2]))
    edges = [(row[0], row[2]) for _, row in data.iterrows()]
    
    num_nodes = len(nodes)
    initial_rank = 1/float(num_nodes)
    graph.add_nodes_from(nodes, rank=initial_rank)
    graph.add_edges_from(edges)
    
    V = float(len(graph))
    s = scaling
    ranks = dict()

    for key, node in graph.nodes(data=True):
        ranks[key] = node.get('rank')

    for _ in range(iterations):
        new_ranks = ranks.copy()
        for key, node in graph.nodes(data=True):
            rank_sum = 0.0
            if directed: # directed graph
                predecessors = graph.predecessors(key)
            else: # undirected graph
                predecessors = graph.neighbors(key)
            for n in predecessors:
                if ranks[n] is not None:
                    outlinks = len(list(graph.neighbors(n))) # number of outlinks of parent node
                    rank_sum += (1 / float(outlinks)) * ranks[n]
            new_ranks[key] = ((1-s)*(1/V)) + s*rank_sum
        ranks = new_ranks
    sorted_ranks = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)
    
    return sorted_ranks
