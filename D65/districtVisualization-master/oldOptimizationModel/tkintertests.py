# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 00:16:36 2018

@author: dipayan
"""

from tkinter import *

# initializes 3 generic input variables
input1 = 0
input2 = 0
input3 = 0
input4 = 0
input5 = 0
input6 = 0

# function is_goodinput(x) takes an input x and tests to see if it is numeric and nonnegative
# returns 1 if both conditions are satisfied, 0 otherwise
def is_goodinput(x):
    # try-except error catcher; returns 0 if the input cannot be converted to a number
    try:
        num = float(x)
    except ValueError:
        return 0
    # if input is numeric, tests to see if it is negative and returns 0 if so
    numeric = float(x)
    if numeric < 0:
        return 0
    # if both tests are passed, return 1 and input is declared good
    return 1

# function saveinputs() tests to see if the values entered in the GUI satisfy the conditions set by is_goodinput()
# returns warninglabel if any of the inputs fail the test
# if all inputs satisfy the tests, assign them to the 3 generic input variables and then close the GUI window
def saveinputs():
    # declare global use of pre-established values for generic input variables
    global input1
    global input2
    global input3
    global input4
    global input5
    global input6
    
    global warninglabel
    
    # defines a warning message to be printed if an input fails the is_goodinput() test
    warninglabel = Label(root, text="Error: \nInputs must be numeric and nonnegative", fg="red")
    
    # checks to see if the values entered in any of the GUI fields fail the is_goodinput() test
    # returns the warning label if any fail
    if (is_goodinput(maxreassign_field.get()) == 0) or (is_goodinput(distobj_field.get()) == 0) or (is_goodinput(excess_field.get()) == 0) or (is_goodinput(totbus_field.get()) == 0) or (is_goodinput(numbus_field.get()) == 0) or (is_goodinput(title1_field.get()) == 0):
        warninglabel.grid(row=25, column=5)
        return
    
    # after all field-entered values pass the is_goodinput() test, assign them to respective input variables
    input1 = maxreassign_field.get()
    input2 = distobj_field.get()
    input3 = excess_field.get()
    input4 = totbus_field.get()
    input5 = numbus_field.get()
    input6 = title1_field.get()
    
    # close the GUI window
    root.destroy()

# userinput() creates the GUI window and defines its elements
def userinput():
    # root is the window reference, needs to be globally used in other functions
    global root
    
    # create a GUI window using the Tk() function
    root = Tk()  
      
    # set the title of GUI window 
    root.title("Northwestern/D65") 
      
    # set the configuration of GUI window - size and is topmost window
    root.geometry("280x840")       
    root.attributes("-topmost", True)    
    
    rows = 0
    while rows < 30:
        root.rowconfigure(rows, weight=1)
        rows += 1 
    
    cols = 0
    while cols < 9:
        root.columnconfigure(cols,weight=1)
        cols += 1
      
    n = 0
    m = 5
    
    # define variables to store user values
    #max_reassign = DoubleVar()
    contig_flag = IntVar()
    
    global maxreassign_field
    global distobj_field
    global excess_field
    global totbus_field
    global numbus_field
    global title1_field
    
    # define form components    
    heading = Label(root, text="Model Parameters", font=('bold'))
    
    reassigns = Label(root, text="Maximum % of blocks reassigned \n[enter value 0 - 100]") 
    maxreassign_field = Entry(root, justify="center") 
    maxreassign_field.insert(0, "15")
    
    distobjs = Label(root, text="Objective scaling factor: \naverage student travel distance (km) \n[enter value ≥ 0]")
    distobj_field = Entry(root, justify="center") 
    distobj_field.insert(0, "1")
    
    excesses = Label(root, text="Objective scaling factor: \n expected yearly # of excess students per school \n[enter value ≥ 0]")
    excess_field = Entry(root, justify="center") 
    excess_field.insert(0, "1")
    
    totbus = Label(root, text="Objective scaling factor: \n expected yearly # of students bused \n[enter value ≥ 0]")
    totbus_field = Entry(root, justify="center") 
    totbus_field.insert(0, "1")

    numbus = Label(root, text = "Objective scaling factor: \n expected yearly # of buses used per school \n[enter value ≥ 0]")    
    numbus_field = Entry(root, justify="center") 
    numbus_field.insert(0, "1")
    
    title1 = Label(root, text = "Objective scaling factor: \n number of Title 1 eligible schools \n[enter value ≥ 0]")    
    title1_field = Entry(root, justify="center") 
    title1_field.insert(0, "1")    
    
    contigq = Checkbutton(root, text = "Require contiguity?", variable = contig_flag, onvalue = 1, offvalue = 0 )
    
    
    # format form components
    heading.grid(row=n, column=m)
     
    reassigns.grid(row=n + 3, column=m) 
    maxreassign_field.grid(row=n + 4, column=m) 
    
    distobjs.grid(row = n + 7, column=m)
    distobj_field.grid(row = n + 8, column = m)
    
    excesses.grid(row = n + 11, column=m)
    excess_field.grid(row = n + 12, column = m)
    
    totbus.grid(row = n+15, column = m)
    totbus_field.grid(row = n+16, column = m)
    
    numbus.grid(row = n + 19, column = m)
    numbus_field.grid(row = n + 20, column = m)
    
    title1.grid(row = n + 23, column = m)
    title1_field.grid(row = n + 24, column = m)
    
    contigq.grid(row = n + 25, column = m)
    
      
    # create a Submit Button and place at bottom 
    submit = Button(root, text="Run", fg="Black", bg="White", command = saveinputs) 
    submit.grid(row=n + 26, column=m) 
     
    max_reassign = maxreassign_field.get()
    
    # start the GUI 
    root.mainloop() 
    
    return float(input1), float(input2), float(input3), float(input4), float(input5), float(input6), contig_flag.get()