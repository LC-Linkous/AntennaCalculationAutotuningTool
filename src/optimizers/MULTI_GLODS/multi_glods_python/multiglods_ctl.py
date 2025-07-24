#! /usr/bin/python3

##--------------------------------------------------------------------\
#   surrogate_model_optimization
#   './surrogate_model_optimization/src/optimizers/multi_glods/multiglods_ctl.py'
#   Constant values for objective function. Formatted for
#       automating objective function integration
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: May 18, 2025
##--------------------------------------------------------------------\


import numpy as np
from numpy.random import default_rng
import time

import sys
try: # for outside func calls, program calls
    sys.path.insert(0, './surrogate_model_optimization/src/optimizers/multi_glods/')
    from multiglods_helpers import feasible
    from multiglods_helpers import logical_index_1d
    from multiglods_helpers import logical_index_h2d
    from multiglods_helpers import logical_set_val
    from multiglods_alg import merge
    from multiglods_alg import select_pollcenter

except:# for local, unit testing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import feasible
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_index_1d
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_index_h2d
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_set_val
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_alg import merge
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_alg import select_pollcenter



def one_time_init(NO_OF_VARS, LB, UB, TARGETS, E_TOL, R_TOL, MAXIT,
                              BP, GP, SF, obj_func, constr_func, evaluate_threshold, THRESHOLD, number_decimals):        

    LB = np.vstack(np.array(LB))
    UB = np.vstack(np.array(UB))
    TARGETS = np.vstack(np.array(TARGETS))

    state = {'eval_done': 0, 'init': 1,
             'post_init': 0, 'main_loop': {'run': 0, 'init': 1},
             'evaluate': 0, 'eval_return': 0, 'location': 1}
    alg = {'lbound': LB,
           'ubound': UB, 'targets': TARGETS, 'threshold': THRESHOLD, 'evaluate_threshold': evaluate_threshold, 
            'err_tol_stop': E_TOL, 'tol_stop': R_TOL, 'beta_par': BP, 'gamma_par': GP, 'poll_complete': 0,
           'search_freq': SF, 'number_decimals': number_decimals}
    
    nn = np.shape(alg['lbound'])[0]
    if NO_OF_VARS > 1:
        Pini = np.hstack([np.tile(alg['lbound'], (1, nn)) +
                         np.tile(np.linspace(0, nn-1, nn)/(nn-1), (nn, 1)) *
                         np.tile(alg['ubound']-alg['lbound'], (1, nn)),
                         (alg['lbound'] + alg['ubound'])/2])
    else:
        Pini = np.array([[1]])

    prob = {'n': nn, 'Pini': Pini,
            'alfa_ini': nn*max(alg['ubound']-alg['lbound']),
            'radius_ini': nn*max(alg['ubound']-alg['lbound']),
            'time': time.process_time(),
            'alfa': 0, 'radius': 0, 'active': 0, 'Plist': [],
            'Psearch': [], 'xtemp': [], 'Ftemp': [], 'FValtemp': [], 'Parent': []}

    ctl = {'func_eval': 0, 'match': 0, 'func_iter': 0, 'objective_iter': 0, 'eval': 0, 'finite': 0,
           'search_loop': 0, 'poll_loop': 0, 'i': 0, 'sel_level': 0,
           'Flist': [], 'D': [], 'count_d': [], 'nd': [], 'maxit': MAXIT, 'number_decimals': number_decimals,
           'obj_func': obj_func, 'constr_func': constr_func}
    init = []
    run_ctl = {'search_size': prob['n'], 'iter': 0,
               'iter_suc': 0, 'unsuc_consec': 0,
               'grid_size': 0, 'success': 0, 'poll': 0,
               'search': 0, 'changes': 0,
               'aux_success': 0}

    return init, run_ctl, alg, prob, ctl, state

def pre_objective_init_loop(ctl, prob):
    init = {"x_ini": [], "alfa_aux": [], "radius_aux": []}

    ctl['i'] = 0
    if ctl['i'] <= np.shape(prob['Pini'])[1]:
        if np.shape(prob['Pini'])[0] == 1:
            init['x_ini'] = prob['Pini']
        else:
            init['x_ini'] = np.vstack(prob['Pini'][:, ctl['i']])

    return init, ctl

def post_objective_init_loop(state, ctl, prob, init, alg):

    Ftemp = prob['Ftemp']
    if state['init'] and not np.shape(ctl['Flist'])[0] \
       and not (ctl['eval'] or ctl['match']) \
       and (ctl['i'] <= np.shape(prob['Pini'])[1]) \
       and feasible(init['x_ini'], alg['ubound'], alg['lbound'], prob['n'], ctl):
        ctl['eval'] = 1

    if state['init'] and not np.shape(ctl['Flist'])[0] and ctl['eval']:
        if ctl['i'] <= np.shape(prob['Pini'])[1]:
            if feasible(init['x_ini'], alg['ubound'],
                        alg['lbound'], prob['n'], ctl):
                if not ctl['match']:
                    ctl['func_eval'] = ctl['func_eval'] + 1
                    ctl['func_iter'] = ctl['func_iter'] + 1
                    ctl['eval'] = 0

                # check here for reshape errors first 
                # - likely caused by obj func return in multiglods_helpers.py
                # print("Ftemp in multiglods_ctl")
                # print(Ftemp)
                # print(np.shape(Ftemp))

                if np.sum(np.isfinite(Ftemp), axis=0) == np.shape(Ftemp)[0]:
                    if not np.shape(ctl['Flist'])[0]:
                        ctl['Flist'] = Ftemp
                        prob['Plist'] = init['x_ini']
                        prob['alfa'] = prob['alfa_ini']
                        prob['radius'] = prob['radius_ini']
                        prob['active'] = 1
                    else:
                        init['alfa_aux'] = prob['alfa_ini']
                        init['radius_aux'] = prob['radius_ini']
                        nn, prob['Plist'], ctl['Flist'], prob['alfa'], \
                            prob['radius'], prob['active'], nm = \
                            merge(init['x_ini'], Ftemp, init['alfa_aux'],
                                  init['radius_aux'], prob['Plist'],
                                  ctl['Flist'], prob['alfa'], prob['radius'],
                                  prob['active'], 0, [])

            ctl['i'] = ctl['i']+1

    else:
        if state['init']:
            state['post_init'] = 1
            state['init'] = 0

        ctl['i'] = 0

    prob['Ftemp'] = Ftemp

    return ctl, prob, init, state

def post_init(state, prob):
    run_ctl = {'search_size': prob['n'], 'iter': 0,
               'iter_suc': 0, 'unsuc_consec': 0,
               'grid_size': 0, 'success': 0, 'poll': 0,
               'search': 0, 'changes': 0,
               'aux_success': 0}
    state['post_init'] = 0
    state['main_loop']['run'] = 1

    return run_ctl, state

def run_no_search_no_poll(ctl, run_ctl):
    if not (ctl['poll_loop'] or ctl['search_loop']):
        ctl['func_iter'] = 0
        run_ctl['success'] = 0
        run_ctl['poll'] = 1
        run_ctl['search'] = 0
        
        if np.shape(np.shape(ctl['Flist']))[0]:
            pass
        else:
            run_ctl['changes'] = np.zeros((1, np.shape(ctl['Flist'])[1]))

    return ctl, run_ctl

def pre_objective_search(ctl, run_ctl, alg, prob):
    Psearch = prob['Psearch']
    xtemp = prob['xtemp']
    if not ctl['poll_loop']:
        if not (run_ctl['iter'] or ctl['search_loop']) and \
            ((alg['search_freq'] == 0) or
             (run_ctl['unsuc_consec'] == alg['search_freq'])):
            run_ctl['search'] = 1

        if run_ctl['search'] and not (ctl['finite'] or ctl['i']):
            rng = default_rng(np.floor(np.random.random()*1000).astype(int))
            ctl['search_loop'] = 1
            run_ctl['unsuc_consec'] = 0
            Psearch = np.tile(alg['lbound'], (1, run_ctl['search_size'])) + \
                np.tile((alg['ubound']-alg['lbound']),
                        (1, run_ctl['search_size'])) * \
                rng.random((prob['n'], run_ctl['search_size']))

        if run_ctl['search'] and \
            not (ctl['finite'] or (not np.shape(Psearch)[0]) or
                 ctl['i']):
            run_ctl['aux_success'] = 0
            ctl['i'] = 1

        if run_ctl['search'] and not (ctl['finite'] or
                                      (not np.shape(Psearch)[0])) \
           and (ctl['i'] <= np.shape(Psearch)[1]):
            xtemp = Psearch[:, ctl['i']]

    prob['Psearch'] = Psearch
    prob['xtemp'] = xtemp

    return run_ctl, ctl, prob

def post_objective_search(ctl, run_ctl, alg, prob):
    Psearch = prob['Psearch']
    xtemp = prob['xtemp']
    Ftemp = prob['Ftemp']
    if run_ctl['search'] and not (ctl['poll_loop'] or
                                  ctl['finite'] or not np.shape(Psearch)[0]):
        if (ctl['i'] <= np.shape(Psearch)[1]) and \
           feasible(xtemp, alg['ubound'], alg['lbound'], prob['n'], ctl) and \
           not ctl['match']:
            ctl['func_eval'] = ctl['func_eval'] + 1
            ctl['func_iter'] = ctl['func_iter'] + 1

        if (ctl['i'] <= np.shape(Psearch)[1]) and \
           feasible(xtemp, alg['ubound'], alg['lbound'], prob['n'], ctl):
            if np.sum(np.isfinite(Ftemp), axis=0) == np.shape(Ftemp)[0]:
                # This line may be a problem ******
                ctl['finite'] = 1
                ctl['search_loop'] = 0
                run_ctl['success'], prob['Plist'], ctl['Flist'], \
                    prob['alfa'], prob['radius'], \
                    prob['active'], run_ctl['changes'] = \
                    merge(xtemp, Ftemp, prob['alfa_ini'], prob['radius_ini'],
                          prob['Plist'], ctl['Flist'],
                          prob['alfa'], prob['radius'],
                          prob['active'], 0, run_ctl['changes'])
                run_ctl['aux_success'] = run_ctl['aux_success'] \
                    + run_ctl['success']

            ctl['i'] = ctl['i']+1
        else:
            ctl['i'] = 0

        if not ctl['i']:
            if run_ctl['aux_success'] > 0:
                run_ctl['success'] = 1
                run_ctl['poll'] = 0
            else:
                run_ctl['success'] = 0
                run_ctl['poll'] = 1

    prob['Psearch'] = Psearch
    prob['xtemp'] = xtemp
    prob['Ftemp'] = Ftemp

    return run_ctl, ctl, prob

def pre_objective_poll(prob, ctl, run_ctl, alg):
    D = ctl['D']
    sel_level = ctl['sel_level']
    count_d = ctl['count_d']
    xtemp = prob['xtemp']
    nd = ctl['nd']

    if run_ctl['poll'] and not (ctl['search_loop'] or ctl['poll_loop']):
        D = np.hstack([np.eye(prob['n']),-np.eye(prob['n'])])

        sel_level, prob['Plist'], ctl['Flist'], \
            prob['alfa'], prob['radius'], prob['active'] = \
            select_pollcenter(prob['Plist'], ctl['Flist'],
                              prob['alfa'], prob['radius'],
                              prob['active'], alg['tol_stop'], ctl['number_decimals'])

        if sel_level:
            nd = np.shape(D)[1]
            count_d = 1
            run_ctl['changes'] = np.hstack([np.array([[1]]),
                                            np.zeros((1,
                                                      np.shape(ctl['Flist'])[1]
                                                      - 1))])

    # START POLLING
    if sel_level and run_ctl['poll'] and not (ctl['search_loop']) and \
       ((count_d <= nd) and (alg['poll_complete'] or not run_ctl['success'])):
        ctl['poll_loop'] = 1
        if np.shape(prob['alfa']):
            xtemp = np.vstack(prob['Plist'][:, 0] + prob['alfa'][0] * D[:, count_d-1])
        else:
            xtemp = np.vstack(prob['Plist'][:, 0] + prob['alfa'] * D[:, count_d-1])

    ctl['D'] = D
    ctl['sel_level'] = sel_level
    ctl['count_d'] = count_d
    ctl['nd'] = nd
    prob['xtemp'] = np.round(xtemp, ctl['number_decimals'])

    return prob, ctl, run_ctl

def post_objective_poll(prob, ctl, run_ctl, alg):
    D = ctl['D']
    sel_level = ctl['sel_level']
    count_d = ctl['count_d']
    xtemp = prob['xtemp']
    Ftemp = prob['Ftemp']
    nd = ctl['nd']
    if sel_level and run_ctl['poll'] and not (ctl['search_loop']) and \
       ((count_d <= nd) and (alg['poll_complete'] or not run_ctl['success'])):
        if feasible(xtemp, alg['ubound'],
                    alg['lbound'], prob['n'], ctl) and not ctl['match']:
            ctl['func_eval'] = ctl['func_eval'] + 1
            ctl['func_iter'] = ctl['func_iter'] + 1

        if feasible(xtemp, alg['ubound'], alg['lbound'],
                    prob['n'], ctl) and (np.sum(np.isfinite(Ftemp))
                                    == np.shape(Ftemp)[0]):
            run_ctl['success_aux'], prob['Plist'], ctl['Flist'], \
               prob['alfa'], prob['radius'], prob['active'], \
               run_ctl['changes'] = merge(xtemp, Ftemp, prob['alfa_ini'],
                                          prob['radius_ini'],
                                          prob['Plist'], ctl['Flist'],
                                          prob['alfa'], prob['radius'],
                                          prob['active'], 1,
                                          run_ctl['changes'])

            if run_ctl['success_aux']:
                run_ctl['success'] = 1

        count_d = count_d + 1

    if sel_level and run_ctl['poll'] and \
       not (ctl['search_loop'] or
            ((count_d <= nd) and
            (alg['poll_complete'] or
             not run_ctl['success']))):
        ctl['poll_loop'] = 0

    ctl['D'] = D
    ctl['sel_level'] = sel_level
    ctl['count_d'] = count_d
    ctl['nd'] = nd
    prob['xtemp'] = xtemp

    return prob, ctl, run_ctl

def run_update(run_ctl, ctl, prob, alg, state):
    if run_ctl['success'] and not (ctl['poll_loop'] or ctl['search_loop']):
        run_ctl['iter_suc'] = run_ctl['iter_suc'] + 1
        run_ctl['unsuc_consec'] = 0

        # replace with logical indices
        prob['alfa'] = logical_set_val((run_ctl['changes'] +
                                        prob['active']) == 2,
                                       prob['alfa'],
                                       prob['alfa']*alg['gamma_par'])

        # replace with logical indices
        rad_temp = np.maximum(prob['radius'], prob['alfa'])
        prob['radius'] = logical_set_val((run_ctl['changes'] +
                                          prob['active']) == 2,
                                         prob['radius'], rad_temp)

    else:
        if not (ctl['poll_loop'] or ctl['search_loop']):
            run_ctl['unsuc_consec'] = run_ctl['unsuc_consec'] + 1

            # replace with logical indices
            prob['alfa'] = logical_set_val((run_ctl['changes'] +
                                            prob['active']) == 2,
                                           prob['alfa'],
                                           prob['alfa']*alg['beta_par'])

    # return logical index in conditional
    if (np.sum(logical_index_1d(prob['active'], prob['alfa']) >=
               alg['tol_stop']) == 0) and not (ctl['poll_loop']
                                               or ctl['search_loop']):

        state['main_loop']['run'] = 0

    # NOTE: this is a change from the original translation. 
    #  Originally the counter was set to check
    # if ctl['func_iter'] >= ctl['maxit']
    # ['func_iter'] is a function iteration, but not how 
    # how many times the objective function has been called. 

    if ctl['objective_iter'] >= ctl['maxit']:
        state['main_loop']['run'] = 0

    return run_ctl, prob, state

def end_processing(prob, ctl, run_ctl):
    prob['Plist'] = logical_index_h2d(prob['active'], prob['Plist'])
    ctl['Flist'] = logical_index_h2d(prob['active'], ctl['Flist'])
    prob['alfa'] = logical_index_1d(prob['active'], prob['alfa'])
    prob['radius'] = logical_index_1d(prob['active'], prob['radius'])
    prob['time'] = time.process_time()-prob['time']

    # variables needed for results: iter, iter_suc, sum(active),ctl.func_eval
    print("Points:")
    print(prob['Plist'])
    print("Iterations:")
    print(run_ctl['iter'])
    print("Flist:")
    print(ctl['Flist'])
    print("Norm Flist:")
    print(np.linalg.norm(ctl['Flist']))