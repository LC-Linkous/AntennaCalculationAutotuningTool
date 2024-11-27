##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/BAYESIAN/controller_BAYESIAN.py'
#   Class interfacing with the bayesian optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.BAYESIAN.bayesian_optimization_python.bayesian_optimizer import BayesianOptimization
from optimizers.BAYESIAN.bayesian_optimization_python.constr_default import constr_default

# #SURROGATE MODELS (customization to be added)
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.RBF_network import RBFNetwork
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.gaussian_process import GaussianProcess
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.kriging_regression import Kriging
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.polynomial_regression import PolynomialRegression
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.polynomial_chaos_expansion import PolynomialChaosExpansion
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.KNN_regression import KNNRegression
# from optimizers.BAYESIAN.bayesian_optimization_python.surrogate_models.decision_tree_regression import DecisionTreeRegression

#SURROGATE MODELS (customization to be added)
from optimizers.surrogate_models.RBF_network import RBFNetwork
from optimizers.surrogate_models.gaussian_process import GaussianProcess
from optimizers.surrogate_models.kriging_regression import Kriging
from optimizers.surrogate_models.polynomial_regression import PolynomialRegression
from optimizers.surrogate_models.polynomial_chaos_expansion import PolynomialChaosExpansion
from optimizers.surrogate_models.KNN_regression import KNNRegression
from optimizers.surrogate_models.decision_tree_regression import DecisionTreeRegression


class CONTROLLER_BAYESIAN():
    def __init__(self, parent): 
        self.parent = parent

        # class vars
        self.optimizer = None           # init as a none obj 
        self.sm = None                  # init surrogate model as none obj
        self.suppress_output = False    # Suppress the console output of multiglods

        self.allow_update = True        # Allow objective call to update state 



####################################################
# GUI interfacing
####################################################

    def updateStatusText(self, t):
        self.parent.updateStatusText(t)


####################################################
# Toggle allow updates
####################################################

    def setAllowUpdate(self, b):
        self.allow_update = b

    def getAllowUpdate(self, b):
        return self.allow_update


######################################################
# Check if complete
#######################################################

    def checkOptimizerComplete(self):
        return self.optimizer.complete()


######################################################
# new run setup
#######################################################

    def unpackOptimizerParameters(self, optimizerParams, func_F):
        print("controller_BAYESIAN unpack optimizer parameters")

        # Bayesian optimizer tuning params
        NO_OF_VARS = float(optimizerParams['num_input'][0])    # Number of input variables (x-values)
        print("NO_OF_VARS")
        print(NO_OF_VARS)
        TOL = float(optimizerParams['tolerance'][0])           # Convergence Tolerance (This is a radius 
        print("TOL")
        print(TOL)                                                               # based tolerance, not target based tolerance)
        LB = list(optimizerParams['lower_bounds'][0])          # Lower boundaries
        print("LB")
        print(LB)
        UB = list(optimizerParams['upper_bounds'][0])          # Upper Boundaries
        print("UB")
        print(UB)
        TARGETS = list(optimizerParams['target_values'][0])    # Target values for output
        print("TARGETS")
        print(TARGETS)       
        MAXIT = float(optimizerParams['max_iterations'][0])    # Maximum allowed iterations 
        print("MAXIT")
        print(MAXIT)
        XI = float(optimizerParams['xi'][0])   
        print("XI")
        print(XI)
        NUM_RESTARTS = float(optimizerParams['num_restarts'][0])    # number of restarts to minimize for randoms
        print("NUM_RESTARTS")
        print(NUM_RESTARTS)


        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        self.out_vars = len(TARGETS)
        init_num_points = 0 # right now, no optimizers are run for data collection before optimizing.
        # TODO, add this as a feature in the GUI. 
        idx = 2
        self.sm = self.select_surrogate_model(idx)

        # instantiation of multiglods optimizer 
        self.optimizer = BayesianOptimization(LB, UB, NO_OF_VARS, TARGETS, TOL, MAXIT,
                                                    func_F=func_F, constr_func=constr_default, 
                                                    init_points=init_num_points, 
                                                    xi = XI, n_restarts=NUM_RESTARTS, 
                                                    parent=self)



        msg = "optimizer configured"
        self.updateStatusText(msg)

        return F, targetMetrics

######################################################
# Optimizer step
#######################################################

    def step(self):
        # step through optimizer processing
        self.optimizer.step(self.suppress_output)

    def callObjective(self):
        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        self.optimizer.call_objective(self.allow_update)

    def get_convergence_data(self):
        return self.optimizer.get_convergence_data()

######################################################
# Optimizer End
######################################################

    def get_optimized_soln(self):
        return self.optimizer.get_optimized_soln()
    
    def get_optimized_outs(self):
        return self.optimizer.get_optimized_outs()
    
######################################################
# SURROGATE MODEL FUNCS
######################################################

    def fit_model(self, x, y):
        # call out to parent class to use surrogate model
        self.sm.fit(x,y)
        

    def model_predict(self, x):
        # call out to parent class to use surrogate model
        #'mean' is regressive definition. not statistical
        #'variance' only applies for some surrogate models
        mean, noErrors = self.sm.predict(x, self.out_vars)
        return mean, noErrors

    def model_get_variance(self):
        variance = self.sm.calculate_variance()
        return variance
    
######################################################
# SURROGATE MODEL SELECTION
######################################################

    def select_surrogate_model(self, idx=2):
        if idx == 0:
            RBF_kernel  = 'gaussian' #options: 'gaussian', 'multiquadric'
            RBF_epsilon = 1.0
            return RBFNetwork(kernel=RBF_kernel, epsilon=RBF_epsilon)  
        elif idx == 1:
            K_noise = 1e-10
            K_length_scale = 1.0      
            return Kriging(length_scale=K_length_scale, noise=K_noise)
        elif idx == 2:
            GP_noise = 1e-10
            GP_length_scale = 1.0
            return GaussianProcess(length_scale=GP_length_scale,noise=GP_noise)
        elif idx == 3:
            PR_degree = 5
            return PolynomialRegression(degree=PR_degree)
        elif idx == 4:
            PC_degree = 5 
            return PolynomialChaosExpansion(degree=PC_degree)
        elif idx == 5:
            KNN_n_neighbors=3
            KNN_weights='uniform'  #options: 'uniform', 'distance'
            return KNNRegression(n_neighbors=KNN_n_neighbors, weights=KNN_weights)
        elif idx == 6:
            DTR_max_depth = 5  # options: ints
            return DecisionTreeRegression(max_depth=DTR_max_depth)
        else:
            self.updateStatusText("ERROR: surrogate model not set")
            return None



