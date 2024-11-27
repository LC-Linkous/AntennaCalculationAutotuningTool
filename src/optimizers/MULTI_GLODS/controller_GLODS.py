##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/GLODS/controller_GLODS.py'
#   Class interfacing with the GLODS optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.MULTI_GLODS.multi_glods_python.multi_glods import multi_glods
from optimizers.MULTI_GLODS.multi_glods_python.constr_default import constr_default



class CONTROLLER_GLODS():
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
        print("controller_GLODS unpack optimizer parameters")

        NO_OF_VARS = float(optimizerParams['num_input'][0])    # Number of input variables (x-values)
        TOL = float(optimizerParams['tolerance'][0])           # Convergence Tolerance (This is a radius 
                                                               # based tolerance, not target based tolerance)
        LB = list(optimizerParams['lower_bounds'][0])          # Lower boundaries
        UB = list(optimizerParams['upper_bounds'][0])          # Upper Boundaries
        BP = float(optimizerParams['beta'][0])                 # Beta Par
        GP = float(optimizerParams['gamma'][0])                # Gamma Par
        SF = float(optimizerParams['search_frequency'][0])     # Search Frequency
        TARGETS = list(optimizerParams['target_values'][0])    # Target values for output
        MAXIT = float(optimizerParams['max_iterations'][0])    # Maximum allowed iterations 
        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        self.out_vars = len(TARGETS)


        # instantiation of multiglods optimizer 
        self.optimizer = multi_glods(NO_OF_VARS, LB, UB, 
                                      TARGETS, TOL, MAXIT,
                                      func_F=func_F, constr_func=constr_default, 
                                      BP=BP, GP=GP, SF=SF,
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
    
