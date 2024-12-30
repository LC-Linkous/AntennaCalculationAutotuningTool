##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/BAYESIAN/controller_BAYESIAN.py'
#   Class interfacing with the bayesian optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: December 2, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.BAYESIAN.bayesian_optimization_python.bayesian_optimizer import BayesianOptimization
from optimizers.BAYESIAN.bayesian_optimization_python.constr_default import constr_default

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
        # Bayesian optimizer tuning params

        # values that apply to all surrogate models
        LB = [list(optimizerParams['lower_bounds'][0])]                    # Lower boundaries
        UB = [list(optimizerParams['upper_bounds'][0])]                    # Upper Boundaries
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = float(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
        INIT_SAMPLES = int(optimizerParams['init_samples'][0])
        SURROGATE_MODEL = int(optimizerParams['surrogate_model'][0]) # integer representation of surrogate model (for later variations)
                                                                        #0 = RBF network, 1 = Gaussian process, 2 = Kriging
                                                                        #3 = Polynomial regression, 4 = polynomial chaos expansion,
                                                                        #5 = KNN regression, 6 = Decision Tree Regression
        XI = float(optimizerParams['xi'][0])   
        NUM_RESTARTS = float(optimizerParams['num_restarts'][0])    # number of restarts to minimize for randoms


        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        self.out_vars = len(TARGETS)


        # SURROGATE MODEL VARS
        # inbuilt error correction here. This will be cleaned up in later versions after some testing.
        if SURROGATE_MODEL == 0:
            # Radial Basis Function Kernel
            # set kernel specific vars
            RBF_KERNEL = optimizerParams['rbf_kernel'][0]#options: 'gaussian', 'multiquadric'
            RBF_EPSILON = float(optimizerParams['rbf_epsilon'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if RBF_KERNEL in ['gaussian', 'multiquadric']:
                pass
            else:
                RBF_KERNEL = 'gaussian'
                msg = "ERROR: unknown RBF kernel. Defaulting to gaussian RBF kernel"
                self.updateStatusText(msg)
           
            # setup
            self.sm = RBFNetwork(kernel=RBF_KERNEL, epsilon=RBF_EPSILON)  
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES, RBF_KERNEL)

        elif SURROGATE_MODEL == 1:
            # Gaussian Process vars
            # set kernel specific vars
            GP_NOISE = float(optimizerParams['gp_noise'][0])#1e-10
            GP_LENGTH_SCALE = float(optimizerParams['gp_length_scale'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)

            self.sm = GaussianProcess(length_scale=GP_LENGTH_SCALE,noise=GP_NOISE) 
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == 2:
            # Kriging vars
            # set kernel specific vars
            K_LENGTH_SCALE = float(optimizerParams['k_length_scale'][0])# 1.0
            K_NOISE = float(optimizerParams['k_noise'][0]) # 1e-10

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 2:
                INIT_SAMPLES = 2
                msg = "WARNING: a minimum number of 2 initial sample(s) must be used for this kernel. Setting minimum to 2."
                self.updateStatusText(msg)
   
            self.sm = Kriging(length_scale=K_LENGTH_SCALE, noise=K_NOISE)
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == 3:
            # Polynomial Regression vars
            # set kernel specific vars
            PR_DEGREE = int(optimizerParams['pr_degree'][0])

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if PR_DEGREE < 1:
                PR_DEGREE = 1
                msg = "WARNING: a polynomial degree must be at least 1. Setting to 1."
                self.updateStatusText(msg)
           
            self.sm = PolynomialRegression(degree=PR_DEGREE)
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == 4:
            # Polynomial Chaos Expansion vars
            # set kernel specific vars
            PC_DEGREE = int(optimizerParams['pc_degree'][0])
            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if PR_DEGREE < 1:
                PR_DEGREE = 1
                msg = "WARNING: a polynomial degree must be at least 1. Setting to 1."
                self.updateStatusText(msg)

            self.sm = PolynomialChaosExpansion(degree=PC_DEGREE)
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == 5:
            # KNN regression vars
            # set kernel specific vars
            KNN_WEIGHTS = optimizerParams['knn_weights'][0]#options: 'uniform', 'distance'
            KNN_N_NEIGHBORS = int(optimizerParams['knn_n_neighbors'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if KNN_N_NEIGHBORS < 1:
                KNN_N_NEIGHBORS = 1
                msg = "WARNING: a minimum number of 1 neighbors must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if KNN_N_NEIGHBORS < INIT_SAMPLES:
                msg = "WARNING: it is suggested that the number of initial samples be equal to the number of neighbors. \n " +\
                    "This is not a fatal error, but the initial predictions may be incorrect or fail to \n " +\
                    "converge until after meeting the number of neighbors + 1"
            if KNN_WEIGHTS in ['uniform', 'distance']:
                pass
            else:
                KNN_WEIGHTS = 'uniform'
                msg = "ERROR: unknown KNN kernel. Defaulting to uniform KNN kernel"
                self.updateStatusText(msg)
           
            self.sm = KNNRegression(n_neighbors=KNN_N_NEIGHBORS, weights=KNN_WEIGHTS)
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == 6:
            # Decision Tree Regression vars
            # set kernel specific vars
            DTR_MAX_DEPTH = int(optimizerParams['dtr_max_depth'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if DTR_MAX_DEPTH < 2:
                DTR_MAX_DEPTH = 2
                msg = "WARNING: the lowest max depth is 2. Setting max depth to 2."
                self.updateStatusText(msg)
          
            self.sm = DecisionTreeRegression(max_depth=DTR_MAX_DEPTH)
            noError, errMsg = self.sm._check_configuration(INIT_SAMPLES)

    
        if noError == False:
            msg = "ERROR in BAYESIAN OPTIMIZATION CONTROLLER. Incorrect surrogate model configuration not recoverable by automated defaults."
            self.updateStatusText(msg)
            self.updateStatusText(errMsg)
            return
        

        # other configuration error correction
        if XI < 0.0:
            XI = 0.01
            msg = "ERROR: xi must be a positive float value (for now). Setting xi to 0.01 as a default"
            self.updateStatusText(msg)
        if NUM_RESTARTS < 2:
            msg = "ERROR: the number of restarts for the surrogate model calculation must be at least 2. \n" + \
                "These restarts do not call the simulation, only a surrogate model calculation. Setting to 2 as a default."
            self.updateStatusText(msg)


        self.best_eval = 9999    # set higher than normal because of the potential for missing the target

        parent = self            # Optional parent class for swarm 
                                            # (Used for passing debug messages or
                                            # other information that will appear 
                                            # in GUI panels)

        self.suppress_output = False    # Suppress the console output of optimizer

        detailedWarnings = False        # Optional boolean for detailed feedback
                                        # (Independent of suppress output. 
                                        #  Includes error messages and warnings)

        self.allow_update = True        # Allow objective call to update state 


        # instantiation of multiglods optimizer 
        self.optimizer = BayesianOptimization(LB, UB, OUT_VARS, TARGETS, E_TOL, MAXIT,
                                                    obj_func=func_F, constr_func=constr_default, 
                                                    init_points=INIT_SAMPLES, 
                                                    xi=XI, n_restarts=NUM_RESTARTS, 
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
 
