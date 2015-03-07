import itertools

from graphs import get_graphs
from utils.store_sentiment import load
from utils.misc import TopScores
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


def main():

    n_topics = 10
    lowest_mse = 100.0
    # highest_accuracy = 0.0
    highest_accuracy = TopScores(0.0)

    # Acquire graphs for all these settings
    # [0] no. of max nodes in each graph
    filter_top_values = range(3, 4) + [False]
    # [1] filter or not nodes w/o persona information
    filter_personas = [True]  # , False]
    # [2] powerset of {A, P, M} as lists
    personas = list(itertools.imap(list,
                       itertools.chain.from_iterable(
                           itertools.combinations('APM', r) for r in range(1, 4))))
    # [3] replace all other topic values in persona distribution with 0
    pick_top = range(1, 5) + [False]

    for config in itertools.product(filter_top_values, filter_personas, personas, pick_top):
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
        # for model in regression_models:
        #     mse = model(data, labels)
        #     if mse < lowest_mse:
        #         best_fit = (model, config)
        #         lowest_mse = mse
        for model in classifiers:
            accuracy = model(data, polarity_labels)
            highest_accuracy.score(accuracy, (model, config))
            # if accuracy > highest_accuracy:
            #     best_classifier = (model, config)
            #     highest_accuracy = accuracy
        print ''

    # print lowest_mse, best_fit
    # print highest_accuracy, best_classifier
    print highest_accuracy.get_sorted()

    # best regression:
    # 6.95012940528 (tree_regression, (False, True, ['P'], False))
    # best decision tree:
    # 0.794117647059 (decision_tree, (3, True, ['A', 'P'], 2))
    # best random forest:
    # 0.852941176471 (random_forest, (3, True, ['M'], False))
    # best SVM:
    # 0.794117647059 [many configurations]

    # transitivity of relations

main()