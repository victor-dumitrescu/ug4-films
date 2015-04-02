import numpy as np
from sklearn import cross_validation
from sklearn.metrics import mean_squared_error
from sklearn import tree


def tree_regression(data, labels, verbose=False):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                     data, labels, test_size=0.2, random_state=0)
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(X_train, y_train)
    mse = mean_squared_error(y_test, np.float64(clf.predict(X_test)))

    if verbose:
        print 'Decision tree regression'
        print 'MSE= ', mse

    return mse
