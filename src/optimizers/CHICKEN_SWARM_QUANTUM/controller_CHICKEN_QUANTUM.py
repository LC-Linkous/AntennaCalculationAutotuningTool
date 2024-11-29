##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/GLODS/controller_GLODS.py'
#   Class interfacing with the GLODS optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: November 27, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.CHICKEN_SWARM_QUANTUM.chicken_swarm_quantum.chicken_swarm import swarm
from optimizers.CHICKEN_SWARM_QUANTUM.chicken_swarm_quantum.constr_default import constr_default


class CONTROLLER_CHICKEN_QUANTUM():
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
        MAXIT = float(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
        RN = int(optimizerParams['rooster_number'][0])                # Target values for output
        HN = int(optimizerParams['hen_number'][0])                  # Variable time-step extinction coefficient
        MN = int(optimizerParams['mother_number'][0])                     # Convergence Tolerance (This is a radius)       
        CN = int(optimizerParams['chick_number'][0])                # Maximum allowed iterations 
        G = int(optimizerParams['generation'][0])
        BETA = float(optimizerParams['beta'][0])                                                                              #              3 = absorbing,   4 = invisible
        QUANTUM_ROOSTERS = optimizerParams['quantum_roosters'][0]                                                                   #              3 = absorbing,   4 = invisible

        NO_OF_PARTICLES = RN + HN + MN + CN       # Number of particles in swarm

        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))


        self.optimizer = swarm(NO_OF_PARTICLES, LB, UB,
                    OUT_VARS, TARGETS,
                    E_TOL, MAXIT, BOUNDARY, 
                    obj_func=func_F, constr_func=constr_default,
                    RN=RN, HN=HN, MN=MN, CN=CN, G=G,
                    beta=BETA, quantum_roosters=QUANTUM_ROOSTERS,
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
#######################################################

    def get_optimized_soln(self):
        return self.optimizer.get_optimized_soln()
    
    def get_optimized_outs(self):
        return self.optimizer.get_optimized_outs()
    
