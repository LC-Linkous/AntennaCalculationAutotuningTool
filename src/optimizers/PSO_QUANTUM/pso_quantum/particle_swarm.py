#! /usr/bin/python3

##--------------------------------------------------------------------\
#   surrogate_model_optimization
#   './surrogate_model_optimization/src/optimizers/surrogate_pso_quantum.py'
#   'quantum' particle swarm class. This class has been modified from the original
#       to include message passing for UI integration, and underflow 
#       and overflow min/max caps to accommodate wider user input
#       options in AntennaCAT.
#      
#
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: June 26, 2025
##--------------------------------------------------------------------\

import numpy as np
from numpy.random import Generator, MT19937
import sys
np.seterr(all='raise')

class swarm:
    # arguments should take the form: 
    # swarm([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj,
    # bool, [int, int, ...]
    # bool, class obj,
    # int)  
    #  
    # opt_df contains class-specific tuning parameters
    # NO_OF_PARTICLES: int
    # boundary: int. 1 = random, 2 = reflecting, 3 = absorbing,   4 = invisible
    # beta: float
    #           

    def __init__(self,  lbound, ubound, targets,E_TOL, maxit,
                 obj_func, constr_func, 
                 opt_df,
                 parent=None, 
                 evaluate_threshold=False, obj_threshold=None, 
                 useSurrogateModel=False, surrogateOptimizer=None,
                 decimal_limit = 4): 

   
        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 
        # vars for using surrogate model
        self.useSurrogateModel = useSurrogateModel # bool for if using surrogate model
        self.surrogateOptimizer = surrogateOptimizer     # pass in the class for the surrogate model
                                                   # optimizer. this is configured as needed 

        self.number_decimals = int(decimal_limit)  # limit the number of decimals
                                                    # used in cases where real life 
                                                    # has limitations on resolution

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
        NO_OF_PARTICLES = int(opt_df['NO_OF_PARTICLES'][0])
        boundary = int(opt_df['BOUNDARY'][0])
        beta = float(opt_df['BETA'][0])
        weights = np.array(opt_df['WEIGHTS'][0])



        heightl = np.shape(lbound)[0]
        widthl = np.shape(lbound)[1]
        heightu = np.shape(ubound)[0]
        widthu = np.shape(ubound)[1]

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
                self.parent.debug_message_printout("Error lbound and ubound must be 1xN-dimensional \
                                                        arrays  with the same length")
           
        else:
        
            if heightl == 1:
                lbound = lbound
        
            if heightu == 1:
                ubound = ubound

            self.lbound = lbound
            self.ubound = ubound
            variation = ubound-lbound


            self.M = np.round(np.array(np.multiply(self.rng.random((1,np.max([heightl, widthl]))), variation)+lbound), self.number_decimals)   

            for i in range(2,int(NO_OF_PARTICLES)+1):
                
                M = np.round(np.array(np.multiply(self.rng.random((1,np.max([heightl, widthl]))), variation)+lbound), self.number_decimals) 
                 
                self.M = \
                    np.vstack([self.M, 
                               M])

            '''
            self.M                      : An array of current particle locations.
            self.beta                   : Float constant controlling influence between the personal and global best positions
            self.output_size            : An integer value for the output size of obj func (y-vals)
            self.input_size             : An integer value for the input size of the obj func (x-vals)
            self.Active                 : An array indicating the activity status of each particle.
            self.Gb                     : Global best position, initialized with a large value.
            self.F_Gb                   : Fitness value corresponding to the global best position.
            self.Pb                     : Personal best position for each particle.
            self.F_Pb                   : Fitness value corresponding to the personal best position for each particle.
            self.weights                : Weights for the optimization process.
            self.targets                : Target values for the optimization process.
            self.maxit                  : Maximum number of iterations.
            self.E_TOL                  : Error tolerance.
            self.obj_func               : Objective function to be optimized.      
            self.constr_func            : Constraint function.  
            self.iter                   : Current iteration count.
            self.current_particle       : Index of the current particle being evaluated.
            self.number_of_particles    : Total number of particles. 
            self.allow_update           : Flag indicating whether to allow updates.
            self.boundary               : Boundary conditions for the optimization problem.
            self.Flist                  : List to store fitness values.
            self.Fvals                  : List to store fitness values.
            self.Mlast                  : Last location of particle
            '''
            self.beta = beta
            self.output_size = len(targets)
            self.input_size = len(lbound)
            self.Active = np.ones((NO_OF_PARTICLES))                        
            self.Gb = sys.maxsize*np.ones((1,np.max([heightl, widthl])))   
            self.F_Gb = sys.maxsize*np.ones((1,self.output_size))                
            self.Pb = sys.maxsize*np.ones(np.shape(self.M))                 
            self.F_Pb = sys.maxsize*np.ones((NO_OF_PARTICLES,self.output_size))  
            self.weights = np.array(weights) 
            self.targets = np.array(targets).reshape(-1, 1)                  
            self.maxit = maxit                                             
            self.E_TOL = E_TOL                                              
            self.obj_func = obj_func                                             
            self.constr_func = constr_func                                   
            self.iter = 0                                                   
            self.current_particle = 0                                       
            self.number_of_particles = NO_OF_PARTICLES                      
            self.allow_update = 0                                           
            self.boundary = boundary                                       
            self.Flist = []                                                 
            self.Fvals = []          
            self.Mlast = 1*self.ubound                                      

            self.debug_message_printout("swarm successfully initialized")
            
    def minimize_surrogate_model(self):
        canUseSurrogate = False
        if self.parent == None:
            self.debug_message_printout("ERROR: no parent selected. cannot use surrogate model. continuing with optimization")
            return canUseSurrogate
        
        if self.surrogateOptimizer == None:
            self.debug_message_printout("ERROR: no second optimizer selected. cannot use surrogate model. continuing with optimization")
            return canUseSurrogate           

        try:

            # call up to the parent function to define and fit the surrogate func, 
            # and set up the surrogate optimizer 
            surrogateOptimizer = self.parent.fit_and_create_surogate(self.M, self.F_Pb,self.surrogateOptimizer)


            best_eval = 10 # set high for testing
            # sometimes an optimizer doesn't call the objective function, so only print out when it does
            last_iter = 0

            while not surrogateOptimizer.complete():
                # step through optimizer processing
                surrogateOptimizer.step(suppress_output=False)

                # call the objective function, control 
                # when it is allowed to update and return 
                # control to optimizer
                surrogateOptimizer.call_objective(allow_update=True)
                iter, eval = surrogateOptimizer.get_convergence_data()
                if (eval < best_eval) and (eval != 0):
                    best_eval = eval
                if iter > last_iter:
                    last_iter = iter

            print("************************************************")
            print("Internal Objective Function Iterations: " + str (iter))
            print("Internal Best Eval: " + str(best_eval))

            # check if G_best of surrogate optimizer is better than what the main optimizer is finding
            potential_Gb =  np.array(surrogateOptimizer.get_optimized_soln()).reshape(1 ,-1)
            potential_F_Gb =  np.array(surrogateOptimizer.get_optimized_outs()).reshape(1 ,-1)
            if np.linalg.norm(potential_F_Gb) < np.linalg.norm(self.F_Gb):
                self.F_Gb = np.array(potential_F_Gb)
                self.Gb = np.array(potential_Gb[0])
                print("NEW BEST!!!!!!")      
                print("self.F_Gb")
                print(self.F_Gb)
                print("self.Gb")
                print(self.Gb)
            
            canUseSurrogate = True
            
        except Exception as e:
            print(e)
            self.debug_message_printout("ERROR: failed to set up and minimize surrogate model")

        return canUseSurrogate
    
    
    def call_objective(self, allow_update):
        if self.Active[self.current_particle]:
            # call the objective function. If there's an issue with the function execution, 'noError' returns False
            newFVals, noError = self.obj_func(self.M[self.current_particle], self.output_size)
            if noError == True:
                self.Fvals = np.array(newFVals).reshape(-1, 1)
                if allow_update:
                    # EVALUATE OBJECTIVE FUNCTION - TARGET OR THRESHOLD
                    self.Flist = self.objective_function_evaluation(self.Fvals, self.targets)# abs(self.targets - self.Fvals)
                    self.iter = self.iter + 1
                    self.allow_update = 1
                else:
                    self.allow_update = 0
            return noError# return is for error reporting purposes only
    

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

        Flist = np.zeros(len(Fvals))


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


    def check_bounds(self, particle):
        update = 0
        for i in range(0,(np.shape(self.M)[1])):
            if (self.lbound[i] > self.M[particle,i]) \
               or (self.ubound[i] < self.M[particle,i]):
                update = i+1        
        return update

    def random_bound(self, particle):
        # If particle is out of bounds, bring the particle back in bounds
        # The first condition checks if constraints are met, 
        # and the second determines if the values are too large (positive or negative)
        # and may cause a buffer overflow with large exponents (a bug that was found experimentally)
        update = self.check_bounds(particle) or not self.constr_func(self.M[particle]) 
        if update > 0:
            while (self.check_bounds(particle) > 0) or (self.constr_func(self.M[particle]) == False):
                variation = self.ubound - self.lbound
                self.M[particle] = np.round(
                    np.squeeze(
                        self.rng.random() *
                        np.multiply(np.ones((1, np.shape(self.M)[1])), variation) +
                        self.lbound
                    ),
                    self.number_decimals
                )
            
    def reflecting_bound(self, particle):        
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[particle])
        if (update > 0) and constr:
            self.M[particle] = 1*self.Mlast
        if not constr:
            self.random_bound(particle)

    def absorbing_bound(self, particle):
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[particle])
        if (update > 0) and constr:
            self.M[particle] = 1*self.Mlast
        if not constr:
            self.random_bound(particle)

    def invisible_bound(self, particle):
        update = self.check_bounds(particle) or not self.constr_func(self.M[particle])
        if update > 0:
            self.Active[particle] = 0  
        else:
            pass          

    def handle_bounds(self, particle):
        if self.boundary == 1:
            self.random_bound(particle)
        elif self.boundary == 2:
            self.reflecting_bound(particle)
        elif self.boundary == 3:
            self.absorbing_bound(particle)
        elif self.boundary == 4:
            self.invisible_bound(particle)
        else:
            self.debug_message_printout("Error: No boundary is set!")

    def check_global_local(self, Flist, particle):
        
        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Gb):
            self.F_Gb = np.array([Flist])
            self.Gb = np.array(self.M[particle])
        
        if np.linalg.norm(Flist) < np.linalg.norm(self.F_Pb[particle]):
            self.F_Pb[particle] = np.squeeze(Flist)
            self.Pb[particle] = self.M[particle]
    
    def update_point(self,particle):
        #updates particle location. in quantum inspired algs, this merges the classical position& velocity update
        # duplicate locals to stick with eqs. in README
        self.Mlast = self.weights[0][0]*self.M[particle]    # save last loc
        p = self.weights[0][1]*self.Pb[particle]            # personal best
        g = self.weights[0][2]*self.Gb   
        
        # Mean Best Position
        mb = self.beta* p + (1 - self.beta) * g

        # Position Update (Update Rule)
        u = self.rng.uniform(size=(1,self.input_size))

        self.M[particle] = np.round(mb + self.beta * np.abs(p - g) * np.log(1 / u), self.number_decimals)


    def converged(self):
        convergence = np.linalg.norm(self.F_Gb) < self.E_TOL
        return convergence
    
    def maxed(self):
        max_iter = self.iter >= self.maxit
        return max_iter
    
    def complete(self):
        done = self.converged() or self.maxed()
        return done
    
    def step(self, suppress_output):
        if not suppress_output:
            msg = "\n-----------------------------\n" + \
                "STEP #" + str(self.iter) +"\n" + \
                "-----------------------------\n" + \
                "Current Particle:\n" + \
                str(self.current_particle) +"\n" + \
                "Current Particle Location\n" + \
                str(self.M[self.current_particle]) +"\n" + \
                "Absolute mean deviation\n" + \
                str(self.absolute_mean_deviation_of_particles()) +"\n" + \
                "-----------------------------"
            self.debug_message_printout(msg)
            

        if self.allow_update:
            if self.Active[self.current_particle]:
                self.check_global_local(self.Flist,self.current_particle)
                self.update_point(self.current_particle)
                self.handle_bounds(self.current_particle)
            self.current_particle = self.current_particle + 1
            if self.current_particle == self.number_of_particles:
                if self.useSurrogateModel == True:
                    print("MINIMIZING SURROGATE MODEL")
                    self.minimize_surrogate_model()
                self.current_particle = 0

            if self.complete() and not suppress_output:
                msg =  "\nPoints: \n" + str(self.Gb) + "\n" + \
                    "Iterations: \n" + str(self.iter) + "\n" + \
                    "Flist: \n" + str(self.F_Gb) + "\n" + \
                    "Norm Flist: \n" + str(np.linalg.norm(self.F_Gb)) + "\n"
                self.debug_message_printout(msg)


    def export_swarm(self):
        #These do NOT export.
        # # These are passed objects created at runtim
        # self.parent # this is an object in memory at runtime
        # self.surrogateOptimizer =  # this is an object in memory at runtime  
        # self.obj_func =  # this is an object in memory at runtime                                             
        # self.constr_func =  # this is an object in memory at runtime    
        # self.useSurrogateModel = # this NEEDS to match every time. Should be part of the init() 
        # self.number_decimals = # this can be changed. IT might be interesting to change between runs
        # self.boundary = boundary     # int. can be chaged, but needs a default
        # These export:


        swarm_export = {            
            # These are values that define the swarm and current solution space
            # These are retained because the dimensionality of M, F_pb, etc. are strict
            'evaluate_threshold': [self.evaluate_threshold],
            'obj_threshold': [self.obj_threshold],
            'targets': [self.targets],
            'lbound': [self.lbound],
            'ubound': [self.ubound],
            'output_size': [self.output_size], # this can be calculated if needed
            'input_size': [self.input_size],  # this can be calculated if needed
            # convergence and step criteria
            'maxit': [self.maxit],                                       
            'E_TOL': [self.E_TOL],                                            
            'iter': [self.iter],
            'current_particle': [self.current_particle],    
            'allow_update': [self.allow_update],
            # optimizer specfic

            'beta': [self.beta],
            'weughts': [self.weights],
            'number_of_particles': [self.number_of_particles], 
            # shared format vars for AntennaCAT set
            'M': [self.M], 
            'Active': [self.Active],                    
            'Gb': [self.Gb],
            'F_Gb': [self.F_Gb],             
            'Pb': [self.Pb],           
            'F_Pb': [self.F_Pb],
            'Flist': [self.Flist],                                                
            'Fvals': [self.Fvals],                                               
            'Mlast': [self.Mlast]
            } 
        
       
        return swarm_export # this is turned into a dataframe in the driver class

    def import_swarm(self, swarm_export):
        
        # swarm export is a dataframe. this is unpacked and converted just like
        # with the initialized opt_df params

        # These are values that define the swarm and current solution space
        # These are retained because the dimensionality of M, F_pb, etc. are strict
        self.evaluate_threshold = bool(swarm_export['evaluate_threshold'][0]) 
        self.obj_threshold = np.array(swarm_export['obj_threshold'][0]) 
        self.targets = np.array(swarm_export['targets'][0]).reshape(-1, 1)   

        self.lbound = np.array(swarm_export['lbound'][0]) 
        self.ubound = np.array(swarm_export['ubound'][0]) 
        self.output_size = int(swarm_export['output_size'][0])  # this can be calculated if needed
        self.input_size = int(swarm_export['input_size'][0])  # this can be calculated if needed
        # convergence and step criteria
        self.maxit = int(swarm_export['maxit'][0])                                              
        self.E_TOL = float(swarm_export['E_TOL'][0])                                               
        self.iter = int(swarm_export['iter'][0])     # NEED 'RESUME' and 'START OVER' options
        self.current_particle = int(swarm_export['current_particle'][0])         
        self.allow_update = int(swarm_export['allow_update'][0])    # BOOL as INT

        # optimizer specfic
        self.weights = np.array(swarm_export['weights'][0])
        self.beta = float(swarm_export['beta'][0]) 
        self.number_of_particles = int(swarm_export['number_of_particles'][0]) 

        # shared format vars for AntennaCAT set

        self.M = np.array(swarm_export['M'][0]) 
        self.Active = np.array(swarm_export['Active'][0])                    
        self.Gb = np.array(swarm_export['Gb'][0]) 
        self.F_Gb = np.array(swarm_export['F_Gb'][0])
        self.Pb = np.array(swarm_export['Pb'][0])              
        self.F_Pb = np.array(swarm_export['F_Pb'][0])  
        self.Flist = np.array(swarm_export['Flist'][0])                                                 
        self.Fvals= np.array(swarm_export['Fvals'][0])                                               
        self.Mlast= np.array(swarm_export['Mlast'][0])    

    def get_obj_inputs(self):
        return np.vstack(self.M[self.current_particle])
    
    def get_convergence_data(self):
        best_eval = np.linalg.norm(self.F_Gb)
        iteration = 1*self.iter
        return iteration, best_eval
        
    def get_optimized_soln(self):
        return self.Gb.reshape(-1, 1) #standardization  
    
    def get_optimized_outs(self):
        return self.F_Gb[0] #correction for extra brackets that happen with the math/passing
    
    def absolute_mean_deviation_of_particles(self):
        mean_data = np.array(np.mean(self.M, axis=0)).reshape(1, -1)
        abs_data = np.zeros(np.shape(self.M))
        for i in range(0,self.number_of_particles):
            abs_data[i] = np.squeeze(np.abs(self.M[i]-mean_data))

        abs_mean_dev = np.linalg.norm(np.mean(abs_data,axis=0))
        return abs_mean_dev

    def debug_message_printout(self, msg):
        if self.parent == None:
            print(msg)
        else:
            self.parent.debug_message_printout(msg)

