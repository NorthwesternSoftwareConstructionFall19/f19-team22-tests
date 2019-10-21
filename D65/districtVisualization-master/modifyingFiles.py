##############################################################
#workbook = xlsxwriter.Workbook('ModelCode_0619/results_7_12/result' + str(sum) + '.xlsx')
#worksheet = workbook.add_worksheet('main')
#worksheet = workbook.add_worksheet('programs')
#worksheet = workbook.add_worksheet('enrollments')
#worksheet = workbook.add_worksheet('busing')
#worksheet = workbook.add_worksheet('demographics')
#workbook.close()

# The code above can be used to create excel files and add sheets during runtime
# see the xlsxwriter module (https://xlsxwriter.readthedocs.io/) for more information



import xlrd
import numpy as np
import xlsxwriter

###########################################
###########################################
# This script is used to modify block-level excel files.
# Basically, there are currently some blocks that are not relevant
# to the model's computation, and therefore are not displayed visually
# so these blocks are not included in many of the excel files.
# However, for some data visualization features and processes, the excel files
# have to account for every block (meaning that each block needs its own row(s)).
# This script basically fills in the "gaps" so to speak, and all it does really
# is that it copies everything from the original excel file of interest, and adds in
# extra rows to represent the blocks that are not being considered, and it fills those
# extra rows with values such as -1 or 300.

results = xlrd.open_workbook("oldOptimizationModel/results_9_10.xlsx")
result1 = results.sheet_by_index(0)
result2 = results.sheet_by_index(1)
result3 = results.sheet_by_index(2)

workbook = xlsxwriter.Workbook("oldOptimizationModel/modifiedResults_9_10.xlsx")
worksheet1 = workbook.add_worksheet('enroll')
worksheet2 = workbook.add_worksheet('bus')
worksheet3 = workbook.add_worksheet('dist')

###########################################
###########################################
# Contains one row with values that signify a block that is not being considered
dummyWorksheet = xlrd.open_workbook('writeJSON/dummyWorkbook.xlsx').sheet_by_index(0)


###########################################
###########################################
# This helper function is used to copy a row from a specific
# excel file into another excel file, and the user designates
# the source file, the target file, the specific row in the
# source file, the specific row in the target file, and the number of
# columns that must be copied (if other than all of the columns)
def copyRow(rowTo, rowFrom, copyTo, copyFrom, numCols_toCopy):
    for col in range(numCols_toCopy):
        if type(copyFrom.cell_value(rowFrom, col)) is not str:
            copyTo.write(rowTo, col, int(copyFrom.cell_value(rowFrom, col)))
        else:
            copyTo.write(rowTo, col, str(copyFrom.cell_value(rowFrom, col)))



###########################################
###########################################
# Modify this section of code to meet your
# specific needs. One thing to note is that
# if the target excel file has to become bigger or
# smaller than the source file (in terms of the number
# of rows/columns) then you may want two index variables:
# one to track where you are in the source file, and one to
# track where you are in the target file
newIndex = 0
index = 0
while index < 725:
    if index == 724:
        copyRow(newIndex, index + 1, worksheet1, result1, 10)
        break
    elif int(result1.cell_value(index + 2, 0) - result1.cell_value(index + 1, 0)) > 1 :

        ###########################################
        ###########################################
        # In this specific example, the "gap" is used to
        # signify how many rows need to be added to the target
        # file, and in this case its the next block's ID minus
        # the current block's ID.
        gap = int(result1.cell_value(index + 2, 0) - result1.cell_value(index + 1, 0))
        numMissingRows = int(gap)
        copyRow(newIndex, index + 1, worksheet1, result1, 10)

        missingRowStart = newIndex + 1
        for missingRowIndex in range(int(numMissingRows - 1)):
            copyRow(missingRowStart + missingRowIndex, 0, worksheet1, dummyWorksheet, 6)

        newIndex = missingRowStart + numMissingRows - 1
        index = index + 1
        continue
    else:
        copyRow(newIndex, index + 1, worksheet1, result1, 10)
    index = index + 1
    newIndex = newIndex + 1

print('1 is done, doing 2')
newIndex = 0
index = 0
while index < 725:
    if index == 724:
        copyRow(newIndex, index + 1, worksheet2, result2, 8)
        break
    elif int(result2.cell_value(index + 2, 0) - result2.cell_value(index + 1, 0)) > 1 :

        ###########################################
        ###########################################
        # In this specific example, the "gap" is used to
        # signify how many rows need to be added to the target
        # file, and in this case its the next block's ID minus
        # the current block's ID.
        gap = int(result2.cell_value(index + 2, 0) - result2.cell_value(index + 1, 0))
        numMissingRows = int(gap)
        copyRow(newIndex, index + 1, worksheet2, result2, 8)

        missingRowStart = newIndex + 1
        for missingRowIndex in range(int(numMissingRows - 1)):
            copyRow(missingRowStart + missingRowIndex, 0, worksheet2, dummyWorksheet, 6)

        newIndex = missingRowStart + numMissingRows - 1
        index = index + 1
        continue
    else:
        copyRow(newIndex, index + 1, worksheet2, result2, 8)
    index = index + 1
    newIndex = newIndex + 1

print('2 is done, doing 3')
newIndex = 0
index = 0
while index < 725:
    if index == 724:
        copyRow(newIndex, index + 1, worksheet3, result3, 7)
        break
    elif int(result3.cell_value(index + 2, 0) - result3.cell_value(index + 1, 0)) > 1 :

        ###########################################
        ###########################################
        # In this specific example, the "gap" is used to
        # signify how many rows need to be added to the target
        # file, and in this case its the next block's ID minus
        # the current block's ID.
        gap = int(result3.cell_value(index + 2, 0) - result3.cell_value(index + 1, 0))
        numMissingRows = int(gap)
        copyRow(newIndex, index + 1, worksheet3, result3, 7)

        missingRowStart = newIndex + 1
        for missingRowIndex in range(int(numMissingRows - 1)):
            copyRow(missingRowStart + missingRowIndex, 0, worksheet3, dummyWorksheet, 6)

        newIndex = missingRowStart + numMissingRows - 1
        index = index + 1
        continue
    else:
        print(index)
        copyRow(newIndex, index + 1, worksheet3, result3, 7)
    index = index + 1
    newIndex = newIndex + 1
###########################################
###########################################
# Make sure to close the workbook or whatever
# variable the target file is stored, to save
# all of the work you did to it
workbook.close()