#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multiglods.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: November 5, 2025
##--------------------------------------------------------------------\

import numpy as np
import sys

try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multiglods_ctl import pre_objective_init_loop
    from multiglods_helpers import feasible
    from multiglods_ctl import post_objective_init_loop
    from multiglods_ctl import post_init
    from multiglods_ctl import run_no_search_no_poll
    from multiglods_ctl import pre_objective_search
    from multiglods_ctl import post_objective_search
    from multiglods_ctl import pre_objective_poll
    from multiglods_ctl import post_objective_poll
    from multiglods_ctl import run_update
    from multiglods_ctl import end_processing
    from multiglods_helpers import inc_iter
    from multiglods_helpers import f_eval
    from multiglods_helpers import f_eval_return
    from multiglods_helpers import print_debug

except:# for local, unit testing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import pre_objective_init_loop
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import feasible
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import post_objective_init_loop
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import post_init
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import run_no_search_no_poll
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import pre_objective_search
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import post_objective_search
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import pre_objective_poll
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import post_objective_poll
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import run_update
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_ctl import end_processing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import inc_iter
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import f_eval
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import f_eval_return
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import print_debug



def multiglods(init, run_ctl, alg, prob, ctl, state, suppress_output):
    
    # Main application loop 
    ## This is the only loop, which allows for easy conversion to external control


    # November 4. 2025 had a lot of state machine changes made. Those are marked with 
    # CHANGE to make them visible. This version is still being stress tested, but appears
    # to do well with simulations.


    # Getting from 2 extra simulations down to 1
    # most of the changes have to do with how this state machine syncs up with the AntennaCAT statemachine
    # because there's been an issue with 2 extra simulations running at the end post-convergence. 
    # Other print/report bugs have been fixed, but at least 1 of those extra simulation runs AFTER the convergence
    # is being caused by the state machines being out of sync. 

    # getting from 1 extra simulation down to 0
    # the revised changes (4.1 and 7.1) should get rid of that last 'over shoot' simulation 
    # updates with 4.2 and 7.2 are to clear a stale state (suspected issue) noticed when checking multiglods_helpers.py
    # the the helper funcs, with the objective_function_evaluation() function call, it was noticed that FLIST is a step 
    # (more like 1.5 steps) behind the simulation. The threshold evaluation DOES evaluate correctly even tho the epsilon looks
    # odd in practice.

    # READABILITY:
    # For righ tnow, LEAVE THE SPACES BETWEEN ACTION CHUNKS. Some parts of this are still a 
    # little weird, but this is so much easier to read without adjusting the formatting.
    # the extra spacing has been added to split up major actions/decisions in the state machine





    if state['init'] or state['post_init'] or state['main_loop']['run']:
        
        # initializations pre objective function call
        if state['init'] and not np.shape(ctl['Flist'])[0] \
           and not ctl['eval'] and not state['evaluate'] \
            and not state['eval_return']:
            init, ctl = pre_objective_init_loop(ctl, prob)
            

        # initialization objective function call
        if state['init'] and not np.shape(ctl['Flist'])[0] \
           and not (ctl['eval'] or ctl['match']) and \
           (ctl['i'] <= np.shape(prob['Pini'])[1]) and \
           feasible(init['x_ini'], alg['ubound'], alg['lbound'], prob['n'], ctl):
            
            # CHANGE 1: Separated marking from processing - only mark for evaluation here
            if not state['evaluate'] and not state['eval_return']:
                # MARK objective function for evaluation     
                # This ONLY sets state['evaluate']=1 and prob['xtemp']
                # The ACTUAL simulation happens in the external loop via callObjective()
                state, prob = f_eval(state, init['x_ini'], prob, 1) 
            
            #CHANGE 1: Separated marking from processing - only mark for evaluation here
            # else:
            #     # call the objective function
            #     # Note: this is the state change/mark and the pass through to call the function that will
            #     # evaluate the data from the simulation
            #     state, prob = f_eval_return(state, prob, alg, 1)




        # CHANGE 2: THIS IS NEW CODE HERE!
        #  Added separate block to process returns when data is ready
        # Process objective function return if data is ready
        # This runs AFTER callObjective() has set state['eval_return']=1 and filled prob['FValtemp']
        if state['init'] and not np.shape(ctl['Flist'])[0] and \
           state['eval_return'] and (state['location'] == 1):
            # Process the returned data: FValtemp to Ftemp. This is pretty true to the original state machine
            state, prob = f_eval_return(state, prob, alg, 1)




        # initalizations post objective function call
        # CHANGE 3: Modified condition to allow processing immediately after eval_return
        # Post objective function processing
        # OLD: if not state['evaluate'] and not state['eval_return']:
        # NEW: if state['init'] and not state['evaluate']:
        # This allows processing immediately after eval_return completes
        if state['init'] and not state['evaluate']:
            ctl, prob, init, state = \
                post_objective_init_loop(state, ctl, prob, init, alg)
        # ORIGINAL CODE for post objective function call:
        # if not state['evaluate'] and not state['eval_return']:
        #     ctl, prob, init, state = \
        #         post_objective_init_loop(state, ctl, prob, init, alg)




        # post initialization loop initializations
        if state['post_init'] and not state['evaluate'] and not state['eval_return']:
            run_ctl, state = post_init(state, prob)
        
        if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:

            # first code in run loop, but not in search or poll mode
            ctl, run_ctl = run_no_search_no_poll(ctl, run_ctl)

            # pre objective function call search step
            run_ctl, ctl, prob = pre_objective_search(ctl, run_ctl, alg, prob)
        


        # NEW: PREEMPTIVE CONVERGENCE CHECK BEFORE SEARCH STEP
        # CHANGE 8: part of the pass for the convergence. 
        # Not fully sure this one actually triggers properly.
        # Check if we're already converged before marking new evaluation
        if state['main_loop']['run'] and not (ctl['poll_loop']) and run_ctl['search']:
            if np.shape(ctl['Flist'])[0] > 0:
                if len(np.shape(ctl['Flist'])) > 1:
                    current_best = np.linalg.norm(ctl['Flist'][:,0])
                else:
                    current_best = np.linalg.norm(ctl['Flist'])
                
                # If already converged, stop the main loop NOW
                if current_best <= alg['err_tol_stop']:
                    state['main_loop']['run'] = 0
                    # Skip to end processing
                    if not suppress_output:
                        end_processing(prob, ctl, run_ctl)
                    return 1, init, run_ctl, alg, prob, ctl, state



        # search step objective function call
        if state['main_loop']['run'] and not (ctl['poll_loop']) and \
           run_ctl['search'] and not (ctl['finite'] or
                                      (not np.shape(prob['Psearch'])[0])) \
           and (ctl['i'] <= np.shape(prob['Psearch'])[1]) and \
           feasible(prob['xtemp'], alg['ubound'], alg['lbound'],
                    prob['n'], ctl) and not ctl['match']:
            # ORIGINAL CODE FOR THIS PART (note the 2s):
            # this has been SPLIT UP
            # if not state['evaluate'] and not state['eval_return']:   
            #     state, prob = f_eval(state, prob['xtemp'], prob, 2) 
            # else:
            #     state, prob = f_eval_return(state, prob, alg, 2)

            # CHANGE 4 pt1: Separated marking from processing - only mark for evaluation here
            # update (I think I understand where this matches up now. No promises)
            # if not state['evaluate'] and not state['eval_return']:   
            #     # MARK for evaluation
            #     state, prob = f_eval(state, prob['xtemp'], prob, 2)
            if not state['evaluate'] and not state['eval_return']:   
                # ADD THIS: Check convergence before marking for evaluation
                # Check if already at tolerance or max iterations
                if state['main_loop']['run'] and ctl['objective_iter'] < ctl['maxit']:
                    # Only mark for evaluation if still running and under max iterations
                    state, prob = f_eval(state, prob['xtemp'], prob, 2)




        # Process search step return if data is ready
        #CHANGE 4 pt2: Separated marking from processing.
        #Added separate block to process search step returns when data is ready
        if state['main_loop']['run'] and not (ctl['poll_loop']) and \
           state['eval_return'] and (state['location'] == 2):
            # Process the returned data
            state, prob = f_eval_return(state, prob, alg, 2)
        





        # Run when NOT currently waiting for evaluation
        # CHANGE 5: Modified condition to allow processing immediately after eval_return
        # OLD: if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:
        # NEW: if state['main_loop']['run'] and not state['evaluate']:
        if state['main_loop']['run'] and not state['evaluate']:
            # post objective call search step
            run_ctl, ctl, prob = post_objective_search(ctl, run_ctl, alg, prob)

            # pre objective call poll step
            prob, ctl, run_ctl = pre_objective_poll(prob, ctl, run_ctl, alg)




        # NEW: PREEMPTIVE CONVERGENCE CHECK BEFORE POLL STEP
        # CHANGE 9: part of the pass for the convergence. 
        # Not fully sure this one actually triggers properly.
        # Check if we're already converged before marking new evaluation
        if state['main_loop']['run'] and ctl['sel_level'] and run_ctl['poll']:
            if np.shape(ctl['Flist'])[0] > 0:
                if len(np.shape(ctl['Flist'])) > 1:
                    current_best = np.linalg.norm(ctl['Flist'][:,0])
                else:
                    current_best = np.linalg.norm(ctl['Flist'])
                
                # If already converged, stop the main loop NOW
                if current_best <= alg['err_tol_stop']:
                    state['main_loop']['run'] = 0
                    # Skip to end processing
                    if not suppress_output:
                        end_processing(prob, ctl, run_ctl)
                    return 1, init, run_ctl, alg, prob, ctl, state




        # poll step objective function call
        # Note the 3s for tracking how this is being adjusted. 
        if state['main_loop']['run'] and ctl['sel_level'] and run_ctl['poll'] and \
            not (ctl['search_loop']) and ((ctl['count_d'] <= ctl['nd']) and
                                          (alg['poll_complete'] or not
                                           run_ctl['success'])) and \
            feasible(prob['xtemp'], alg['ubound'], alg['lbound'], prob['n'], ctl) and \
           not ctl['match']: 
            # ORIGINAL CODE: 
            # if not state['evaluate'] and not state['eval_return']:
            #     state, prob = f_eval(state, prob['xtemp'], prob, 3)
            # else:
            #     state, prob = f_eval_return(state, prob, alg, 3)

            # CHANGE 6pt1: Separated marking from processing - only mark for evaluation here
            # # this helped get from 2 extra simulations down to 1 extra
            # if not state['evaluate'] and not state['eval_return']:
            #     # MARK for evaluation
            #     state, prob = f_eval(state, prob['xtemp'], prob, 3)
            if not state['evaluate'] and not state['eval_return']:
                # ADD THIS: Check convergence before marking for evaluation
                # Check if already at tolerance or max iterations
                if state['main_loop']['run'] and ctl['objective_iter'] < ctl['maxit']:
                    # Only mark for evaluation if still running and under max iterations
                    state, prob = f_eval(state, prob['xtemp'], prob, 3)                


        # CHANGE 6pt2: Added separate block to process poll step returns when data is ready
        # Process poll step return IF data is ready
        if state['main_loop']['run'] and ctl['sel_level'] and \
           state['eval_return'] and (state['location'] == 3):
            # Process the returned data
            state, prob = f_eval_return(state, prob, alg, 3)
        



        # Run when NOT currently waiting for evaluation
        # CHANGE 7: Modified condition to allow processing immediately after eval_return
        # NOTE: still a little wonky here, but this needs more logs when sim testing.
        # it's either the root of the problem, or just better reporting when there's an timing issue
        # OLD: if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:
        # NEW: if state['main_loop']['run'] and not state['evaluate']:
        if state['main_loop']['run'] and not state['evaluate']:

            # post objective poll step
            prob, ctl, run_ctl = post_objective_poll(prob, ctl, run_ctl, alg)

            # update run loop parameters and check end condition
            run_ctl, prob, state = run_update(run_ctl, ctl, prob, alg, state)

            # if end condition met, display data
            if not state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:
                if not suppress_output:
                    end_processing(prob, ctl, run_ctl)
                return 1, init, run_ctl, alg, prob, ctl, state
            # increment iteration
            run_ctl = inc_iter(ctl, run_ctl)
            # state, NO_OF_LOOPS = print_debug(run_ctl, state, ctl, prob, init, alg, NO_OF_LOOPS, 22)

        if state['init'] or state['post_init'] or state['main_loop']['run']:
            return 0, init, run_ctl, alg, prob, ctl, state

