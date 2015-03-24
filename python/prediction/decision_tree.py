import numpy as np
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn import tree


def decision_tree(data, labels, verbose=False):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))

    if verbose:
        print 'Decision tree classification'
        print 'Accuracy: ', acc

    return acc

