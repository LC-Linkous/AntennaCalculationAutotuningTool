#! /usr/bin/python3

##--------------------------------------------------------------------\
#   surrogate_model_optimization
#   './surrogate_model_optimization/src/optimizers/multi_glods/multiglods_helpers.py'
#   MultiGLODS helper functions for supporting algorithm, controller, 
#       and statemachine
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: May 18, 2025
##--------------------------------------------------------------------\


import numpy as np
import copy

# check feasibility
def feasible(x, ubound, lbound, n, ctl):
    feas = 1
    bound = np.array([[x - ubound], [lbound - x]])
    if np.sum(bound <= 0) != 2*n:
        feas = 0
    if feas:
        feas = ctl['constr_func'](x)
    return feas

# increment iteration
def inc_iter(ctl, run_ctl):
    if not (ctl['poll_loop'] or ctl['search_loop']):
        run_ctl['iter'] = run_ctl['iter'] + 1

    return run_ctl

# replicate 
def replicate(v, M):
    if np.ndim(v) < 2:
        v = np.array([v])

    M_new = np.hstack([M, np.tile(v[0][0], (np.shape(M)[0], 1))])
    if (np.shape(v)[0] > 1):
        for i in np.linspace(2, np.shape(v)[0], np.shape(v)[0]-1):
            M_new = np.vstack([M_new,
                               np.hstack([M,
                                          np.tile(v[int(i-1)],
                                                  (np.shape(M)[0],
                                                   1))])])

    return M_new

# logical indexing
def logical_index_1d(log_idx, list_in):
    log_idx = copy.deepcopy(log_idx)
    list_out = copy.deepcopy(list_in)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)

    ret_list = list_out

    if np.shape(np.shape(list_out))[0]:
        if np.shape(np.shape(list_out))[0] > 1:
            if np.shape(list_out)[0] > np.shape(list_out)[1]:
                length = np.shape(list_out)[0]
            else:
                length = np.shape(list_out)[1]
        else:
            length = np.shape(list_out)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[count] = np.squeeze(list_out)[i]
                    count = count+1

            else:
                if log_idx:
                    ret_list = list_out
                    count = count+1
        if np.shape(np.shape(ret_list))[0] > 1:
            ret_list = ret_list[0][0:count]
        else:
            ret_list = ret_list[0:count]

    return ret_list

# logical indexing
def logical_index_h2d(log_idx, list):
    log_idx = copy.deepcopy(log_idx)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)
    ret_list = list
    if np.shape(np.shape(list))[0]:
        if (np.shape(np.shape(list))[0] > 1):               
            length = np.shape(list)[1]
        else:         
            length = np.shape(list)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[:, count] = list[:, i]
                    count = count + 1
            else:
                if log_idx:
                    ret_list = list
                    count = count + 1
        if count:
            ret_list = ret_list[:, 0:count]

    return ret_list

# logical indexing
def logical_index_h2d_Plist(log_idx, list):
    log_idx = copy.deepcopy(log_idx)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)
    ret_list = list
    if np.shape(np.shape(list))[0]:

        if (np.shape(np.shape(list))[0] > 1):
            length = np.shape(list)[1]
        else:
            length = np.shape(list)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[:, count] = list[:, i]
                    count = count + 1
            else:
                if log_idx:
                    ret_list = list
                    count = count + 1
        if count:
            ret_list = ret_list[:, 0:count]

    return ret_list

# logical indexing
def logical_index_v2d(log_idx, list):
    log_idx = copy.deepcopy(log_idx)
    log_idx = log_idx.astype(int)
    ret_list = list

    if np.shape(np.shape(list))[0]:

        if np.shape(np.shape(list))[0] > 1:
            if np.shape(list)[0] > np.shape(list)[1]:
                length = np.shape(list)[0]
            else:
                length = np.shape(list)[1]
        else:
            length = np.shape(list)[0]
        count = 0
        for i in range(0, length):
            if log_idx[i]:
                ret_list[count, :] = list[i, :]
                count = count + 1

        ret_list = ret_list[0:count, :]

    return ret_list

# set value from logical index
def logical_set_val(log_idx, list, val):
    log_idx = copy.deepcopy(log_idx)
    log_idx = log_idx.astype(int)
    ret_list = list

    if np.shape(np.shape(list))[0]:
        if np.shape(np.shape(list))[0] > 1:
            if np.shape(list)[0] > np.shape(list)[1]:
                length = np.shape(list)[0]
            else:
                length = np.shape(list)[1]
        else:
            length = np.shape(list)[0]

        for i in range(0, length):
            if length == 1 and np.squeeze(log_idx):
                ret_list = val
            else:
                if np.squeeze(log_idx)[i]:
                    ret_list[i] = val[i]
    else:
        if log_idx:
            ret_list = val

    return ret_list

# debug statement for multiglods main loop
def print_debug(run_ctl, state, ctl, prob, init, alg, NO_OF_LOOPS, INSPECT_LOOP):

    if NO_OF_LOOPS == INSPECT_LOOP:
        print("run_ctl")
        print(run_ctl)
        print("state")
        print(state)
        print("ctl")
        print(ctl)
        print("prob")
        print(prob)
        print("init")
        print(init)
        print("alg")
        print(alg)
        state['main_loop']['run'] = 0

    NO_OF_LOOPS = NO_OF_LOOPS + 1
    return state, NO_OF_LOOPS

# mark objective function for evaluation
def  f_eval(state, xlist, prob, location):
    state['evaluate'] = 1
    state['location'] = location
    prob['xtemp'] = xlist   
    return state, prob

# handle objective function return at appropriate call location
def f_eval_return(state, prob, alg, location):
    if state['eval_return'] and (state['location'] == location):
        state['eval_return'] = 0

        ## We can either use the distance to target, 
        ## or include a threshold evaulation. 


        # The values for 'Ftemp' will 
        # be set to ctl['Flist'] in post_objective_init_loop

        prob['Ftemp'] = objective_function_evaluation(prob['FValtemp'], 
                                                    alg['targets'],
                                                    alg['evaluate_threshold'],
                                                    alg['threshold'])
    
        
        # # IF TARGET:
        # if alg['evaluate_threshold'] == False:
        #     prob['Ftemp'] = abs(alg['targets']-prob['FValtemp'])

            # target format here is:
            # [[0]
            #  [0]]

        # IF THRESHOLD:
        
    return state, prob

# call objective function, allow it to update when desired
def f_eval_objective_call(state, prob, ctl, allow_update):

    noErrorBool = True #this is pretty stable, 
                        # so default of true when NOT evaluating 
                        # has not shown issues in testing. 


    if state['evaluate']:
        # NOTE: this is a change from the original multiglods_helpers.py
        # the new objective functioon configuration takes a horizontal array.
        # prob['FValtemp'], noErrorBool = ctl['obj_func'](prob['parent'], prob['xtemp'])
        FVals, noErrorBool = ctl['obj_func'](np.hstack(prob['xtemp']))
        # NOTE: multiGLODS needs a vertically stacked array
        # print("SHAPE FVALS in multiglods_holders")
        # print(FVals)
        # print(np.shape(FVals))
        if noErrorBool == True:
            # this is the standard setup/shape for the AntennaCAT optimizer set. 
            # left here for featuing matching between optimizers. 
            prob['FValtemp'] = np.array(FVals).reshape(-1, 1)
            # print(prob['FValtemp'])
            # print(np.shape(prob['FValtemp']))   

            # adjust the fitness values output to be vertical to match multiGLODS expectations
            prob['FValtemp'] = np.vstack(prob['FValtemp'])  



            if allow_update:
                state['evaluate'] = 0
                state['eval_return'] = 1
                ctl['objective_iter'] = ctl['objective_iter']  + 1


        else:
            print("ERROR: error in evaluation of the objective function. Check evaluation")


        # if allow_update:
        #     state['evaluate'] = 0
        #     state['eval_return'] = 1
        #     ctl['objective_iter'] = ctl['objective_iter']  + 1

    return state, prob, noErrorBool
 

def objective_function_evaluation(Fvals, targets, evaluate_threshold, obj_threshold):
        #pass in the Fvals & targets so that it's easier to track bugs
        # this is pulled directly from the antennaCAT optimizer set as a way to 
        # streamline the development. 

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

        if evaluate_threshold == True: #THRESHOLD
            ctr = 0
            for i in targets:
                o_thres = int(obj_threshold[ctr]) #force type as err check
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
                    print("ERROR: unrecognized threshold value. Evaluating as TARGET")
                    Flist[ctr] = abs(t - fv)

                ctr = ctr + 1

        else: #TARGET as default
            # arrays are already the same dimensions. 
            # no need to loop and compare to anything
            Flist = abs(targets - Fvals)


        return Flist
        