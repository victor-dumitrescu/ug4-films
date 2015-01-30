import re


def get_summaries(filtered=False):

    # returns a list containing, for each, summary, a list of word lemmas

    data = {}
    path = '../../experiment/'
    if filtered:
        f_name = path + 'filtered.movies.data'
    else:
        f_name = path + 'movies.data'
    f_name = path + 'filtered.movies.data'

    def get_lemma(tup):
        m = re.search(r'(?P<entity>(e\d+|/m/\w+)):(?P<type>[tm]\.?\d+\.\d+\.\d+):(?P<ss>[\w\.]+):(?P<token>.+):(?P<type2>[map]):(?P<dependency>\w+)', tup.strip())
        return m.group(5)

    docs = []
    with open(f_name) as f:
        for row in f:
            m = re.search(r'(?P<id>\d+)\s+(?P<tuples>.*)\s+(?P<ents1>{.*})\s+(?P<ents2>{.*})', row)
            word_lemmas = map(get_lemma, m.group('tuples').split())  # list of all lemmas from current summary
            docs.append(word_lemmas)

    return docs

