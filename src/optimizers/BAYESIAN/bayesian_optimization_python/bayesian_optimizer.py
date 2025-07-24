#! /usr/bin/python3

##--------------------------------------------------------------------\
#   bayesian_optimization_python
#   './bayesian_optimization_python/src/bayesian_optimizer.py'
#   
#   Class for bayesian optimizer. Controlled by a driving test class as
#   a parent, which also passes arguments to the surrogate model.
#      
#
#   Author(s): Lauren Linkous
#   Last update: July 23, 2025
##--------------------------------------------------------------------\


import numpy as np
import time
from numpy.random import Generator, MT19937
import sys


class BayesianOptimization:
    # arguments should take form: 
    # optimizer([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj, 
    # bool, [int, int, ...], 
    # int) 
    #  
    # opt_df contains class-specific tuning parameters
    # NO_OF_PARTICLES: int
    # weights: [[float, float, float]]
    # boundary: int. 1 = random, 2 = reflecting, 3 = absorbing,   4 = invisible
    # vlimit: float
    # 
   
    def __init__(self, lbound, ubound, targets,E_TOL, maxit,
                 obj_func, constr_func, 
                 opt_df,
                 parent=None, 
                 evaluate_threshold=False, obj_threshold=None,
                 useSurrogateModel=False,  # This optimizer cannot use an internal optimizer
                 surrogateOptimizer=None, # used for format streamlining
                 decimal_limit = 4): # set precision

        
        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 

        self.number_decimals = int(decimal_limit)  # limit the number of decimals
                                              # used in cases where real life has limitations on resolution


        #evaluation method for targets
        # True: Evaluate as true targets
        # False: Evaluate as thesholds based on information in obj_threshold
        if evaluate_threshold==False:
            self.evaluate_threshold = False
            self.obj_threshold = None

        else:
            if not(len(obj_threshold) == len(targets)):
                self.debug_message_printout("WARNING: THRESHOLD option selected.  +\
                Dimensions for THRESHOLD do not match TARGET array. Defaulting to TARGET search.")
                self.evaluate_threshold = False
                self.obj_threshold = None
            else:
                self.evaluate_threshold = evaluate_threshold #bool
                self.obj_threshold = np.array(obj_threshold).reshape(-1, 1) #np.array





        #unpack the opt_df standardized vals
        init_points = int(opt_df['INIT_PTS'][0])
        n_restarts = int(opt_df['NUM_RESTARTS'][0])
        xi = float(opt_df['XI'][0])
        self.sm = opt_df['SM_MODEL'][0] #No force type, this is a class object
        

        # problem height and width
        heightl = np.shape(lbound)[0]
        widthl = np.shape(lbound)[1]
        heightu = np.shape(ubound)[0]
        widthu = np.shape(ubound)[1]

        # extract from array
        lbound = np.array(lbound[0])
        ubound = np.array(ubound[0])

        self.rng = Generator(MT19937())

        if ((heightl > 1) and (widthl > 1)) \
           or ((heightu > 1) and (widthu > 1)) \
           or (heightu != heightl) \
           or (widthl != widthu):
            
            if self.parent == None:
                pass
            else:
                self.parent.record_params()
                self.parent.debug_message_printout("ERROR: lbound and ubound must be 1xN-dimensional \
                                                        arrays  with the same length")
           
        else:

            
            if heightl == 1:
                lbound = lbound
        
            if heightu == 1:
                ubound = ubound

            self.lbound = lbound
            self.ubound = ubound


            '''
            self.M                      : An array of current X sample locations. 
            self.output_size            : An integer value for the output size of obj func
            self.Gb                     : Global best position, initialized with a large value.
            self.F_Gb                   : Fitness value corresponding to the global best position.
            self.F_Pb                   : Fitness value corresponding to the personal best position for each sample. Y sample locations. 
            self.targets                : Target values for the optimization process.
            self.maxit                  : Maximum number of iterations.
            self.E_TOL                  : Error tolerance.
            self.obj_func               : Objective function to be optimized.      
            self.constr_func            : Constraint function. Not used because of how points are generated.  
            self.iter                   : Current iteration count.
            self.allow_update           : Flag indicating whether to allow updates.
            self.Flist                  : List to store fitness values.
            self.Fvals                  : List to store fitness values.
            self.init_points            : Integer. Number of initial points before optimization.
            self.xi                     : Float. Encourages exploration in expected improvement.
            self.n_restarts             : Integer. Number of randomly genreated proposed sample candiates. 
            self.new_point              : Newest proposed/passed in point.
            '''

            self.M = [] #set below
            self.output_size = len(targets)
            self.Gb = sys.maxsize*np.ones((1,np.max([heightl, widthl])))   
            self.F_Gb = sys.maxsize*np.ones((1,self.output_size))
            self.F_Pb = []  #set below
            self.targets = np.array(targets).reshape(-1, 1)         
            self.maxit = maxit                       
            self.E_TOL = E_TOL
            self.obj_func = obj_func                                             
            self.constr_func = constr_func   
            self.iter = 0
            self.allow_update = 0                                           
            self.Flist = []                                                 
            self.Fvals = []
            self.init_points = init_points    
            self.xi = xi
            self.n_restarts = n_restarts
            self.new_point = []
    

            # state machine control flow
            self.firstOptimizationRun = False
            self.doneInitializationBoolean = False
            self.ctr  = 0
            self.objective_function_case = 0 #initial pts by default
        

    def call_objective(self, allow_update=False):

       # may have re-run in an upstream optimizer
        # so this may be triggered when the point should not be sampled
        if allow_update == False:
            self.allow_update = 0
            return
        else:        
            self.allow_update = 1

        # these cases are different for the error messages, and some features in development for prediction. This couls be streamlined

        # case 0: first point of initial points (must have minimum 1)
        if self.objective_function_case == 0:
            new_M = np.round(self.rng.uniform(self.lbound.reshape(1,-1)[0], self.ubound.reshape(1,-1)[0], (1, len(self.ubound))).reshape(1,len(self.ubound)), self.number_decimals)
            newFVals, noError = self.obj_func(new_M[0], self.output_size)  # Cumulative Fvals

            if noError == True:
                self.Fvals = np.array([newFVals]).reshape(-1, 1) 
                self.M = new_M
                self.F_Pb = newFVals
            else:
                msg = "ERROR: initial point creation issue"
                self.debug_message_printout(msg)

            self.is_fitted = False

        # case 1: any other initial points before optimiation begins
        elif self.objective_function_case == 1:
            new_M = np.round(self.rng.uniform(self.lbound.reshape(1,-1)[0], self.ubound.reshape(1,-1)[0], (1, len(self.ubound))).reshape(1,len(self.ubound)), self.number_decimals)
            newFVals, noError = self.obj_func(new_M[0], self.output_size) 
            if noError == True:
                self.Fvals = np.array([newFVals]).reshape(-1, 1) 
                self.M = np.vstack([self.M, new_M])
                self.F_Pb = np.vstack((self.F_Pb, newFVals))#.reshape(-1, 1) 

            else:
                msg = "ERROR: objective function error when initilaizing random points"
                self.debug_message_printout(msg)

            self.is_fitted = False

        # case 2: normal objective function calls, optimization running live
        elif self.objective_function_case == 2:
            if len(self.new_point) < 1: # point not set
                msg = "WARNING: no point set for objective call. Skipping. Ignore unless this is persistent."
                self.debug_message_printout(msg)
                return

            newFVals, noError = self.obj_func(self.new_point[0], self.output_size)
            if noError==True:
                self.Fvals = np.array([newFVals]).reshape(-1, 1) 
                #self.Flist = abs(self.targets - self.Fvals)
                # EVALUATE OBJECTIVE FUNCTION - TARGET OR THRESHOLD
                # this evaluation happens here because there's enough points 
                # to actually build and evaluate the surrogate model approximation
                self.Flist = self.objective_function_evaluation(self.Fvals, self.targets)# abs(self.targets - self.Fvals)
                self.M = np.vstack((self.M, self.new_point))
                self.F_Pb = np.vstack((self.F_Pb, newFVals))#.reshape(-1, 1) 
                self.fit_model(self.M, self.F_Pb)

        else:
            msg = "ERROR: in call objective objective function evaluation"
            self.debug_message_printout(msg)


        self.iter = self.iter + 1


    def objective_function_evaluation(self, Fvals, targets):
        #pass in the Fvals & targets so that it's easier to track bugs

        # this uses the fitness values and target (or threshold) to determine the Flist values
        # Option #1: TARGET
        # get DISTANCE FROM TARGET
        # Option #2: THRESHOLD
        # use THRESHOLD TO DETERMINE INTEREST
        # if threshold is met, the distance is set to a small value (epsilon).
        #  Setting the 'distance' to epsilon, the convergence value check can
        # also remain the same format. 


        # testing different values of epsilon
        epsilon = np.finfo(float).eps #smallest system constant
        # Ex: 2.220446049250313e-16  
        # #may be greater than tolerance if tolerance is set very low for testing
        #epsilon = 10**-18
        #epsilon = 0  # causes issues with imag. numbers

        Flist = np.zeros_like(Fvals)

        if self.evaluate_threshold == True: #THRESHOLD
            ctr = 0
            for i in targets:
                o_thres = int(self.obj_threshold[ctr]) #force type as err check
                t = targets[ctr]
                fv = Fvals[ctr]

                if o_thres == 0: #TARGET. default
                    # sets Flist[ctr] as abs distance of  Fvals[ctr] from target
                    Flist[ctr] = abs(t - fv)

                elif o_thres == 1: #LESS THAN OR EQUAL 
                    # checks if the Fvals[ctr] is LESS THAN OR EQUAL to target
                    # if yes, then distance is 0 (considered 'on target)
                    # if no, then Flist is abs distance of  Fvals[ctr] from target
                    if fv <= t:
                        Flist[ctr] = epsilon
                    else:
                        Flist[ctr] = abs(t - fv)

                elif o_thres == 2: #GREATER THAN OR EQUAL
                    # checks if the Fvals[ctr] is GREATER THAN OR EQUAL to target
                    # if yes, then distance is 0 (considered 'on target)
                    # if no, then Flist is abs distance of  Fvals[ctr] from target
                    if fv >= t:
                        Flist[ctr] = epsilon
                    else:
                        Flist[ctr] = abs(t - fv)

                else: #o_thres == 0. #TARGET. default
                    self.parent.debug_message_printout("ERROR: unrecognized threshold value. Evaluating as TARGET")
                    Flist[ctr] = abs(t - fv)



                ctr = ctr + 1

        else: #TARGET as default
            # arrays are already the same dimensions. 
            # no need to loop and compare to anything
            Flist = abs(targets - Fvals)

        return Flist
        
    # SURROGATE MODEL FUNCS
    # testing moving these from the controller class. 
    def fit_model(self, x, y):
        # call out to parent class to use surrogate model
        self.sm.fit(x,y)

    def model_predict(self, x) : #, outvar):
        # call out to parent class to use surrogate model
        # mu, noError = self.parent.model_predict(x)
        #'mean' is regressive definition. not statistical
        #'variance' only applies for some surrogate models
        mu, noError = self.sm.predict(x, self.output_size)
        return mu, noError
    
    def model_get_variance(self):
        # sigma = self.parent.model_get_variance()
        # return sigma
        variance = self.sm.calculate_variance()
        return variance


    # COMPLETION CHECKS
    def converged(self):
        # check if converged
        if (len(self.F_Gb) < 1): # no points, no sample
            return False
        convergence = np.linalg.norm(self.F_Gb) < self.E_TOL
        return convergence

    def maxed(self):
        # check if search max iterations hit
        max_iter = self.iter >= self.maxit
        return max_iter

    def complete(self):
        done = self.converged() or self.maxed()
        return done

    # CHECK PROGRESS
    def check_global_local(self, Flist):
        # use L2 norm to check if fitness val is less than global best fitness
        # if yes, update with the new best point
        if (len(Flist) < 1) or (len(self.F_Gb)<1): # list is empty. not enought points yet
            return
        # if the current fitness is better than the current global best, replace the var.
        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Gb):
            self.F_Gb = Flist
            self.Gb = 1*np.vstack(np.array(self.new_point))     

    def get_convergence_data(self):
        best_eval = np.linalg.norm(self.F_Gb)
        iteration = 1*self.iter
        return iteration, best_eval

    # GETTERS
    def get_optimized_soln(self):
        return self.Gb 
    
    def get_optimized_outs(self):
        return self.F_Gb

    def get_sample_points(self):
        # returns sample locations (self.M) and the associated evaluations (self.F_Pb)
        return self.M, self.F_Pb
   
    # OPTIMIZER FUNCTIONS
    def expected_improvement(self, X):
        X = np.atleast_2d(X)

        mu, noError = self.model_predict(X) #mean and standard deviation
        sigma = self.model_get_variance()
        mu_sample, _ = self.model_predict(self.M) #predict using sampled locations
        mu_sample_opt = np.min(mu_sample)
        
        imp = mu_sample_opt - mu - self.xi

        #Standardize Improvement
        #Z = np.where(sigma != 0, imp / sigma, 0)
        Z = np.divide(imp, sigma, out=np.zeros_like(imp), where=sigma!=0)
        ei = imp * (1 + np.tanh(Z))
        # # This introduces more stability into the model, 
        # # but the tested problems do much worse with exploration
        # for idx in range(0, len(sigma)):
        #     if sigma[idx] == 0.0:
        #         ei[:,idx] = np.multiply(ei[:,idx],0.0)
        
        return ei

    def propose_location(self):
        dim = len(self.lbound)
        min_val = 1
        min_x = None # may stay none if it doesn't minimize

        for x0 in self.rng.uniform(self.lbound.reshape(1,-1)[0], self.ubound.reshape(1,-1)[0], size=(self.n_restarts, dim)):
            x, f_x = self.minimize(x0)
            #using the l2norm to handle single and multi objective
            if np.linalg.norm(f_x) < np.linalg.norm(min_val):
                min_val = f_x
                min_x = x

        if min_x is None:
            # Return a random point in bounds
            min_x = self.rng.uniform(self.lbound.reshape(1, -1)[0], self.ubound.reshape(1, -1)[0])


        return np.round(np.array([min_x]), self.number_decimals)


    def minimize(self, x0, max_iter=100, tol=1e-6):
        x = np.array(x0)
        alpha = 0.1
        for i in range(max_iter):
            grad = self.numerical_gradient(x, tol)
            x_new = np.clip(x - alpha * grad, self.lbound.reshape(1,-1)[0], self.ubound.reshape(1,-1)[0])
            if np.linalg.norm(x_new - x) < tol:
                break
            x = x_new
        f_x = -self.expected_improvement(np.array([x]))
        return x, f_x

    def numerical_gradient(self, x, eps=1e-8):
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_eps = x.copy()
            x_eps[i] += eps
            ei_x_eps = -self.expected_improvement(np.array([x_eps]))
            ei_x = -self.expected_improvement(np.array([x]))
            grad_arr = (ei_x_eps - ei_x) / eps
            grad[i] = np.linalg.norm(grad_arr) # Aggregate. explore other methods later. (summation?)

        return grad



    def step(self, suppress_output=False):
        if not suppress_output:
            if self.ctr < self.init_points:
                msg = "\n-----------------------------\n" + \
                "STEP #" + str(self.iter) +"\n" + \
                "-----------------------------\n" + \
                "Completed Initial Sample #" + str(self.ctr) + " of " + str(self.init_points) + "\n" +\
                "Last Proposed Point:\n" + \
                str(self.new_point) +"\n" + \
                "Best Fitness Solution: \n" +\
                str(np.linalg.norm(self.F_Gb)) +"\n" +\
                "Best Particle Position: \n" +\
                str(np.hstack(self.Gb)) + "\n" +\
                "-----------------------------"
            else:
                msg = "\n-----------------------------\n" + \
                "STEP #" + str(self.iter) +"\n" + \
                "-----------------------------\n" + \
                "Initial samples done, now running optimizer\n" +\
                "Last Proposed Point:\n" + \
                str(self.new_point) +"\n" + \
                "Best Fitness Solution: \n" +\
                str(np.linalg.norm(self.F_Gb)) +"\n" +\
                "Best Particle Position: \n" +\
                str(np.hstack(self.Gb)) + "\n" +\
                "-----------------------------"



            self.debug_message_printout(msg)

        if self.allow_update:     
            #initialize the first couple runs
            if self.doneInitializationBoolean == False:
                #1) the initial points need to be run
                #2) getter for sample points (to ensure standard formatting)
                #3) fit the surrogate model

                # running the initial point collection 
                if self.ctr < self.init_points:
                    
                    # these are split into 2 cases for easier debug
                    if self.ctr == 0: # first point
                        #calling the objective function with the first random pt 
                        self.objective_function_case = 0
                        
                    else: # rest of the points
                        self.objective_function_case = 1
                    self.ctr = self.ctr + 1
                
                else: #if self.ctr >= self.init_points: 
                    msg = "Model initialized with " + str(self.ctr) + " points. \n \
                    The iteration counter will start from " + str(self.iter) + "\n\n"
                    self.debug_message_printout(msg)
                    # get the sample points out (to ensure standard formatting)
                    x_sample, y_sample = self.get_sample_points()
                    # fit GP model.
                    self.fit_model(x_sample, y_sample)
                    ### ABOVE HERE IS THE END OF THE FULL INITIALIZATION SETUP###
                    self.doneInitializationBoolean = True
                    

            # NOT an elif, so that this condition is hit immediately after the setup is done above
            if self.doneInitializationBoolean == True:
                # set to case 2 for objective function call
                self.objective_function_case = 2

                # check if points are better than last global bests
                self.check_global_local(self.Flist)

                #self.sample_next_point() in original example, but now split up
                self.new_point = self.propose_location()

                # check if points are better than last global bests
                self.check_global_local(self.Flist)

                #self.sample_next_point(), but split up
                self.new_point = self.propose_location()
            

            # There is no handling boundaries for points in the bayesian optimizer
            # because the proposed location is already bounded by the problem space

            if self.complete() and not suppress_output:
                msg =  "\nPoints: \n" + str(self.Gb) + "\n" + \
                    "Iterations: \n" + str(self.iter) + "\n" + \
                    "Flist: \n" + str(self.F_Gb) + "\n" + \
                    "Norm Flist: \n" + str(np.linalg.norm(self.F_Gb)) + "\n"
                self.debug_message_printout(msg)



    def debug_message_printout(self, msg):
        # for error messages, but also repurposed for general updates
        if self.parent == None:
            print(msg)
        else:
            self.parent.debug_message_printout(msg)