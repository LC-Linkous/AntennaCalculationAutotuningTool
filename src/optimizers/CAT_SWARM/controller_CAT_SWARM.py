##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/CAT_SWARM/controller_CAT_SWARM.py'
#   Class interfacing with the cat swarm optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.CAT_SWARM.cat_swarm_python.cat_swarm import swarm
from optimizers.CAT_SWARM.cat_swarm_python.constr_default import constr_default


class CONTROLLER_CAT_SWARM():
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
        WEIGHTS = [float(optimizerParams['weights'][0])]                    # Update vector weights
        VLIM = float(optimizerParams['velocity_limit'][0])                 # Initial velocity limit
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = int(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
                                                                           #              3 = absorbing,   4 = invisible

        # cat swarm specific
        MR = float(optimizerParams['mixture_ratio'][0])                    # Mixture Ratio (MR). Small value for tracing population %.
        SMP = int(optimizerParams['seeking_pool'][0])                      # Seeking memory pool. Num copies of cats made.
        SRD = float(optimizerParams['seeking_range'][0])                   # Seeking range of the selected dimension. 
        CDC = int(optimizerParams['mutation_dim'][0])                      # Counts of dimension to change. mutation.
        SPC = bool(optimizerParams['self_position'][0])                    # self-position consideration. boolean.          
           
        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))

        self.out_vars = len(TARGETS)

        self.optimizer = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, VLIM, OUT_VARS, TARGETS,
                        E_TOL, MAXIT, BOUNDARY, 
                        obj_func=func_F, constr_func=constr_default,
                        MR=MR, SMP=SMP, SRD=SRD, CDC=CDC, SPC=SPC,
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
    
