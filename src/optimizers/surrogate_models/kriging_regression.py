#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/kriging_regression.py'
#   Kriging (Gaussian process regression) surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: June 25, 2024
##--------------------------------------------------------------------\

import numpy as np

class Kriging:
    def __init__(self, length_scale=1.1, noise=1e-10):
        self.length_scale = length_scale
        self.K_ss = None
        self.weights = None
        self.covariances = None
        self.last_X = None
        self.noise = noise
        self.is_fitted = False

    def empirical_variogram(self, X, Y):
        # Calculate empirical variogram from data X and Y
        dists = np.sqrt(np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2))  # Euclidean distance
        variogram = np.abs(Y[:, None, :] - Y[None, :, :]) ** 2 / 2
        return dists, variogram.mean(axis=2)  # Average over the third dimension

    def fit(self, X_sample, Y_sample):
        self.X_sample = np.atleast_2d(X_sample)
        self.Y_sample = np.atleast_2d(Y_sample).reshape(X_sample.shape[0], -1)  # Flatten Y_sample to 2D

        # Calculate empirical variogram
        dists, variogram = self.empirical_variogram(self.X_sample, self.Y_sample)

        # Fit a variogram model to the empirical variogram (simplified example)
        # For example, fitting a linear model to the variogram
        self.variogram_model_params = np.polyfit(dists.flatten(), variogram.flatten(), deg=1)

        # Compute the covariance matrix of the sample points using the variogram model
        self.K = self.variogram_model_params[0] * dists + self.variogram_model_params[1] + self.noise * np.eye(len(X_sample))
        self.K_inv = np.linalg.inv(self.K)

        self.is_fitted = True

    def predict(self, X, out_dims=1):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: Kriging model is not fitted yet")
            noErrors = False
        
        self.last_X = np.atleast_2d(X)
       
        try: 
            # Calculate distances between sample points and new points X
            dists_to_sample = np.sqrt(np.sum((self.X_sample[:, None, :] - self.last_X[None, :, :]) ** 2, axis=2))
            
            # Use the variogram model to compute covariances
            self.covariances = self.variogram_model_params[0] * dists_to_sample + self.variogram_model_params[1]
            
            # Compute the weights using the inverse of the covariance matrix
            self.weights = np.dot(self.K_inv, self.covariances)
            
            # Compute the predictions
            predictions = np.dot(self.weights.T, self.Y_sample)
        except:
            predictions = []
            noErrors = False
        
        return predictions, noErrors

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        
        # Estimate the variance of the prediction
        self.K_ss = np.zeros((len(self.last_X), len(self.last_X)))  # Placeholder for self-covariance matrix of new points
        for i in range(len(self.last_X)):
            for j in range(len(self.last_X)):
                self.K_ss[i, j] = self.variogram_model_params[0] * np.linalg.norm(self.last_X[i] - self.last_X[j]) + self.variogram_model_params[1]

        cov_prediction = self.K_ss - np.dot(self.weights.T, self.covariances)
        return np.diag(cov_prediction).reshape(-1,1)