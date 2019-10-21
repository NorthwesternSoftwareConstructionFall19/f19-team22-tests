# -*- coding: utf-8 -*-
"""
New districting test script
Created on Thu Jul 11 12:56:46 2019

@author: f3lix
"""
# import written scripts and functions
from districtModel import *
from districtFunctions import *
from tkintertests import *

# import packages for reading and writing data into Excel
import pandas as pd
import csv
import xlsxwriter
from openpyxl import Workbook
from openpyxl import load_workbook
import sys

# declare parameter values
J = 2                                                                           # 2 grade buckets
N = 12                                                                          # 12 schools
M = [10, 11]                                                                    # set of indices corresponding to magnet schools in N
T = 6                                                                           # 6 years of enrollment projections  
S = 4                                                                           # 4 enrollment scenarios
R = 5                                                                           # 5 race categories
D = 4                                                                           # maximum distance a block can be from a school to be assigned
E = 1                                                                           # distance from a school in which a block must be assigned to it

# run function 1: blocksetup(blockfile, N)
(I, I_set, l) = blocksetup('currassign.csv', N)

# run function 2: capacities(capfile)
c = capacities('capacities.csv')

# run function 3: schools()
h = schools(I, I_set, N)                                                               # manual function, sets up which blocks are adjacent to/contain a school

# run function 4: adjacency() and sub-functions A1 and A2
adj = adjacency('segments.csv', 'bridges.csv', 'islands.csv', I, I_set)
path = contig(adj, 0, path = [])                                                # sub function A1, builds a path of blocks contiguous to block 0 (1)
miss = find_missing(path)                                                       # sub function A2, finds the blocks that are missing from the list

if miss:
    sys.exit("Error: not a contiguous network of blocks\n")                     # checks to see if there are missing blocks, and aborts script if so
else:
    print("Block network is contiguous. Proceeding...\n")

# run function 5: contiguity()
W = contiguity('edist.csv', adj, I, I_set, N)

# run function 6: truedist(truedistfile, I, N)
(h, d) = truedist('tdist.csv', E, I, I_set, N, h)

# run function 7: busreqs(busfile)
b = busreqs('busing.csv', I_set)

# run function 8: enrollments()
(e, p, q, pbar, qbar, phi, rho, psi) = enrollments('enrollments.csv', I_set, J, S, T, N)

# run function 9: demographics()

# run model
(assn, cap, elapsed) = districtmodel(D, E, I, I_set, J, M, N, R, S, T, W, b, c, d, h, l, p, q, pbar, qbar, phi, rho, psi)

# run function 10: busing()

# run function 11: writeresults(resultfile, assn, cap, I_set, b, d, pbar, qbar)
writeresults('results.xlsx', assn, cap, I_set, b, d, pbar, qbar)
