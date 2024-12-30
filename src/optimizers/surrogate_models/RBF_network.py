#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/RBF_network.py'
#   Radial Basis Function network surrogate model for optimization. 
#
#   Note: the underscores before the func names are to differentiate the 
#       layers of optimizer/surrogate modeling
#
#
#   Author(s): Lauren Linkous 
#   Last update: December 3, 2024
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

        
    # configuration check for surrogate models
    # important for AntennCAT surrogate model use. can skip otherwise
    def _check_configuration(self, init_pts, kernel):
        noError, errMsg = self._check_initial_points(init_pts)

        if noError == False: #return first issue
            return noError, errMsg

        noError, errMsg = self._check_kernel(kernel)

        return noError, errMsg
        

    def _check_initial_points(self, init_pts):
        MIN_INIT_POINTS = 1
        errMsg = ""
        noError = True        
        if init_pts < MIN_INIT_POINTS:
            errMsg = "ERROR: minimum required initial points is" + str(MIN_INIT_POINTS)
            noError = False
        return noError, errMsg

    def _check_kernel(self, kernel):
        errMsg = ""
        noError = True        
        if not(kernel == 'gaussian' or kernel == 'multiquadric'):
            errMsg = "WARNING: unrecognized kernel type:" + str(kernel)
            noError = False
        return noError, errMsg
    
    # SM functions
    def _kernel_function(self, x, c):
        if self.kernel == 'gaussian':
            return np.exp(-self.epsilon * np.linalg.norm(x - c) ** 2)
        elif self.kernel == 'multiquadric':
            return np.sqrt(1 + self.epsilon * np.linalg.norm(x - c) ** 2)
        else:
            
            print("ERROR: Unsupported kernel type in RBFNetwork: " + str(self.kernel))
            

    def _compute_design_matrix(self, X):
        num_samples = X.shape[0]
        num_centers = self.centers.shape[0]
        Phi = np.zeros((num_samples, num_centers))
        for i in range(num_samples):
            for j in range(num_centers):
                Phi[i, j] = self._kernel_function(X[i], self.centers[j])
        return Phi

    def fit(self, X, y):
        if len(X) < 1:
            print("ERROR: at least one initial point needed for this kernel")
            return
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
