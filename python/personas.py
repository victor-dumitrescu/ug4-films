import lda
import numpy as np
from utils.process_summaries import construct_lda_structs


def basic_lda():

    X, vocab = construct_lda_structs()
    model = lda.LDA(n_topics=50, n_iter=500, random_state=1)
    model.fit(X)

    # sample code from https://pypi.python.org/pypi/lda
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
