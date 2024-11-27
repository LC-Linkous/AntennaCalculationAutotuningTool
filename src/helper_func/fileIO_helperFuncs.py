##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/helper_func/fileIO_helperFuncs.py'
#   Helper functions for reading and writing files
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

#######################################################################
# Generic helper functions
#######################################################################

import wx
import os

#######################################################################
# Writing Out Files
#######################################################################
def writeOut(projectPath, inputTxt):
    noErrors = errorCheckOut(projectPath, inputTxt)
    if noErrors:
        writeToFile(projectPath, inputTxt)
    return noErrors

def writeToFile(projectPath, inputTxt):
    filepath = projectPath
    file = open(filepath, "w")
    for l in inputTxt:
        file.write(l)
    file.close()

def errorCheckOut(projectPath, inputTxt):
    noErrors = True
    if projectPath==None:
        noErrors = False
        wx.MessageBox('Invalid path for file.', 'Error', wx.OK | wx.ICON_ERROR)
        return noErrors
    if inputTxt==[] or inputTxt==[[]] or inputTxt==None or inputTxt==str(None):
        noErrors = False
        wx.MessageBox('No file data. File will not be written.', 'Error', wx.OK | wx.ICON_ERROR)
    return noErrors

#######################################################################
# Reading in Files
#######################################################################

def readIn(projectPath):
    inputTxt = None
    #error check
    noErrors = errorCheckIn(projectPath)
    if noErrors:
        inputTxt = readFileIn(projectPath)
    return inputTxt, noErrors

def readFileIn(filename):
    txt = []
    file1 = open(filename, 'r')
    while True:
        l = file1.readline()
        txt.append(l)
        if not l:
            break
    return txt

def errorCheckIn(projectPath):
    noErrors = True
    if projectPath==None:
        noErrors = False
        wx.MessageBox('Invalid path for file. No path information.', 'Error', wx.OK | wx.ICON_ERROR)
        return noErrors
    if os.path.exists(projectPath)==False:
        noErrors = False
        wx.MessageBox('Invalid path for file.', 'Error', wx.OK | wx.ICON_ERROR)
    return noErrors
