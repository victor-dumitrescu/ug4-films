import itertools

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
lowest_mse = TopScores(100.0, order_max=False)
highest_accuracy = TopScores(0.0)


def make_predictions(config):

    global lowest_mse
    global highest_accuracy

    graphs = get_graphs(filter_nodes=config[0],
                        filter_by_persona=config[1],
                        verbose=False)
    data = []
    pairs = []
    labels = []

    for g in graphs:

        p, vectors = construct_feature_vectors(graphs[g],
                                               n_topics,
                                               pers=config[2],
                                               pick_top=config[3],
                                               normalize=True)
        data += vectors
        pairs += map((lambda x: x + (graphs[g].graph['title'],)), p)

        sent_timeline = load(graphs[g].graph['gexf'][:-5])
        labels += construct_labels(p, sent_timeline)

        # if graphs[g].graph['title'] == 'Midnight in Paris':
        #     plot_trajectory(sent_timeline, 'GIL', 'INEZ', mode='compound')

    polarity_labels = map(lambda x: 0 if x < 0.0 else 1, labels)

    export_to_arff(data, polarity_labels, config)

    regression_models = [
        linear_regression,
        tree_regression,
        ridge_regression,
        svm_regression
    ]

    classifiers = [
        decision_tree,
        random_forest,
        support_vector_machines
    ]

    print "With ", config
    print 'Number of feature vectors: ' + str(len(data))
    # for model in regression_models:
    #     mse = model(data, labels)
    #     lowest_mse.score(mse, (model, config))
    for model in classifiers:
        accuracy = model(data, polarity_labels)
        highest_accuracy.score(accuracy, (model, config))
    print ''
    print 'Total: %d; Pos: %d; Baseline: %f' % (len(polarity_labels),
                                                sum(polarity_labels),
                                                float(sum(polarity_labels))/len(polarity_labels))
    print ''
    print highest_accuracy.get_sorted()
    print lowest_mse.get_sorted()
    print ''
    print ''


def main():

    # Define the ranges of possible configurations for feature engineering
    # All configurations will be tested with all predictors

    # [0] no. of max nodes in each graph
    filter_top_values = [False]  # + range(3, 11)

    # [1] filter or not nodes w/o persona information
    filter_personas = [False]

    # [2] powerset of {A, P, M} as lists
    personas = list(itertools.imap(list,
                       itertools.chain.from_iterable(
                           itertools.combinations('APM', r) for r in range(1, 4))))

    # [3] replace all other topic values in persona distribution with 0 and normalise
    pick_top = [False] + range(1, 3)

    # for config in itertools.product(filter_top_values, filter_personas, personas, pick_top):
    #     make_predictions(config)

    config = (False, False, ['A', 'P', 'M'], False)
    make_predictions(config)



main()