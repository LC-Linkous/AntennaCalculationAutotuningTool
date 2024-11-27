#! /usr/bin/python3

##--------------------------------------------------------------------\
#   sweep_python
#   './sweep_python/src/main_test_details.py'
#   Test function/example for using the 'sweep' class in sweep.py.
#   Format updates are for integration in the AntennaCAT GUI.
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 19, 2024
##--------------------------------------------------------------------\


import numpy as np
import time
from sweep import sweep

# OBJECTIVE FUNCTION SELECTION
import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
#import lundquist_3_var.configs_F as func_configs     # multi objective function


class TestDetails():
    def __init__(self):
        # Constant variables
        NO_OF_PARTICLES = 4             # Number of indpendent agents searching the space
        MIN_RES = [[0.01, 0.02, 0.01]]  # Minimum resolution for search
        MAX_RES = [[0.01, 0.02, 0.01]]  # Maximum resolution for search
        E_TOL = 10 ** -6                # Convergence Tolerance
        MAXIT = 10000                   # Maximum allowed iterations
        SEARCH_METHOD = 2               # int search 1 = basic_grid, 2 = random_search

        # Objective function dependent variables
        LB = func_configs.LB                    # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB                    # Upper boundaries, [[1, 1, 0.5]]
        IN_VARS = func_configs.IN_VARS          # Number of input variables (x-values)   
        OUT_VARS = func_configs.OUT_VARS        # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS          # Target values for output

        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function


        
        # Swarm vars
        self.best_eval = 9999         # set higher than normal because of the potential for missing the target

        parent = self                 # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        self.suppress_output = False   # Suppress the console output of particle swarm

        detailedWarnings = False        # Optional boolean for detailed feedback
                                        # (Independent of suppress output. 
                                        #  Includes error messages and warnings)

        self.allow_update = True      # Allow objective call to update state 



        self.mySweep = sweep(NO_OF_PARTICLES,LB, UB, MIN_RES, MAX_RES, 
                        OUT_VARS, TARGETS, E_TOL, MAXIT,
                        SEARCH_METHOD, func_F, constr_F, parent, detailedWarnings)  



    def debug_message_printout(self, txt):
        if txt is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(txt)
        print(msg)


    def record_params(self):
        # this function is called from particle_swarm.py to trigger a write to a log file
        # running in the AntennaCAT GUI to record the parameter iteration that caused an error
        pass
         

    def run(self):

        # instantiation of particle swarm optimizer 
        while not self.mySweep.complete():

            # step through optimizer processing
            self.mySweep.step(self.suppress_output)

            # call the objective function, control 
            # when it is allowed to update and return 
            # control to optimizer
            self.mySweep.call_objective(self.allow_update)
            iter, eval = self.mySweep.get_convergence_data()
            if (eval < self.best_eval) and (eval != 0):
                self.best_eval = eval
            if self.suppress_output:
                if iter%100 ==0: #print out every 100th iteration update
                    print("Iteration")
                    print(iter)
                    print("Best Eval")
                    print(self.best_eval)

        print("Optimized Solution")
        print(self.mySweep.get_optimized_soln())
        print("Optimized Outputs")
        print(self.mySweep.get_optimized_outs())



if __name__ == "__main__":
    td = TestDetails()
    td.run()
