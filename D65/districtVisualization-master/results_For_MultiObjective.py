
###############################################################
# This script is used to generate many different result files
# with various sets of input combinations for the purposes of
# preloading data for the multi-objective comparison feature.
# Modify the for loops below as needed


###############################################################
#workbook = xlsxwriter.Workbook('ModelCode_0619/results_7_12/result' + str(sum) + '.xlsx')
#worksheet = workbook.add_worksheet('main')
#worksheet = workbook.add_worksheet('programs')
#worksheet = workbook.add_worksheet('enrollments')
#worksheet = workbook.add_worksheet('busing')
#worksheet = workbook.add_worksheet('demographics')
#workbook.close()

# The code above can be used to create excel files and add sheets during runtime
# see the xlsxwriter module (https://xlsxwriter.readthedocs.io/) for more information



from oldOptimizationModel.multiObjective_Results_GeneratorScript import *
import xlsxwriter

###########################################
# This function call reads in all of the
# necessary excel files once, so that
# the subsequent optimization model runs
# can just use the files which are stored
# in global variables as a result of this function
# call

###########################################
# This the function definition for runModel:
# def runModel(blocksAssigned, travelDistance, excessStudents, contiguity,
#              studentsBussed, yearlyBusPerSchool, titleOneEligibleSchools, resultNum):


readFiles()


numList = [0, 1, 2, 3]
sum = 0
for index1 in range(4):
    for index2 in range(4):
        for index3 in range(4):
            for index4 in range(4):
                   sum = sum + 1
                   runModel(75, numList[index1], 0, 0,
                            numList[index2], numList[index3],numList[index4], sum, "75")
                   runModel(100, numList[index1], 0, 0,
                            numList[index2], numList[index3], numList[index4], sum, "100")

