#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/lagrangian_linear_regression.py'
#    Lagrangian penalty linear regression.
#
#   Author(s): Lauren Linkous
#   Last update: March 12, 2025
##--------------------------------------------------------------------\


import numpy as np

class LagrangianLinearRegression:
    def __init__(self, noise=1e-10, constraint_degree=1):
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

        # Add a column of ones for the intercept term (bias)
        X_with_intercept = np.hstack([np.ones((self.X_sample.shape[0], 1)), self.X_sample])

        try:
            # Perform least squares to find weights for linear regression
            self.weights = np.linalg.lstsq(X_with_intercept, self.Y_sample, rcond=None)[0]
            self.intercept = self.weights[0]  # The intercept is the first element
            self.weights = self.weights[1:]  # The rest are the regression weights
            self.is_fitted = True
        except Exception as e:
            print("ERROR in lagrangian_surrogate.fit()")
            print(e)

    def predict(self, X, out_dims=1):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: Lagrangian surrogate model is not fitted yet")
            noErrors = False
            predictions = []

        else:
            self.last_X = np.atleast_2d(X)

            try:
                # Add intercept term to X for prediction
                X_with_intercept = np.hstack([np.ones((self.last_X.shape[0], 1)), self.last_X])

                # Predict using the linear regression model
                predictions = np.dot(X_with_intercept, np.vstack([self.intercept, self.weights]))

            except Exception as e:
                predictions = []
                noErrors = False
                print(f"Prediction error: {e}")
        
        return predictions, noErrors

    def calculate_variance(self):
        # Variance calculation based on residuals for linear regression
        if self.is_fitted:
            # Add intercept term to the training data
            X_with_intercept = np.hstack([np.ones((self.X_sample.shape[0], 1)), self.X_sample])

            # Calculate the predicted Y from the linear model
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
        # Objective function: Linear regression prediction
        predictions, _ = self.predict(X)
        objective = np.sum(predictions**2)  # Example: minimizing the squared predictions

        # Constraint function: Polynomial of degree `constraint_degree`
        constraint = np.power(X, self.constraint_degree) - 1  # g(X) = X^constraint_degree - 1

        # Lagrangian: objective + λ * constraint
        lagrangian_value = objective + lambda_value * np.sum(constraint**2)

        return lagrangian_value
