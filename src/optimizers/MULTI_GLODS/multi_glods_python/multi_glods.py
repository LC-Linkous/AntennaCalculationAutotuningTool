#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multi_glods.py'
#   Class for intializing and interfacing with the multiGLODS algorithm
#   NOTE: multiglods.py is the statemachine, 
#       and multiglods_ctl.py is the controller
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: March 13, 2025
##--------------------------------------------------------------------\


import numpy as np
import sys

try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multiglods_ctl import one_time_init
    from multiglods_helpers import f_eval_objective_call
    from multiglods import multiglods

except:# for local, unit testing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import one_time_init
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import f_eval_objective_call
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods import multiglods

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
                    surrogateOptimizer=None): # used for format streamlining


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

   
        #reformat since multi_glods needs single []
        # LB = LB[0]
        # UB = UB[0]

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
                print("WARNING: THRESHOLD option selected.  +\
                Dimensions for THRESHOLD do not match TARGET array. Defaulting to TARGET search.")
                evaluate_threshold = False
                THRESHOLD = None
            else:
                evaluate_threshold = evaluate_threshold #bool
                THRESHOLD = np.array(obj_threshold).reshape(-1, 1) #np.array
        




        self.init, self.run_ctl, self.alg, \
            self.prob, self.ctl, self.state = \
                one_time_init(NO_OF_VARS, LB, UB, TARGETS, E_TOL, R_TOL, MAXIT,
                              BP, GP, SF, obj_func, constr_func, evaluate_threshold, THRESHOLD)

        self.prob['parent'] = parent
        self.done = 0

    def step(self, suppress_output):
        self.done, self.init, self.run_ctl, \
            self.alg, self.prob, self.ctl, self.state = \
                multiglods(self.init, self.run_ctl, self.alg, 
                           self.prob, self.ctl, self.state, 
                           suppress_output)
        
   
    def call_objective(self, allow_update):
        self.state, self.prob, noErrorBool = f_eval_objective_call(self.state, 
                                                      self.prob, 
                                                      self.ctl,
                                                      allow_update)
        return noErrorBool

    def export_glods(self):
        glods_export = {'init': self.init, 'run_ctl': self.run_ctl,
                        'alg': self.alg, 'prob': self.prob,
                        'ctl': self.ctl, 'state': self.state}
        return glods_export
    
    def import_glods(self, glods_export, obj_func):
        self.init = glods_export['init']
        self.run_ctl = glods_export['run_ctl']
        self.alg = glods_export['alg']
        self.prob = glods_export['prob']
        self.ctl = glods_export['ctl']
        self.state = glods_export['state']
        self.ctl['obj_func'] = obj_func

    # swapping this version out for one that matches the AntennaCAT standard set
    # def complete(self):
    #     return self.done
    
    def get_obj_inputs(self):
        if self.state['init']:
            return self.init['x_ini']
        else:
            return self.prob['xtemp']
        
    def get_convergence_data(self):
        # used the L2 norm to get the distance from target
        # distance from target at each metric (Flist) has already been handled 

        if len(np.shape(self.ctl['Flist'])) > 1:
            best_eval = np.linalg.norm(self.ctl['Flist'][:,0])
        else:
            best_eval = np.linalg.norm(self.ctl['Flist'])

        # return iteration for objective function call.
        #  There's several 'iter' counters.
        #  self.run_ctl['iter'] : 
        #  self.ctl['objective_iter'] : objective func call counter   
    
        iteration = 1*self.ctl['objective_iter']
        return iteration, best_eval 

    def get_optimized_soln(self):
        soln = np.vstack(self.prob['Plist'][:,0])
        return soln
    
    def get_optimized_outs(self):
        soln = np.vstack(self.ctl['Flist'][:,0])
        return soln
    

    # for plotting
    def get_search_locations(self):
        x_locations = self.prob['Plist'] 
        return x_locations

    def get_fitness_values(self):
        x_locations = self.ctl['Flist']
        return x_locations

    # funcs from other optimizers in the AntennaCAT set for stop conditions
    def converged(self):
       
        if np.shape(self.ctl['Flist'])[0] == 0:
            return False
        elif len(np.shape(self.ctl['Flist'])) > 1:
            best_eval = np.linalg.norm(self.ctl['Flist'][:,0])
        else:
            best_eval = np.linalg.norm(self.ctl['Flist'])

        convergence = best_eval < self.alg['err_tol_stop'] #E_TOL comparison. returns bool
        return convergence
    
    def maxed(self):
        max_iter = self.ctl['objective_iter'] >= self.ctl['maxit']
        return max_iter
    
    def complete(self):
        # includes  self.done from this optimizer, and the standardized  'self.converged() or self.maxed()'
        done = self.done or self.maxed() or self.converged() 
        # print("CHECK COMPLETE")
        # print(self.done)
        # print(self.maxed())
        # print(self.converged())

        return done
