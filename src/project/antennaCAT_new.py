##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/project/antennaCAT_new.py'
#   Class for creating new antennaCAT projects
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import os
import project.config.antennaCAT_config as c

DIR_LIST = c.DIR_LIST

class NewAntennaCATProject():
    def __init__(self, PC):
        self.PC = PC

    def createProjectFile(self, filepath):
        # split path into name and dir
        resultsDir, projDir, catFile = self.splitPathIntoParts(filepath)
        # make main project directory
        os.makedirs(resultsDir)
        #create an empty antennaCAT project file in newDir
        with open(filepath, 'w') as fp:
            pass
        # make subdirectories used by project in newDir
        self.checkProjectDirsExist(resultsDir)
        #set the project paths - everything else is optional
        self.PC.setProjectDirectory(projDir)
        self.PC.setResultsDirectory(resultsDir) #full path
        self.PC.setProjectName(catFile)  
        self.PC.setFullPath(filepath) # this is everything. mostly used for backup if something is weird
    
    def splitPathIntoParts(self, filepath):
        pathArr = os.path.split(filepath) #head, tail. Makes sure no file selected by accident
        projDir = pathArr[0]
        catFile = pathArr[1]
        resultsDir = pathArr[1].split('.')[0]
        resultsDir = os.path.join(projDir, resultsDir)
        return resultsDir, projDir, catFile


    def checkProjectDirsExist(self, newDir):
        # this function checks that needed directories for operation exists, 
        # and creates them if they do not
        for dl in DIR_LIST:
            checkDir = os.path.join(newDir, dl)
            isdir = os.path.isdir(checkDir)
            if isdir == False: # directory doesn't exist. create it                
                os.makedirs(checkDir)