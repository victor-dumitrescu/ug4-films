import numpy as np
from graphs import get_graphs
from utils.store_sentiment import load


def construct_feature_vectors(graph, n_topics):

    # construct a vector with 3*n_topics+1 elements, by concatenating
    # the 6 distributions (3 from each character) and the weight of
    # the edge between them

    pairs = []
    vectors = []
    graph.filter_by_persona()
    for e in graph.edges():
        for char in range(2):
            X = None
            for role in ['agent', 'patient', 'modifier']:
                distr = getattr(graph.node[e[char]]['persona'], role)
                if np.isnan(distr[0]):
                    # if distribution is missing, replace with uniform
                    distr = np.ones(n_topics) / n_topics
                assert len(distr) == n_topics
                X = np.append(X, distr)
        X = np.append(X, np.array([graph.edge[e[0]][e[1]]['weight']]))
        pairs.append((e[0], e[1]))
        vectors.append(X[1:])

    return pairs, vectors


def construct_labels():
    #TODO Get labels: total sentiment from one person to the other
    pass


def main():

    graphs = get_graphs()
    n_topics = 20
    data = []
    pairs = []
    for g in graphs:
        p, vectors = construct_feature_vectors(graphs[g], n_topics)
        data += vectors
        pairs += map((lambda x: x + (graphs[g].graph['title'],)), p)

        sent_timeline = load(graphs[g].graph['gexf'][:-5])
        #TODO Filter timeline by char pair, then compute total sentiment