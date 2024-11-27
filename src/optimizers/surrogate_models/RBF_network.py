#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/RBF_network.py'
#   Radial Basis Function network surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: June 25, 2024
##--------------------------------------------------------------------\


import numpy as np

class RBFNetwork:
    def __init__(self, kernel='gaussian', epsilon=1.0):
        self.kernel = kernel
        self.epsilon = epsilon
        self.last_predictions  = []
        self.centers = None
        self.weights = None
        self.is_fitted = False

    def _kernel_function(self, x, c):
        if self.kernel == 'gaussian':
            return np.exp(-self.epsilon * np.linalg.norm(x - c) ** 2)
        elif self.kernel == 'multiquadric':
            return np.sqrt(1 + self.epsilon * np.linalg.norm(x - c) ** 2)
        else:
            print("ERROR: Unsupported kernel type in RBFNetwork")

    def _compute_design_matrix(self, X):
        num_samples = X.shape[0]
        num_centers = self.centers.shape[0]
        Phi = np.zeros((num_samples, num_centers))
        for i in range(num_samples):
            for j in range(num_centers):
                Phi[i, j] = self._kernel_function(X[i], self.centers[j])
        return Phi

    def fit(self, X, y):
        y = y.reshape(y.shape[0], -1)

        self.centers = X
        Phi = self._compute_design_matrix(X)
        self.weights = np.linalg.lstsq(Phi, y, rcond=None)[0]
        self.is_fitted = True

    def predict(self, X, out_vars=None):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: RBFNetwork model is not fitted yet")
            noErrors = False
        
        try:
            Phi = self._compute_design_matrix(X)
            self.last_predictions = np.dot(Phi, self.weights)
        except: 
            self.last_predictions = []
            noErrors
        return self.last_predictions , noErrors

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        variance = np.zeros_like(self.last_predictions)  # No variance
        return variance
