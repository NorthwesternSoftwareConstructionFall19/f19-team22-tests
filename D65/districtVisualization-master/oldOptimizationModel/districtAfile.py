# -*- coding: utf-8 -*-
"""
Districting IP model file
Dec 2018/Jan 2019

Northwestern/D65 Team

K-5 together as one group
BR and MLK included but magnet program location fixed
TWI students considered part of general student population

Potential objectives: student travel distance, expected students over capacity

"""
from gurobipy import *
import csv
import numpy as np
import time
from random import *

'''

MODEL INPUTS
------------
SETS:
 I_set keeps track of which blocks are relevant (i.e. in the district)
 M == number of educational programs including dummy OOD programs
 N == number of K-5 schools
 K == number of middle schools
 J == number of grade buckets
 S == number of population change scenarios
 T == number of years (year 0 through year T - 1)
 R == number of races
 TP == number of TWI programs
 W[i, n] == set of blocks adjacent to block i which are closer to school n than block i is
DATA PARAMETERS:
 gamma[m, n] == 1 if program m is eligible for school n, 0 otherwise
 d[i, n] == distance from block i to school n
 f[n, k] == 1 if school n feeds into school u, 0 otherwise
 h[i, n] == 1 if block i contains school n, 0 otherwise
 p[i, j, s, t] == number of neighborhood school-attending students from block i in grade bucket j in scenario s in year t
 q[i, j, m, s, t] == number of students from block i in grade bucket j attending program m in scenario s in year t
 p_exp[i] == average number of neighborhood school-attending students across all years and scenarios
 q_exp[i, m] == average number of students from block i attending program m across all years and scenarios
 c[n] == capacity of school n
 buscap == capacity of standard school bus
 l[i, n] == 1 if block i currently assigned to school n
 rho[n] == maximum percentage allowed over capacity in any year in any scenario for school n
 bus[i, n] == 1 if students from block i require busing to school n
 rac[i, race] == number of students in block i in category race
 twi[i] == number of students in block i who are enrolled in any TWI program
 frl[i] == number of students in block i who are free and reduced lunch eligible
OBJECTIVE VARIABLES:   
 max_reassign == maximum % of blocks allowed to be reassigned
 contig_flag == 1 if we want contiguity, 0 otherwise
 distobj_coeff == scaling coefficient for distance objective
 excess_coeff == scaling coefficient for excess student objective

'''



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


def districtA(I_set, M, N, K, J, S, T, R, W, d, f, h, gamma, p, q, p_exp,
              q_exp, c, buscap, l, rho, bus, rac, twi, frl, grades, max_reassign,
              contig_flag, distobj_coeff, excess_coeff, bus_coeff, num_coeff, title1_coeff):

    model = Model("districting")

    model.Params.UpdateMode = 1 # allows you to use new variables and constraints immediately for building or modifying the model
    
    model.setParam('OutputFlag', 1) # enables/disables solver console/log output
    model.setParam('MIPGap', .7) # optimality gap for termination

    
    start_time = time.time() # time at which model building begins
    
    '''
    ~~~~~~~~ MODEL ~~~~~~~~
    '''

    #############################
    ######### VARIABLES #########
    #############################
    
    ## define variables ##
    u = {}
    x = {}
    z = {}
    totbus = {}
    numbus = {}
    theta = {}
    
    # construct x variables (binary)
    # 1 if block i is assigned to school n, 0 otherwise
    for i in I_set:
        for n in range(N):
            x[i,n] = model.addVar(vtype = GRB.BINARY, name = "x_{}_{}".format(i,n))
            
    # construct z variables (binary)
    # 1 if program m is assigned to school n, 0 otherwise
    for m in range(M):
        for n in range(N):
            z[m, n] = model.addVar(vtype = GRB.BINARY, name = "z_{}_{}".format(m, n))
            
    # construct u variables (nonnegative)
    # tracks number of students over capacity for each school for each scenario in each year
    for n in range(N):
        for s in range(S):
            for t in range(T):
                u[n, s, t] = model.addVar(lb=0, vtype = GRB.CONTINUOUS, name = "u_{}_{}_{}".format(n, s, t))
                
    # construct variable to track expected total number of bus-eligible students
    totbus = model.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = "totbus") 
    
    # construct variable to track expected number of buses required per school
    for n in range(N):
        numbus[n] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = "numbus_{}".format(n))
        
    # construct theta variables (binary)
    # 1 if a school is Title 1 eligible, 0 otherwise
    for n in range(N):
        theta[n] = model.addVar(vtype = GRB.BINARY, name = "theta_{}".format(n))

    ###############################
    ######### CONSTRAINTS #########
    ###############################

    # BASE CONSTRAINTS (1) #
    # each program is assigned to exactly one school
    for m in range(M):
        model.addConstr(quicksum(z[m, n] for n in range(N)) == 1, name = "c1_{}".format(m))


    # BASE CONSTRAINTS (2) #
    # programs are only assigned to eligible schools
    for m in range(M):
        for n in range(N):
            model.addConstr(z[m, n] <= gamma[m, n], name = "c2_{}_{}".format(m, n))


    # BASE CONSTRAINTS (3) #
    # each block is assigned to exactly one school
    for i in I_set:
        model.addConstr(quicksum(x[i, n] for n in range(N)) == 1, name = "c3_{}".format(i))


    # BASE CONSTRAINTS (4) #
    # expected number of students at each school cannot exceed capacity
    for n in range(10):
        model.addConstr(quicksum(quicksum(p_exp[i, j] for j in range(J)) * x[i, n] for i in I_set) <=
        (c[n] - quicksum(z[m, n] * quicksum(q_exp[i, j, m] for j in range(J)) for m in range(M) for i in I_set)), name = "c4_{}".format(n))


    # BASE CONSTRAINTS (5), (6) #
    # defining u variables
    # ensuring u variables are maximum percentage allowed over capacity for each year
    for n in range(N):
        for s in range(S):
            for t in range(T):
                model.addConstr(quicksum(quicksum(p[i, j, s, t] for j in range(J)) * x[i, n] for i in I_set)
                + quicksum(quicksum(q[i, j, m, s, t] for j in range(J)) * z[m, n] for m in range(M) for i in I_set) - u[n, s, t] <= c[n],
                name = "c5_{}_{}_{}".format(n, s, t))

                # model.addConstr(u[n, s, t] <= c[n] * r, name = "c6_{}_{}_{}".format(n, s, t))


    # BASE CONSTRAINTS (7) #
    # no blocks are assigned to magnet schools
    for n in range(N):
        for i in I_set:
            for m in range(10, 12):
                model.addConstr(z[m, n] + x[i, n] <= 1, name = "c7_{}_{}_{}".format(m, i, n))


    # CONTIGUITY CONSTRAINTS (8)#
    # recursively defining contiguity (see Caro et al. 2004)
    if contig_flag == 1:
        for i in I_set:
            for n in range(N):
                model.addConstr(x[i, n] <= h[i, n] + quicksum(x[j, n] for j in W[i, n]), name = "c8_{}_{}".format(i, n))

    # BASE CONSTRAINTS (9) #
    # limit the % of blocks reassigned
    model.addConstr(quicksum(x[i, n] * l[i, n] for i in I_set for n in range(N)) >= (1 - max_reassign)*len(I_set), name = "c9")


    # BUSED STUDENTS CONSTRAINT (10) #
    # calculating how many students require busing post-assignmnet
    model.addConstr(totbus == quicksum(x[i, n] * bus[i, n] * quicksum(p_exp[i, j] for j in range(J)) for i in I_set for n in range(N)) +
                    quicksum(z[m, n] * quicksum(q_exp[i, j, m] for j in range(J)) * bus[i, n] for i in I_set for n in range(N) for m in range(M)),
                    name = "c10")

    # NUMBER OF BUSES CONSTRAINT (11) #
    # constraining number of buses relative to students bused per school
    for n in range(N):
        model.addConstr(numbus[n] >= (quicksum(x[i,n] * bus[i,n] * quicksum(p_exp[i,j] for j in range(J)) for i in I_set) +
                                     quicksum(z[m, n] * quicksum(q_exp[i, j, m] for j in range(J)) * bus[i, n] for i in I_set for m in range(M)))/buscap,
                                     name = "c11_{}".format(n))

    # TITLE 1 ELIGIBILITY CONSTRAINT (12) #
    # constraining y[n] to equal the proportion of FRL students at each school n
    for n in range(N):
        model.addConstr(0.4 * theta[n] <= quicksum(frl[i] * x[i, n] for i in I_set)/c[n], name = "c12_{}".format(n))

    ##############################
    ######### OBJECTIVES #########
    ##############################
    
    # calculate total expected student population
    exp_tot = 0
    for i in I_set:
        for j in range(J):
            exp_tot = exp_tot + p_exp[i, j] 
            for m in range(M):
                exp_tot = exp_tot + q_exp[i, j, m]
    
    # scale down distobj_coeff to find average distance per student        
    distobj = distobj_coeff/exp_tot
    distobj = distobj/1.609 # convert to miles
    
    # scale down excess_coeff to find average excess per school per year
    excess = excess_coeff/(S * T * N)
    
    # scale down busing coefficient to find average number of students bused per school
    busobj = bus_coeff/N
    
    # scale down number of buses coefficient to find average number of buses per school
    numobj = num_coeff/N
    
    # currently no need to scale down title 1 coefficient
    t1obj = title1_coeff

    model.setObjective(
        distobj * (quicksum(p_exp[i, j] * (d[i, n]) ** 2 * x[i, n] for i in I_set for n in range(N) for j in range(J)) +
                   quicksum(
                       q_exp[i, j, m] * (d[i, n]) ** 2 * z[m, n] for i in I_set for m in range(M) for n in range(N) for
                       j in range(J))) +
        excess * quicksum(u[n, s, t] for t in range(T) for n in range(N) for s in range(S)) +
        busobj * totbus +
        numobj * quicksum(numbus[n] for n in range(N)) -
        t1obj * quicksum(theta[n] for n in range(N)),
        GRB.MINIMIZE)
    
    ##############################
    ############ SOLVE ###########
    ##############################
    
    model.optimize()
    
    progs = {}
    print("\n")
    for m in range(M):
        for n in range(N):
            if z[m, n].x > 0.5:
                # print("Program %.0f assigned to School %.0f" % (m, n))
                progs[m] = n
     
    blocks = {}           
    print("\n")
    for n in range(N):
        for i in I_set:
            if x[i, n].x > 0.5:
                # print("Block %.0f assigned to School %.0f" % (i, n))
                blocks[i] = n
                
    overcaps = {}
    for n in range(N):
        overcaps[n] = 0
        for s in range(S):
            for t in range(T):
                overcaps[n] = overcaps[n] + u[n, s, t].x
                
        overcaps[n] = overcaps[n]/(S * T)
        
    enrollment = {}
    for s in range(S):
        for t in range(T):
            for n in range(N):
                for j in range(J):
                    enrollment[n, j, s, t] = 0
                
                    for i in I_set:
                        if x[i, n].x > 0.5:
                            enrollment[n, j, s, t] = enrollment[n, j, s, t] + p[i, j, s, t]
                        
                    for m in range(M):
                        if z[m, n].x > 0.5:
                            enrollment[n, j, s, t] = enrollment[n, j, s, t] + q[i, j, m, s, t]
    
    # ms_enroll calculates the expected enrollment in middle school nm for a given scenario and time period based on feeder assignments
    ms_enroll = {}
    
    # ms_enroll is a 3-dimensional dictionary indexed by the middle school number, scenario, and time period
    for t in range(T):
        for s in range(S):
            for k in range(K):
                # using quicksum to sum an elementary school's enrollment with its corresponding assignment indicator
                # wrapping with LinExpr.getValue() as the quicksum returns a gurobi.LinExprt value type
                # using 1 for the j index so as to only sum population of students in grades 3-5 for middle school projected enrollment
                ms_enroll[k, s, t] = LinExpr.getValue(quicksum(enrollment[n, 1, s, t] * f[n, k] for n in range(N)))
    
    # population characteristic calculations
    # sch_twi displays how many TWI students are at each school
    sch_twi = {}
    for n in range(N):
        sch_twi[n] = 0
    
    for i in I_set:
        for n in range(N):
            if x[i, n].x > 0.5:
                sch_twi[n] = sch_twi[n] + twi[i]
                
    # sch_rac displays how many students of each race are at each school
    sch_rac = {}
    for n in range(N):
        for r in range(R):
            sch_rac[n, r] = 0
    
    for n in range(N):
        for i in I_set:
            for r in range(R):
                if x[i, n].x > 0.5:
                    sch_rac[n, r] = sch_rac[n, r] + rac[i, r]
                    
    # sch_frl displays how many students in FRL program are at each school
    sch_frl = {}
    for n in range(N):
        sch_frl[n] = 0
    
    for n in range(N):
        for i in I_set:
            if x[i, n].x > 0.5:
                sch_frl[n] = sch_frl[n] + frl[i]
    
    # sch_grades displays how many students of each grade bucket are at each school
    sch_grades = {}
    for n in range(N):
        for j in range(J):
            sch_grades[n, j] = 0

    for n in range(N):
        for i in I_set:
            if x[i, n].x > 0.5:
                for j in range(J):
                    sch_grades[n, j] = sch_grades[n, j] + grades[i, j]
                                 
    totaltrav = 0
    for i in I_set:
        for j in range(J):
            for n in range(N):
                totaltrav = totaltrav + (p_exp[i, j] * d[i, n] * x[i, n].x)

                for m in range(M):
                    totaltrav = totaltrav + (q_exp[i, j, m] * d[i, n] * z[m, n].x)
                    
    # busperschool[n] returns the optimized number of buses required per school
    busperschool = {}
    
    for n in range(N):
        busperschool[n] = numbus[n].x
    
    # t1elig[n] returns the Title 1 eligibility of school n
    t1elig = {}
    
    for n in range(N):
        if theta[n].x == 1:
            t1elig[n] = "Yes"
        else:
            t1elig[n] = "No"
        
    exptrav = totaltrav/exp_tot
    
    totnumbus = totbus.x
    totpcbus = totnumbus/exp_tot
    
    return(blocks, progs, overcaps, enrollment, ms_enroll, sch_twi, sch_rac, sch_frl, sch_grades, exptrav, totnumbus, totpcbus, busperschool, t1elig)
    