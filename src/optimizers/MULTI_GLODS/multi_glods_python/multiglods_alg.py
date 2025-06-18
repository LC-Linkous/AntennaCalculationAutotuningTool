#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_surrogate
#   './multi_glods_surrogate/src/configs_F.py'
#   The main multiglods algorithm where the math happens
#   NOTE: multiglods.py is the statemachine, 
#       and multiglods_ctl.py is the controller
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: March 13, 2025
##--------------------------------------------------------------------\


import numpy as np
import copy
import sys
try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multiglods_helpers import logical_index_1d
    from multiglods_helpers import logical_index_h2d
    from multiglods_helpers import logical_index_h2d_Plist

except:# for local, unit testing
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_index_1d
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_index_h2d
    from optimizers.MULTI_GLODS.multi_glods_python.multiglods_helpers import logical_index_h2d_Plist



def match_point(x, xnorm, CacheP, CacheF, CachenormP, tol_match):

    index = np.array([])
    if (np.shape(np.where(np.abs(CachenormP - xnorm) <= tol_match)[0]) > 0):
        index = np.where(np.abs(CachenormP - xnorm) <= tol_match)[0]
        CacheP = CacheP[:, index]
        CacheF = CacheF[:, index]

        nCacheP = np.shape(CacheP)[1]
        index = np.where(np.max(np.abs(CacheP -
                                       np.tile(x,
                                               (1, nCacheP))),
                                axis=1) <= tol_match)

    match = not np.shape(index)[0]
    # perfect isempty function

    if match:
        x = CacheP[:, index[0]]
        F = CacheF[:, index[0]]

    return match, x, F

def merge(x, F, alfa_ini, radius_ini, Plist,
          Flist, alfa, radius, active, poll, changes):
    success = 0
    dist_list = np.sqrt(np.sum((Plist -
                                np.tile(x, (1, np.shape(Plist)[1]))) ** 2,
                               axis=0))

    if np.min(dist_list-radius, axis=0) > 0:
        success = 1
        Plist = np.hstack([Plist, x])
        Flist = np.hstack([Flist, F])
        alfa = np.hstack([alfa, alfa_ini])
        radius = np.hstack([radius, radius_ini])
        active = np.hstack([active, 1])
        changes = np.hstack([changes, 1])
    else:
        if np.min(dist_list, axis=0) != 0:
            index = np.where((dist_list-radius) <= 0)
            m_index = np.shape(index)[1]
            index = index[0]
            active_new = 0
            alfa_new = 0
            radius_new = 0
            idom = 0
            pdom = 0
            for i in (np.linspace(1, m_index, m_index)-1):
                ii = int(i)
                if np.sum((np.vstack(Flist[:, ii]) >= F).astype(int)) \
                   == np.shape(F)[0]:
                    if np.shape(active):
                        idom = idom + active[index[ii]]
                        active[index[ii]] = 0
                        if alfa[index[ii]] > alfa_new:
                            alfa_new = alfa[index[ii]]
                            radius_new = radius[index[ii]]
                    else:
                        idom = idom + active
                        active = 0
                        if np.shape(alfa):
                            if alfa[ii] > alfa_new:
                                alfa_new = alfa[ii]
                                radius_new = radius
                        else:
                            if alfa > alfa_new:
                                alfa_new = alfa
                                radius_new = radius
                else:
                    if np.sum(F >= np.vstack(Flist[:, index[ii]])) \
                       == np.shape(F)[0]:
                        pdom = 1

            if pdom == 0:
                active_new = 1
                success = 1

            if alfa_new == 0:
                alfa_new = alfa_ini
                radius_new = radius_ini

            if (idom > 0) or (pdom == 0):
                Plist = np.hstack([Plist, x])
                Flist = np.hstack([Flist, F])
                active = np.hstack([active, active_new])
                changes = np.hstack([changes, [[1]]])
                if poll:
                    if np.shape(alfa):
                        alfa = np.hstack([alfa, alfa[0]])
                        radius = np.hstack([radius, alfa[0]])
                    else:
                        alfa = np.hstack([alfa, alfa])
                        radius = np.hstack([radius, alfa[0]])

                else:
                    alfa = np.hstack([alfa, alfa_new])
                    radius = np.hstack([radius, radius_new])

    return success, Plist, Flist, alfa, radius, active, changes

def select_domlevel(Plist, Flist, alfa_in, active, tol_active_points, level):
    Plist = copy.deepcopy(Plist)
    Flist = copy.deepcopy(Flist)
    sel_level = 1
    Plist = logical_index_h2d_Plist(active != 0, Plist)
    Flist = logical_index_h2d(active != 0, Flist)
    alfa = logical_index_1d(active != 0, alfa_in)
    index = np.nonzero(alfa >= tol_active_points)[0]
    if np.size(index):

        Plist = Plist[:, index]
        Flist = Flist[:, index]
        if np.shape(alfa):
            alfa = alfa[index]

        level_stop = 0
        ll = 0

        while not level_stop:
            if np.size(Flist):
                nlist, mlist = np.shape(Flist)
                dom = np.zeros((1, mlist))
                for i in range(0, mlist):

                    if dom[0][i] == 0:
                        Faux = np.tile(np.vstack(Flist[:, i]), (1, mlist))
                        index = np.sum((Faux <= Flist).astype(int), axis=0)[0]
                        dom[0, (index == nlist).astype(int)-1] = 1
                        index = np.sum((Faux == Flist).astype(int), axis=0)[0]
                        index_p = (index == nlist).astype(int)-1
                        dom[index_p] = 0
                        index = ((np.sum((Faux < Flist).astype(int), axis=0))
                                 != 0).astype(int)[0]

                    if (np.sum(index, axis=0) <
                       (mlist - np.sum(index_p, axis=0))):
                        dom[index_p] = 1

            if (np.sum((dom == 0).astype(int), axis=1) == mlist) \
               or (ll == level):
                level_stop = 1
            else:
                Plist = logical_index_h2d(active != 0, Plist)
                Flist = logical_index_h2d(active != 0, Flist)
                alfa = logical_index_1d(active != 0, alfa)

            ll = ll+1

    else:
        sel_level = 0
        Plist = np.array([])
        Flist = np.array([])
        alfa = np.array([])

    return sel_level, Plist, Flist, alfa

def select_pollcenter(Plist, Flist, alfa, radius, active, tol_active_points):
    level = 0
    sel_level = 0

    while not sel_level:

        sel_level, Plist_aux, Flist_aux, alfa_aux = \
           select_domlevel(Plist, Flist, alfa, active,
                           tol_active_points, level)

        level = level + 1

    index = alfa_aux.argsort()[::-1]

    Plist_aux = Plist_aux[:, index]

    mlist = Flist.shape[1]

    Xcenter = np.tile(np.vstack(Plist_aux[:,0]), (1, mlist))

    if np.shape(np.nonzero(np.sum(np.absolute(Plist-Xcenter),
                                  axis=0) == 0))[1] > 1:
        index = np.nonzero(np.sum(np.absolute(Plist-Xcenter),
                                  axis=0) == 0)[0][1]
    else:
        index = np.nonzero(np.sum(np.absolute(Plist-Xcenter),
                                  axis=0) == 0)[0][0]

    Plist = np.hstack([np.vstack(Plist[:, int(index)]),
                       Plist[:, 0:int(index)],
                       Plist[:, (int(index)+1):(mlist)]])
    Flist = np.hstack([np.vstack(Flist[:, int(index)]),
                       Flist[:, 0:int(index)],
                       Flist[:, (int(index)+1):(mlist)]])
    if np.shape(alfa):
        alfa = np.hstack([alfa[int(index)],
                          alfa[0:int(index)],
                          alfa[(int(index)+1):(mlist)]])
    if np.shape(radius):
        radius = np.hstack([radius[int(index)],
                            radius[0:int(index)],
                            radius[(int(index+1)):(mlist)]])

    if np.shape(active):
        active = np.hstack([active[int(index)],
                            active[0:int(index)],
                            active[(int(index)+1):(mlist)]])

    return sel_level, Plist, Flist, alfa, radius, active