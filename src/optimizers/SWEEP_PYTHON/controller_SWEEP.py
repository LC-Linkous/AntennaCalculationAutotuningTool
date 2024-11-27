##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/GLODS/controller_GLODS.py'
#   Class interfacing with the GLODS optimizer
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
        return self.multiGLODS.complete()


######################################################
# new run setup
#######################################################

    def unpackOptimizerParameters(self, optimizerParams, func_F):
        print("controller_GLODS unpack optimizer parameters")

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
        BP = float(optimizerParams['beta'][0])                 # Beta Par
        print("BP")
        print(BP)
        GP = float(optimizerParams['gamma'][0])                # Gamma Par
        print("GP")
        print(GP)        
        SF = float(optimizerParams['search_frequency'][0])     # Search Frequency
        print("SF")
        print(SF)        
        TARGETS = list(optimizerParams['target_values'][0])    # Target values for output
        print("TARGETS")
        print(TARGETS)       
        MAXIT = float(optimizerParams['max_iterations'][0])    # Maximum allowed iterations 
        print("MAXIT")
        print(MAXIT)

        targetMetrics = optimizerParams['target_metrics']
        F = np.zeros((np.prod(np.shape(TARGETS)), 1))


        # instantiation of multiglods optimizer 
        self.multiGLODS = multi_glods(NO_OF_VARS, LB, UB, 
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
        self.multiGLODS.step(self.suppress_output)
        print(self.multiGLODS.ctl['Flist'])

    def callObjective(self):
        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        self.multiGLODS.call_objective(self.allow_update)

    def get_convergence_data(self):
        return self.multiGLODS.get_convergence_data()

######################################################
# Optimizer End
#######################################################

    def get_optimized_soln(self):
        return self.multiGLODS.get_optimized_soln()
    
    def get_optimized_outs(self):
        return self.multiGLODS.get_optimized_outs()
    
