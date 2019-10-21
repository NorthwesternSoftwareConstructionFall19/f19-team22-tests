# -*- coding: utf-8 -*-
"""
Created on Mon May 20 23:59:12 2019

@author: f3lix
"""

### TEST FILE FOR POPULATION DATA SPLIT INTO GRADE BUCKETS ###
### 0 corresponds to grades K-2 and a 1 corresponds to 3-5 ###

from oldOptimizationModel.districtAfile import *
from oldOptimizationModel.districtAhelpers import *
from oldOptimizationModel.tkintertests import *
import pandas as pd
import xlsxwriter
from openpyxl import Workbook
from openpyxl import load_workbook


def runModel(blocksAssigned, travelDistance, excessStudents, contiguity,
             studentsBussed, yearlyBusPerSchool, titleOneEligibleSchools):


    # number of elementary schools
    N = 12

    # number of middle schools
    K = 3

    # number of grade buckets
    # 0 K-2
    # 1 3-5
    # 2 6-8
    J = 2

    # number of programs
    M = 12

    # number of blocks (including outside of district)
    I = 829

    # number of scenarios
    S = 3

    # number of years
    T = 2

    # number of race categories
    R = 5

    # number of TWI programs
    TP = 3

    ###############################################################################


    # read school capacities
    c = readcapacities('oldOptimizationModel/capacitiesK5.xlsx', 'Sheet1', N)

    # enter bus capacity
    buscap = 60

    # set program eligibilities
    gamma = eligible(M, N)

    # set up blocks (which blocks are in I_set and where each block is currently assigned)
    (I_set, l) = blocksetup('oldOptimizationModel/currassign.xlsx', I, N)

    # find in which block each school is located
    h = schoolinblock(I_set, N)

    # define maximum % allowed over capacity for any year
    rho = 1

    # create adjacency dictionary
    W_pre = blockadjacency('oldOptimizationModel/adjacency.xlsx', I_set)

    # use Euclidean distances to populate W dictionary
    W = blockcontiguity('oldOptimizationModel/euclidean.xlsx', I_set, N, W_pre)

    # load true (walking) distances
    d = truedistances('oldOptimizationModel/truedist.xlsx', I_set, N)

    # read population data, create p, q, p_exp, q_exp
    (p, q, p_exp, q_exp) = popsetup('oldOptimizationModel/popB.xlsx', I_set, M, N, J, S, T, l)

    # read demographic data, create frl, twi, rac
    (twi, rac, frl, grades) = blockchars('oldOptimizationModel/demo2.xlsx', I_set, J, R, TP)

    # read feeder school data, create f array
    f = feederschools('oldOptimizationModel/feeders.xlsx', N, K)

    # read busing data
    (bus, bustrue) = busblocks('oldOptimizationModel/color_by_school.xlsx', I_set, N)

    # GUI for additional input
    (max_reassign, distobj_coeff, excess_coeff, bus_coeff, num_coeff, title1_coeff, contig_flag) = \
             (blocksAssigned, travelDistance, excessStudents,
              studentsBussed, yearlyBusPerSchool, titleOneEligibleSchools, contiguity)
    max_reassign = max_reassign / 100

    # run model
    (blocks, progs, overcaps, enrollments, ms_enroll, sch_twi, sch_rac, sch_frl, sch_grades, exptrav, totnumbus, totpcbus,
     busperschool, t1elig) = districtA(I_set, M, N, K, J, S, T, R, W, d, f, h, gamma, p, q, p_exp, q_exp, c, buscap, l, rho,
                                       bus, rac, twi, frl, grades, max_reassign, contig_flag, distobj_coeff, excess_coeff,
                                       bus_coeff, num_coeff, title1_coeff)

    # bus calculations and results writing
    buscalcs('oldOptimizationModel/dummyResults.xlsx', I_set, M, N, J, blocks, progs, p_exp, q_exp, bustrue, busperschool)

    # write results
    writeresults('oldOptimizationModel/dummyResults.xlsx', I_set, M, N, J, S, T, R, c, blocks, progs, enrollments, overcaps, exptrav, contig_flag,
                 sch_twi, sch_rac, sch_frl, sch_grades, totnumbus, totpcbus, t1elig)

    print("Program complete.")
