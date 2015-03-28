import numpy as np
from copy import copy

def construct_feature_vectors(graph, n_topics, **kwargs):

    # construct a vector with 3*n_topics+1 elements, by concatenating
    # the 6 distributions (3 from each character) and the weight of
    # the edge between them

    # optional arguments:
    # pers=['A', 'P', 'M'] or a subset
    #    indicated which persona distributions should be included
    #    default is all
    #
    # pick_top
    #
    # normalize
    #
    # edge_weights
    #    True if graph edge weights should be included as a feature
    #    False otherwise

    pers = kwargs.get('pers', None)
    filter_persona = kwargs.get('filter_persona', True)
    pick_top = kwargs.get('pick_top', None)
    edge_weights = kwargs.get('edge_weights', True)


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
    graph.filter_by_persona(n_topics=n_topics, remove=filter_persona)
    for e in graph.edges():
        X = None
        X1 = None
        X2 = None
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
        X = X[1:]  # skip the None

        # X1 and X2 represent the complementary relationships between the same 2 characters
        X1 = copy(X)
        if edge_weights:
            X1 = np.append(X1, np.array([graph.edge[e[0]][e[1]]['weight']]))
        vectors.append(copy(X1))
        pairs.append((e[0], e[1]))

        X2 = np.append(X[len(roles)*n_topics:], X[:len(roles)*n_topics])
        if edge_weights:
            X2 = np.append(X2, np.array([graph.edge[e[0]][e[1]]['weight']]))
        pairs.append((e[1], e[0]))
        vectors.append(copy(X2))

        # make sure feature vectors have the same size
        assert len(vectors[-1]) == len(vectors[-2])

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


def construct_labels(pairs, sent_timeline, variation=False):

    if variation:
        halves = [[None] * len(pairs), [None] * len(pairs)]
        lengths = [[None] * len(pairs), [None] * len(pairs)]
        mid_point = len(sent_timeline) / 2
        for i, event in enumerate(sent_timeline):
            participants = (event.speaker, event.receiver)
            if participants in pairs:
                # add sentiment to the corresponding list, depending on the half of the film
                # in which the event occurs
                if i < mid_point:
                    h = 0
                else:
                    h = 1

                if halves[h][pairs.index(participants)]:
                    halves[h][pairs.index(participants)] += event.sentiment['compound']
                    lengths[h][pairs.index(participants)] += 1
                else:
                    halves[h][pairs.index(participants)] = event.sentiment['compound']
                    lengths[h][pairs.index(participants)] = 1

    # else:
    labels = [0.0]*len(pairs)
    for event in sent_timeline:
        participants = (event.speaker, event.receiver)
        if participants in pairs:
            labels[pairs.index(participants)] += event.sentiment['compound']

    # check the integrity of the halves by adding them up and comparing with the total sentiment
    assert len(labels) == len(halves[0]) == len(halves[1])
    for i in range(len(labels)):
        try:
            if labels[i] == 0.0:
                assert ((not halves[0][i]) and (not halves[1][i]) or
                       ((not halves[0][i]) and halves[1][i] == 0.0) or
                       (halves[0][i] == 0.0 and (not halves[1][i])) or
                       (halves[0][i] + halves[1][i] == 0.0))
            elif halves[0][i] and halves[1][i]:
                assert abs(halves[0][i] + halves[1][i] - labels[i]) < 0.001
        except AssertionError:
            print labels[i], halves[0][i], halves[1][i]

    if variation:
        for h in range(2):
            for i, cumulative_sentiment in enumerate(halves[h]):
                if halves[h][i]:
                    halves[h][i] = cumulative_sentiment/lengths[h][i]

        return halves
    else:
        return labels
