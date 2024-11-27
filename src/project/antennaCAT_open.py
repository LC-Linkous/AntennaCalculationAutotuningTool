##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/project/antennaCAT_open.py'
#   Class for opening antennaCAT project
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os

import project.config.antennaCAT_config as c

class OpenAntennaCATProject():
    def __init__(self, DC, PC, SO):
        self.DC = DC
        self.PC = PC
        self.SO = SO

    def openProjectFile(self, filepath):
        validProject = False
        newDir = None
        projDir = None
        catFile = None
        if os.path.exists(filepath) == True:
            validProject = True
            # split path into name and dir
            newDir, projDir, catFile = self.splitPathIntoParts(filepath)

        if validProject == False:
            # print("failed to open project")
            return

        # set save paths - 
        self.PC.setProjectDirectory(projDir)
        self.PC.setResultsDirectory(newDir) #full path
        self.PC.setProjectName(catFile)

        self.openFileAndSetProjectValues(filepath)


    def splitPathIntoParts(self, filepath):
        pathArr = os.path.split(filepath) #head, tail. Makes sure no file selected by accident
        projDir = pathArr[0]
        catFile = pathArr[1]
        resultsDir = pathArr[1].split('.')[0]
        newDir = os.path.join(projDir, resultsDir)
        return newDir, projDir, catFile

    def openFileAndSetProjectValues(self, filepath):
        
        #TODO: set the rest of it
        self.readTempDebugInfo(filepath)

    def readTempDebugInfo(self, filepath):
        tmpArr=[]
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                tmpArr.append(line)

        if len(tmpArr) > 0:
            softwareSelection = str(tmpArr[0])
            softwarePath = str(tmpArr[1])
            numLicenses = float(tmpArr[2])
            self.PC.setSimulationSoftware(softwareSelection)
            self.PC.setSimulationSoftwarePath(softwarePath)
            self.PC.setNumSimulationLicenses(numLicenses)

            self.SO.setupSI(softwareSelection, softwarePath, numLicenses)

        # else:
        #     print("read in error with file in antennaCAT_open.py")

