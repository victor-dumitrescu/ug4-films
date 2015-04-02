import numpy as np
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.metrics import mean_squared_error


# http://scikit-learn.org/stable/modules/linear_model.html#ridge-regression

def ridge_regression(data, labels, test_size=0.2, verbose=False):

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                        data, labels, test_size=test_size, random_state=0)

    alphas = np.arange(1, 10000)
    clf = linear_model.RidgeCV(alphas)
    clf.fit(X_train, y_train)
    mse = mean_squared_error(y_test, np.float64(clf.predict(X_test)))

    if verbose:
        print 'Ridge regression'
        print 'MSE=', mse
        print 'alpha', clf.alpha_

    return mse