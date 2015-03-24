import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import accuracy_score


def support_vector_machines(data, labels, verbose=False):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']

    best_accuracy = 0.0
    best_kernel = None
    remarks = ''
    for kernel in kernels:
        clf = svm.SVC(kernel=kernel)
        clf = clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        if acc > best_accuracy:
            if best_kernel != None:
                remarks = 'clear: '   # shows not all kernels had same accuracy
            best_accuracy = acc
            best_kernel = kernel

    if verbose:
        print 'SVMs (%s%s)' % (remarks, best_kernel)
        print 'Accuracy: ', best_accuracy

    return best_accuracy


