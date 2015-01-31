import re
import numpy as np

path = '/home/victor/GitHub/experiment/'


def get_summaries():

    # returns a list containing, for each, summary, a list of word lemmas

    f_name = path + 'movies.data'

    def get_lemma(tup):
        m = re.search(r'(?P<entity>(e\d+|/m/\w+)):(?P<type>[tm]\.?\d+\.\d+\.\d+):(?P<ss>[\w\.]+):(?P<token>.+):(?P<type2>[map]):(?P<dependency>\w+)', tup.strip())
        return m.group(5)

    # the list of remaining film ids from our filtered ids.txt
    with open(path + 'genres/ids.txt') as f:
        remaining = map((lambda x: x.strip()), f.readlines())

    vocabulary = set()
    docs = []
    with open(f_name) as f:
        for row in f:
            m = re.search(r'(?P<id>\d+)\s+(?P<tuples>.*)\s+(?P<ents1>{.*})\s+(?P<ents2>{.*})', row)
            film_id = m.group('id')
            if film_id in remaining:
                word_lemmas = []
                for lemma in map(get_lemma, m.group('tuples').split()):  # list of all lemmas from current summary
                    word_lemmas.append(lemma)
                    vocabulary.add(lemma)
                docs.append(word_lemmas)
                remaining.remove(film_id)

    return docs, list(vocabulary)


def construct_document_matrix(docs, vocabulary):

    # vocabulary becomes a keymap from words to indices in doc matrix
    vocabulary_dict = dict(zip(vocabulary, range(len(vocabulary))))
    X = np.zeros((len(docs), len(vocabulary)))
    for i, doc in enumerate(docs):
        for lemma in doc:
            X[i, vocabulary_dict[lemma]] += 1

    f_matrix = path + 'genres/doc_matrix.npy'
    np.save(f_matrix, X)

    f_vocabulary = path + 'genres/vocabulary.npy'
    np.save(f_vocabulary, np.array(vocabulary))


def main():

    docs, vocab = get_summaries()
    construct_document_matrix(docs, vocab)


main()