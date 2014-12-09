import re
import json
import numpy as np
from collections import namedtuple


Tuple = namedtuple('Tuple', 'entity, type, ss, lemma, type2, dependency')


def construct_lda_structs():

    data = get_summaries()

    # construct vocabulary
    vocab = set()
    for item in data:
        lemmas = []
        tups = data[item][0]
        for t in tups:
            lemmas.append(t.lemma)
            vocab = vocab.union(lemmas)


    # construct frequency matrix

    # lemma-position dict
    indices = dict(zip(vocab, range(len(vocab))))
    size_vocab = len(indices)
    X = []
    for item in data:
        tups = data[item][0]
        freqs = np.zeros(size_vocab)
        for t in tups:
            i = indices[t.lemma]
            freqs[i] += 1
        print freqs
        X.append(freqs)

    X = np.array(X)
    vocab = tuple(vocab)

    return X, vocab


def make_tuple(str):
    str = str.strip()
    m = re.search(r'(?P<entity>(e\d+|/m/\w+)):(?P<type>[tm]\.?\d+\.\d+\.\d+):(?P<ss>[\w\.]+):(?P<token>.+):(?P<type2>[map]):(?P<dependency>\w+)', str)
    try:
        return Tuple._make(m.groups()[1:])
    except:
        print str, m.groups()
        raise


def get_summaries():

    data = {}
    path = '../../experiment/'
    with open(path + 'filtered.movies.data') as f:
        for row in f:
            m = re.search(r'(?P<id>\d+)\s+(?P<tuples>.*)\s+(?P<ents1>{.*})\s+(?P<ents2>{.*})', row)
            data[m.group('id')] = (map(make_tuple, m.group('tuples').split()),
                                   json.loads(m.group('ents1')),
                                   json.loads(m.group('ents2')))

    return data