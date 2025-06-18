#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/surrogate_models/decision_tree_regression.py'
#   Decision Tree Regression surrogate model for optimization. 
#
#   Author(s): Lauren Linkous 
#   Last update: December 2, 2024
##--------------------------------------------------------------------\


import numpy as np

class DecisionTreeRegression:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None
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
        Y = Y.reshape(Y.shape[0], -1)  # Ensure Y is 2D
        self.tree = self._build_tree(X, Y, depth=0)
        self.is_fitted = True

    def _build_tree(self, X, Y, depth):
        if depth == self.max_depth or self._check_uniform(Y):
            return np.mean(Y)  # Leaf node, return mean of Y

        num_features = X.shape[1]
        best_feature, best_split_value = None, None
        best_mse = np.inf

        for feature in range(num_features):
            unique_values = np.unique(X[:, feature])
            for value in unique_values:
                left_mask = X[:, feature] <= value
                right_mask = X[:, feature] > value
                if np.sum(left_mask) > 0 and np.sum(right_mask) > 0:
                    left_y = Y[left_mask]
                    right_y = Y[right_mask]
                    mse = self._calculate_mse(left_y, right_y)
                    if mse < best_mse:
                        best_mse = mse
                        best_feature = feature
                        best_split_value = value

        if best_feature is None:
            return np.mean(Y)  # Leaf node, return mean of Y

        left_mask = X[:, best_feature] <= best_split_value
        right_mask = X[:, best_feature] > best_split_value
        left_subtree = self._build_tree(X[left_mask], Y[left_mask], depth + 1)
        right_subtree = self._build_tree(X[right_mask], Y[right_mask], depth + 1)

        return {'feature': best_feature,
                'split_value': best_split_value,
                'left': left_subtree,
                'right': right_subtree}

    def _check_uniform(self, Y):
        return np.all(Y == Y[0])

    def _calculate_mse(self, left_y, right_y):
        mse_left = np.var(left_y) * len(left_y)
        mse_right = np.var(right_y) * len(right_y)
        return mse_left + mse_right

    def predict(self, X, out_vars=None):
        noErrors = True
        # this is applying the objective function for the surrogate model
        if not self.is_fitted:
            print("ERROR: DecisionTreeRegression model is not fitted yet")
            noErrors = False
        X = np.atleast_2d(X)  # Ensure X is 2D
        try:        
            self.last_predictions = np.array([self._traverse_tree(x, self.tree) for x in X])
        except:
            self.last_predictions = []
            noErrors = False
        return self.last_predictions, noErrors
    
    def calculate_variance(self):
        #used for calculating expected improvement, but not applying objective func
        # use the last predictions so not calculating everything twice
        variance = np.zeros_like(self.last_predictions)  # No variance
        return variance

    
    def _traverse_tree(self, x, node):
        if isinstance(node, (float, int)):
            return node

        feature = node['feature']
        split_value = node['split_value']

        if x[feature] <= split_value:
            return self._traverse_tree(x, node['left'])
        else:
            return self._traverse_tree(x, node['right'])
