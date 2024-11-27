#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/polynomial_regression.py'
#   Polynomial Regression surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: June 25, 2024
##--------------------------------------------------------------------\

import numpy as np

class PolynomialRegression:
    def __init__(self, degree=2):
        self.degree = degree
        self.mean = []
        self.coefficients = None
        self.is_fitted = False

    def _polynomial_features(self, X):
        X = np.atleast_2d(X) # catches some edge cases

        # Generate polynomial features
        X_poly = np.ones((X.shape[0], 1))
        for d in range(1, self.degree + 1):
            X_poly = np.hstack((X_poly, X ** d))
        return X_poly

    def fit(self, X_sample, Y_sample):
        # Ensure y has the correct shape
        Y_sample = np.atleast_2d(Y_sample)
        X_sample = np.atleast_2d(X_sample)

        # if len(y.shape)>2:
        #     if y.shape[0] != X.shape[0] or y.shape[2] != 1:
        #         print("ERROR:Shape of y is not compatible with X.")
        Y_sample = Y_sample.reshape(Y_sample.shape[0], -1)

        # Fit the model using the normal equation
        X_poly = self._polynomial_features(X_sample)

        # Compute pseudo-inverse for numerical stability
        self.coefficients = np.linalg.pinv(X_poly.T.dot(X_poly)).dot(X_poly.T).dot(Y_sample)

        self.is_fitted = True

    def predict(self, X, out_vars=None):
        noErrors = True
        if not self.is_fitted:
            print("PolynomialRegression model is not fitted yet")
            noErrors = False
        X = np.atleast_2d(X)

        try: 
            X_poly = self._polynomial_features(X)
            
            # Reshape coefficients to match dimensions for matrix multiplication
            reshaped_coefficients = self.coefficients.reshape((self.coefficients.shape[0], -1))
                
            mean = np.dot(X_poly, reshaped_coefficients)
            
            self.mean = mean.reshape((X_poly.shape[0], -1))
        except:
            self.mean = []
            noErrors = False
        
        return self.mean, noErrors

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        variance = np.zeros_like(self.mean)  # No variance
        return variance