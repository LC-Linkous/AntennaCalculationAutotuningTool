#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multi_glods.py'
#   Class for intializing and interfacing with the multiGLODS algorithm
#   NOTE: multiglods.py is the statemachine, 
#       and multiglods_ctl.py is the controller
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: November 5, 2025
##--------------------------------------------------------------------\


import numpy as np
import sys
import logging
logger = logging.getLogger(__name__)

try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multiglods_ctl import one_time_init
    from multiglods_helpers import f_eval_objective_call
    from multiglods import multiglods

except:# for local, unit testing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import one_time_init
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import f_eval_objective_call
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods import multiglods
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import f_eval_return

class multi_glods:
    # arguments should take the form: 
    # multi_glods([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj,
    # bool, [int, int, ...]
    # bool, class obj) 
    #  
    # opt_df contains class-specific tuning parameters
    # BP: float
    # GP: int
    # SF: int
    #


    def __init__(self, LB, UB, TARGETS, TOL, MAXIT,
                    obj_func, constr_func, 
                    opt_df,
                    parent=None, 
                    evaluate_threshold=False, obj_threshold=None,
                    useSurrogateModel=False,  # This optimizer cannot use an internal optimizer
                    surrogateOptimizer=None,  # used for format streamlining
                    decimal_limit = 4):      # this is used in this optimizer


        # vars for using surrogate model
        self.useSurrogateModel = useSurrogateModel # bool for if using surrogate model
        self.surrogateOptimizer = surrogateOptimizer     # pass in the class for the surrogate model
                                                   # optimizer. this is configured as needed 




        #unpack the opt_df standardized vals
        BP = float(opt_df['BP'][0])
        GP = float(opt_df['GP'][0])
        SF = float(opt_df['SF'][0])
        R_TOL = float(opt_df['R_TOL'][0]) #override because this is the RADIUS not the ERROR tolerance
                                        # this version of multiGLODS
                                        # R_TOL becomes 'tol_stop' & 'tol_active_points' in the polling step. 

   
        # NOTE: this is a difference in optimizer structures that's compensated for in the controller
        #reformat since multi_glods needs single []
        LB = LB[0]
        UB = UB[0]

        # enforce typing
        NO_OF_VARS = int(len(LB))
        E_TOL = float(TOL) #the l2norm distance from target
        MAXIT = int(MAXIT)
        TARGETS = TARGETS


        #evaluation method for targets
        # True: Evaluate as true targets
        # False: Evaluate as thesholds based on information in obj_threshold
        if evaluate_threshold==False:
            THRESHOLD = None # for error checking later via wrapper

        else:
            if not(len(obj_threshold) == len(TARGETS)):
                logger.info("WARNING: THRESHOLD option selected.  +\
                Dimensions for THRESHOLD do not match TARGET array. Defaulting to TARGET search.")
                evaluate_threshold = False
                THRESHOLD = None
            else:
                evaluate_threshold = evaluate_threshold #bool
                THRESHOLD = np.array(obj_threshold).reshape(-1, 1) #np.array
        

        self.init, self.run_ctl, self.alg, \
            self.prob, self.ctl, self.state = \
                one_time_init(NO_OF_VARS, LB, UB, TARGETS, E_TOL, R_TOL, MAXIT,
                              BP, GP, SF, obj_func, constr_func, evaluate_threshold, THRESHOLD, decimal_limit)

        self.prob['parent'] = parent
        self.done = 0

    def step(self, suppress_output):
        self.done, self.init, self.run_ctl, \
            self.alg, self.prob, self.ctl, self.state = \
                multiglods(self.init, self.run_ctl, self.alg, 
                           self.prob, self.ctl, self.state, 
                           suppress_output)
        
   
    def call_objective(self, allow_update):
        # this is called from outside by the optimizer controller.\
        self.state, self.prob, noErrorBool = f_eval_objective_call(self.state, 
                                                      self.prob, 
                                                      self.ctl,
                                                      allow_update)
        return noErrorBool

    def export_configuration(self):
        glods_export = {'init': self.init, 'run_ctl': self.run_ctl,
                        'alg': self.alg, 'prob': self.prob,
                        'ctl': self.ctl, 'state': self.state}
        return glods_export
    
    def import_configuration(self, glods_export) : #, obj_func):
        self.init = glods_export['init']
        self.run_ctl = glods_export['run_ctl']
        self.alg = glods_export['alg']
        self.prob = glods_export['prob']
        self.ctl = glods_export['ctl']
        self.state = glods_export['state']
        #self.ctl['obj_func'] = obj_func #add this back with the streamline

    # swapping this version out for one that matches the AntennaCAT standard set
    # def complete(self):
    #     return self.done
    
    def get_obj_inputs(self):
        if self.state['init']:
            return self.init['x_ini']
        else:
            return self.prob['xtemp']
        
    def get_convergence_data(self):
        # used the L2 norm to get the distance magnitude from target
        # distance from target at each metric (Flist) has already been handled 

        # Note: this is used by the outer controller for logging progress, NOT the optimizer

        if len(np.shape(self.ctl['Flist'])) > 1:
            best_eval = np.linalg.norm(self.ctl['Flist'][:,0])
        else:
            best_eval = np.linalg.norm(self.ctl['Flist'])

        iteration = 1*self.ctl['objective_iter']
        return iteration, best_eval 
    

    def get_optimized_soln(self):
        # this is the list of points
        soln = np.vstack(self.prob['Plist'][:,0])
        return soln
    
    
    def get_optimized_outs(self):
        # this is the results of running the simulation/math model
        soln = np.vstack(self.prob['FValtemp'])
        return soln
    
    
    def get_dist_from_target(self):
        # this is the convergence distance. Total COST of the current location
        soln = np.vstack(self.ctl['Flist'][:,0])
        return soln
    

    # for plotting
    def get_search_locations(self):
        x_locations = self.prob['Plist'] 
        return x_locations


    def get_fitness_values(self):
        # this list of ALL of the active points, where each of the values
        # is the DISTANCE from target, not the actual evaluated values.
        # think of these like COST values
        x_locations = self.ctl['Flist']
        return x_locations


    # funcs from other optimizers in the AntennaCAT set for stop conditions
    def converged(self):
        # the convergence looks at the L2 norm in terms of the convergence to the TARGET, 
        # not the radii tolerance. The MultiGLODS optimizer can terminate early based on that condition
        # but this is specific for the state machine


        # LEAVE THE COMMENTS FOR THE STRESS TEST DURATION
        # This should be fine, since we use the Flist across optimizers to check for convergence,
        # so I want to keep that the same across the set. HOWEVER, there is the interesting issue
        # where FValtemp is more accurate with some versions of the state machine we're testing.
        
        '''
        self.ctl['Flist']" the list of distances from the target for EACH particle in play
        self.prob['FValtemp']  the returned values from the last processed simulation
        self.prob['Ftemp'] last objective function evaluation
        '''



        #If we have unprocessed FValtemp, process it now for convergence check
        # This uses the new bypass for the objective function evaluation f_eval_return(...), which calls objective_function_evaluation(...) 
        # (both occur in multiglods_helpers.py). This bypass does NOT update the state of change ANY info (it passes the inputs right back out), 
        # but it does do the cost function evaluation
        #if len(self.prob['FValtemp']) > 0 and self.state['eval_return']: 
        # check every time as long as there's something in the value
        if len(self.prob['Ftemp']) > 0: 
            # Process the latest evaluation results
            self.state, self.prob = f_eval_return(self.state, self.prob, self.alg, 
                                                self.state['location'], bypass=True)

        # while this IS updated sooner than FList, it doesn't actually solve the issue where the data isn't
        # READ IN FROM FILE until the NEXT objective function is called.

        # HOWEVER, this does return the convergence value early enough to end the extra simulation before it
        # starts.

        if np.shape(self.prob['Ftemp'])[0] == 0:
            # early on, it's possible that there are no evaluated fitness values/active particles
            # if that is the case, ctl['Flist'] = []
            return False
        elif len(np.shape(self.prob['Ftemp'])) > 1:
            best_eval = np.linalg.norm(self.prob['Ftemp'][:,0])
        else:
            best_eval = np.linalg.norm(self.prob['Ftemp'])


        # # original just used the best/top Flist value
        # if np.shape(self.ctl['Flist'])[0] == 0:
        #     # early on, it's possible that there are no evaluated fitness values/active particles
        #     # if that is the case, ctl['Flist'] = []
        #     return False
        # elif len(np.shape(self.ctl['Flist'])) > 1:
        #     best_eval = np.linalg.norm(self.ctl['Flist'][:,0])
        # else:
        #     best_eval = np.linalg.norm(self.ctl['Flist'])

        convergence = best_eval <= self.alg['err_tol_stop'] #E_TOL comparison. returns bool

        return convergence
    

    def maxed(self):
        max_iter = self.ctl['objective_iter'] >= self.ctl['maxit']
        return max_iter
    

    def complete(self):
        # includes  self.done from this optimizer, and the standardized  'self.converged() or self.maxed()'
        done = bool(self.done) or self.maxed() or self.converged() 

        return done
