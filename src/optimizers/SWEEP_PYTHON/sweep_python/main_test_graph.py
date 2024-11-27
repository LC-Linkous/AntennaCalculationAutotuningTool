#! /usr/bin/python3

##--------------------------------------------------------------------\
#   sweep_python
#   './sweep_python/src/main_test_graph.py'
#   Test function/example for using the 'sweep' class in sweep.py.
#   Format updates are for integration in the AntennaCAT GUI.
#   This version builds from 'test_details.py' to include a 
#       matplotlib plot of particle location
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 26, 2024
##--------------------------------------------------------------------\


import numpy as np
import time
import matplotlib.pyplot as plt
from sweep import sweep

# OBJECTIVE FUNCTION SELECTION
import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
#import lundquist_3_var.configs_F as func_configs     # multi objective function





class TestGraph():
    def __init__(self):
        self.ctr = 0

        NO_OF_PARTICLES = 4             # Number of indpendent agents searching the space
        E_TOL = 10 ** -2                # Convergence Tolerance
        MAXIT = 10000                   # Maximum allowed iterations
        SEARCH_METHOD = 1               # int search 1 = basic_grid, 2 = random_search

        #NOTE: resolution should match the LB and UB formats. If it is
        # a higher dimensionality, ALL combinations of that non-applicable
        # dimensionality will be searched
        # MIN_RES = [[0.01, 0.02, 0.01]]  # Minimum resolution for search
        # MAX_RES = [[0.01, 0.02, 0.01]]  # Maximum resolution for search
        MIN_RES = [[0.03]]  # Minimum resolution for search
        MAX_RES = [[0.03]]  # Maximum resolution for search


        # Objective function dependent variables
        LB = func_configs.LB                    # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB                    # Upper boundaries, [[1, 1, 0.5]]
        IN_VARS = func_configs.IN_VARS          # Number of input variables (x-values)   
        OUT_VARS = func_configs.OUT_VARS        # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS          # Target values for output

        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function


        self.best_eval = 9999         # set higher than normal because of the potential for missing the target


        parent = None           # Optional parent class for swarm 
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        self.suppress_output = False   # Suppress the console output for updates

        self.allow_update = True      # Allow objective call to update state 
                                      # (can be set on each iteration)

        detailedWarnings = False      # Optional boolean for detailed feedback


        self.mySweep = sweep(NO_OF_PARTICLES,LB, UB, MIN_RES, MAX_RES, 
                        OUT_VARS, TARGETS, E_TOL, MAXIT,
                        SEARCH_METHOD, func_F, constr_F, parent, detailedWarnings)  
            


        # Matplotlib setup

        ## Standard search area and distance of solution to target plot
        self.targets = TARGETS
        self.fig = plt.figure(figsize=(10, 5))#(figsize=(14, 7))
        ### position
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax1.set_title("Particle Location, Iteration: " +str(self.ctr))
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('Y')
        self.ax1.set_zlabel('Z')
        self.scatter1 = None
        ### fitness
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        self.ax2.set_title("Fitness Relation to Target")
        self.ax2.set_xlabel('X')
        self.ax2.set_ylabel('Y')
        self.ax2.set_zlabel('Z')
        self.scatter2 = None


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
         

    def update_plot(self, x_coords, y_coords, targets, showTarget=True, clearAx=True):
        
        # check if any points. first call might not have anythign set yet.
        if len(x_coords) < 1:
            return 


        if clearAx == True:
            self.ax1.clear() #use this to git rid of the 'ant tunnel' trails
            self.ax2.clear()

        # MOVEMENT PLOT
        if np.shape(x_coords)[1]==1: # 1 dim function
            x_plot_coords = np.array(x_coords[:,0])*0.0
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("filler coords")
            self.scatter = self.ax1.scatter(x_coords, x_plot_coords, edgecolors='b')   
        
        elif np.shape(x_coords)[1] == 2: #2-dim func
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], edgecolors='b')

        elif np.shape(x_coords)[1] == 3: #3-dim func
            self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("$x_3$")
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], x_coords[:,2], edgecolors='b')


        # FITNESS PLOT
        if np.shape(y_coords)[1] == 1: #1-dim obj func
            y_plot_filler = np.array(y_coords[:,0])*0.0
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x,y)$")
            self.ax2.set_ylabel("filler coords")
            self.scatter = self.ax2.scatter(y_coords, y_plot_filler,  marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 2: #2-dim obj func
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x,y)$")
            self.ax2.set_ylabel("$F_{2}(x,y)$")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 3: #3-dim obj fun
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x,y)$")
            self.ax2.set_ylabel("$F_{2}(x,y)$")
            self.ax2.set_zlabel("$F_{3}(x,y)$")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], y_coords[:,2], marker='o', s=40, facecolor="none", edgecolors="k")


        if showTarget == True: # plot the target point
            if len(targets) == 1:
                self.scatter = self.ax2.scatter(targets[0], 0, marker='*', edgecolors='r')
            if len(targets) == 2:
                self.scatter = self.ax2.scatter(targets[0], targets[1], marker='*', edgecolors='r')
            elif len(targets) == 3:
                self.scatter = self.ax2.scatter(targets[0], targets[1], targets[2], marker='*', edgecolors='r')


        plt.pause(0.0001)  # Pause to update the plot
        if self.ctr == 0:
            time.sleep(2)
            
        self.ctr = self.ctr + 1


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
            m_coords = self.mySweep.M  #get x,y,z coordinate locations
            f_coords = self.mySweep.F_Gb # global best of set
            self.update_plot(m_coords, f_coords, self.targets, showTarget=True, clearAx=False) #update matplot

        print("Optimized Solution")
        print(self.mySweep.get_optimized_soln())
        print("Optimized Outputs")
        print(self.mySweep.get_optimized_outs())


if __name__ == "__main__":
    tg = TestGraph()
    tg.run()
