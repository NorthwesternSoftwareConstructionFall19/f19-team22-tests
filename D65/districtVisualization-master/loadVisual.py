#######################################################################
#######################################################################
# This script is the connection between all of the important aspects
# of the interactive modeling data visualization tool. It uses flask,
# a Python micro web framework, see tutorials here: https://www.youtube.com/watch?v=ZVGwqnjOKjk,
# https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH



#School district boundaries/Numbering System
# 0 - Dawes
# 1 - Dewey
# 2 - Kingsley
# 3 - Lincoln
# 4 - Lincolnwood
# 5 - Oakton
# 6 - Orrington
# 7 - Walker
# 8 - Washington
# 9 - Willard
# 10 - Bessie Rhodes
# 11 - MLK


#######################################################################
#######################################################################
# Importing all relevant modules/libraries/packages
from oldOptimizationModel.testB1 import *
from writeJSON.writeToJSON import *
from flask import Flask, render_template, request, jsonify
import json

import matplotlib.pyplot as plt
import numpy as np
import xlrd
import matplotlib
import math








#######################################################################
#######################################################################
# Creating the flask object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



#######################################################################
#######################################################################
# A truncate function that allows the user to truncate a float to
# a certain number of digits after the decimal point
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



#######################################################################
#######################################################################
# Global list used to hold the names of the schools currently displayed/
# manipulated
global schoolNameArray
schoolNameArray = ["Dawes", "Dewey", "Kingsley",
                   "Lincoln", "Lincolnwood", "Oakton",
                   "Orrington", "Walker", "Washington",
                   "Willard", "Bessie Rhodes", "MLK"]


####################################################
####################################################
# Opening the results file and going to the
# demographics sheet, made the result file global for future use
# in the script
global resultsFile
resultsFile = ("oldOptimizationModel/results.xlsx")
sheet = xlrd.open_workbook(resultsFile).sheet_by_index(4)

global totalStudentsArray
totalStudentsArray = [] # list to store the total amount of students per school
for schoolRow in range(12):  # runs 12 times for twelve schools
    totalCount = 0
    for index in range(5): # this for loops runs for each racial category
                           # pertaining to the above for loop's current iteration/school
        totalCount = totalCount + int(sheet.cell_value(schoolRow + 1, index + 3)) # adding the count of students
                                                                                  # in each racial group for current school
    totalStudentsArray.append(totalCount)



#######################################################################
#######################################################################
# Currently running all (current number of objective inputs here) objectives each with values of
# something to something, multiObjInputCombinations holds every possible combination
# which is i^o, where i is the number of different input values and o is
# the number of objectives
multiObjInputs = [0, 1, 2, 3]
multiObjInputCombinations = []

# the following for loops fills the inputCombinations list
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
# This helper function is used to fill various dictionaries/lists with open'd excel files.
# Modify this function as needed for your specific needs.
def fillMultiObjResults(multiObj_ObjValues, percentString):
    for index in range(256):
        fileLocation = "./oldOptimizationModel/multiObjective_Results_Percent" + percentString + "/result" + str(
            index + 1) + ".xlsx"

        workbook = xlrd.open_workbook(fileLocation)

        multiObj_ObjValues.append(
            [workbook.sheet_by_index(0), workbook.sheet_by_index(3), workbook.sheet_by_index(4)])
    return  multiObj_ObjValues

#####################################################
#####################################################
# Below is a list(s) of lists of dictionary(ies) that
# can pair respective input combinations with various
# data that one may want to include about each block
print('fillMultiObjResults: 25')
global multiObj_ObjValues_25
multiObj_ObjValues_25 = []
multiObj_ObjValues_25 = fillMultiObjResults(multiObj_ObjValues_25, "25")

print('fillMultiObjResults: 50')
global multiObj_ObjValues_50
multiObj_ObjValues_50 = []
multiObj_ObjValues_50 = fillMultiObjResults(multiObj_ObjValues_50, "50")

print('fillMultiObjResults: 75')
global multiObj_ObjValues_75
multiObj_ObjValues_75 = []
multiObj_ObjValues_75 = fillMultiObjResults(multiObj_ObjValues_75, "75")

print('fillMultiObjResults: 100')
global multiObj_ObjValues_100
multiObj_ObjValues_100 = []
multiObj_ObjValues_100 = fillMultiObjResults(multiObj_ObjValues_100, "100")

global multiObj_ObjValues
multiObj_ObjValues = [multiObj_ObjValues_25, multiObj_ObjValues_50,
                      multiObj_ObjValues_75, multiObj_ObjValues_100]

avgTravelDistance = {}
avgStudentsBused = {}
totalBusses = {}
titleOnes = {}

for percent in range(4):
    print("Retrieving the objective values of all multi-objective results for " + str(25 * (percent + 1)) + "% of blocks reassigned")
    currentPercent = str(25 * (percent + 1))
    for index in range(256):
        avgTravelDistance[currentPercent + '_' + multiObjInputCombinations[index]] = \
                                            multiObj_ObjValues[percent][index][0].cell_value(3, 11)
        avgStudentsBused[currentPercent + '_' + multiObjInputCombinations[index]] = \
            multiObj_ObjValues[percent][index][0].cell_value(5, 11)

        totalBusNum = 0
        for indexBus in range(12):
            totalBusNum = totalBusNum + multiObj_ObjValues[percent][index][1].cell_value(indexBus + 1, 5)
        totalBusses[currentPercent + '_' + multiObjInputCombinations[index]] = totalBusNum

        titleOneCount = 0
        for indexTitle in range(12):
            if multiObj_ObjValues[percent][index][2].cell_value(indexTitle + 1, 10) == "Yes":
                titleOneCount = titleOneCount + 1
        titleOnes[currentPercent + '_' + multiObjInputCombinations[index]] = titleOneCount



#######################################################################
#######################################################################
# Adding a route for the home page
@app.route('/')
def index():
    return render_template("mapHomePage.html")

#######################################################################
#######################################################################
# Adding routes to all of the relevant pages of the web application
@app.route('/SchoolAssignment')
def test():
    return render_template("School_Assignment.html")

@app.route('/multiObjective')
def comparingSolutions():
    ####################################
    ####################################
    # Passing in the objective values as JSON
    # strings, because Python dictionaries do
    # not translate to JavaScript objects directly,
    # so JSON is used a bridge between the two programming
    # languages
    return render_template("multiObjective.html", avgTravelDistance = json.dumps(avgTravelDistance),
                                                  avgStudentsBused = json.dumps(avgStudentsBused),
                                                  totalBusses = json.dumps(totalBusses),
                                                  titleOnes = json.dumps(titleOnes))



####################################
####################################
# Some comment here
schoolCapacities = [459, 612, 459, 612, 459,
                        612, 459, 459, 638, 612]
file_schoolIndices = [13, 14, 17, 18, 19,
                          21, 22, 23, 24, 25]

def overCapacity_CurrYear(currentYearData, overCapacity_18, currYear_SchoolTotals):
    ####################################
    ####################################
    # Some comment here

    for index in range(2160):
        for schoolIndex in range(10):
            currYear_SchoolTotals[schoolIndex] += currentYearData.cell_value(index + 1, file_schoolIndices[schoolIndex])

    for index in range(10):
        if currYear_SchoolTotals[index] > schoolCapacities[index]:
            overCapacity_18[index] = 1

    return overCapacity_18

@app.route('/predictionScenarios')
def predictionScenarios():
    ####################################
    ####################################
    # Some comment here

    currentYearData = xlrd.open_workbook("./writeJSON/Current_year.xlsx").sheet_by_index(0)
    overCapacity_18 = [0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0]
    currYear_SchoolTotals = [0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0]

    otherProjections = xlrd.open_workbook("./writeJSON/Projections_v2.xlsx").sheet_by_index(0)



    return render_template("predictionScenarios.html", overCapacity_18 = overCapacity_CurrYear(currentYearData,
                                                                                               overCapacity_18,
                                                                                               currYear_SchoolTotals),
                                                        )


#######################################################################
#######################################################################
# Render_template is really cool because how it works is that
# you pass in the html file to want to be displayed/rendered
# and then you pass in various variables you want to use in the html file
# along with their values. To use the variable you pass in, in the actual
# html file, you use this format: {{ variable name here }}
# if a dictionary is passed in then use this format: {{ dictionary name here|safe }}
# if a list is passed in then use this format to index it: {{ list name here }}[ index here ]


@app.route('/boundingTests_solutions')
def boundingTests_solutions():
    return render_template("boundingTests.html", methodName = 'solution')

@app.route('/boundingTests_single')
def boundingTests_single():
    return render_template("boundingTests.html", methodName = 'single')

@app.route('/boundingTests_norm')
def boundingTests_norm():
    return render_template("boundingTests.html", methodName = 'norm')

@app.route('/Schools')
def schools():
    return render_template("Individual_Schools_HomePage.html")

@app.route('/twi_grade_groups')
def twi_grade_groups():
    return render_template("twi_grade_groups.html")


#######################################################################
#######################################################################
# Adding individual routes for each school and their respective pages.
# Passing in the school name and number to use in a general school page
# template.
@app.route('/dawes')
def dawes():
    return render_template("schoolLevelAnalysis.html", schoolNum= 0, schoolName= 'Dawes')

@app.route('/dewey')
def dewey():
    return render_template("schoolLevelAnalysis.html", schoolNum= 1, schoolName= 'Dewey')

@app.route('/kingsley')
def kingsley():
    return render_template("schoolLevelAnalysis.html", schoolNum= 2, schoolName= 'Kingsley')

@app.route('/lincoln')
def lincoln():
    return render_template("schoolLevelAnalysis.html", schoolNum= 3, schoolName= 'Lincoln')

@app.route('/lincolnwood')
def lincolnwood():
    return render_template("schoolLevelAnalysis.html", schoolNum= 4, schoolName= 'Lincolnwood')

@app.route('/oakton')
def oakton():
    return render_template("schoolLevelAnalysis.html", schoolNum= 5, schoolName= 'Oakton')

@app.route('/orrington')
def orrington():
    return render_template("schoolLevelAnalysis.html", schoolNum= 6, schoolName= 'Orrington')

@app.route('/walker')
def walker():
    return render_template("schoolLevelAnalysis.html", schoolNum= 7, schoolName= 'Walker')

@app.route('/washington')
def washington():
    return render_template("schoolLevelAnalysis.html", schoolNum= 8, schoolName= 'Washington')

@app.route('/willard')
def willard():
    return render_template("schoolLevelAnalysis.html", schoolNum= 9, schoolName= 'Willard')

@app.route('/bessieRhodes')
def bessieRhodes():
    return render_template("schoolLevelAnalysis.html", schoolNum= 10, schoolName= 'Bessie Rhodes')

@app.route('/mlk')
def mlk():
    return render_template("schoolLevelAnalysis.html", schoolNum= 11, schoolName= 'MLK')


###############################################################
###############################################################
# Adding a route and input function to communicate to the model
# code and run the optimization code successfully, update the
# results excel file, rerun the writeToJSON scripts, and
# update the blocks. Refresh the page to see changes
@app.route('/square/', methods=['POST'])
def square():
    # inputs are converted into floats to avoid data type issues
    blocksAssigned = float(request.form.get('blocksAssigned', 0))
    travelDistance = float(request.form.get('travelDistance', 0))
    excessStudents = float(request.form.get('excessStudents', 0))
    contiguity = float(request.form.get('contiguity', 0))
    studentsBussed = float(request.form.get('studentsBussed', 0))
    yearlyBusPerSchool = float(request.form.get('yearlyBusPerSchool', 0))
    titleOneEligibleSchools = float(request.form.get('titleOneEligibleSchools', 0))

    # Runs the model
    runModel(blocksAssigned, travelDistance, excessStudents, contiguity,
             studentsBussed, yearlyBusPerSchool, titleOneEligibleSchools)

    # Runs the converting to JSON script
    writeToFile()
    return "awesome" # something needs to be returned, "awesome" has no significance


###############################################################
###############################################################
# This route is added to a produce a bar graph created by
# matplotlib
@app.route('/titleOneBarGraph.png')
def titleOneBarGraph():
    plt.figure(figsize=(32, 20))

    # To open Workbook
    wb = xlrd.open_workbook(resultsFile)
    sheet = wb.sheet_by_index(4)

    # Note: to obtain the row 0 and column 0
    # value, do this:
    # sheet.cell_value(0, 0)

    frlProportionArray = [] # list to store the percent of frl students in each school
    for schoolRow in range(12): # runs 12 times for twelve schools
        if (totalStudentsArray[schoolRow] == 0):
            frlProportionArray.append(0)
        else:
            # truncating proportion to two decimals and multiplying by 100 to get base 10 numbers
            frlProportion = round(((int(sheet.cell_value(schoolRow + 1, 2)) / totalStudentsArray[schoolRow]) * 100), 2)
            frlProportionArray.append(frlProportion)

    bars = plt.bar(schoolNameArray, frlProportionArray, width=0.6)
    plt.xlabel('D65 Schools')
    plt.ylabel('Percentage of Students that Are Free/Reduced Lunch')
    plt.yticks(np.arange(0, 101, 10))
    plt.title('Percentage of FRL Students Per School')

    def autolabel(bars):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            plt.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(bars)

    #######################################################################
    #######################################################################
    # The figure is saved first, then it is linked to a short HTML file
    # allowing the figure to be displayed despite being stored locally on one's computer
    # (yippee!!!)
    # So with the render template, the "url" that is passed in is the location of the image
    # with respect to where this Python function is being called, and that is why the image
    # has to be saved first or else Python will produce some error saying the image/file
    # does not exist
    plt.savefig('./static/titleOneBarGraph.png')
    return render_template('displayingMatplotlib_Figures.html', name='new_plot', url='./static/titleOneBarGraph.png')

###############################################################
###############################################################
# This route is added to a produce a pie chart created by
# matplotlib
@app.route('/reassignmentGraph.png')
def reassignmentGraph():
    plt.figure(figsize=(56, 40))

    # To open Workbook
    wb = xlrd.open_workbook(resultsFile)
    sheet = wb.sheet_by_index(0)

    # loading in the demographic data using np, because
    # it is a CSV, and xlsxwriter only works with Excel files
    demographicData = np.loadtxt("./writeJSON/Demographic Data 2018-2019.csv", skiprows=1, delimiter=",")

    # stores the aggregate amount of students that are in blocks that WERE reassigned
    # and the aggregate amount of students that are in blocks that WERE NOT reassigned
    reassignedStudentCount = 0
    not_reassignedStudentCount = 0

    # stores the aggregate amount of frl students that are in blocks that WERE reassigned
    # and the aggregate amount of frl students that are in blocks that WERE NOT reassigned
    frl_reassignedStudentCount = 0
    frl_not_reassignedStudentCount = 0

    for index in range(828):
        # checking for the empty string which would mean that
        # the loop is currently analyzing a block that is
        # "out of district"/not considered
        if sheet.cell_value(index + 2, 5) == '':
            continue
        # this subtracts the current block's new school value from the old school,
        # so a difference of 0 means that the new school and old school are the same
        # any other value means that the block was reassigned
        reassigned_or_not = int(float(sheet.cell_value(index + 2, 4))) - int(float(sheet.cell_value(index + 2, 5)))
        if (reassigned_or_not == 0):
            not_reassignedStudentCount = not_reassignedStudentCount + float(demographicData[index, 1])
            frl_not_reassignedStudentCount = frl_not_reassignedStudentCount + float(demographicData[index, 28])
        else:
            reassignedStudentCount = reassignedStudentCount + float(demographicData[index, 1])
            frl_reassignedStudentCount = frl_reassignedStudentCount + float(demographicData[index, 28])


    # formats each wedge in the pie chart according to which percent
    # is currently being formatted
    def func(pct, allvals):
        if abs(pct - (reassignedStudentCount / 148.06)) < 0.001:
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}% of students".format(pct, absolute) + \
                   '\nFree/Reduced Lunch: ' + str(frl_reassignedStudentCount)
        elif abs(pct - (not_reassignedStudentCount / 148.06)) < 0.001:
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}% of students".format(pct, absolute) + \
                   '\nFree/Reduced Lunch: ' + str(frl_not_reassignedStudentCount)
        else:
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}% of students".format(pct, absolute)

    legendLabels = ['% of Students Actually Reassigned',
                    "% of Students That Weren't Reassigned",
                    "Non-D65 Students"]

    wedges, texts, autotexts = plt.pie([reassignedStudentCount / 14806,
                                                not_reassignedStudentCount / 14806,
                                                1 - ((reassignedStudentCount + not_reassignedStudentCount) / 14806)],
                                     autopct=lambda pct: func(pct, [reassignedStudentCount / 14806,
                                                                    not_reassignedStudentCount / 14806,
                                                                    1 - ((reassignedStudentCount + not_reassignedStudentCount) / 14806)]),
                                     labels=legendLabels,
                                     textprops=dict(color="w"))

    plt.legend(wedges, legendLabels,
              loc=5,
              bbox_to_anchor=(1.4, 1.05),
              prop= {'size': 60})

    # change the size field to adjust the font size of
    # the labels for the pie chart wedges
    plt.setp(autotexts, size=45, weight="bold")

    plt.title('Reassigned v. Not Reassigned', fontdict= {'fontsize': 50})
    plt.savefig('./static/reassignment.png')
    return render_template('displayingMatplotlib_Figures.html', name='new_plot', url='./static/reassignment.png')


###############################################################
###############################################################
# This route is added to a produce a bar graph created by
# matplotlib
@app.route('/gradeDistributionGraph.png')
def gradeDistributionGraph():
    plt.figure(figsize=(18, 9))

    # To open Workbook
    wb = xlrd.open_workbook(resultsFile)
    sheet = wb.sheet_by_index(4)

    # lists to contain each school's k-2 and 3-5 proportions
    # the model currently outputs a higher student population for
    # each school (which will be corrected at some point I think)
    # so each school has more students than it actually should
    gradesk_2_proportions = []
    grades3_5_proportions = []
    otherProportions = []

    for schoolIndex in range(10):
        gradesk_2_proportions.append(truncate((sheet.cell_value(schoolIndex + 1, 8) / totalStudentsArray[schoolIndex]), 2))
        grades3_5_proportions.append(truncate((sheet.cell_value(schoolIndex + 1, 9) / totalStudentsArray[schoolIndex]), 2))

        otherProp = 1 - gradesk_2_proportions[schoolIndex] - grades3_5_proportions[schoolIndex]
        otherProp = truncate(otherProp, 2)
        if otherProp < 0:
            otherProportions.append(0)
        else:
            otherProportions.append(otherProp)

    # appending values of zero to fill in the lists to account
    # for Bessie Rhodes and MLK, which are currently not being
    # manipulated in the model
    gradesk_2_proportions.append(0)
    gradesk_2_proportions.append(0)
    grades3_5_proportions.append(0)
    grades3_5_proportions.append(0)
    otherProportions.append(0)
    otherProportions.append(0)

    # truncating each proportion to two decimal places
    gradesk_2_proportions = [truncate(x * 100, 2) for x in gradesk_2_proportions]
    grades3_5_proportions = [truncate(x * 100, 2) for x in grades3_5_proportions]
    otherProportions = [truncate(x * 100, 2) for x in otherProportions]

    print(np.arange(len(schoolNameArray)))
    x = np.arange(0, 60, 5) # the label locations
    print(x)
    width = 0.70  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - (width * 1.15), gradesk_2_proportions, width, label='K-2')
    rects3 = ax.bar(x, grades3_5_proportions, width, label='3-5')
    rects2 = ax.bar(x + (width * 1.15), otherProportions, width, label='Other')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage of Total Students in the School', fontdict={'fontsize': 8})
    ax.set_xlabel('Schools', fontdict={'fontsize': 8})
    ax.set_title('Grade Distribution by School', fontdict={'fontsize': 8})
    ax.set_xticks(x)
    ax.set_xticklabels(schoolNameArray, fontdict={'fontsize': 5.5})
    ax.set_yticks([10, 20, 30, 40, 50, 60, 70, 80])
    ax.set_yticklabels(labels= [10, 20, 30, 40, 50, 60, 70, 80],
                      fontdict= {'fontsize': 6})
    ax.legend(loc=5,
              bbox_to_anchor=(1.12, 1),
              prop= {'size': 9})

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        fontsize= 6,
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.savefig('./static/gradeDistribution.png')
    return render_template('displayingMatplotlib_Figures.html', name='new_plot', url='./static/gradeDistribution.png')


###############################################################
###############################################################
# This route is added to a produce a bar graph created by
# matplotlib
@app.route('/predictionGraph1.png')
def predictionGraph1():
    fig = plt.figure(figsize=(18, 9))

    predictionFile = (xlrd.open_workbook("writeJSON/Predictions_All_Fields.xlsx")).sheet_by_index(0)

    total_18 = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    total_23 = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    total_28 = [
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0
            ]

    total_33 = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    def incrementStudentCounts(rowNum, givenList):

        excelFileIndexList = [13, 14, 17, 18, 19, 21, 22, 23, 24, 25]

        for index in range(10):
            givenList[index] = givenList[index] + predictionFile.cell_value(rowNum, excelFileIndexList[index])

        return givenList

    for index in range(34800):

        currentYear = int(predictionFile.cell_value(index + 1, 1))
        currentSample = predictionFile.cell_value(index + 1, 3)
        currentGrade = predictionFile.cell_value(index + 1, 2)

        if currentYear == 18 and currentSample == 'Sample1' and currentGrade != "g_6_8":
            total_18 = incrementStudentCounts(index + 1, total_18)
        elif currentYear == 23 and currentSample == 'Sample1' and currentGrade != "g_6_8":
            total_23 = incrementStudentCounts(index + 1, total_23)
        elif currentYear == 28 and currentSample == 'Sample1' and currentGrade != "g_6_8":
            total_28 = incrementStudentCounts(index + 1, total_28)
        else:
            total_33 = incrementStudentCounts(index + 1, total_33)

    x = [18, 23, 28, 33]

    for index in range(10):

        subplot = fig.add_subplot(5, 2, (index+1))
        subplot.scatter(x,  [total_18[index], total_23[index], total_28[index], total_33[index]], s=200, marker=(index))
        subplot.set_title(str(schoolNameArray[index]))

    plt.savefig('./static/predictionGraph1.png')
    return render_template('displayingMatplotlib_Figures.html', name='new_plot', url='./static/predictionGraph1.png')



#######################################################################
#######################################################################
# I think it helps to prevent caching ("storing the result of an operation
#  so that future requests return faster"); all you have to do is reload
# the page to see changes to the map, clear the cache in your browser
# every now and then though
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

#######################################################################
#######################################################################
# When this Python script is called this command is called too, to actively
# host the routes on a local server, to change the port (like 5000 or 3000)
# run app.run(debug=True, port = 3000), app.run MUST be placed at the end of
# the script
app.run(debug=True)




