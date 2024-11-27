##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/CAT_SWARM_QUANTUM/controller_CAT_QUANTUM.py'
#   Class interfacing with the cat_swarm_quantum optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: July 06, 2024
##--------------------------------------------------------------------\


import numpy as np
from optimizers.CAT_SWARM_QUANTUM.cat_swarm_quantum.cat_swarm import swarm
from optimizers.CAT_SWARM_QUANTUM.cat_swarm_quantum.constr_default import constr_default


class CONTROLLER_CAT_SWARM_QUANTUM():
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
        print("controller_CAT_QUANTUM unpack optimizer parameters")

        NO_OF_PARTICLES = int(optimizerParams['num_particles'][0])         # Number of particles in swarm
        LB = [list(optimizerParams['lower_bounds'][0])]                    # Lower boundaries
        UB = [list(optimizerParams['upper_bounds'][0])]                    # Upper Boundaries
        WEIGHTS = [list(optimizerParams['weights'][0])]                    # Update vector weights
        VLIM = float(optimizerParams['velocity_limit'][0])                 # Initial velocity limit
        OUT_VARS = int(optimizerParams['num_output'][0])                   # Number of output variables
        TARGETS = list(optimizerParams['target_values'][0])                # Target values for output
        T_MOD = float(optimizerParams['time_modulus'][0])                  # Variable time-step extinction coefficient
        E_TOL = float(optimizerParams['tolerance'][0])                     # Convergence Tolerance (This is a radius)       
        MAXIT = float(optimizerParams['max_iterations'][0])                # Maximum allowed iterations 
        BOUNDARY = int(optimizerParams['boundary'][0])                     # int boundary 1 = random,      2 = reflecting
                                                                           #              3 = absorbing,   4 = invisible

        # cat swarm specific
        MR = .02                    # Mixture Ratio (MR). Small value for tracing population %.
        SMP = 5                     # Seeking memory pool. Num copies of cats made.
        SRD = .45                   # Seeking range of the selected dimension. 
        CDC = 2                     # Counts of dimension to change. mutation.
        SPC = True                  # self-position consideration. boolean.

        # quantum swarm variables
        BETA = 0.5                  #Float constant controlling influence 
                                        #between the personal and global best positions


        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))
        

        self.optimizer = swarm(NO_OF_PARTICLES, LB, UB,
                        WEIGHTS, OUT_VARS, TARGETS,
                        E_TOL, MAXIT, BOUNDARY,
                        func_F=func_F, constr_func=constr_default,
                        MR=MR, SMP=SMP, SRD=SRD, CDC=CDC, SPC=SPC,
                        beta=BETA, input_size=len(LB), 
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
    
