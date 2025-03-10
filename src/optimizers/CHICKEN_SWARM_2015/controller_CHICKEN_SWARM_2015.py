##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/GLODS/controller_GLODS.py'
#   Class interfacing with the GLODS optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.CHICKEN_SWARM_2015.chicken_swarm_python.chicken_swarm import swarm
from optimizers.CHICKEN_SWARM_2015.chicken_swarm_python.constr_default import constr_default


class CONTROLLER_CHICKEN_SWARM_2015():
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
        LB = [list(optimizerParams['lower_bounds'][0])]                    # Lower boundaries
        UB = [list(optimizerParams['upper_bounds'][0])]                    # Upper Boundaries
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = int(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
        RN = int(optimizerParams['rooster_number'][0])                     # Target values for output
        HN = int(optimizerParams['hen_number'][0])                         # Variable time-step extinction coefficient
        MN = int(optimizerParams['mother_number'][0])                      # Convergence Tolerance (This is a radius)       
        CN = int(optimizerParams['chick_number'][0])                       # Maximum allowed iterations 
        G = int(optimizerParams['generation'][0])                          # How often to randomize groups. Integer. Num full cycles of chickens
        WMIN = float(optimizerParams['weight_min'][0])                     # Constant float. minimum weight.
        WMAX = float(optimizerParams['weight_max'][0])                     # Constant float. maximum, starting weight
        C = float(optimizerParams['c_factor'][0])                          # Learning factor. Weight of rooster location for current particle sub-group


        NO_OF_PARTICLES = RN + HN + MN + CN       # Number of particles in swarm

        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        self.out_vars = len(TARGETS)

        self.optimizer = swarm(NO_OF_PARTICLES, LB, UB,
                        OUT_VARS, TARGETS,
                        E_TOL, MAXIT, BOUNDARY, 
                        obj_func=func_F, constr_func=constr_default, 
                        RN=RN, HN=HN, MN=MN, CN=CN, G=G,
                        W_min=WMIN, W_max=WMAX, C=C,
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
    
