#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/polynomial_chaos_expansion.py'
#   Polynomial Chaos Expansion surrogate model for optimization. 
#       #https://en.wikipedia.org/wiki/Polynomial_chaos
#
#   Author(s): Lauren Linkous 
#   Last update: June 25, 2024
##--------------------------------------------------------------------\

import numpy as np

class PolynomialChaosExpansion:
    def __init__(self, degree=2):
        self.degree = degree
        self.mean = []
        self.coefficients = None
        self.is_fitted = False

    def _hermite_polynomials(self, X):
        # Generate Hermite polynomials (orthogonal polynomials for Gaussian input variables)
        X = np.atleast_2d(X)
        num_features = X.shape[1]
        H = [np.ones(X.shape[0])]  # Start with the zeroth order polynomial (constant)
        
        for i in range(num_features):
            Xi = X[:, i]
            H.append(Xi)
            
            for n in range(2, self.degree + 1):
                Hn = Xi * H[-1] - (n - 1) * H[-2]
                H.append(Hn)
        
        return np.column_stack(H)

    def fit(self, X_sample, Y_sample):
        self.X_sample = np.atleast_2d(X_sample)
        self.Y_sample = np.atleast_2d(Y_sample)  # Ensure Y_sample is 2-dimensional

        # Generate polynomial features
        H_poly = self._hermite_polynomials(self.X_sample)
        
        # Compute coefficients using regularized least squares
        self.coefficients, _, _, _ = np.linalg.lstsq(H_poly, self.Y_sample, rcond=None)

        self.is_fitted = True

    def predict(self, X, out_vars=None):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: PolynomialChaosExpansion model is not fitted yet")
            noErrors = False

        X = np.atleast_2d(X)
        try: 
            if X.shape[1] != self.X_sample.shape[1]:
                print("ERROR: Number of features in X does not match the training data in predict")

            H_poly = self._hermite_polynomials(X)

            reshaped_coefficients = self.coefficients.reshape((self.coefficients.shape[0], -1))

            mean = np.dot(H_poly, reshaped_coefficients)
            self.mean = mean.reshape((H_poly.shape[0], -1))
        except:
            self.mean = []
            noErrors = False
        
        return self.mean, noErrors

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        variance = np.zeros_like(self.mean)  # No variance
        return variance