import numpy as np
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


def random_forest(data, labels, verbose=False):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)

    best_accuracy = 0.0
    best_criterion = None
    for criterion in ['gini', 'entropy']:
        for repeat in range(20):
            clf = RandomForestClassifier(n_estimators=15, criterion=criterion)
            clf = clf.fit(X_train, y_train)
            acc = accuracy_score(y_test, clf.predict(X_test))
            if acc > best_accuracy:
                best_accuracy = acc
                best_criterion = criterion

    if verbose:
        print 'Random forest classification (criterion: %s)' % best_criterion
        print 'Accuracy: ', best_accuracy

    return best_accuracy


