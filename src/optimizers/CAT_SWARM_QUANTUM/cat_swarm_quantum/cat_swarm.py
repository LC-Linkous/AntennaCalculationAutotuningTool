#! /usr/bin/python3

##--------------------------------------------------------------------\
#   cat_swarm_quantum
#   './cat_swarm_quantum/src/cat_swarm.py'
#   A quantum-inspired Cat swarm optimization class. This class follows the same 
#       format as pso_python and pso_basic to make them interchangeable
#       in function calls. 
#       
#
#   Author(s): Lauren Linkous
#   Last update: November 28, 2024
##--------------------------------------------------------------------\


import numpy as np
from numpy.random import Generator, MT19937, shuffle
import sys
import time
np.seterr(all='raise')


class swarm:
    # arguments should take form: 
    # swarm(int, [[float, float, ...]], 
    # [[float, float, ...]], [[float, ...]], 
    # float, int, [[float, ...]], float, 
    # float, int, int, func) 
    # int boundary 1 = random,      2 = reflecting
    #              3 = absorbing,   4 = invisible
    def __init__(self, NO_OF_PARTICLES, lbound, ubound,
                 weights, output_size, targets,
                 E_TOL, maxit, boundary, 
                 obj_func, constr_func,
                 MR=0.12, SMP=5, SRD=0.2, CDC=2, SPC=False,
                 beta=0.5,
                 parent=None, detailedWarnings=False, runningWithSim=False):  

        
        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 
        # Additional output for advanced debugging to TERMINAL. 
        # Some of these messages will be returned via debugTigger
        self.detailedWarnings = detailedWarnings 

        #antennaCAT vars
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
            self.output_size = output_size
            self.input_size = len(lbound)
            self.Active = np.ones((NO_OF_PARTICLES))                        
            self.Gb = sys.maxsize*np.ones((1,np.max([heightl, widthl])))   
            self.F_Gb = sys.maxsize*np.ones((1,output_size))                
            self.Pb = sys.maxsize*np.ones(np.shape(self.M))                 
            self.F_Pb = sys.maxsize*np.ones((NO_OF_PARTICLES,output_size))  
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




            self.error_message_generator("swarm successfully initialized")
            

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
                        self.Flist = abs(self.targets - self.Fvals)
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
                "Current Particle Location\n" + \
                str(self.M[self.current_particle]) +"\n" + \
                "Current Seeking/Tracing Status\n" + \
                str(self.cat_mode[self.current_particle]) +"\n" + \
                "Absolute mean deviation\n" + \
                str(self.absolute_mean_deviation_of_particles()) +"\n" + \
                "-----------------------------"
            self.error_message_generator(msg)
            
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