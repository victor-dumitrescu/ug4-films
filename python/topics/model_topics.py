import lda
import numpy as np
import cPickle as pickle

path = '/home/victor/GitHub/experiment/genres/'


def get_lda_structs():

    X = np.load(path + 'doc_matrix.npy')
    vocab = np.load(path + 'vocabulary.npy')
    return X, vocab


def get_topic_top_words(topic, topic_word, vocab):

    topic_dist = topic_word[topic]
    n_top_words = 100
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    return topic_words


def basic_lda(n_topics, verbose=False):

    # sample code from https://pypi.python.org/pypi/lda
    X, vocab = get_lda_structs()
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


def main():

    n_topics = 10
    topics, vocab = basic_lda(n_topics)
    # pickle.dump(topics, open(path + 'topics.pickle', 'w'))
    # pickle.dump(vocab, open(path + 'vocab.pickle', 'w'))
    # print 'Pickled topics'

    with open(path + 'topics.csv', 'w') as f:
        for i in range(n_topics):
            f.write('%d, %s\n' % (i, ', '.join(get_topic_top_words(i, topics, vocab))))


main()


