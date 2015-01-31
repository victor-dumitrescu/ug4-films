g_path = 'topics/'

# filter the ids of films from which we construct topic models
# output:  ids.txt
# edit:    main.max_films
execfile(g_path + 'filter_genres.py')
print 'Filtering done.'

# construct document matrix and vocabulary from films in the filtered list
# output:  doc_matrix.npy
#          vocabulary.npy

execfile(g_path + 'acquire_vocab.py')
print 'Constructing LDA structures done.'

# run LDA on the data generated above
# output:  topics.pickle
#          vocab.pickle
#          topics.csv (list of topics together with top words)
# edit:    main.n_topics
execfile(g_path + 'model_topics.py')
print 'LDA done.'
