#! /usr/bin/python3

##--------------------------------------------------------------------\
#   sand_cat_python
#   './sand_cat_python/src/cat_swarm.py'
#   A basic sand cat swarm optimization class. See the README for
#       publication details.
#       
#
#   Author(s): Lauren Linkous, Jonathan Lundquist
#   Last update: August 18, 2024
##--------------------------------------------------------------------\


import numpy as np
from numpy.random import Generator, MT19937, shuffle
import sys
np.seterr(all='raise')


class swarm:
    # arguments should take form: 
    # swarm(int, [[float, float, ...]], [[float, float, ...]], 
    #  [[float, ...]], int, [[float, ...]], 
    #  float, int, int, 
    #  func, func,
    #  class object, bool) 
    # int boundary 1 = random,      2 = reflecting
    #              3 = absorbing,   4 = invisible
    def __init__(self, NO_OF_PARTICLES, lbound, ubound,
                 output_size, targets,
                 E_TOL, maxit, boundary, 
                 obj_func, constr_func,
                 parent=None, detailedWarnings=False):  

        
        # Optional parent class func call to write out values that trigger constraint issues
        self.parent = parent 
        # Additional output for advanced debugging to TERMINAL. 
        # Some of these messages will be returned via debugTigger
        self.detailedWarnings = detailedWarnings 

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
                self.parent.updateStatusText("Error lbound and ubound must be 1xN-dimensional \
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

            '''
            self.M                      : An array of current particle (cat) locations.
            self.S                      : Maximum sensitivity range. Constant.
            self.rg                     : General sensitivity range that is decreased linearly from 2 to 0
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
            self.InitDeviation          : Initial deviation of particles.
            self.delta_t                : static time modulation. retained for comparison to original repo. and swarm export
            '''
            self.S = 2
            self.rg = None # set at the start of iterating through a population
            self.output_size = output_size
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
  
    def exploitation_mode(self, particle):
        # NOTE: in MATLAB rand() returns a random scalar drawn from the uniform distribution in the interval (0,1).
        # MATLAB implementation: r = rand() * rg
        # Python equivalent:  np.random.uniform()  . However, uniform() is a half-open interval such that [0, 1)
        
        r = self.rng.uniform()*self.rg
        
        
        # NOTE:
        # the MATLAB code provided with the paper uses 2 nested for loops in order
        # to set each dimension of the agent (cat) seperately. This is similar
        # to the original cat swarm allowing the user to choose an integer for 
        # how many dimensions to mutate.

        # start with current agent position so the shape is always retained
        rand_position = self.M[particle]

        # generate an array of random thetas (the routlette wheel selction from 1:360 degs)
        random_thetas = self.rng.integers(low=1, high=360, size=len(rand_position), endpoint=True)
        # generate an array of random numbers 
        rand_nums = (self.rng.uniform(0,1,len(rand_position)))

        rand_position = abs(rand_nums*np.hstack(self.Gb)-self.M[particle])
        self.M[particle] = np.hstack(self.Gb)-r*rand_position*np.cos(random_thetas)


    def exploration_mode(self, particle):
        # NOTE: in MATLAB rand() returns a random scalar drawn from the uniform distribution in the interval (0,1).
        # MATLAB implementation: r = rand() * rg
        # Python equivalent:  np.random.uniform()  . However, uniform() is a half-open interval such that [0, 1)
        
        r = self.rng.uniform()*self.rg

        # adaption of:
        # cp=floor(SearchAgents_no*rand()+1);
        # CandidatePosition =Positions(cp,:);
        # Positions(i,j)=r*(CandidatePosition(j)-rand*Positions(i,j));

        # choose an idx based off random agent from the cat herd
        # idx is from [0, number of particles). idx from 0 so do not include high
        agent_idx =self.rng.integers(low=0, high=self.number_of_particles, endpoint=False) 
        # get the location of the agent from the idx
        candidate_position = self.M[agent_idx]
        # generate the random numbers to mutate n-dims of the position
        rand_nums = (self.rng.uniform(0,1,len(candidate_position)))
        # update the location with a mix of the candidate position and the current agent loc
        self.M[particle] = r*(candidate_position-rand_nums*self.M[particle] )
        
  
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
                "Absolute mean deviation\n" + \
                str(self.absolute_mean_deviation_of_particles()) +"\n" + \
                "-----------------------------"
            self.error_message_generator(msg)
            
        if self.allow_update: # The first time step is called, this is false
            if self.Active[self.current_particle]:
                # save global best
                self.check_global_local(self.Flist,self.current_particle)
                # 
                if self.current_particle == 0:
                    # Update the sensitivity range

                    # NOTE:
                    # https://www.mathworks.com/matlabcentral/fileexchange/110185-sand-cat-swarm-optimization
                    # Following the algrithm provided by the author, these ranges are set for the entire group
                    # of cats until they've all been iterated over once. This is distinct from some other 
                    # sand/cat swarm algorithms that were popular at the time of writing this code.

                    #self.S = 2  # Maximum sensitivity range. Constant. Set in _init_()
                    self.rg = self.S-((self.S)*self.iter/(self.maxit)) # guides R
                    # NOTE:
                    # matlab code uses: S-((S)*t/(Max_iter))
                    # paper equation uses: S - (2*S*t)/(2*max_iterations), equation 1. 
                    # Difference is simplification.


                # r is generated in the mode func()
                # R, but avoiding CONSTANT notation
                R_transition = (2 * self.rg) * self.rng.uniform() - self.rg # controls transition phases

                # split cats into the algorithm's 2 phases
                if np.abs(R_transition)<=1: # R value is between -1 and 1 
                    # Exploitation (attacking prey)
                    self.exploitation_mode(self.current_particle)
                else: 
                    # Exploration phase
                    self.exploration_mode(self.current_particle)


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