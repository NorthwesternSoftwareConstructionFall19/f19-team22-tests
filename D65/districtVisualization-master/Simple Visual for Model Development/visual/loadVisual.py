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
resultsFile = ("../results.xlsx")
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
    # blocksAssigned = float(request.form.get('blocksAssigned', 0))
    # travelDistance = float(request.form.get('travelDistance', 0))
    # excessStudents = float(request.form.get('excessStudents', 0))
    # contiguity = float(request.form.get('contiguity', 0))
    # studentsBussed = float(request.form.get('studentsBussed', 0))
    # yearlyBusPerSchool = float(request.form.get('yearlyBusPerSchool', 0))
    # titleOneEligibleSchools = float(request.form.get('titleOneEligibleSchools', 0))

    # # Runs the model
    # runModel(blocksAssigned, travelDistance, excessStudents, contiguity,
    #          studentsBussed, yearlyBusPerSchool, titleOneEligibleSchools)

    # Runs the converting to JSON script
    writeToFile()
    return "awesome" # something needs to be returned, "awesome" has no significance




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




