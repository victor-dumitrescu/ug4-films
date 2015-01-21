import numpy as np
import networkx as nx
from personas import Persona
from graphs import get_graphs

P = 'persona'


def get_ranked_nodes(self):
    output = []
    for n in sorted(self.node.items(), key=lambda x: int(x[1]['rank'])):
        output.append(n[1])
    return output


def naive_compare(graph1, graph2):

    g1 = graph1.get_ranked_nodes()
    g2 = graph2.get_ranked_nodes()
    diffs = []
    assert len(g1) == len(g2)  # check that graphs have been filtered in the same way
    N = len(g1)

    for i in range(N):
        assert g1[i]['rank'] == g2[i]['rank'] == i+1  # check that lists are sorted by rank
        if P in g1[i] and P in g2[i]:
            d = 0.0
            roles = 0
            for role in ['agent', 'patient', 'modifier']:
                a1 = getattr(g1[i][P], role)
                a2 = getattr(g2[i][P], role)
                if not np.isnan(np.sum(a1 - a2)):
                    d += np.linalg.norm(a1 - a2)
                    roles += 1
            if roles:
                diffs.append((i+1, d/roles))

    if len(diffs):
        return reduce((lambda x, y: x + y[1]), diffs, 0.0) / len(diffs)
    else:
        return 1.0


def main():

    graphs = get_graphs()
    setattr(nx.classes.graph.Graph, 'get_ranked_nodes', get_ranked_nodes)

    pairs = []
    for n1 in graphs:
        for n2 in graphs:
            if n1 != n2:
                dif = naive_compare(graphs[n1], graphs[n2])
                pairs.append((graphs[n1].graph['title'], graphs[n2].graph['title'], dif))

    filter((lambda x: x[0] == 'Analyze That'), sorted(pairs, key=lambda x: x[2], reverse=True))
    for (e, pair) in enumerate(sorted(pairs, key=lambda x: x[2], reverse=True)):
        if e%2:
            print pair

main()