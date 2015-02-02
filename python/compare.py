import numpy as np
import networkx as nx

from personas import Persona
from graphs import get_graphs

P = 'persona'


def get_ranked_nodes(self):
    # method added to the Graph class
    # retrieves the nodes, ordered by rank

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


def node_objective(x, g1, g2):

    def node_difference(n1, n2):

        if P in n1 and P in n2:
            d = 0.0
            roles = 0
            for role in ['agent', 'patient', 'modifier']:
                a1 = getattr(n1[P], role)
                a2 = getattr(n2[P], role)
                if not np.isnan(np.sum(a1 - a2)):
                    d += np.linalg.norm(a1 - a2)
                    roles += 1
            if roles:
                diff = d/roles
            else:
                return 1.0
        else:
            return 1.0

        return diff

    N = len(g1)
    cost = 0.0
    for i in range(N):
        cost += node_difference(g1[i], g2[int(np.around(x[i]))])

    return cost


def main():

    graphs = get_graphs(verbose=True)
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