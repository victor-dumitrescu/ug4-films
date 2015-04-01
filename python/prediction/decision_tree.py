import numpy as np
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn import tree

from sklearn.externals.six import StringIO
import pydot

def decision_tree(data, labels, verbose=False):

    assert len(data) == len(labels)
    print data
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))

    if verbose:
        print 'Decision tree classification'
        print 'Accuracy: ', acc

    if acc > 0.9:
        dot_data = StringIO()
        tree.export_graphviz(clf, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("decision_tree.pdf")

    return acc

