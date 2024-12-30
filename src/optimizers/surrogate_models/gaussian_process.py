#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/gaussian_process.py'
#   Guassian Process surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: December 2, 2024
##--------------------------------------------------------------------\

import numpy as np

class GaussianProcess:
    def __init__(self, length_scale=1.1, noise=1e-10):
        self.length_scale = length_scale
        self.K_s = None
        self.K_ss = None
        self.noise = noise
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
    def rbf_kernel(self, X1, X2):
        X1 = np.atleast_2d(X1)
        X2 = np.atleast_2d(X2)
        dists = np.sum((X1[:, None, :] - X2[None, :, :]) ** 2, axis=2)
        return np.exp(-0.5 * dists / self.length_scale**2)

    def fit(self, X_sample, Y_sample):
        # returns mean and variance
        self.X_sample = np.atleast_2d(X_sample)
        self.Y_sample = np.atleast_2d(Y_sample)
        self.K = self.rbf_kernel(self.X_sample, self.X_sample) + self.noise * np.eye(len(self.X_sample))
        self.K_inv = np.linalg.inv(self.K)
        self.is_fitted = True

    def predict(self, X, out_dims=2):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: GaussianProcess model is not fitted yet")
            noErrors = False
        X = np.atleast_2d(X)
        try:
            self.K_s = self.rbf_kernel(self.X_sample, X)
            self.K_ss = self.rbf_kernel(X, X) + self.noise * np.eye(len(X))

            ysample = self.Y_sample.reshape(-1, out_dims)
            mu_s = self.K_s.T.dot(self.K_inv).dot(ysample)
            mu_s = mu_s.ravel()
        except:
            mu_s = []
            noErrors = False
        return mu_s, noErrors
    

    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        cov_s = self.K_ss - self.K_s.T.dot(self.K_inv).dot(self.K_s) 
        return np.diag(cov_s)
