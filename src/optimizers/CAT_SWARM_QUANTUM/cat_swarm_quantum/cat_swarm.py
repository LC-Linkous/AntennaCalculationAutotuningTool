#! /usr/bin/python3

##--------------------------------------------------------------------\
#   surrogate_model_optimization
#   './surrogate_model_optimization/src/surrogate_cat_quantum.py'
#   A quantum-inspired Cat swarm optimization class. This class follows the same 
#       format as pso_python and pso_basic to make them interchangeable
#       in function calls. 
#       
#
#   Author(s): Lauren Linkous
#   Last update: May 18, 2025
##--------------------------------------------------------------------\


import numpy as np
from numpy.random import Generator, MT19937, shuffle
import sys
np.seterr(all='raise')


class swarm:
    # arguments should take the form: 
    # swarm([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj,
    # bool, [int, int, ...]
    # bool, class obj) 
    #  
    # opt_df contains class-specific tuning parameters
    # NO_OF_PARTICLES: int
    # weights: [[float, float, float]]
    # boundary: int. 1 = random, 2 = reflecting, 3 = absorbing,   4 = invisible
    # MR: float. Small value
    # SMP: int
    # SRD: float
    # CDC: int
    # SPC: bool
    #              

    def __init__(self,  lbound, ubound, targets,E_TOL, maxit,
                 obj_func, constr_func, 
                 opt_df,
                 parent=None, 
                 evaluate_threshold=False, obj_threshold=None, 
                 useSurrogateModel=False, surrogateOptimizer=None): 
        

        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 
        # vars for using surrogate model
        self.useSurrogateModel = useSurrogateModel # bool for if using surrogate model
        self.surrogateOptimizer = surrogateOptimizer     # pass in the class for the surrogate model
                                                   # optimizer. this is configured as needed 


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
        NO_OF_PARTICLES = opt_df['NO_OF_PARTICLES'][0]
        weights = opt_df['WEIGHTS'][0]
        boundary = opt_df['BOUNDARY'][0]
        MR = opt_df['MR'][0]
        SMP = opt_df['SMP'][0]
        SRD = opt_df['SRD'][0]
        CDC = opt_df['CDC'][0]
        SPC = opt_df['SPC'][0]
        beta = opt_df['BETA'][0]



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


            #randomly initialize the positions and velocities of the cats
            # position
            self.M = np.array(np.multiply(self.rng.random((1,np.max([heightl, widthl]))), 
                                                                            variation)+lbound)    


  



            for i in range(2,int(NO_OF_PARTICLES)+1):
                
                self.M = \
                    np.vstack([self.M, 
                               np.multiply( self.rng.random((1,np.max([heightl, widthl]))), 
                                                                               variation) 
                                                                               + lbound])

            #randomly classify cats into seeking or tracing. 
                # 0 = tracing, 1 = seeking
            # MR controls how many cats are tracking (usually a small amount),
                # however it is random WHICH cats are tracking

            # cat vars
            self.MR = MR  #mixture ratio (MR), % of population in tracing state
            self.SMP = SMP
            self.SRD = SRD
            self.CDC = CDC
            self.SPC = SPC
 
            
            cat_mode = np.array([[1]]) # if there's 1 cat, just make it seeking to start
            
            if NO_OF_PARTICLES >1: #more cats
                tracingRatio = int(self.MR*NO_OF_PARTICLES) #how many tracing in population
                # arrays of tracing (0) or seeking (1)
                array_of_zeros = np.zeros((tracingRatio,1))
                array_of_ones = np.ones((NO_OF_PARTICLES-tracingRatio,1))   

                # combine arrays for whole population
                cat_mode = np.concatenate((cat_mode, array_of_zeros, array_of_ones))

                # shuffle
                self.rng.shuffle(cat_mode)

            self.cat_mode = cat_mode



            '''
            self.M                      : An array of current particle (cat) locations.
            self.cat_mode               : An array of if cats are in tracing (0) or seeking (1) mode
            self.MR                     : Mixture ratio (MR). Small value for tracing population
            self.SMP                    : seeking memory pool. Num copies of cats made 
            self.SRD                    : seeking range of the selected dimension 
            self.CDC                    : counts of dimension to change. mutation.
            self.SPC                    : self-position consideration. boolean.
            self.beta                   : Float constant controlling influence between the personal and global best positions
            self.output_size            : An integer value for the output size of obj func (y-vals)
            self.input_size             : An integer value for the input size of the obj func (x-vals)
            self.Active                 : An array indicating the activity status of each particle. (e.g., in bounds)
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
            self.weights = np.array(weights[0])                     
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
                                        

            self.createCandidateSet = True
            self.candidateCtr = 0             
            self.candidate_positions = []
            self.candidate_probability = []      
            self.fitness_values = []
            self.doneCandidateIteration = True     
            self.evaluateCandidate = False 




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

            if self.evaluateCandidate == False:
                # Normal objective function call for particle
                # call the objective function. 
                # If there's an issue with the function execution, 'noError' returns False
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
            else:
                # evaluating a candidate position
                # call the objective function. 
                # If there's an issue with the function execution, 'noError' returns False

                # Seeking
                # Step 3: calculate fitness values of all candidates
                # with additional error checking  

                newFVals, noError = self.obj_func(self.candidate_positions[self.candidateCtr], self.output_size)
                if noError == True:
                    self.fitness_values[self.candidateCtr] = 1.0*np.hstack(newFVals)
                else:
                    pass # leave as sys.maxsize


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



    def seeking_mode_create_candidates(self, particle):
        # this is the "resting" function for the cat swarm
        # SMP : seeking memory pool. Num copies of cats made 
        # SRD : seeking range of the selected dimension 
        # CDC : counts of dimension to change. mutation.
        # SPC : self-position consideration. boolean.
        

        # Step 1: generate candidate positions (copies)
        current_position = self.M[particle]
               
        if self.SPC == True: # current cat included in pool (added later)
            self.candidate_positions = np.tile(current_position, (self.SMP-1, 1))
        else: # current cat not included. make SMP copies
            self.candidate_positions  = np.tile(current_position, (self.SMP, 1))

        # Step 2: modify each candidate position
            # new_position = (1+(random sign)*SRD)*current_position
        # duplicate locals to stick with eqs. in README
        p = self.Pb[particle]                # personal best
        g = np.hstack(self.Gb)               # global best

        # Mean Best Position (for the cat)
        mb = self.beta* p + (1 - self.beta) * g

        for i in range(len(self.candidate_positions)):
            # Position Update (Update Rule), applied on copies
            u = self.rng.uniform(size=(1,self.input_size))
            self.candidate_positions[i] = mb + self.beta * np.abs(p - g) * np.log(1 / u)

        if self.SPC== True: # add current cat into the pool
            self.candidate_positions = np.vstack((self.candidate_positions, current_position))

        # Step 3: calculate fitness values of all candidates
            # with additional error checking
        self.fitness_values =  np.ones((self.SMP,self.output_size))*sys.maxsize

        # Step 3: calculate fitness values of all candidates
        # with additional error checking  
        # 
        # HAPPENS IN OBJECTIVE FUNCTION CALL     


    def seeking_mode_best_position(self, particle):
        # Step 4: Select the best position based on fitness
            #If all Fitness_values are not exactly equal, calculate the selecting probability of each
            #candidate point by equation (1), otherwise set all the selecting probability
            #of each candidate point be 1. (2007, computational intelligence based on the behaviour of cats)

        # Compute the L2 norm of each row
        l2_norms = np.linalg.norm(self.fitness_values, axis=1)
        # Check if all L2 norms are the same
        all_norms_same = np.all(l2_norms == l2_norms[0])

        self.candidate_probability = np.ones(len(self.fitness_values))/len(self.fitness_values)
        if all_norms_same == False: #calculate probability
            idx = 0
            for c in self.candidate_positions:
                FS_cat = l2_norms[idx]
                FSmin = np.min(l2_norms)
                FSmax = np.max(l2_norms)
                FSb =  FSmax# max bc minimization problem
                self.candidate_probability[idx] = abs(FS_cat-FSb)/abs(FSmax-FSmin)
                idx = idx + 1
        
        # normalize the probability so it adds to 1
        self.candidate_probability = self.candidate_probability/np.sum(self.candidate_probability)
        # Randomly select new position
        candidate_idx = np.arange(0, len(self.candidate_probability), 1)

        new_position = self.rng.choice(candidate_idx, 1, p=self.candidate_probability)

        self.M[particle] = self.candidate_positions[new_position]
            


    def tracing_mode(self, particle):
        # this is the "movement" function for the cat swarm
        p = self.Pb[particle]             # personal best
        g = self.Gb                       # global best
        u = self.rng.uniform(size=self.input_size)
        # new location
        self.M[particle] = p  + self.weights * u * (g - p)

      
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
        # and the second determins if the values are to large (positive or negitive)
        # and may cause a buffer overflow with large exponents (a bug that was found experimentally)
        update = self.check_bounds(particle) or not self.constr_func(self.M[particle])
        if update > 0:
            while(self.check_bounds(particle)>0) or (self.constr_func(self.M[particle])==False): 
                variation = self.ubound-self.lbound
                self.M[particle] = \
                    np.squeeze(self.rng.random() * 
                                np.multiply(np.ones((1,np.shape(self.M)[1])),
                                            variation) + self.lbound)
            
    def reflecting_bound(self, particle):        
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[particle])
        if (update > 0) and constr:
            self.M[particle] = 1*self.Mlast
            NewV = np.multiply(-1,self.V[update-1,particle])
            self.V[update-1,particle] = NewV
        if not constr:
            self.random_bound(particle)

    def absorbing_bound(self, particle):
        update = self.check_bounds(particle)
        constr = self.constr_func(self.M[particle])
        if (update > 0) and constr:
            self.M[particle] = 1*self.Mlast
            self.V[particle,update-1] = 0
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
                "Current Seeking/Tracing Status\n" + \
                str(self.cat_mode[self.current_particle]) +"\n" + \
                "Absolute mean deviation\n" + \
                str(self.absolute_mean_deviation_of_particles()) +"\n" + \
                "-----------------------------"
            self.debug_message_printout(msg)
            
        if self.allow_update: # The first time step is called, this is false
            if self.Active[self.current_particle]:
                # save global best
                self.check_global_local(self.Flist,self.current_particle)
                # split cats into tracing and seeking
                    # this combines the update_velocity and update_point in the pso_python repos
                if self.cat_mode[self.current_particle] == 0: #tracing
                    self.tracing_mode(self.current_particle)

                    # remove this after debug
                    #self.doneCandidateIteration == True
                else: # seeking
                    #create the candidate pool if it doesnt exist
                    if self.createCandidateSet == True:
                        self.candidateCtr = -1 #incremented to idx 0 in next if statement
                        self.seeking_mode_create_candidates(self.current_particle)
                        self.createCandidateSet = False
                        self.evaluateCandidate = True
                    else:
                        pass # don't create, just iterate in next steps
                    
                    if self.candidateCtr < (len(self.candidate_positions)-1):
                        # iterate through the list of the candidates.
                        # can't call the objective function FROM this class, 
                        # so use a bool to toggle what is being evaluated
                        self.candidateCtr = self.candidateCtr + 1
                        self.doneCandidateIteration = False #redundant, remove in cleanup

                    else:
                        #hit the end of the candidate list. 
                        self.evaluateCandidate = False #for objective func toggle
                        self.seeking_mode_best_position(self.current_particle)
                        self.doneCandidateIteration = True
                        # create a new list next time a particle is in seeking mode
                        self.createCandidateSet = True


                self.handle_bounds(self.current_particle)

            if self.doneCandidateIteration == True:
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
        swarm_export = {'lbound': self.lbound,
                        'ubound': self.ubound,
                        'M': self.M,
                        'Gb': self.Gb,
                        'F_Gb': self.F_Gb,
                        'Pb': self.Pb,
                        'F_Pb': self.F_Pb,
                        'weights': self.weights,
                        'targets': self.targets,
                        'maxit': self.maxit,
                        'E_TOL': self.E_TOL,
                        'iter': self.iter,
                        'current_particle': self.current_particle,
                        'number_of_particles': self.number_of_particles,
                        'allow_update': self.allow_update,
                        'Flist': self.Flist,
                        'Fvals': self.Fvals,
                        'Active': self.Active,
                        'Boundary': self.boundary,
                        'Mlast': self.Mlast}
        
        return swarm_export

    def import_swarm(self, swarm_export, obj_func):
        self.lbound = swarm_export['lbound'] 
        self.ubound = swarm_export['ubound'] 
        self.M = swarm_export['M'] 
        self.Gb = swarm_export['Gb'] 
        self.F_Gb = swarm_export['F_Gb'] 
        self.Pb = swarm_export['Pb'] 
        self.F_Pb = swarm_export['F_Pb'] 
        self.weights = swarm_export['weights'] 
        self.targets = swarm_export['targets'] 
        self.maxit = swarm_export['maxit'] 
        self.E_TOL = swarm_export['E_TOL'] 
        self.iter = swarm_export['iter'] 
        self.current_particle = swarm_export['current_particle'] 
        self.number_of_particles = swarm_export['number_of_particles'] 
        self.allow_update = swarm_export['allow_update'] 
        self.Flist = swarm_export['Flist'] 
        self.Fvals = swarm_export['Fvals']
        self.Active = swarm_export['Active']
        self.boundary = swarm_export['Boundary']
        self.Mlast = swarm_export['Mlast']
        self.obj_func = obj_func 

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
