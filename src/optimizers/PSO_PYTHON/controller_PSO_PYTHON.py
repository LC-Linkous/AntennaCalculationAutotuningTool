##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/opimizers/PSO1/controller_PSO1.py'
#   Main class for managing the optimizer hooks
#   Scripts are NOT written or read to file in this class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import numpy as np
# OPTIMIZER IMPORTS
from optimizers.PSO_PYTHON.pso_python.particle_swarm import swarm
from optimizers.PSO_PYTHON.pso_python.constr_default import constr_default


class CONTROLLER_PSO_PYTHON():
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
        NO_OF_PARTICLES = int(optimizerParams['num_particles'][0])         # Number of particles in swarm
        LB = [list(optimizerParams['lower_bounds'][0])]                    # Lower boundaries
        UB = [list(optimizerParams['upper_bounds'][0])]                    # Upper Boundaries
        WEIGHTS = [list(map(float, optimizerParams['weights'][0]))]        # Update vector weights
        VLIM = float(optimizerParams['velocity_limit'][0])                 # Initial velocity limit
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        T_MOD = float(optimizerParams['time_modulus'][0])                  # Variable time-step extinction coefficient
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = float(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
                                                                           #              3 = absorbing,   4 = invisible

        # set for data processing
        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

       
        # instantiation of optimizer vars
        self.out_vars = len(TARGETS)
        
        self.optimizer = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, VLIM, OUT_VARS, TARGETS,
                        T_MOD, E_TOL, MAXIT, BOUNDARY,
                        obj_func=func_F, constr_func=constr_default,  
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
#######################################################

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
    
