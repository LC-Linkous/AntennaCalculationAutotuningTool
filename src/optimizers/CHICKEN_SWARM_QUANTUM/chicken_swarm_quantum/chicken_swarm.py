#! /usr/bin/python3

##--------------------------------------------------------------------\
#   chicken_swarm_quantum
#   './chicken_swarm_quantum/src/chicken_swarm.py'
#   A quantum-inspired chicken swarm optimization class. This class follows the same 
#
#   This approach mimics a general and very simple probabilistic approach.
#       It is not meant to directly mimic qiskit or other libraries.
#       This is a snapshot of some of the most basic behavior found in
#       literature.     
#
#   Author(s): Lauren Linkous
#   Last update: November 28, 2024
##--------------------------------------------------------------------\
#! /usr/bin/python3


import numpy as np
from numpy.random import Generator, MT19937
import sys
import time
np.seterr(all='raise')


class swarm:
    # arguments should take form: 
    # swarm(int, 
    # [[float, float, ...]], [[float, float, ...]], [[float, ...]], 
    # int, [[float, ...]], 
    # float, int, int, func, func,
    # int, int, int, int, int,
    # obj, bool) 
    # int boundary 1 = random,      2 = reflecting
    #              3 = absorbing,   4 = invisible
    def __init__(self, NO_OF_PARTICLES, 
                 lbound, ubound,
                 output_size, targets,
                 E_TOL, maxit, boundary, 
                 obj_func, constr_func,
                 RN=3, HN=12, MN=8, CN=15, G=150,
                 beta=0.5, quantum_roosters=False,
                 parent=None, detailedWarnings=False,
                 runningWithSim=True):  

        
        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 
        # Additional output for advanced debugging to TERMINAL. 
        # Some of these messages will be returned via debugTigger
        self.detailedWarnings = detailedWarnings 

        # AntennaCAT vars
        self.runningWithSim=runningWithSim


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
            
            self.G = G      # num steps to update chicken status
 
            # error checking on population split
            total_chickens = RN + HN + MN + CN
            if (NO_OF_PARTICLES < total_chickens):
                self.parent.debug_message_printout("WARNING: number of chickens adds up to more \
                                                   than the expected number of particles. Attempting fix.")
                # subtract number of roosters and chicks. rest are hens
                num_hens = NO_OF_PARTICLES - RN - CN
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

                    # print("chicken info")
                    # print(np.shape(self.chicken_info))
                    # print(self.chicken_info)
                    # print(self.chicken_info[0][chicken_idx])
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
            self.quantum_roosters       : Boolean. 
            self.beta                   : Float constant controlling influence between the personal and global best positions
            self.output_size            : An integer value for the output size of obj func (y-vals)
            self.input_size             : An integer value for the input size of the obj func (x-vals)
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
            self.InitDeviation          : Initial deviation of particles.
            self.delta_t                : static time modulation. retained for comparison to original repo. and swarm export
            '''


            self.quantum_roosters = quantum_roosters
            self.beta = beta
            self.output_size = output_size
            self.input_size = len(lbound)
            self.Active = np.ones((NO_OF_PARTICLES))                        
            self.Gb = sys.maxsize*np.ones((1,np.max([heightl, widthl])))   
            self.F_Gb = sys.maxsize*np.ones((1,output_size))                
            self.Pb = sys.maxsize*np.ones(np.shape(self.M))                 
            self.F_Pb = sys.maxsize*np.ones((NO_OF_PARTICLES,output_size))  
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
            self.InitDeviation = self.absolute_mean_deviation_of_particles()
                                         

            self.error_message_generator("swarm successfully initialized")

    def call_objective(self, allow_update):
        if self.Active[self.current_particle]:
            # call the objective function. If there's an issue with the function execution, 'noError' returns False
            newFVals, noError = self.obj_func(self.M[self.current_particle], self.output_size)
            if noError == True:
                self.Fvals = np.array(newFVals).reshape(-1, 1)
                if allow_update:
                    self.Flist = abs(self.targets - self.Fvals)
                    self.iter = self.iter + 1
                    self.allow_update = 1
                else:
                    self.allow_update = 0
            return noError# return is for error reporting purposes only
   
    # MOVEMENT MODELS
    def move_rooster(self, particle):
        # roosters in this class can exhibit classical or quantum behavior based on a user-set bool

        if self.quantum_roosters == False:

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
                clipped_val = np.clip(((random_rooster_fitness-this_rooster_fitness)/(abs(this_rooster_fitness)+epsilon)), -709.00, 709.00)
                sig_squared = np.exp(clipped_val)


            #update new location based on random()
            self.M[particle] = self.M[particle]*(1+self.rng.normal(0, sig_squared))
        
        else:

            # duplicate locals to stick with eqs. in README
            p = self.Pb[particle]             # personal best
            g = self.Gb                       # global best

            # Mean Best Position (for the cat)
            mb = self.beta* p + (1 - self.beta) * g

            # Position Update (Update Rule)
            u = self.rng.uniform(size=(1,self.input_size))
            self.M[particle] = mb + self.beta * np.abs(p - g) * np.log(1 / u)


    def move_hen(self, particle):

        # get the rooster information
        group_rooster_idx = int(self.chicken_info[particle][1]) #also the group index
        rooster_loc = self.M[group_rooster_idx]

        # duplicate locals to stick with eqs. in README
        p = self.Pb[particle]             # personal best
        g = rooster_loc                   # rooster best bc that's the well

        # Mean Best Position
        mb = self.beta* p + (1 - self.beta) * g

        # Position Update (Update Rule)
        u = self.rng.uniform(size=(1,self.input_size))
        self.M[particle] = mb + self.beta * np.abs(p - g) * np.log(1 / u)



    def move_chick(self, particle):
        
        # get the mother hen location
        mother_idx = int(self.chicken_info[particle][2]) # the the idx of the mother chicken
        mother_loc = self.M[mother_idx]

        # duplicate locals to stick with eqs. in README
        p = self.Pb[particle]             # personal best
        g = mother_loc                    # mother best bc that's the well

        # Mean Best Position
        mb = self.beta* p + (1 - self.beta) * g

        # Position Update (Update Rule)
        u = self.rng.uniform(size=(1,self.input_size))
        self.M[particle] = mb + self.beta * np.abs(p - g) * np.log(1 / u)


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
        self.chicken_info = [0, 0, -1]

        for i in range(1,int(self.number_of_particles)):
            if classList[i] == 0: #rooster
                # assign to the next group (i-1), and done.
                # CLASSIFICATION(0-4), GROUP(0-m), MOTHER-CHILD ID
                self.chicken_info = \
                    np.vstack([self.chicken_info,[classList[i], i, -1]])

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
            self.error_message_generator("Error: No boundary is set!")

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
        max_iter = self.iter > self.maxit
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
            self.error_message_generator(msg)
            
        if self.allow_update: # The first time step is called, this is false
            if self.Active[self.current_particle]:
                # save global best
                self.check_global_local(self.Flist,self.current_particle)

                # every self.G iterations, reorganize the swarm
                if self.iter%self.G == 0:
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
                self.current_particle = 0
            if self.complete() and not suppress_output:
                msg =  "\nPoints: \n" + str(self.Gb) + "\n" + \
                    "Iterations: \n" + str(self.iter) + "\n" + \
                    "Flist: \n" + str(self.F_Gb) + "\n" + \
                    "Norm Flist: \n" + str(np.linalg.norm(self.F_Gb)) + "\n"
                self.error_message_generator(msg)

    def export_swarm(self):
        swarm_export = {'lbound': self.lbound,
                        'ubound': self.ubound,
                        'M': self.M,
                        'Gb': self.Gb,
                        'F_Gb': self.F_Gb,
                        'Pb': self.Pb,
                        'F_Pb': self.F_Pb,
                        'targets': self.targets,
                        'maxit': self.maxit,
                        'E_TOL': self.E_TOL,
                        'iter': self.iter,
                        'delta_t': self.delta_t,
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
        return self.Gb 
    
    def get_optimized_outs(self):
        return self.F_Gb
    
    def absolute_mean_deviation_of_particles(self):
        mean_data = np.array(np.mean(self.M, axis=0)).reshape(1, -1)
        abs_data = np.zeros(np.shape(self.M))
        for i in range(0,self.number_of_particles):
            abs_data[i] = np.squeeze(np.abs(self.M[i]-mean_data))

        abs_mean_dev = np.linalg.norm(np.mean(abs_data,axis=0))
        return abs_mean_dev


    def error_message_generator(self, msg):
        if self.parent == None:
            print(msg)
        else:
            self.parent.updateStatusText(msg)
