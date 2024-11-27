#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multiglods.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 28, 2024
##--------------------------------------------------------------------\

import numpy as np
import sys

#unit testing vs. program call
try:
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

except:
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
    
    # Main application loop (This is the only loop,
    # allows for easy conversion to external control)

    if state['init'] or state['post_init'] or state['main_loop']['run']:
        
        # initializations pre objective function call
        if state['init'] and not np.shape(ctl['Flist'])[0] \
           and not ctl['eval'] and not state['evaluate'] \
            and not state['eval_return']:
            init, ctl = pre_objective_init_loop(ctl, prob)
            

        # initialization objective functionc call
        if state['init'] and not np.shape(ctl['Flist'])[0] \
           and not (ctl['eval'] or ctl['match']) and \
           (ctl['i'] <= np.shape(prob['Pini'])[1]) and \
           feasible(init['x_ini'], alg['ubound'], alg['lbound'], prob['n'], ctl):
            
            if not state['evaluate'] and not state['eval_return']:               
                state, prob = f_eval(state, init['x_ini'], prob, 1)
            else:
                state, prob = f_eval_return(state, prob, alg, 1)
        
        # initalizations post objective function call
        if not state['evaluate'] and not state['eval_return']:
            ctl, prob, init, state = \
                post_objective_init_loop(state, ctl, prob, init, alg)

        # post initialization loop initializations
        if state['post_init'] and not state['evaluate'] and not state['eval_return']:
            run_ctl, state = post_init(state, prob)
        
        if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:

            # first code in run loop, but not in search or poll mode
            ctl, run_ctl = run_no_search_no_poll(ctl, run_ctl)

            # pre objective function call search step
            run_ctl, ctl, prob = pre_objective_search(ctl, run_ctl, alg, prob)
        
        # search step objective function call
        if state['main_loop']['run'] and not (ctl['poll_loop']) and \
           run_ctl['search'] and not (ctl['finite'] or
                                      (not np.shape(prob['Psearch'])[0])) \
           and (ctl['i'] <= np.shape(prob['Psearch'])[1]) and \
           feasible(prob['xtemp'], alg['ubound'], alg['lbound'],
                    prob['n'], ctl) and not ctl['match']:
            if not state['evaluate'] and not state['eval_return']:   
                state, prob = f_eval(state, prob['xtemp'], prob, 2)
            else:
                state, prob = f_eval_return(state, prob, alg, 2)
        
        if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:

            # post objective call search step
            run_ctl, ctl, prob = post_objective_search(ctl, run_ctl, alg, prob)

            # pre objective call poll step
            prob, ctl, run_ctl = pre_objective_poll(prob, ctl, run_ctl, alg)
        
        # poll step objective function call
        if state['main_loop']['run'] and ctl['sel_level'] and run_ctl['poll'] and \
            not (ctl['search_loop']) and ((ctl['count_d'] <= ctl['nd']) and
                                          (alg['poll_complete'] or not
                                           run_ctl['success'])) and \
            feasible(prob['xtemp'], alg['ubound'], alg['lbound'], prob['n'], ctl) and \
           not ctl['match']: 
            if not state['evaluate'] and not state['eval_return']:
                state, prob = f_eval(state, prob['xtemp'], prob, 3)
            else:
                state, prob = f_eval_return(state, prob, alg, 3)
        
        if state['main_loop']['run'] and not state['evaluate'] and not state['eval_return']:

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

        
