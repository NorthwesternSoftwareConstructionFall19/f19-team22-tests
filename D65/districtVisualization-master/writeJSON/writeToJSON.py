###########################################
###########################################
# Import some packages/libraries for specific
# processes later in the script
import json
import numpy as np
import csv
import xlrd
from operator import itemgetter





############################################
############################################
# Setting up chunks of code for profiling this
# script. Add "@profile" above the definition of
# a function you would like to profile, and make sure
# that the function of interest will be called in whichever you
# run. So something like this would suffice:
#
# @profile
# def dummyFunction():
#       some code here;
#
# ....
#
# dummyFunction()
import cProfile, pstats, io
from multiprocessing import Process, freeze_support

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



#################################################################
#################################################################
# To load in xlsx files, use the command xlrd.open_workbook( file path/location as a string)
# to obtain a specific sheet, use the command .sheet_by_index(index goes here)
# the sheet indeces start from zero, so the 0th sheet is actually the first
# to obtain a specific cell value, use .cell_value(row, column). The row and column
# also start at index 0

#################################################################
#################################################################
# To load in csv (comma separated values) files, use the command
# np.loadtxt(file path/location as a string, skiprows= *pass in a number here
# if you want skip a particular row, like the first row with all
# of the column titles for example*, delimiter=",")
# the delimiter separates the values by commas if I am not mistaken


#################################################################
#################################################################
# To avoid performance issues, try to load in the files you'll need
# and open relevant sheets at the start of the script. In general,
# if files are constantly reopened in multiple iterations for example,
# the performance of this script will decrease, particularly if the files
# are large





presentation9_10_enroll = xlrd.open_workbook("oldOptimizationModel/results_9_10.xlsx").sheet_by_index(0)
presentation9_10_bus = xlrd.open_workbook("oldOptimizationModel/results_9_10.xlsx").sheet_by_index(1)
presentation9_10_dist = xlrd.open_workbook("oldOptimizationModel/results_9_10.xlsx").sheet_by_index(2)






#################################################################
#################################################################
# currently running all (current number of objective inputs here) objectives each with values of
# something to something, multiObjInputCombinations holds every possible combination
# which is i^o, where i is the number of different input values and o is
# the number of objectives
multiObjInputs = [0, 1, 2, 3]
multiObjInputCombinations = []

###########################################
###########################################
# The following for loops fills the inputCombinations list
# uses a map function to convert all of the numbers to strings
# with one function call
for index1 in range(4):
    for index2 in range(4):
        for index3 in range(4):
            for index4 in range(4):
                    combination = [multiObjInputs[index1], multiObjInputs[index2],
                                   multiObjInputs[index3], multiObjInputs[index4]]
                    combination = map(str, combination)
                    multiObjInputCombinations.append("".join(combination))




######################################################################################
######################################################################################
# This helper function is used to fill various dictionaries/lists with open'd excel files,
# and this greatly improves the performance of this script because all of the excel files
# would have been opened prior to the iteration that goes through all of the blocks.
# Modify this function as needed for your specific needs.
def fillMultiObjResults(multiObjResults, multiObjResults1, multiObjResults2, multiObj_ObjValues, percentString):
    for index in range(256):
            fileLocation = "./oldOptimizationModel/multiObjective_Results_Percent" + percentString + "/result" + str(index + 1) + ".xlsx"

            workbook = xlrd.open_workbook(fileLocation)

            combination = multiObjInputCombinations[index]

            # school data
            multiObjResults.append([percentString + 'school' + combination,
                                    workbook.sheet_by_index(0),
                                    0])
            # busing hazard data
            multiObjResults1.append([percentString + 'busHazard' + combination,
                                    workbook.sheet_by_index(3),
                                    0])
            # busing distance data
            multiObjResults2.append([percentString + 'busDistance' + combination,
                                     workbook.sheet_by_index(3),
                                     0])

            multiObj_ObjValues.append([workbook.sheet_by_index(0), workbook.sheet_by_index(3), workbook.sheet_by_index(4)])
    return multiObjResults, multiObjResults1, multiObjResults2, multiObj_ObjValues





#############################################
#############################################
# Loading in various files and additional data from excel files stored
# # in the writeJSON folder
filename = "writeJSON/Data_blocks_Total_171018_2.csv"

results = "./oldOptimizationModel/results.xlsx"

# edge_coor: edge_id, start_x, start_y, end_x, end_y, block_id
edge_coor_remove_deadend = np.loadtxt("./writeJSON/edge_coor_remove_deadend.csv", delimiter=",")
#edge_coor_remove_deadend = np.loadtxt("edge_coor_remove_deadend.csv", delimiter=",")

# get dummyEnrollment Data
enrollment = np.loadtxt("./writeJSON/enrollmentDummyData.csv", skiprows=1, delimiter=",")
#enrollment = np.loadtxt("enrollmentDummyData.csv", skiprows=1, delimiter=",")
# gets all demographic data

genDemoData = np.loadtxt("./writeJSON/Demographic Data 2018-2019.csv", skiprows=1, delimiter=",")
#genDemoData = np.loadtxt("Demographic Data 2018-2019.csv", skiprows=1, delimiter=",")

#predictionScenarios = xlrd.open_workbook("writeJSON/newPredictions.xlsx").sheet_by_index(0)
#predictionScenarios = xlrd.open_workbook("newPredictions.xlsx").sheet_by_index(0)

wb = xlrd.open_workbook(results)
bussingInfo = wb.sheet_by_index(3)

# onTheSpotFile goes here: if the team wants you to quickly display the new school
# assignments of a particular results file, then you can create a variable that opens
# and stores the excel file sheet.
# onTheSpotFile = xlrd.open_workbook( " file location here " ). sheet_by_index( index of the specific sheet )





########################################
########################################
# this function is called when the model
# input box is filled out and
# "run optimization" is clicked

@profile
def writeToFile():
    print("beginning of JSON")

    #####################################################
    #####################################################
    # Below is a list(s)/dictionary(ies) that
    # can pair respective input combinations with various
    # data that one may want to include about each block
    global multiObjResults_School_25
    multiObjResults_School_25 = []

    global multiObjResults_BusHazard_25
    multiObjResults_BusHazard_25 = []

    global multiObjResults_BusDistance_25
    multiObjResults_BusDistance_25 = []

    #####################################################
    #####################################################
    # Below is a list(s)/dictionary(ies) that
    # can pair respective input combinations with various
    # data that one may want to include about each block
    global multiObjResults_School_50
    multiObjResults_School_50 = []

    global multiObjResults_BusHazard_50
    multiObjResults_BusHazard_50 = []

    global multiObjResults_BusDistance_50
    multiObjResults_BusDistance_50 = []

    #####################################################
    #####################################################
    # Below is a list(s)/dictionary(ies) that
    # can pair respective input combinations with various
    # data that one may want to include about each block
    global multiObjResults_School_75
    multiObjResults_School_75 = []

    global multiObjResults_BusHazard_75
    multiObjResults_BusHazard_75 = []

    global multiObjResults_BusDistance_75
    multiObjResults_BusDistance_75 = []

    #####################################################
    #####################################################
    # Below is a list(s)/dictionary(ies) that
    # can pair respective input combinations with various
    # data that one may want to include about each block
    global multiObjResults_School_100
    multiObjResults_School_100 = []

    global multiObjResults_BusHazard_100
    multiObjResults_BusHazard_100 = []

    global multiObjResults_BusDistance_100
    multiObjResults_BusDistance_100 = []

    #####################################################
    #####################################################
    # Below is a list(s)/dictionary(ies) that
    # can pair respective input combinations with various
    # data that one may want to include about each block
    global multiObj_ObjValues_25
    multiObj_ObjValues_25 = []

    global multiObj_ObjValues_50
    multiObj_ObjValues_50 = []

    global multiObj_ObjValues_75
    multiObj_ObjValues_75 = []

    global multiObj_ObjValues_100
    multiObj_ObjValues_100 = []

    ####################################
    global multiObjResults_Schools
    multiObjResults_Schools = [multiObjResults_School_25, multiObjResults_School_50,
                               multiObjResults_School_75, multiObjResults_School_100]

    global multiObjResults_BusDistances
    multiObjResults_BusDistances = [multiObjResults_BusDistance_25, multiObjResults_BusDistance_50,
                                    multiObjResults_BusDistance_75, multiObjResults_BusDistance_100]

    global multiObjResults_BusHazards
    multiObjResults_BusHazards = [multiObjResults_BusHazard_25, multiObjResults_BusHazard_50,
                                    multiObjResults_BusHazard_75, multiObjResults_BusHazard_100]

    global multiObj_ObjValues
    multiObj_ObjValues = [multiObj_ObjValues_25, multiObj_ObjValues_50,
                          multiObj_ObjValues_75, multiObj_ObjValues_100]

    print('Beginning the function calls for: fillMultiObjResults')
    multiObjResults_School_25, multiObjResults_BusHazard_25, multiObjResults_BusDistance_25, multiObj_ObjValues_25\
        = fillMultiObjResults(multiObjResults_School_25, multiObjResults_BusHazard_25,
                              multiObjResults_BusDistance_25, multiObj_ObjValues_25,
                              '25')


    print('25 IS DONE, DOING 50')
    multiObjResults_School_50, multiObjResults_BusHazard_50, multiObjResults_BusDistance_50, multiObj_ObjValues_50 \
        = fillMultiObjResults(multiObjResults_School_50, multiObjResults_BusHazard_50,
                              multiObjResults_BusDistance_50, multiObj_ObjValues_50,
                              '50')


    print('50 IS DONE, DOING 75')
    multiObjResults_School_75, multiObjResults_BusHazard_75, multiObjResults_BusDistance_75, multiObj_ObjValues_75 \
        = fillMultiObjResults(multiObjResults_School_75, multiObjResults_BusHazard_75,
                              multiObjResults_BusDistance_75, multiObj_ObjValues_75,
                              '75')



    print('75 IS DONE, DOING 100')
    multiObjResults_School_100, multiObjResults_BusHazard_100, multiObjResults_BusDistance_100, multiObj_ObjValues_100 \
        = fillMultiObjResults(multiObjResults_School_100, multiObjResults_BusHazard_100,
                              multiObjResults_BusDistance_100, multiObj_ObjValues_100,
                              '100')

    print('DONE')
    ##########################################
    ##########################################
    ##########################################
    # myCSV columns: startX, startY, endX, endY, blockID, blockCenterX, blockCenterY
    # each row is an edge
    myCSV = np.loadtxt(filename, usecols=(4, 5, 8, 9, 30, 31, 32), skiprows=1, delimiter=",")

    # block_center has columns blockID, blockCenterX, blockCenterY
    block_centers = np.loadtxt(filename, usecols=(30, 31, 32), skiprows=1, delimiter=",")

    # block_id is list of unique block id's
    block_ids = np.loadtxt(filename, usecols=(30), skiprows=1, delimiter=",")
    ##removes duplicates from block_id
    block_ids = list(dict.fromkeys(block_ids))


    ##########################################
    ##########################################
    # Setting up three 2D arrays to open and store the
    # files that hold the results of the bounding tests
    # that Felix ran

    print("Beginning the function calls for: Loading in the results of the Bounding Tests")
    global workbooks_solutions
    workbooks_solutions = []

    global workbooks_singles
    workbooks_singles = []

    global workbooks_norms
    workbooks_norms = []

    for index in range(5):
        workbooks_solutions.append(xlrd.open_workbook('./oldOptimizationModel/sol' + str(index + 1) + '.xlsx'))
        workbooks_singles.append(xlrd.open_workbook('./oldOptimizationModel/single' + str(index + 1) + '.xlsx'))
        workbooks_norms.append(xlrd.open_workbook('./oldOptimizationModel/norm' + str(index + 1) + '.xlsx'))

    ################################################################################
    ################################################################################
    # Setting up three 2D arrays to opens the bussing sheets from the files that
    # contain the results of the bounding tests. Each subarray has two zeros in the
    # first and second indices, and those are place holders for the bus for distance
    # and bus for hazard data values
    global bussingInfo_solutions
    bussingInfo_solutions = []
    for index in range(5):
        bussingInfo_solutions.append([workbooks_solutions[index].sheet_by_index(3),
                                      0,
                                      0])
    global bussingInfo_singles
    bussingInfo_singles = []
    for index in range(5):
        bussingInfo_singles.append([workbooks_singles[index].sheet_by_index(3),
                                    0,
                                    0])
    global bussingInfo_norms
    bussingInfo_norms = []
    for index in range(5):
        bussingInfo_norms.append([workbooks_norms[index].sheet_by_index(3),
                                  0,
                                  0])

    ##############################################################################
    # Results get school info
    global schoolInfo
    wb = xlrd.open_workbook(results)
    schoolInfo = wb.sheet_by_index(0)

    ################################################################################
    ################################################################################
    # Setting up 2D arrays to store the school sheets of the bounding test excel files,
    # each subarray has a zero in the first index, and it is a placeholder for the new
    # school assignment
    global schoolInfo_solutions
    schoolInfo_solutions = []
    for index in range(5):
        schoolInfo_solutions.append([workbooks_solutions[index].sheet_by_index(0), 0])

    global schoolInfo_singles
    schoolInfo_singles = []
    for index in range(5):
        schoolInfo_singles.append([workbooks_singles[index].sheet_by_index(0), 0])

    global schoolInfo_norms
    schoolInfo_norms = []
    for index in range(5):
        schoolInfo_norms.append([workbooks_norms[index].sheet_by_index(0), 0])

    ################################################################################
    ################################################################################
    # Storing the sheet from the result file that contains the data about title one schools
    global titleOneInfo
    wb = xlrd.open_workbook(results)
    titleOneInfo = wb.sheet_by_index(4)

    ################################################################################
    ################################################################################
    # Setting up 2D arrays to store the title one sheets from the bounding tests excel
    # files, each subarray has a zero in the first index as a placeholder for the title
    # one data
    global titleOneInfo_solutions
    titleOneInfo_solutions = []
    for index in range(5):
        titleOneInfo_solutions.append([workbooks_solutions[index].sheet_by_index(4), 0])

    global titleOneInfo_singles
    titleOneInfo_singles = []
    for index in range(5):
        titleOneInfo_singles.append([workbooks_singles[index].sheet_by_index(4), 0])

    global titleOneInfo_norms
    titleOneInfo_norms = []
    for index in range(5):
        titleOneInfo_norms.append([workbooks_norms[index].sheet_by_index(4), 0])

    print("DONE")
    ##############################################################################

    num_block = 828
    num_edge = 4554
    num_edge_remove_deadend = edge_coor_remove_deadend.shape[0]

    ##############################################################################
    # getting rid of deadends/etc, cleaning up blocks
    print("Getting rid of deadends/etc, cleaning up blocks")
    for j in range(num_block):
        block_id = j + 1
        # block_center_coor = [ block_center[j,1],block_center[j,2] ]

        edge_set = set()

        for k in range(num_edge_remove_deadend):
            if edge_coor_remove_deadend[k, 5] == block_id:
                edge_set.add((edge_coor_remove_deadend[k, 1], edge_coor_remove_deadend[k, 2]))
                edge_set.add((edge_coor_remove_deadend[k, 3], edge_coor_remove_deadend[k, 4]))
    ##############################################################################
    print("Calling writeJSON(block_ids, block_centers)")
    writeJSON(block_ids, block_centers)


##############################################################################
##############################################################################
# A master function that calls two functions to generate and record the block
# labels and blocks
def writeJSON(block_ids, block_centers):
    print("Calling writeBlockLabels(block_ids, block_centers)")
    writeBlockLabels(block_ids, block_centers)
    # writeSchoolNames(block_ids, block_centers)
    print("Calling writeBlocks(block_ids, block_centers)")
    writeBlocks(block_ids, block_centers)


##############################################################################
##############################################################################
# A function that records the block labels
def writeBlockLabels(block_ids, block_centers):
    # Writing to GeoJSON file
    blockLabels = {}

    ##this is an array of features. Each feature is a dictionary
    featureArray = []
    currFeature = {}

    for id in block_ids:
        # gets the block center coordinates for each blockid
        block_center_coor_list = block_centers[np.where(block_centers[:, 0] == id)]
        block_center_coor = [block_center_coor_list[0][1], block_center_coor_list[0][2]]

        currFeature = {"type": "Feature",
                       "geometry": {"type": "Point",
                                    "coordinates": block_center_coor},
                       "properties": {"title": id,
                                      "id": id}}
        featureArray.append(currFeature)


    # adds the featureCollection prefix and the array of features to JSON
    # don't need the other prefixes/suffixes bc they are not part of the data source
    blockLabels = {"type": "FeatureCollection",
                   "features": featureArray}

    #######################################
    # transfers the blockLabels to the respective geojson file
    print("Transferring the blockLabels to the respective geojson file")
    with open('static/blockLabels.geojson', 'w') as outfile:
    #with open('../static/blockLabels.geojson', 'w') as outfile:
        json.dump(blockLabels, outfile, indent=4)


##############################################################################
##############################################################################
# A few helper functions:
#
# assign300 is a function that can be mapped onto an array, to set properties equal
# to 300, and 300 means that the block is out of district
#
# getSchoolVals is a function that can be mapped onto a 2D array, and it retrieves the
# new school value from each list element's excel file
#
# getBusHazardVals and getBusDistanceVals do the same thing as getSchoolVals,
# they just retrieve different data from the excel files
def assign300(listEl):
    listEl.pop()
    listEl.append(300)
    return listEl

def getSchoolVals(listEl):
    temp = listEl[1].cell_value(schoolRowNum, 5)
    listEl.pop()
    listEl.append(temp)
    return listEl

def getBusHazardVals(listEl):
    temp = listEl[1].cell_value(busRowNum, 2)
    listEl.pop()
    listEl.append(temp)
    return listEl

def getBusDistanceVals(listEl):
    temp = listEl[1].cell_value(busRowNum, 1)
    listEl.pop()
    listEl.append(temp)
    return listEl


##############################################################################
##############################################################################
# A function that records all of the blocks into the geojson file, and gives
# each block its relevant properties
def writeBlocks(block_ids, block_centers):
    print("in writeBlocks(block_ids, block_centers)")
    # Writing to GeoJSON file
    blocks = {}

    ##this is an array of features. Each feature is a dictionary
    featureArray = []

    global currFeature
    currFeature = {}

    # need to delete these blocks from the blocks.geojson
    deletedBlocks = [492, 109, 66, 385, 567, 97, 732, 576, 575, 568, 148, 625]
    check = False

    #####################################################################
    #####################################################################
    # Declaring two global variables that determine which block is being operated
    # on in each iteration of the following for loop. It is incremented accordingly
    # to skip past the blocks that are out of district

    # tracking the row num for the bussing data
    # want to skip the title row, start at 1
    global busRowNum
    busRowNum = 1
    global schoolRowNum
    schoolRowNum = 2  # start at 2 because first two rows are junk

    #####################################################################
    #####################################################################
    # Loops through all of the blocks, computing the necessary properties
    print("Looping through all of the blocks, calculating all of the properties for each block")
    for id in block_ids:
        ####################################################
        newSchool = 0  # clear out these variables each time
        currentSchool = 0

        ####################################################
        # setting bussing property data
        if bussingInfo.cell_value(busRowNum, 0) == id:
            busedForDistance = bussingInfo.cell_value(busRowNum, 1)  # value at row index id and first column
            busedForHazard = bussingInfo.cell_value(busRowNum, 2)

            ######################################
            ######################################
            # Retrieves all of the busing data from all of
            # the bounding tests excel files
            for index in range(5):
                bussingInfo_solutions[index][1] = bussingInfo_solutions[index][0].cell_value(busRowNum, 1)
                bussingInfo_solutions[index][2] = bussingInfo_solutions[index][0].cell_value(busRowNum, 2)

                bussingInfo_singles[index][1] = bussingInfo_singles[index][0].cell_value(busRowNum, 1)
                bussingInfo_singles[index][2] = bussingInfo_singles[index][0].cell_value(busRowNum, 2)

                bussingInfo_norms[index][1] = bussingInfo_norms[index][0].cell_value(busRowNum, 1)
                bussingInfo_norms[index][2] = bussingInfo_norms[index][0].cell_value(busRowNum, 2)

            ######################################
            ######################################
            # Retrieves all of the busing data, distance and hazard
            # from all of the result files for the multiobjective feature
            for index in range(4):
                multiObjResults_BusDistances[index] = list(map(getBusDistanceVals, multiObjResults_BusDistances[index]))
                multiObjResults_BusHazards[index] = list(map(getBusHazardVals, multiObjResults_BusHazards[index]))

            busRowNum = busRowNum + 1

        ######################################
        ######################################
        # if the bus data is not included for that id, just say it's 300. Not in district
        else:
            busedForDistance = 300  # value at row index id and first column
            busedForHazard = 300

            ######################################
            ######################################
            # Assigning 300 to all of the 2D arrays for the
            # bounding tests excel files, for the bussing
            # data specifically
            for index in range(5):
                bussingInfo_singles[index][1] = 300
                bussingInfo_singles[index][2] = 300

                bussingInfo_singles[index][1] = 300
                bussingInfo_singles[index][2] = 300

                bussingInfo_norms[index][1] = 300
                bussingInfo_norms[index][2] = 300

            ######################################
            ######################################
            # Assigning 300 to the 2 arrays for the
            # results for the multiobjective feature,
            # for the bus-distance and bus-hazard data
            # specifically
            for index in range(4):
                multiObjResults_BusDistances[index] = list(map(assign300, multiObjResults_BusDistances[index]))
                multiObjResults_BusHazards[index] = list(map(assign300, multiObjResults_BusHazards[index]))

        ######################################
        ######################################
        # setting schools property data
        if schoolInfo.cell_value(schoolRowNum, 0) == id:
            currentSchool = schoolInfo.cell_value(schoolRowNum, 4)  # value at row index id and first column
            if currentSchool == 300:  # if curr school is not in district, newschool won't be either
                newSchool = 300

                ######################################
                ######################################
                # Assigning 300 to all of the 2D arrays for the
                # bounding tests excel files, for the school data
                # specifically
                for index in range(5):
                    schoolInfo_solutions[index][1] = 300
                    schoolInfo_singles[index][1] = 300
                    schoolInfo_norms[index][1] = 300

                ######################################
                ######################################
                # Assign 300 to the array for the
                # multi-objective results, school data
                # specifically
                for index in range(4):
                    multiObjResults_Schools[index] = list(map(assign300, multiObjResults_Schools[index]))

                schoolRowNum = schoolRowNum + 1

            else:
                newSchool = schoolInfo.cell_value(schoolRowNum, 5)

                ######################################
                ######################################
                # Retrieves the new school assignment data
                # for the 2D arrays for the bounding tests
                # excel files, the school data specifically
                for index in range(5):
                    schoolInfo_solutions[index][1] = schoolInfo_solutions[index][0].cell_value(schoolRowNum, 5)
                    schoolInfo_singles[index][1] = schoolInfo_singles[index][0].cell_value(schoolRowNum, 5)
                    schoolInfo_norms[index][1] = schoolInfo_norms[index][0].cell_value(schoolRowNum, 5)

                ######################################
                ######################################
                # Retrieves the new school assignments
                # from the excel files for the multi-objective
                # feature
                for index in range(4):
                    multiObjResults_Schools[index] = list(map(getSchoolVals, multiObjResults_Schools[index]))

                #onTheSpotSchool = 0
                schoolRowNum = schoolRowNum + 1

        ######################################
        ######################################
        # if the data is not included, say its 300 ie not in district
        else:
            currentSchool = 300  # value at row index id and first column
            newSchool = 300

            ######################################
            ######################################
            # Assigning 300 to the 2D arrays for the bounding
            # tests excel files, for the school data specifically
            for index in range(5):
                schoolInfo_solutions[index][1] = 300
                schoolInfo_singles[index][1] = 300
                schoolInfo_norms[index][1] = 300

            ######################################
            ######################################
            # Assigning 300 to the array for the multi-objective
            # feature
            for index in range(4):
                multiObjResults_Schools[index] = list(map(assign300, multiObjResults_Schools[index]))

        presentation9_10_newSchool = -1
        presentation9_10_neighborhood = -1
        for index in range(725):
            if presentation9_10_enroll.cell_value(index + 1, 0) == int(id):
                presentation9_10_newSchool = presentation9_10_enroll.cell_value(index + 1, 5)
                presentation9_10_neighborhood = presentation9_10_enroll.cell_value(index + 1, 6)
                break

        presentation9_10_numBus = -1
        for index in range(725):
            if presentation9_10_bus.cell_value(index + 1, 0) == int(id):
                presentation9_10_numBus = presentation9_10_bus.cell_value(index + 1, 2)
                break

        presentation9_10_busDistance = -1
        for index in range(725):
            if presentation9_10_dist.cell_value(index + 1, 0) == int(id):
                presentation9_10_busDistance = presentation9_10_dist.cell_value(index + 1, 2)
                break




        ####################################################
        # gets dummy enrollment Data
        enrollment2019 = enrollment[int(id) - 1, 1]
        enrollment2020 = enrollment[int(id) - 1, 2]
        enrollment2021 = enrollment[int(id) - 1, 3]
        enrollment2022 = enrollment[int(id) - 1, 4]
        enrollment2023 = enrollment[int(id) - 1, 5]

        ############################################################
        # Creating fields for the counts of students from
        # various races, in each block

        AfroAmericanNum = genDemoData[int(id) - 1, 23]
        MultiRacialNum = genDemoData[int(id) - 1, 25]
        OtherRaceNum = genDemoData[int(id) - 1, 26]
        CaucasianNum = genDemoData[int(id) - 1, 27]
        HispanicNum = genDemoData[int(id) - 1, 24]

        ############################################################
        # Creating fields for the counts of students from
        # various grade ranges, in each block

        gradesK_2Num = genDemoData[int(id) - 1, 17]
        grades3_5Num = genDemoData[int(id) - 1, 18]
        grades6_8Num = genDemoData[int(id) - 1, 19]

        ############################################################
        # Creating fields for the counts of Free/Reduced Lunch

        totalStudentsNum = genDemoData[int(id) - 1, 1]
        frlNum = genDemoData[int(id) - 1, 28]

        ############################################################
        # Creating fields for the counts of various TWI groups

        twiEnglish = genDemoData[int(id) - 1, 20]
        twiOther = genDemoData[int(id) - 1, 21]
        twiSpanish = genDemoData[int(id) - 1, 22]


        ######################################
        ######################################
        # Checks if the block is out of district by
        # checking if the current school is 300,
        # if so then it assigns 300 to the title One
        # property for the results file and 300 to
        # to the 2D arrays for the bounding tests results
        # if not it retrieves yes or no from the results file
        # and from the bounding tests files and assigns 1 for
        # yes and 0 for no
        if currentSchool == 300:
            titleOne = 300
            for index in range(5):
                titleOneInfo_solutions[index][1] = 300
                titleOneInfo_singles[index][1] = 300
                titleOneInfo_norms[index][1] = 300

        ######################################
        ######################################
        #if not it retrieves yes or no from the results file
        # and from the bounding tests files and assigns 1 for
        # yes and 0 for no
        else:
            if titleOneInfo.cell_value(int(currentSchool) + 1, 10) == "Yes":
                titleOne = 1
            else:
                titleOne = 0

            ######################################
            ######################################
            # retrieves the yeses or nos from each
            # bounding test file and assigns 1 or 0
            # accordingly
            for index in range(5):
                if titleOneInfo_solutions[index][0].cell_value(int(currentSchool) + 1, 10) == "Yes":
                    titleOneInfo_solutions[index][1] = 1
                else:
                    titleOneInfo_solutions[index][1] = 0

                if titleOneInfo_singles[index][0].cell_value(int(currentSchool) + 1, 10) == "Yes":
                    titleOneInfo_singles[index][1] = 1
                else:
                    titleOneInfo_singles[index][1] = 0

                if titleOneInfo_norms[index][0].cell_value(int(currentSchool) + 1, 10) == "Yes":
                    titleOneInfo_norms[index][1] = 1
                else:
                    titleOneInfo_norms[index][1] = 0


        #############################################################
        # we have it in this order bc it messed up the bussingInfo stuff, make a cleaner fix later
        # checking if it needs to be deleted
        for i in range(len(deletedBlocks)):
            if id == deletedBlocks[i]:  # if we are checking an id that belongs to deletedBlocks
                check = True
        if check:
            check = False
            continue  # start over with next id

        # gets ordered vertices for this blockid
        vertexVector = getOrderedVertices(id, block_centers)

        if len(vertexVector) == 0:
            continue

        ######################################
        ######################################
        # currFeature is basically an object that defines
        # a block, so it has its coordinates, its id,
        # its current school assignment, new school assignment,
        # count of Hispanic students, count of 3-5 students,
        # its new school assignment according to all of the result files
        # for the multi-objective feature, and so on...
        currFeature = {"type": "Feature",
                       "geometry": {"type": "Polygon",
                                    "coordinates": [vertexVector]},  # for some reason it needs to be in []
                       "properties": {"id": id,
                                      "busedDistance": busedForDistance,
                                      "busedHazard": busedForHazard,

                                      "currentSchool": currentSchool,
                                      "newSchool": newSchool,

                                      #######################################################
                                      #######################################################
                                      "2019": enrollment2019,
                                      "2020": enrollment2020,
                                      "2021": enrollment2021,
                                      "2022": enrollment2022,
                                      "2023": enrollment2023,
                                      #####################################################
                                      "AfroAmericanNum": AfroAmericanNum,
                                      "CaucasianNum": CaucasianNum,
                                      "HispanicNum": HispanicNum,
                                      "OtherRaceNum": OtherRaceNum,
                                      "MultiRacialNum": MultiRacialNum,
                                      #####################################################
                                      "k-2": gradesK_2Num,
                                      "3-5": grades3_5Num,
                                      "6-8": grades6_8Num,
                                      #####################################################
                                      "frlNum": frlNum,
                                      #####################################################
                                      "totalStudentsNum": totalStudentsNum,
                                      #####################################################
                                      "twiEnglish": twiEnglish,
                                      "twiOther": twiOther,
                                      "twiSpanish": twiSpanish,
                                      #####################################################
                                      "titleOne": titleOne,
                                      "presentation9_10_newSchool": presentation9_10_newSchool,
                                      "presentation9_10_neighborhood": presentation9_10_neighborhood,
                                      "presentation9_10_numBus": presentation9_10_numBus,
                                      "presentation9_10_busDistance": presentation9_10_busDistance
                                      }}

        ######################################
        ######################################
        # Appending the relevant data from
        # the result files for the multi-objective feature
        # adjust these chunks of code as needed
        for percent in range(4):
            for index in range(256):
                currFeature["properties"][str(multiObjResults_Schools[percent][index][0])] = multiObjResults_Schools[percent][index][2]
                currFeature["properties"][str(multiObjResults_BusDistances[percent][index][0])] = multiObjResults_BusDistances[percent][index][2]
                currFeature["properties"][str(multiObjResults_BusHazards[percent][index][0])] = multiObjResults_BusHazards[percent][index][2]

        for index in range(5):
            ######################################
            ######################################
            # Appending the bus-distance and bus-hazard
            # data to each block from the bounding tests
            currFeature["properties"]['busedDistance_solution' + str(index + 1)] = bussingInfo_solutions[index][1]
            currFeature["properties"]['busedHazard_solution' + str(index + 1)] = bussingInfo_solutions[index][2]

            currFeature["properties"]['busedDistance_single' + str(index + 1)] = bussingInfo_singles[index][1]
            currFeature["properties"]['busedHazard_single' + str(index + 1)] = bussingInfo_singles[index][2]

            currFeature["properties"]['busedDistance_norm' + str(index + 1)] = bussingInfo_norms[index][1]
            currFeature["properties"]['busedHazard_norm' + str(index + 1)] = bussingInfo_norms[index][2]

            ######################################
            ######################################
            # Appending the new school assignment data
            # to each block from the bounding tests
            currFeature["properties"]['newSchool_solution' + str(index + 1)] = schoolInfo_solutions[index][1]
            currFeature["properties"]['newSchool_single' + str(index + 1)] = schoolInfo_singles[index][1]
            currFeature["properties"]['newSchool_norm' + str(index + 1)] = schoolInfo_norms[index][1]

            ######################################
            ######################################
            # Appending the title one data to each
            # block from the bounding tests
            currFeature["properties"]['titleOne_solution' + str(index + 1)] = titleOneInfo_solutions[index][1]
            currFeature["properties"]['titleOne_single' + str(index + 1)] = titleOneInfo_singles[index][1]
            currFeature["properties"]['titleOne_norm' + str(index + 1)] = titleOneInfo_norms[index][1]

        ######################################
        ######################################
        # Appending each currFeature or "block"
        # to a list that holds all of the currFeatures
        featureArray.append(currFeature)

    ######################################
    ######################################
    # adds the featureCollection prefix and the array of features to JSON
    # don't need the other prefixes/suffixes bc they are not part of the data source
    blocks = {"type": "FeatureCollection",
              "features": featureArray}

    ######################################
    ######################################
    # Transferring all of the blocks into the
    # geojson file
    print("Transferring all of the blocks into the geojson file")
    with open('static/blocks.geojson', 'w') as outfile:
    #with open('../static/blocks.geojson', 'w') as outfile:
        json.dump(blocks, outfile, indent=4)


def writeSchoolNames(block_ids, block_centers):
    print("writing school names")


######################################
######################################
# given a blockid and list of block_centers, gets list of ordered vertices
def getOrderedVertices(id, block_centers):
    # gets the block center coordinates for each blockid
    block_center_coor_list = block_centers[np.where(block_centers[:, 0] == id)]
    block_center_coor = [block_center_coor_list[0][1], block_center_coor_list[0][2]]
    vertex_set = set()  # set bc removes duplicates

    # get list of vertices associated with given blockid
    for i in edge_coor_remove_deadend:  # i is a row of CSV
        blockid = i[5]
        if blockid == id:
            vertex_set.add((i[1], i[2]))
            vertex_set.add((i[3], i[4]))

    vertex_set = list(vertex_set)
    if len(vertex_set) > 0:
        myVertexSorted = sort_vertex(vertex_set, block_center_coor)

        # vertex array needs to start and end with the same vertex to form a closed polygon
        myVertexSorted.append(myVertexSorted[0])
        return myVertexSorted
    return vertex_set


######################################
######################################
# Given a Vertex (latitude, longitude pair) and the Center
# of a given block (latitude, longitude pair)
# returns the angle between vertex and center
# [float, float], [float, float] -> float
def angle_center(vertex, center):
    x0 = vertex[0] - center[0]
    y0 = vertex[1] - center[1]

    if x0 > 0: \
            return np.arctan(y0 / x0)
    if x0 < 0:
        return np.arctan(y0 / x0) + np.pi


######################################
######################################
# given a list of vertices (start and end vertices, no duplicates)
# and center, sorts them in clockwise order
# gives you lat, long, angle
def sort_vertex(vertex_list, center):
    list_new = []
    list_no_angle = []

    for vertex in vertex_list:
        list_new.append([vertex[0], vertex[1], angle_center(vertex, center)])

    # sorting list_new by the attribute at index 2 (angle_center) in each item
    # aka sorting the list of vertices by their angles to the center
    list_new = sorted(list_new, key=itemgetter(2))
    ##list_new is a vector of vertices and angles. only want the vertices

    for row in list_new:
        list_no_angle.append([row[0], row[1]])

    return list_no_angle

####################################################################
####################################################################
# This segment of code is for allowing a user to call this script from the
# command line. Changes to the file paths used in this script
# would need to be made for this to work correctly.
if __name__ == '__main__':
    writeToFile()