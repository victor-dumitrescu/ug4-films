import numpy as np


def construct_feature_vectors(graph, n_topics, **kwargs):

    # construct a vector with 3*n_topics+1 elements, by concatenating
    # the 6 distributions (3 from each character) and the weight of
    # the edge between them

    # optional arguments:
    # pers=['A', 'P', 'M'] or a subset, indicating
    # which persona distributions should be included
    # default is all
    #
    # pick_top
    #
    # normalize

    pick_top = kwargs.get('pick_top', None)
    pers = kwargs.get('pers', None)

    if pers:
        roles = []
        if 'A' in pers:
            roles.append('agent')
        if 'P' in pers:
            roles.append('patient')
        if 'M' in pers:
            roles.append('modifier')
    else:
        roles = ['agent', 'patient', 'modifier']

    if pick_top:
        normalize = kwargs.get('normalize', False)

    pairs = []
    vectors = []
    graph.filter_by_persona()
    for e in graph.edges():
        X = None
        for char in range(2):
            for role in roles:
                distr = getattr(graph.node[e[char]]['persona'], role)
                if pick_top:
                    distr = pick_top_topics(distr, pick_top, normalize)
                else:
                    if np.isnan(distr[0]):
                        # if distribution is missing, replace with uniform
                        distr = np.ones(n_topics) / n_topics
                assert len(distr) == n_topics
                X = np.append(X, distr)
        X = X[1:]  # skip the none
        X1 = np.append(X, np.array([graph.edge[e[0]][e[1]]['weight']]))
        pairs.append((e[0], e[1]))
        vectors.append(X1)

        X2 = np.append(X[3*n_topics:], X[:3*n_topics])
        X2 = np.append(X2, np.array([graph.edge[e[0]][e[1]]['weight']]))
        pairs.append((e[1], e[0]))
        vectors.append(X2)

    return pairs, vectors


def pick_top_topics(persona, top_n, normalize):

    # a persona should be a distribution over topics for one role (A/P/M)
    # transforms vector such that the top_n topics are 1 and the other are 0
    n_topics = len(persona)
    t_persona = np.zeros(n_topics)
    if np.isnan(persona[0]):
        if normalize:
            t_persona = np.ones(n_topics) / n_topics
    else:
        args = np.argsort(-persona)
        for arg in args[:top_n]:
            if normalize:
                t_persona[arg] = 1/top_n
            else:
                t_persona[arg] = 1

    return t_persona


def construct_labels(pairs, sent_timeline):
    labels = [0.0]*len(pairs)
    for event in sent_timeline:
        participants = (event.speaker, event.receiver)
        if participants in pairs:
            labels[pairs.index(participants)] += event.sentiment['compound']

    return labels
