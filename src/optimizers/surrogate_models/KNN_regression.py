#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/KNN_regression.py'
#   K-Nearest Neighbors surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: December 2, 2024
##--------------------------------------------------------------------\

import numpy as np

class KNNRegression:
    def __init__(self, n_neighbors=5, weights='uniform'):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.X_sample = None
        self.Y_sample = None
        self.last_predictions = None
        self.is_fitted = False

    # configuration check for surrogate models
    # important for AntennCAT surrogate model use. can skip otherwise
    def _check_configuration(self, init_pts):
        noError, errMsg = self._check_initial_points(init_pts)
        return noError, errMsg
        
    def _check_initial_points(self, init_pts):
        MIN_INIT_POINTS = 1
        errMsg = ""
        noError = True        
        if init_pts < MIN_INIT_POINTS:
            errMsg = "ERROR: minimum required initial points is" + str(MIN_INIT_POINTS)
            noError = False
        return noError, errMsg

    
    # SM functions
    def fit(self, X, Y):
        self.X_sample = np.atleast_2d(X)
        self.Y_sample = np.atleast_2d(Y).reshape(Y.shape[0], -1)  # Ensure Y_sample is 2D
        self.is_fitted = True

    def predict(self, X, out_vars=None):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: KNNRegression model is not fitted yet")
            noErrors = False
            
        X = np.atleast_2d(X)
        self.X_sample = np.atleast_2d(self.X_sample)

        try:
            if np.any(np.isnan(X)) or np.any(np.isnan(self.X_sample)):
                print("WARNING: Input data contains NaN values")

            # Compute distances
            distances = np.sqrt(np.sum((X[:, np.newaxis, :] - self.X_sample[np.newaxis, :, :]) ** 2, axis=-1))
            distances += 1e-45  # Add a small epsilon to avoid division by zero

            # Find indices of nearest neighbors
            nearest_indices = np.argsort(distances, axis=1)[:, :self.n_neighbors]

            # Calculate weights
            if self.weights == 'uniform':
                weights = np.ones_like(nearest_indices, dtype=float)
            elif self.weights == 'distance':
                weights = 1.0 / distances[np.arange(distances.shape[0])[:, None], nearest_indices]
            else:
                print("ERROR: Unsupported weight type in KNNRegression")

            # Normalize weights
            weights_sum = np.sum(weights, axis=1, keepdims=True)
            weights_normalized = weights / weights_sum

            # Predict using weighted average of nearest neighbors
            nearest_y = self.Y_sample[nearest_indices]

            # Reshape weights_normalized for broadcasting
            weights_normalized = weights_normalized[:, :, np.newaxis]

            # Compute predictions
            self.last_predictions = np.sum(weights_normalized * nearest_y, axis=1)
        except:
            self.last_predictions = []
            noErrors = False
            
        return self.last_predictions, noErrors

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        variance = np.zeros_like(self.last_predictions)  # No variance
        return variance