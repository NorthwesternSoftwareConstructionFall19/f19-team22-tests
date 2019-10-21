# -*- coding: utf-8 -*-
"""
New districting model file
Created on Thu Jul 11 09:00:37 2019

@author: f3lix
"""

from gurobipy import *
import numpy as np
import time
from random import *
import cProfile, pstats, io

def profile(fnc):

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
'''
### MODEL INPUTS ###
--------------------
## SETS ##
 D                  distance of block i from school n where it cannot be assigned to n
 E                  distance of block i from school n where it must be assigned to n
 I                  number of blocks in the district
 I_set              set of relevant blocks in the district
 J                  grade buckets
 M                  programs
 N                  K-5 schools
 R                  number of races
 S                  number of population change scenarios
 T                  number of years
 W[i,n]             blocks adjacent to block i that are closer to school n than block i is

## PARAMETERS ##
 b[i, n]            1 if block i requires busing to school n, 0 otherwise
 c[n]               capacity of school n
 d[i, n]            walking/busing distance from block i to school n
 h[i, n]            1 if block i is adjacent to or contains school n, 0 otherwise
 l[i, n]            current (pre-model) block-school assignments; 1 if block i assigned to school n, 0 otherwise
 p[i, j, s, t]      number of students from block i in grade bucket j attending school n (neighborhood school) in scenario s, year t
 q[i, j, s, t]      number of students from block i in grade bucket j attending school m (magnet school) in scenario s, year t
 pbar[i, j]         average number of students from block i in grade bucket j attending a neighborhood school across all scenarios and years
 qbar[i, j, m]      average number of students from block i in grade bucket j attending program m
 r
 phi
 rho                

## DECISION VARIABLES ##
 x[i, n]            1 if block i is assigned to school n, 0 otherwise
 u[n, s, t]         number of students over capacity at school in scenario s, year t
 alpha              average number of students bused across all scenarios and years
 beta[n]            average number of buses required to bus students to school n across all scenarios and years
 gamma[n]           1 if school is Title 1 eligible (40% or more students are FRL), 0 otherwise (based on averages over all scenarios and years)
 delta[i]           1 if block i assigned to a school requiring busing, when assignment to another school would allow walking

## OBJECTIVES ##
 1. minimize average and maximum distances traveled by students
 2. minimize the amount of students over capacity at any school
 3. minimize the number of students that require busing to their school
 4. minimize the number of buses required
 5. maximize the number of Title 1 eligible schools (>= 40% of students qualify for free and reduced lunch)
 
'''

# Declaring optimization model
@profile
def districtmodel(D, E, I, I_set, J, M, N, R, S, T, W, b, c, d, h, l, p, q, pbar, qbar, phi, rho, psi):
    # Phase 1: basic declarations and parameter setting
    model = Model("districting")
    model.setParam('UpdateMode', 1)                                             # allows immediate modification to the model
    model.setParam('OutputFlag', 1)                                             # enables/disables solver console/log output
    model.setParam('MIPGap', 0.01)                                              # optimality gap for termination  
    start_time = time.time()                                                    # time at which model building begins
    
    # Phase 2: variable setup
    II = len(I_set)
    x = model.addVars(II, N, vtype = GRB.BINARY)                                # x[i, n]: 1 if block i assigned to school n, 0 otherwise
    y = model.addVars(II, J, N, vtype = GRB.BINARY)
    u = model.addVars(N, S, T, vtype = GRB.INTEGER)                             # u[n, s, t]: number of students over capacity at school n in scen s, year t
    alpha = model.addVar(lb = 0, vtype = GRB.CONTINUOUS)                        # alpha: average number of students bused across all n, s, t
    beta = model.addVars(N, lb = 0, vtype = GRB.INTEGER)                        # beta[n]: number of buses required to bus assigned students to school n
    gamma = model.addVars(N, vtype = GRB.BINARY)                                # gamma[n]: 1 if school n is Title 1 eligible, 0 otherwise
    delta = model.addVars(I_set, vtype = GRB.BINARY)                            # delta[i]: 1 if block i is bused but could walk to a different school
    
    
    # Phase 3: constraint setup
    model.addConstrs((x.sum(i, '*') == 1 for i in range(II)), name = 'c1')      # c1: each block can only be assigned to 1 school
    
    model.addConstrs((x.sum('*', i) == 0 for i in M), name = 'c2')              # c2: no blocks are assigned to magnet schools (n = 10, n = 11)
    
    model.addConstrs((x[i, n] <= h[i, n] +                                      # c3: i cannot be assigned to n unless i either borders n or an adjacent
                      quicksum(x[j, n] for j in W[i, n])                        #     block j closer to n is already assigned to n
                      for n in range(N)                                         
                      for i in range(II)), name = 'c3')
    
    model.addConstrs((quicksum(x[i, n] * p[i, j, s, t]                          # c4: number of students attending school n cannot exceed capacity in (s, t)
                               for i in range(II)                               #     with allowance for u variable of students over capacity
                               for j in range(J)) <= c[n] + u[n, s, t]
                      for n in range(N)
                      for s in range(S)
                      for t in range(T)), name = 'c4')
    
    model.addConstrs((u[n, s, t] <= rho * c[n]                                  # c5: constraining u[n, s, t] to be <= c[n] * rho, or the % over capacity
                      for n in range(N)
                      for s in range(S)
                      for t in range(T)), name = 'c5')
    
    model.addConstrs((x[i, n] <= 0                                              # c6: constraining x[i, n] to be 0 if i is too far (> D) from n
                      for i in range(II)
                      for n in range(N)
                      if d[i, n] > D), name = 'c6')
    '''
    model.addConstrs((x[i, n] >= 1                                              # c7: constraining x[i, n] to be 1 if i is close enough (<= E) to n
                      for i in range(II)
                      for n in range(N)
                      if d[i, n] <= E), name = 'c7')
    '''
    
    # Phase 4: objective function declarations
    model.setObjective((quicksum(pbar[i] * d[i, n]**2 * x[i, n]                 # o1: total distance squared traveled by students (neighborhood and magnet)
                                 for n in range(N) for i in range(II)) +
                        quicksum(qbar[i] * d[i, m]**2 * l[i, m]
                                 for m in M for i in range(II))),
                       GRB.MINIMIZE)                                            # minimization objective
    '''
    model.setObjective(0, GRB.MINIMIZE)                                         # o': test objective to make sure constraints aren't causing infeasibility
    '''
    
    # Phase 5: optimization
    model.optimize()
    
    # Phase 6: recording results
    a = np.arange(12, dtype = int)                                              # set up a vector containing the school index numbers
    sol = np.zeros((II, N), dtype = int)                                        # recording optimal values of x-variables
    for i in range(II):
        for n in range(N):
            sol[i, n] = x[i, n].x
    assn = sol @ a
    
    cap = np.zeros((N, S, T), dtype = int)                                      # recording optimal values of u-variables
    for n in range(N):
        for s in range(S):
            for t in range(T):
                cap[n, s, t] = u[n, s, t].x
    
    
    # Phase 7: outputs
    end_time = time.time()
    elapsed = end_time - start_time
    print("Optimization complete\n")
    
    return assn, cap, elapsed