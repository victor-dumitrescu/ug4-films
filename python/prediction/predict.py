import itertools
import cPickle as pickle

from graphs import get_graphs
from utils.store_sentiment import load
from utils.misc import TopScores, export_to_arff
from sentiment.trajectories import plot_trajectory
from personas import Persona

from prediction.features import construct_feature_vectors, construct_labels
from prediction.lin_regression import linear_regression
from prediction.regression_tree import tree_regression
from prediction.ridge_regression import ridge_regression
from prediction.svm_regression import svm_regression
from prediction.decision_tree import decision_tree
from prediction.random_forest import random_forest
from prediction.svm import support_vector_machines


n_topics = 10
lowest_mse = TopScores(100.0, order_max=False, max_items=300)
highest_accuracy = TopScores(0.0, max_items=300)

# VAR_THRESHOLD = 0.05
# VAR_THRESHOLD = 0.06
# VAR_THRESHOLD = 0.07
VAR_THRESHOLD = 0.08


def compute_variance_class((a, b)):
    try:
        if abs(a-b) < VAR_THRESHOLD:
            # variation across halves is not significant
            return 1
        elif a > b:
            # sentiment evolves negatively
            return 0
        else:
            # sentiment evolves positively
            return 2
    except TypeError:
        return None


def make_predictions(config, variation=False, verbose=False):

    global lowest_mse
    global highest_accuracy

    graphs = get_graphs(filter_nodes=config[0],
                        # filter_by_persona=config[1],
                        verbose=False)
    data = []
    pairs = []
    if variation:
        labels = [[], []]
    else:
        labels = []

    for g in graphs:

        p, vectors = construct_feature_vectors(graphs[g],
                                               n_topics,
                                               pers=config[2],
                                               pick_top=config[3],
                                               filter_persona=config[1],
                                               edge_weights=False)
        data += vectors
        pairs += map((lambda x: x + (graphs[g].graph['title'],)), p)

        sent_timeline = load(graphs[g].graph['gexf'][:-5])

        if variation:
            halves = construct_labels(p, sent_timeline, variation=True)
            labels[0] += halves[0]
            labels[1] += halves[1]
        else:
            labels += construct_labels(p, sent_timeline, variation=False)


        ### code snippet for plotting sentiment trajectories
        # if graphs[g].graph['title'] == 'Midnight in Paris':
        #     plot_trajectory(sent_timeline, 'GIL', 'INEZ', mode='compound', title='Midnight in Paris')
        # if graphs[g].graph['title'] == 'The Silence of the Lambs':
        #     plot_trajectory(sent_timeline, 'DR. LECTER', 'CLARICE', title='The Silence of the Lambs')

        ### code snippet for plotting every sentiment trajectory
        try:
            if graphs[g].graph['title'] in ['Chasing Amy']:
                chars = graphs[g].node.keys()
                plot_trajectory(sent_timeline, chars[2], chars[1],
                                mode='compound',
                                title=graphs[g].graph['title'])
                plot_trajectory(sent_timeline, chars[0], chars[2],
                                mode='compound',
                                title=graphs[g].graph['title'])
                plot_trajectory(sent_timeline, chars[0], chars[1],
                                mode='compound',
                                title=graphs[g].graph['title'])

            # print graphs[g].graph['title']
        except:
            print graphs[g].node, len(graphs[g].node)

    if variation:
        class_labels = map(compute_variance_class, zip(labels[0], labels[1]))
        assert len(class_labels) == len(data) == len(pairs)
        # prune data for which we do not have a label
        for i in reversed(range(len(class_labels))):
            if class_labels[i] is None:
                del class_labels[i]
                del data[i]
                del pairs[i]
    else:
        class_labels = map(lambda x: 0 if x < 0.0 else 1, labels)

    # export_to_arff(data, class_labels, config)
    regression_models = [
        # linear_regression,
        # tree_regression,
        # ridge_regression,
        # svm_regression
    ]

    classifiers = [
        decision_tree#,
        # random_forest,
        # support_vector_machines
    ]

    if verbose:
        print "With ", config
        print 'Number of feature vectors: ' + str(len(data))

    for model in regression_models:
        mse = model(data, labels, verbose=verbose)
        lowest_mse.score(mse, (model, config))

    if variation:
        maj_count = 0
        for i in range(3):
            count = class_labels.count(i)
            if count > maj_count:
                maj_count = count
        baseline = float(maj_count)/len(class_labels)
    else:
        baseline = float(sum(class_labels))/len(class_labels)

    for model in classifiers:
        accuracy = model(data, class_labels, verbose=verbose)
        highest_accuracy.score(accuracy, (baseline, model, config))

    if verbose:
        print ''
        if variation:
            print 'Total: %d; C0: %d; C1: %d; C2: %d; Classification baseline: %f' % (len(class_labels),
                                                                                      class_labels.count(0),
                                                                                      class_labels.count(1),
                                                                                      class_labels.count(2),
                                                                                      baseline)
        else:
            print 'Total: %d; Pos: %d; Classification baseline: %f' % (len(class_labels),
                                                                       sum(class_labels),
                                                                       baseline)
        print ''
        print highest_accuracy.get_sorted()
        print lowest_mse.get_sorted()
        print ''
        print ''


def main():

    # Predictions can either be made by exploring a space of possible configurations
    # for data and predictors or on a preset list of configurations
    # The global variables
    #    highest_accuracy
    #    lowest_mse
    # will hold the best results together with their configurations.
    #
    #
    # Define the ranges of possible configurations for feature engineering
    # All configurations will be tested with all predictors
    #
    # [0] no. of max nodes in each graph
    filter_top_values = [2] #range(2, 8) + [False]
    #
    # [1] filter or not nodes w/o persona information
    filter_personas = [True]
    #
    # [2] powerset of {A, P, M} as lists
    personas = list(itertools.imap(list,
                       itertools.chain.from_iterable(
                           itertools.combinations('APM', r) for r in range(1, 4))))
    personas = [['A', 'M']]
    #
    # [3] replace all other topic values in persona distribution with 0 and normalise
    pick_top = [3]# + range(1, 8)
    #
    # [4] use the edge weight information or not
    edge_weights = [False]#, False]

    for config in itertools.product(filter_top_values, filter_personas, personas, pick_top, edge_weights):
            try:
                make_predictions(config, variation=False, verbose=True)
            except:
                print 'error with ' + str(config)
                raise
    #
    # pickle.dump(lowest_mse, open('/home/victor/GitHub/experiment/final_results/regression.pickle', 'w'))
    # pickle.dump(highest_accuracy, open('/home/victor/GitHub/experiment/final_results/classification_var008.pickle', 'w'))
    #     print 'dumped'

    # for i in range(2):
    #     config = (2, True, ['A', 'P'], 3, True)
    #     make_predictions(config, verbose=True)

    ### Results 1:
    # full_data_set_configs = [(False, True, ['A', 'P', 'M'], False, True),
    #                          (False, True, ['A', 'P', 'M'], False, False),
    #                          (False, False, ['A', 'P', 'M'], False, True),
    #                          (False, False, ['A', 'P', 'M'], False, False)]
    #
    # for config in full_data_set_configs:
    #     config = full_data_set_configs[3]
    #     make_predictions(config, verbose=True)

    ### Results 2:
    # filter_top_values = range(2,6)

    # config = (False, True, ['A', 'P', 'M'], False, True)
    # make_predictions(config, variation=True, verbose=True)

main()