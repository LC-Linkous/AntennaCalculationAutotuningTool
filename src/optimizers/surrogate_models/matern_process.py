#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/matern_process.py'
#   Matern Process surrogate model for optimization. RBF generalization
#
#   Author(s): Lauren Linkous
#   Last update: March 12, 2025
##--------------------------------------------------------------------\

import numpy as np

class MaternProcess:
    def __init__(self, length_scale=1.1, noise=1e-10, nu=3/2):
        self.length_scale = length_scale
        self.noise = noise
        self.nu = nu
        self.K_s = None
        self.K_ss = None
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

    # Matern kernel function
    def matern_kernel(self, X, Y):
        X = np.atleast_2d(X)
        Y = np.atleast_2d(Y)
        dists = np.sum((X[:, None, :] - Y[None, :, :]) ** 2, axis=2)

        if self.nu == 1/2:
            # Matern kernel with nu = 1/2 (rough process)
            return np.exp(-np.sqrt(dists) / self.length_scale)
        elif self.nu == 3/2:
            # Matern kernel with nu = 3/2
            return (1 + np.sqrt(3) * np.sqrt(dists) / self.length_scale) * np.exp(-np.sqrt(3) * np.sqrt(dists) / self.length_scale)
        elif self.nu == 5/2:
            # Matern kernel with nu = 5/2
            return (1 + np.sqrt(5) * np.sqrt(dists) / self.length_scale + (5 * dists) / (3 * self.length_scale**2)) * np.exp(-np.sqrt(5) * np.sqrt(dists) / self.length_scale)
        else:
            # Generalized Matern kernel
            factor = (np.sqrt(2 * self.nu) * np.sqrt(dists)) / self.length_scale
            return (1 + factor) ** self.nu * np.exp(-factor)

    def fit(self, X, Y):
        # returns mean and variance
        self.X_sample = np.atleast_2d(X)
        self.Y_sample = np.atleast_2d(Y)
        self.K = self.matern_kernel(self.X_sample, self.X_sample) + self.noise * np.eye(len(self.X_sample))
        self.K_inv = np.linalg.inv(self.K)
        self.is_fitted = True

    def predict(self, X, out_vars=None):
        noErrors = True
        if not self.is_fitted:
            print("ERROR: MaternProcess model is not fitted yet")
            noErrors = False

        X = np.atleast_2d(X)
        self.X_sample = np.atleast_2d(self.X_sample)

        try:
            self.K_s = self.matern_kernel(self.X_sample, X)
            self.K_ss = self.matern_kernel(X, X) + self.noise * np.eye(len(X))

            ysample = self.Y_sample.reshape(self.Y_sample.shape[0], -1)
            mu_s = self.K_s.T.dot(self.K_inv).dot(ysample)
            mu_s = mu_s.ravel()
        except:
            mu_s = []
            noErrors = False
        return mu_s, noErrors

    def calculate_variance(self):
        # used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        cov_s = self.K_ss - self.K_s.T.dot(self.K_inv).dot(self.K_s) 
        return np.diag(cov_s)
