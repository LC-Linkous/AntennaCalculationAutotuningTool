#! /usr/bin/python3

##--------------------------------------------------------------------\
#   surrogate_model_optimization
#   './surrogate_model_optimization/src/surrogate_chicken_swarm.py'
#   A basic chicken swarm optimization class. 
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: May 18, 2025
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
    # bool, class obj) 
    #  
    # opt_df contains class-specific tuning parameters
    # boundary: int. 1 = random, 2 = reflecting, 3 = absorbing,   4 = invisible
    # RN: int
    # HN: int
    # MN: int
    # CN: int
    # G: int
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
        boundary = opt_df['BOUNDARY'][0]
        RN = opt_df['RN'][0]
        HN = opt_df['HN'][0]
        MN = opt_df['MN'][0]
        CN = opt_df['CN'][0]
        G = opt_df['G'][0]
        NO_OF_PARTICLES =  RN + HN + MN + CN


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
                self.parent.debug_message_printout("ERROR: lbound and ubound must be 1xN-dimensional \
                                                        arrays  with the same length")
           
        else:
        
            if heightl == 1:
                lbound = lbound
        
            if heightu == 1:
                ubound = ubound

            self.lbound = lbound
            self.ubound = ubound
            variation = ubound-lbound


            # chicken swarm vars
            # population split
            self.RN = RN    # rooster number
            self.HN = HN    # hen number
            self.MN = MN    # mother hen number
            self.CN = CN    # chick number
            total_chickens = RN + HN + MN + CN       

            self.G = G                       # num full cycles before updating the 
            self.G_steps = G*total_chickens  # how many iterations happen in a generation

 
            # error checking on population split
            if (NO_OF_PARTICLES < total_chickens):
                self.parent.debug_message_printout("WARNING: number of chickens adds up to more \
                                                   than the expected number of particles. Attempting fix.")
                # subtract number of roosters and chicks. rest are hens
                num_hens = NO_OF_PARTICLES - RN - CN - MN
                if (num_hens <=0):
                    self.parent.debug_message_printout("ERROR: total of roosters and chicks is higher than \
                                                       the expected swarm size. Swarm init failed.")
                    return
                else:
                    if (num_hens > MN):
                        self.MN = MN
                        self.HN = num_hens - MN # extra non-mother hens
                        self.parent.debug_message_printout("WARNING: reduced number of hens used for swarm initiation.\
                                                            Number of mother hens is " + str(self.MN) +\
                                                            ". Total number of hens is " + str(num_hens))
            elif (NO_OF_PARTICLES > total_chickens):
                    num_hens = NO_OF_PARTICLES - total_chickens
                    self.HN = self.HN + num_hens # extra non-mother hens
                    self.parent.debug_message_printout("WARNING: there are fewer than expected chickens, adding extra hens.\
                                    Check categories for chickens.")

            elif (MN < 1) and (CN>0): #chicks but no mother hens
                self.parent.debug_message_printout("ERROR: there are chicks, but no mother hens.\
                Check categories for chickens.")
                return
   
            #split chickens into groups           
            # Each group has a rooster (chicken with best fitness value)
            # The worst preforming agents are chicks.
            # The rest are hens. hens randomly chose a group to liven in.
            # mother-child relation in randomly established
            
            # assign which group the chickens are in 
            # first chicken is a rooster, in case there's only 1 searching agent
            # chicken_info = array of [CLASSIFICATION(0-4), GROUP(0-(RN-1)), MOTHER-HEN-ID]
            # classificition: 0 = rooster, 1 = hen, 2 = mother hen, 3 = chicks
            self.chicken_info = np.array([0, 0, -1])

            #randomly initialize the positions 
            self.M = np.vstack(np.multiply(self.rng.random((np.max([heightl, 
                                                                     widthl]),1)), 
                                                                     variation) + 
                                                                     lbound)    


            if NO_OF_PARTICLES > 1:
                # make temp classification list
                classList = np.zeros(NO_OF_PARTICLES)
                # rooster
                classList[0:RN] = 0
                # hen
                start = RN
                end = RN + HN
                classList[start:end] = 1
                # mother hen
                start = RN + HN
                end = RN + HN + MN
                classList[start:end] = 2
                # chicks
                start = RN + HN + MN
                classList[start:] = 3
                # array of groups to use in random allocation
                group_nums = np.arange(RN)

            for i in range(2,int(NO_OF_PARTICLES)+1):
                # set initial location
                self.M = \
                    np.vstack([self.M, 
                               np.multiply( self.rng.random((1,np.max([heightl, widthl]))), 
                                                                               variation) 
                                                                               + lbound])
                if classList[i-1] == 0: #rooster
                    # assign to the next group (i-1), and done.
                    self.chicken_info = \
                        np.vstack([self.chicken_info, 
                                [classList[i-1], i-1, -1]])

                elif (classList[i-1] == 1) or (classList[i-1] == 2): #hen, mother hen
                    # assign to a random group.
                    hen_group = self.rng.choice(group_nums)
                    self.chicken_info = \
                        np.vstack([self.chicken_info, 
                                [classList[i-1], hen_group, -1]])

                elif classList[i-1] == 3: #chick
                    # select a random hen to be the 'mother' and assign to group
                    groupAssigned = False

                    while (groupAssigned == False):
                        chicken_idx = self.rng.integers(0, i-1)# index after a chick will always be the chick
                        if self.chicken_info[chicken_idx][0] == 2: #is mother hen
                            # get the group the random mother hen is from
                            mother_group = self.chicken_info[chicken_idx][1]         
                            # assign chick to group, and to that mother hen                    
                            self.chicken_info = \
                                np.vstack([self.chicken_info, 
                                        [classList[i-1], mother_group, chicken_idx]])
                            groupAssigned = True


            '''
            self.M                      : An array of current particle (cat) locations.
            self.RN                     : Number of roosters. Integer.
            self.HN                     : Total number of hens. Integer. 
            self.MN                     : Number of mother hens. Integer.
            self.CN                     : Number of chicks. Integer.  
            self.chicken_info           : classification (R,H,C), group #, mother ID. Array.          
            self.G                      : How often to randomize groups. Integer.
            self.output_size            : An integer value for the output size of obj func
            self.Active                 : An array indicating the activity status of each particle. (e.g., in bounds)
            self.Gb                     : Global best position, initialized with a large value.
            self.F_Gb                   : Fitness value corresponding to the global best position.
            self.Pb                     : Personal best position for each particle.
            self.F_Pb                   : Fitness value corresponding to the personal best position for each particle.
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

            self.output_size = len(targets)
            self.Active = np.ones((NO_OF_PARTICLES))                        
            self.Gb = sys.maxsize*np.ones((1,np.max([heightl, widthl])))   
            self.F_Gb = sys.maxsize*np.ones((1,self.output_size))                
            self.Pb = sys.maxsize*np.ones(np.shape(self.M))                 
            self.F_Pb = sys.maxsize*np.ones((NO_OF_PARTICLES,self.output_size))  
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


    # MOVEMENT MODELS

    def move_rooster(self, particle):
        # epsilon = 'smallest system constant'. improvised.
        epsilon = 10e-50 

        # choose a random rooster
        rooster_arr = np.arange(self.RN)
        random_rooster_idx = self.rng.choice(rooster_arr)
        # use L2 norm for fitness to account for multi-objective funcs
        random_rooster_fitness = np.linalg.norm(self.F_Pb[random_rooster_idx])
        
        this_rooster_fitness = np.linalg.norm(self.F_Pb[particle])

        if this_rooster_fitness <= random_rooster_fitness:
            sig_squared = 1
        else:
            # exp((fitness_random_rooster - fitness_this_rooster)/(abs(fitness_this_rooster)-epsilon))
            #sig_squared = np.exp((random_rooster_fitness-this_rooster_fitness)/(abs(this_rooster_fitness)+epsilon))
            # -709.00 and 709.00 are the integer limits to np.exp() on system that handles float64 at most (Windows)
            clipped_val = np.clip(((random_rooster_fitness-this_rooster_fitness)/(abs(this_rooster_fitness)+epsilon)), -700.00, 700.00)
            sig_squared = np.exp(clipped_val)


        #update new location based on random()
        self.M[particle] = self.M[particle]*(1+self.rng.normal(0, sig_squared))
    

    def move_hen(self, particle):
        #newLoc = oldLoc 
        # + S1*RANDOM(0-to-1)*(LocationRoosterGroupmate-thisChickenLocation)
        #  + S2*RANDOM(0-to-1)*(LoctionRandomChickenInSwarm-thisChickenLocation)
        # where:
        #   S1 = exp((FitnessThisChicken-FitnessRoosterGroupmate)/(abs(FitnessThisChicken)+epsilon))
        #   S2 = exp(FitnessRandomChickenInSwarm-FitnessThisChicken)
        # NOTE: FitnessRoosterGroupmate and FitnessRandomChickenInSwarm cannot be the same chicken

        # get the rooster information
        group_rooster_idx = int(self.chicken_info[particle][1]) #also the group index
        rooster_loc = self.M[group_rooster_idx]
        fitness_rooster = np.linalg.norm(self.F_Pb[group_rooster_idx])
        
        # get the random chicken information
        # initial random
        random_chicken_idx = self.rng.integers(0, self.number_of_particles)
        # random cannot be the idx of the rooster, the current chicken, or be from a chick
        while (random_chicken_idx == group_rooster_idx) or \
                        (random_chicken_idx == particle) or \
                        (int(self.chicken_info[random_chicken_idx][0]) == 3):
            random_chicken_idx = self.rng.integers(0, self.number_of_particles)

        random_chicken_loc = self.M[random_chicken_idx]
        fitness_random_chicken = np.linalg.norm(self.F_Pb[random_chicken_idx])

        fitness_this_chicken = np.linalg.norm(self.F_Pb[particle])

        # epsilon = 'smallest system constant'. improvised.
        epsilon = 10e-50 

        # exp((FitnessThisChicken-FitnessRoosterGroupmate)/(abs(FitnessThisChicken)+epsilon))
        #S1 = np.exp((fitness_this_chicken-fitness_rooster)/(np.abs(fitness_this_chicken) + epsilon))
        clipped_val = np.clip(((fitness_this_chicken-fitness_rooster)/(np.abs(fitness_this_chicken) + epsilon)), -700.00, 700.00)
        S1 = np.exp(clipped_val)
        # S1*RANDOM(0-to-1)*(LocationRoosterGroupmate-thisChickenLocation)
        # these terms can overflow because of the exp()
        # some S2 results are evaluating on the scale of 8.218407461554972e+307
        # these clipped bounds are effectively are zero and inf
        # term_1 = S1*self.rng.uniform(0,1)*(rooster_loc-self.M[particle])
        # still dealing with overflow issues. apply cap to S1
        if S1 > 10e50:
            S1 = 10e50
        elif S1 < -10e50:
            S1 = -10e50
        clipped_term1 = np.clip((S1*self.rng.uniform(0,1)*(rooster_loc-self.M[particle])), -10e50, 10e10)
        term_1 = clipped_term1

        #S2 = np.exp(float(fitness_random_chicken-fitness_this_chicken))
        #np.exp(...) throws overflow errors. Using clip as a generic catch
        clipped_val = np.clip((fitness_random_chicken-fitness_this_chicken), -700.00, 700.00)
        S2 = np.exp(clipped_val)
        #S2*RANDOM(0-to-1)*(LoctionRandomChickenInSwarm-thisChickenLocation)

        # these terms can overflow because of the exp()
        # some S2 results are evaluating on the scale of 8.218407461554972e+307
        # these clipped bounds are effectively are zero and inf
        #term_2 = S2*self.rng.uniform(0,1)*(random_chicken_loc-self.M[particle])
        # This still causes overflow:
        # clipped_term2 = np.clip((S2*self.rng.uniform(0,1)*(random_chicken_loc-self.M[particle])), -10e50, 10e10)
        if S2 > 10e50:
            S2 = 10e50
        elif S2 < -10e50:
            S2 = -10e50

        clipped_term2 = np.clip((S2*self.rng.uniform(0,1)*(random_chicken_loc-self.M[particle])), -10e50, 10e10)
        term_2 = clipped_term2

        # new_loc = old_loc + term_1 + term_2
        self.M[particle] = self.M[particle] + term_1 + term_2


    def move_chick(self, particle):
        #nextLoc = currentLoc + FL*(locationMother - currentLoc)
        # NOTE: FL is a value 0 or 2 that determines if a chick follows the mother
        #  The chick RANDOMLY chooses between 0 or 2

        mother_idx = int(self.chicken_info[particle][2]) # the the idx of the mother chicken
        mother_loc = self.M[mother_idx]
        self.M[particle] = self.M[particle] + self.rng.choice([0,2])*(mother_loc-self.M[particle])

    def reorganize_swarm(self):
        # rank the chickens' fitness vals and establish hierarchial order
        # divide swarm into groups, determine relationship between mother hens and chicks

        #get the indexs that sort the personal best fitness from best (lowest) to worst
        l2_norm_vals = []
        for idx in range(0, self.number_of_particles):
            l2_norm_vals.append(np.linalg.norm(self.F_Pb[idx]))
      
        fitness_sort_idx = np.argsort(l2_norm_vals)# lowest are first
        
        #use the idx values to sort self.M and personal best fitness self.F_Pb
        temp_M = 1*self.M
        temp_F_Pb = 1*self.F_Pb
        temp_Active = 1*self.Active #tracking which are active
        ctr = 0

        for idx in fitness_sort_idx:
            temp_M[ctr] = self.M[idx]
            temp_F_Pb[ctr] = self.F_Pb[idx]
            temp_Active[ctr] = self.Active[idx]
            ctr = ctr + 1
        self.M = 1*temp_M
        self.F_Pb = 1*temp_F_Pb
        self.Active = 1*temp_Active

        # update the chicken_information (category, group, mother-child ID)
        # top RN are roosters. Middle HN are hens, with MN being mother hens.
        # last (and worst preforming) are chicks

        # make temp classification list
        classList = np.zeros(self.number_of_particles)
        # rooster
        classList[0:self.RN] = 0
        # hen
        start = self.RN
        end = self.RN + self.HN
        classList[start:end] = 1
        # mother hen
        start = self.RN + self.HN
        end = self.RN + self.HN + self.MN
        classList[start:end] = 2
        # chicks
        start = self.RN + self.HN + self.MN
        classList[start:] = 3
        # array of groups to use in random allocation
        group_nums = np.arange(self.RN)

        # first rooster, to reset the array
        self.chicken_info = np.array([0, 0, -1])

        for i in range(1,int(self.number_of_particles)):
            if classList[i] == 0: #rooster
                # assign to the next group (i-1), and done.
                # CLASSIFICATION(0-4), GROUP(0-m), MOTHER-CHILD ID
                self.chicken_info = \
                    np.vstack([self.chicken_info, [classList[i], i, -1]])

            elif (classList[i] == 1) or (classList[i] == 2): #hen, mother hen
                # assign to a random group.
                # CLASSIFICATION(0-4), GROUP(0-m), MOTHER-CHILD ID
                hen_group = self.rng.choice(group_nums)
                self.chicken_info = \
                    np.vstack([self.chicken_info,[classList[i], hen_group, -1]])

            elif classList[i] == 3: #chick
                # select a random hen to be the 'mother' and assign to group
                # CLASSIFICATION(0-4), GROUP(0-m), MOTHER-CHILD ID
                groupAssigned = False
                while (groupAssigned == False):
                    chicken_idx = self.rng.integers(0, i-1, endpoint=False)# index after a chick will always be the chick
                    if self.chicken_info[chicken_idx][0] == 2: #is mother hen
                        # get the group the random mother hen is from
                        mother_group = self.chicken_info[chicken_idx][1]         
                        # assign chick to group, and to that mother hen                    
                        self.chicken_info = \
                            np.vstack([self.chicken_info,[classList[i], mother_group, chicken_idx]])

                        groupAssigned = True


  
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
                "Current Particle Active\n" + \
                str(self.Active[self.current_particle]) +"\n" + \
                "Current Particle Location\n" + \
                str(self.M[self.current_particle]) +"\n" + \
                "Absolute mean deviation\n" + \
                str(self.absolute_mean_deviation_of_particles()) +"\n" + \
                "-----------------------------"
            self.debug_message_printout(msg)
            
        if self.allow_update: # The first time step is called, this is false
            if self.Active[self.current_particle]:
                # save global best
                self.check_global_local(self.Flist,self.current_particle)

                # every self.G full cycle iterations reorganize the swarm
                #  self.G_steps is the # of chickens multiplied by the generations for the number of iterations
                if self.iter%self.G_steps == 0:

                    self.reorganize_swarm()
                    #start with the new best rooster
                    self.current_particle = 0
                
                # move chickens
                # roosters are always at the top of the list so that they're moved first.
                # Then the hens are moved. It doesn't matter which type of hen is moved first.
                # Chicks are moved last so that they can follow the mother hens
                chicken_type = self.chicken_info[self.current_particle][0]
                if chicken_type == 0: #update rooster location
                    self.move_rooster(self.current_particle)

                elif (chicken_type == 1): #update hen
                    self.move_hen(self.current_particle)

                elif (chicken_type == 2): #update hen location
                    self.move_hen(self.current_particle)

                elif chicken_type == 3: #update chick location
                    self.move_chick(self.current_particle)

                # handle any out-of-bounds situation
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
        swarm_export = {'lbound': self.lbound,
                        'ubound': self.ubound,
                        'M': self.M,
                        'V': self.V,
                        'Gb': self.Gb,
                        'F_Gb': self.F_Gb,
                        'Pb': self.Pb,
                        'F_Pb': self.F_Pb,
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
        self.V = swarm_export['V'] 
        self.Gb = swarm_export['Gb'] 
        self.F_Gb = swarm_export['F_Gb'] 
        self.Pb = swarm_export['Pb'] 
        self.F_Pb = swarm_export['F_Pb'] 
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

