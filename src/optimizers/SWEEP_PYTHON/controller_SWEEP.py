##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/optimizers/SWEEP_PYTHON/controller_SWEEP.py'
#   Class interfacing with the Sweep search optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: March 19, 2025
##--------------------------------------------------------------------\


import numpy as np
import pandas as pd
from optimizers.SWEEP_PYTHON.sweep_python.sweep import sweep
from optimizers.SWEEP_PYTHON.sweep_python.constr_default import constr_default


class CONTROLLER_SWEEP():
    def __init__(self, parent): 
        self.parent = parent

        # class vars
        self.optimizer = None           # init as a none obj. THIS optimizer 

        self.suppress_output = False    # Suppress the console output
        self.allow_update = True        # Allow objective call to update state 
        self.evaluate_threshold = False # use target or threshold. True = THRESHOLD, False = EXACT TARGET
                                        # default is False

        # Functions for using a surrogate mode with secondary, internal optimizer
        self.useSurrogateModel = False
        self.sm_approx = None     # the surrogate approximator. The kernel
        self.sm_opt = None        # the internal optimizer used to solve the surrogate model.
        self.sm_tol = 10*-6       # default internal optimizer tolerance
        self.sm_maxit = 1000      # default internal optimizer maximum iterations
        self.sm_opt_df = None     # default data frame of params for internal optimizer
        self.out_vars = None      # used to shape surrogate model approx.



####################################################
# GUI interfacing
####################################################

    def debug_message_printout(self, t):
        self.parent.updateStatusText(t)

    def get_export_configuration(self):
        # returns dictionary to parent class
        return self.optimizer.export_configuration()

    def set_import_configuration(self, import_df):
        # passes in dataframe
        return self.optimizer.import_configuration()
    

####################################################
# Toggle allow updates
####################################################

    def setAllowUpdate(self, b):
        self.allow_update = b

    def getAllowUpdate(self):
        return self.allow_update


######################################################
# Check if complete
#######################################################

    def checkOptimizerComplete(self):
        return self.optimizer.complete()


######################################################
# new run setup - base optimizer
#######################################################

    def unpackOptimizerParameters(self, optimizerParams, func_F):
        NO_OF_PARTICLES = int(optimizerParams['num_particles'][0])        # Number of particles in swarm
        self.LB = [list(optimizerParams['lower_bounds'][0])]              # Lower boundaries
        self.UB = [list(optimizerParams['upper_bounds'][0])]              # Upper Boundaries
        self.TARGETS = list(optimizerParams['target_values'][0])          # Target values for output
        TOL = float(optimizerParams['tolerance'][0])                      # Convergence Tolerance      
        MAXIT = int(optimizerParams['max_iterations'][0])                 # Maximum allowed iterations 


        SEARCH = float(optimizerParams['search_selection'][0])             # Sweep/search method
        MIN_RES = [float(optimizerParams['min_res'][0])]                   # min search resolution
        MAX_RES = [float(optimizerParams['max_res'][0])]                   # max search resolution (for adaptive search)


        DECIMALS = int(optimizerParams['numerical_precision'][0])
        THRESHOLD = list(optimizerParams['target_threshold'][0])          # Threshold symbols ["=", "≤", "≥"]

        self.useSurrogateModel = optimizerParams['use_surrogate_bool'][0]   # UPDATE THIS IN THE UI. The model is set up from an external call, (where the swarm obj is created)
        self.out_vars = len(self.TARGETS)
        #convert threshold from symbolics to ints:
        threshold_dict = {"=": 0, "≤": 1, "<": 1, "≥": 2, ">":2}
        self.THRESHOLD = np.array([threshold_dict.get(x, x) for x in THRESHOLD])

        # ERROR CHECK THRESHOLD
        # threshold is same dims as TARGETS
        # 0 = use target value as actual target. value should EQUAL target
        # 1 = use as threshold. value should be LESS THAN OR EQUAL to target
        # 2 = use as threshold. value should be GREATER THAN OR EQUAL to target

        if not np.any(self.THRESHOLD): # ALL TARGET values are to be evaluated at EXACTLY the target val
            self.evaluate_threshold = False
        else: #Evaulate at least one value in the TARGET list as a THRESHOLD
            self.evaluate_threshold = True 

        # ERROR SWEEP SURROGATE MODEL
        ## SWEEP is the base optimizer. It can have an internal optimizer solving a surrogate model approximation.
        if self.useSurrogateModel == True: # user has set this on menu to use surrogate model
            #if (self.sm_approx == None) or (self.sm_opt == None):    # surrogate model and internal optimizer not setup properly
            msg = "WARNING: SWEEP optimizer cannot currently be used with an internal optimizer."
            self.debug_message_printout(msg)
            self.useSurrogateModel = False


        # SETUP THE MAIN OPTIMIZER
        # Constant variables
        opt_params = {'NO_OF_PARTICLES': [NO_OF_PARTICLES],     # Number of indpendent agents searching the space
                    'SEARCH_METHOD': [SEARCH],                  # int search 1 = basic_grid, 2 = random_search
                    'MIN_RES': [MIN_RES],                       # min resolution for search
                    'MAX_RES': [MAX_RES]}                       # max resolution for search
            

        opt_df = pd.DataFrame(opt_params)
        self.optimizer = sweep(self.LB, self.UB, self.TARGETS, TOL, MAXIT,
                                obj_func=func_F, constr_func=constr_default,  
                                opt_df=opt_df,
                                parent=self,
                                evaluate_threshold=self.evaluate_threshold, 
                                obj_threshold=self.THRESHOLD, 
                                useSurrogateModel=self.useSurrogateModel, 
                                surrogateOptimizer=self.sm_opt,
                                decimal_limit=DECIMALS)        
    
        msg = "optimizer configured"
        self.debug_message_printout(msg)

        # returns for the controller integrator and initial setup for the optimization process
        targetMetrics = optimizerParams['target_metrics'] #this is the NAME of the TARGET value for pattern matching a few levels up
        F = np.zeros((np.prod(np.shape(self.TARGETS)), 1)) # set the initial F evaluation to an array of ZEROs. 

        msg = "initial values set"
        self.debug_message_printout(msg)

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
# SURROGATE MODEL APPROXIMATOR FUNCS
######################################################

    def fit_model(self, x, y):
        # call out to parent class to use surrogate model
        self.sm_approx.fit(x,y)
        

    def model_predict(self, x, output_size=None):
        # call out to parent class to use surrogate model
        #'mean' is regressive definition. not statistical
        #'variance' only applies for some surrogate models

        if output_size == None:
            output_size = self.out_vars

        mean, noErrors = self.sm_approx.predict(x, output_size)
        return mean, noErrors


    def model_get_variance(self):
        variance = self.sm_approx.calculate_variance()
        return variance



######################################################
# SURROGATE MODEL SOLVED WITH INTERNAL OPTIMIZER 
#
#
#   NOTE: the PARENT OPTIMIZER (the BASE OPTIMIZER) will always be the one that is called
#       for the surrogate model creation. If PSO_BASIC is used with a CAT_SWARM model,
#       then the functions below for PSO_BASIC will be used for the surrogate model 
#       driver and solver 
#
#
#
#
######################################################

    
    def fit_and_create_surogate(self, opt_M, opt_F_Pb,surrogateOptimizer):
        # opt_M : 'base' optimizer particle locs
        # opt_F_Pb: 'base' optimizer personal best fitness
        # surrogateOptimizer : the surrogate optimizer class obj. 
    
        #called at the controller level so that the params don't 
        # get passed down and then used at this level anyways

        # fit surrogate model using current particle positions
        # this model needs to be fit to create something that can then be modeled
        self.fit_model(opt_M, opt_F_Pb)

        # define objective function pass through via parent 
        func_f = self.model_predict   

        # use the default constraint function. these can be customized later
        constr_F = constr_default

        # to make models modular & not deal with 
        # re-converting values or storing duplicates, the surrogate optimizer
        # is set up here. 

        setup_sm_opt = surrogateOptimizer(self.LB, self.UB, self.TARGETS, self.sm_tol, self.sm_maxit,  
                                            obj_func=func_f, constr_func=constr_F, 
                                            opt_df=self.sm_opt_df, 
                                            parent=self,
                                            evaluate_threshold=self.evaluate_threshold, 
                                            obj_threshold=self.THRESHOLD, 
                                            useSurrogateModel=False, # IS SURROGATE MODEL
                                            surrogateOptimizer=None)  # Do NOT put surrogate model INTO this optimizer
                
                

        return setup_sm_opt

    
    def create_internal_optimizer(self, optimizerParams):
        # this is SEPERATE from the main optimizer creation to ensure that there's no crossover right now
        # this can be streamlined in the next release after the surrogate modeling features are more developed


        NO_OF_PARTICLES = int(optimizerParams['sm_num_particles'][0])         # Number of particles in swarm
        SEARCH = float(optimizerParams['sm_search_selection'][0])             # Sweep/search method
        MIN_RES = [float(optimizerParams['sm_min_res'][0])]                   # min search resolution
        MAX_RES = [float(optimizerParams['sm_max_res'][0])]                   # max search resolution (for adaptive search)

        INIT_SAMPLES = int(optimizerParams['sm_init_samples'][0])
        SURROGATE_MODEL = int(optimizerParams['sm_model_name'][0]) # integer representation of surrogate model (for later variations)
                                                                        #0 = RBF network, 1 = Gaussian process, 2 = Kriging
                                                                        #3 = Polynomial regression, 4 = polynomial chaos expansion,
                                                                        #5 = KNN regression, 6 = Decision Tree Regression
        

        # inbuilt error checking and surrogate model approximation selection/config
        sm_approx, noError, errMsg = self.parent.check_model_approximator(SURROGATE_MODEL, INIT_SAMPLES, optimizerParams, is_internal_optimizer=True)
        if noError == False:
            msg = "ERROR in CAT_QUANTUM OPTIMIZATION CONTROLLER. Incorrect surrogate model configuration not recoverable by automated defaults."
            self.debug_message_printout(msg)
            self.debug_message_printout(errMsg)
            return
        


        # SETUP THE MAIN OPTIMIZER
        # Constant variables
        opt_params = {'NO_OF_PARTICLES': [NO_OF_PARTICLES],     # Number of indpendent agents searching the space
                    'SEARCH_METHOD': [SEARCH],                  # int search 1 = basic_grid, 2 = random_search
                    'MIN_RES': [MIN_RES],                       # min resolution for search
                    'MAX_RES': [MAX_RES]}                       # max resolution for search
            

        opt_df = pd.DataFrame(opt_params)
        sm_optimizer = sweep
        
        return sm_approx, opt_df, sm_optimizer #sm_approx is the kernel approximator model
