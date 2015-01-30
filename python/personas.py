import lda
import numpy as np
import cPickle as pickle
import utils.process_summaries as ps
from collections import defaultdict, namedtuple

Topic = namedtuple('Topic', 'role, topic, val')


class Persona:

    def __init__(self, tuples, name, name2, fb):

        self.agent_lemmas = defaultdict(int)
        self.patient_lemmas = defaultdict(int)
        self.modifier_lemmas = defaultdict(int)
        self.get_lemmas(tuples)

        self.name = name
        self.name2 = name2
        self.fb = fb

        self.agent = None
        self.patient = None
        self.modifier = None

    def get_lemmas(self, tuples):
        for t in tuples:
            if t.type2 == 'a':
                self.agent_lemmas[t.lemma] += 1
            elif t.type2 == 'p':
                self.patient_lemmas[t.lemma] += 1
            elif t.type2 == 'm':
                self.modifier_lemmas[t.lemma] += 1

    def compute_topic_scores(self, topics, vocab):
        n_topics = len(topics)
        for role in ['agent', 'patient', 'modifier']:
            lemmas = getattr(self, role + '_lemmas')
            norm = sum([lemmas[l] for l in lemmas])
            d = np.zeros(n_topics)
            for (t, topic) in enumerate(topics):
                for l in lemmas:
                    d[t] += lemmas[l] * topic[vocab[l]]
                d[t] /= norm

            setattr(self, role, d)

    def get_top_topics(self, no_topics):
        a = np.argsort(-self.agent)
        p = np.argsort(-self.patient)
        m = np.argsort(-self.modifier)
        ai, pi, mi = [0]*3

        n_retrieved = 0
        output = []
        while n_retrieved < no_topics or (ai == len(a) and pi == len(p) and mi == len(m)):
            arg = np.nanargmax([self.agent[a[ai]], self.patient[p[pi]], self.modifier[m[mi]]])
            assert arg in range(3)
            if arg == 0:
                output.append(Topic('agent', a[ai], self.agent[a[ai]]))
                ai += 1
            elif arg == 1:
                output.append(Topic('patient', p[pi], self.patient[p[pi]]))
                pi += 1
            else:
                output.append(Topic('modifier', m[mi], self.modifier[m[mi]]))
                mi += 1
            n_retrieved += 1

        return output


def basic_lda(n_topics, verbose=False):

    # sample code from https://pypi.python.org/pypi/lda
    X, vocab = ps.construct_lda_structs()
    print 'Started LDA.'
    model = lda.LDA(n_topics=n_topics, n_iter=500, random_state=1)
    model.fit(X)
    print 'Finished LDA.'

    if verbose:
        topic_word = model.topic_word_
        n_top_words = 8
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    return model.components_, vocab


def get_topic_top_words(topic, topic_word, vocab):


    topic_dist = topic_word[topic]
    n_top_words = 8
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    return topic_words


def make_personas(data):

    tuples = data[0]
    tups_by_char = defaultdict(list)

    characters = set()
    for t in tuples:
        characters.add(t.entity)
        tups_by_char[t.entity].append(t)

    personas = {}
    for c in characters:
        personas[c] = Persona(tups_by_char[c], data[1][c], data[2][c], c)

    return personas


def main():

    path = '../../experiment/'

    n_topics = 50  # for filtered data, use 10 instead
    topics, vocab = basic_lda(n_topics)
    pickle.dump(topics, open(path + 'topics.pickle', 'w'))
    pickle.dump(vocab, open(path + 'vocab.pickle', 'w'))
    print 'Pickled topics'

    vocab_dict = dict(zip(vocab, range(len(vocab))))

    films = {}
    summs =ps.get_summaries(filtered=True)
    for s in summs:
        personas = make_personas(summs[s])

        # for p in personas:
        #     personas[p].compute_topic_scores(topics, vocab_dict)
        #     print personas[p].get_top_topics(5)

        films[s] = personas


    pickle.dump(films, open(path + 'personas.pickle', 'w'))

    with open(path + 'topics.csv', 'w') as f:
        for i in range(n_topics):
            f.write('%d, %s\n' % (i, ', '.join(get_topic_top_words(i, topics, vocab))))


main()