import numpy as np
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from personas import Persona


def linear_regression(data, labels, verbose=False):

    assert len(data) == len(labels)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
                         data, labels, test_size=0.2, random_state=0)
    regression = LinearRegression()
    regression.fit(X_train, y_train)
    mse = mean_squared_error(y_test, np.float64(regression.predict(X_test)))

    if verbose:
        print 'Linear regression'
        print 'MSE= ', mse
        return mse
    # scores = cross_validation.cross_val_score(regression, data, labels, cv=5)
