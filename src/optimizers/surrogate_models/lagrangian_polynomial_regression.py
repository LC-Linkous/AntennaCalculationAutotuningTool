#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/lagrangian_polynomial_regression.py'
#    Lagrangian penalty polynomial regression.
#
#   Author(s): Lauren Linkous
#   Last update: March 12, 2025
##--------------------------------------------------------------------\


import numpy as np

class LagrangianPolynomialRegression:
    def __init__(self, degree=2, noise=1e-10, constraint_degree=1):
        self.degree = degree  # Polynomial degree for the objective function
        self.noise = noise
        self.weights = None
        self.intercept = None
        self.is_fitted = False
        self.X_sample = None
        self.Y_sample = None
        self.constraint_degree = constraint_degree  # degree for the constraint function

    def _check_configuration(self, init_pts):
        MIN_INIT_POINTS = 2
        errMsg = ""
        noError = True        
        if init_pts < MIN_INIT_POINTS:
            errMsg = f"ERROR: minimum required initial points is {MIN_INIT_POINTS}"
            noError = False
        return noError, errMsg

    def _check_initial_points(self, init_pts):
        return self._check_configuration(init_pts)
    
    def fit(self, X_sample, Y_sample):
        self.X_sample = np.atleast_2d(X_sample)
        self.Y_sample = np.atleast_2d(Y_sample).reshape(X_sample.shape[0], -1)  # Flatten Y_sample to 2D

        if len(self.X_sample) < 2:
            print("ERROR: lagrangian_surrogate.fit()")
            print("Use 2 or more initial samples for this kernel")
            return

        # Polynomial feature expansion: Generate terms X, X^2, ..., X^degree
        X_poly = self._polynomial_features(self.X_sample, self.degree)

        try:
            # Linear regression: Solve for weights using least squares
            # X_poly * [intercept, weights] = Y_sample
            # Add a column of ones for the intercept term (bias)
            X_with_intercept = np.hstack([np.ones((X_poly.shape[0], 1)), X_poly])

            # Perform least squares to find weights
            self.weights = np.linalg.lstsq(X_with_intercept, self.Y_sample, rcond=None)[0]
            self.intercept = self.weights[0]  # The intercept is the first element
            self.weights = self.weights[1:]  # The rest are the polynomial regression weights
            self.is_fitted = True
        except Exception as e:
            print("ERROR in lagrangian_surrogate.fit()")
            print(e)

    def _polynomial_features(self, X, degree):
        """
        Expand input X into polynomial features up to the specified degree.
        Returns a matrix where each column is X^i for i in range(1, degree+1).
        """
        X_poly = X
        for i in range(2, degree + 1):
            X_poly = np.hstack([X_poly, np.power(X, i)])
        return X_poly
    
    def predict(self, X, out_dims=1):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: Lagrangian surrogate model is not fitted yet")
            noErrors = False
            predictions = []

        else:
            self.last_X = np.atleast_2d(X)

            try:
                # Expand the input X into polynomial features
                X_poly = self._polynomial_features(self.last_X, self.degree)

                # Add intercept term to X for prediction
                X_with_intercept = np.hstack([np.ones((X_poly.shape[0], 1)), X_poly])

                # Predict using the polynomial model
                predictions = np.dot(X_with_intercept, np.vstack([self.intercept, self.weights]))

            except Exception as e:
                predictions = []
                noErrors = False
                print(f"Prediction error: {e}")
        
        return predictions, noErrors

    def calculate_variance(self):
        # Variance calculation based on residuals for polynomial regression
        if self.is_fitted:
            # Polynomial feature expansion for the training data
            X_poly = self._polynomial_features(self.X_sample, self.degree)
            X_with_intercept = np.hstack([np.ones((X_poly.shape[0], 1)), X_poly])
            
            # Calculate the predicted Y from the polynomial model
            Y_pred = np.dot(X_with_intercept, np.vstack([self.intercept, self.weights]))

            # Compute residuals: difference between actual and predicted values
            residuals = self.Y_sample - Y_pred

            # Variance of the residuals (mean squared error)
            variance = np.var(residuals, axis=0)
            return variance
        else:
            return np.zeros((len(self.X_sample), 1))  # Return zero variance if not fitted

    def lagrangian(self, X, lambda_value=1.0):
        """
        A simple Lagrangian function combining the objective and constraint.
        The objective is to minimize f(X), and the constraint is based on the constraint degree.
        
        Lagrangian: L(X, λ) = f(X) + λ * (g(X))
        where g(X) = X^constraint_degree - 1
        """
        # Objective function: Polynomial regression prediction
        predictions, _ = self.predict(X)
        objective = np.sum(predictions**2)  # Example: minimizing the squared predictions

        # Constraint function: Polynomial of degree `constraint_degree`
        constraint = np.power(X, self.constraint_degree) - 1  # g(X) = X^constraint_degree - 1

        # Lagrangian: objective + λ * constraint
        lagrangian_value = objective + lambda_value * np.sum(constraint**2)

        return lagrangian_value