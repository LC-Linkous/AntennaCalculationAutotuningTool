##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/project/antennaCAT_open.py'
#   Class for opening antennaCAT project
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 28, 2025
##--------------------------------------------------------------------\

import os
import pandas as pd
import copy

import project.config.antennaCAT_config as c

class OpenAntennaCATProject():
    def __init__(self, DC, PC, SO):
        self.DC = DC
        self.PC = PC
        self.SO = SO # this might need to be removed. 
                    # there's too many mem object passes. 
                    # might be better to reconstruct

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
        self.PC.setFullPath(filepath) # this is everything. mostly used for backup if something is weird


        self.openFileAndSetProjectValues(filepath)


    def splitPathIntoParts(self, filepath):
        pathArr = os.path.split(filepath) #head, tail. Makes sure no file selected by accident
        projDir = pathArr[0]
        catFile = pathArr[1]
        resultsDir = pathArr[1].split('.')[0]
        newDir = os.path.join(projDir, resultsDir)
        return newDir, projDir, catFile

    def openFileAndSetProjectValues(self, filepath):
        #TODO: needs detailed error checks for logging
        # Also, figure out the SO set up bc that's not df based

        # read in the file
        PC_import = pd.read_pickle(filepath) 

        # set main shared objects
        self.DC.import_DC(copy.deepcopy(PC_import['df_DC'][0]))
        self.PC.import_PC(copy.deepcopy(PC_import['df_PC'][0]))
        self.SO.import_SO(copy.deepcopy(PC_import['df_SO'][0]))

        # SO is set up from vals from DC and PC
        #self.SO.setupSI(softwareSelection, softwarePath, numLicenses)
        self.SO.openFileSetupSI()


        # after these are imported, higher up in the project structure
        # it has to go down the list of major pages and set everything.
        # That does not happen HERE




