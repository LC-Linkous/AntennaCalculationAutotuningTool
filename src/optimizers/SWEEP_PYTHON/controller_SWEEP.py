##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/SWEEP_PYTHON/controller_SWEEP.py'
#   Class interfacing with the Sweep search optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.SWEEP_PYTHON.sweep_python.sweep import sweep
from optimizers.SWEEP_PYTHON.sweep_python.constr_default import constr_default


class CONTROLLER_SWEEP():
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

    def unpackOptimizerParameters(self, optimizerParams, func_F, internalOptimizerParams=None):
        NO_OF_PARTICLES = int(optimizerParams['num_particles'][0])         # Number of particles in swarm
        LB = [list(optimizerParams['lower_bounds'][0])]                    # Lower boundaries
        UB = [list(optimizerParams['upper_bounds'][0])]                    # Upper Boundaries
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = float(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        SEARCH = float(optimizerParams['search_selection'][0])             # Sweep/search method
        MIN_RES = [float(optimizerParams['min_res'][0])]                     # min search resolution
        MAX_RES = [float(optimizerParams['max_res'][0])]                     # max search resolution (for adaptive search)


        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        # class vars
        self.out_vars = len(TARGETS)

      
        # OPTIMIZER INIT
        self.best_eval = 1      #usually set to 1 because anything higher is too many magnitutes to high to be useful
                                    #when collecting data, setting a max of 5 is useful

        self.suppress_output = True   # Suppress the console output of particle swarm

        self.allow_update = True      # Allow objective call to update state 



        self.optimizer = sweep(NO_OF_PARTICLES, LB, UB,
                        OUT_VARS, TARGETS,
                        E_TOL, MAXIT,
                        obj_func=func_F, constr_func=constr_default,  
                        search_method=SEARCH, min_res=MIN_RES, max_res=MAX_RES,
                        parent=self, detailedWarnings=False)
         
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
    
