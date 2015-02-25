import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import accuracy_score


def support_vector_machines(data, labels):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)
    clf = svm.SVC()
    clf = clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))

    print 'SVMs'
    print 'Accuracy: ', acc

    return acc


