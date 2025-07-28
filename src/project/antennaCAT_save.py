##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/project/antennaCAT_save.py'
#   Class for saving antennaCAT projects
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 28, 2025
##--------------------------------------------------------------------\


import os
import numpy as np
import pandas as pd
import copy
import time

import project.config.antennaCAT_config as c
import helper_func.fileIO_helperFuncs as fIO

DIR_LIST = c.DIR_LIST

class SaveAntennaCATProject():
    def __init__(self, DC, PC, SO):
        self.DC = DC  
        self.PC = PC
        self.SO = SO# this might need to be removed. 
                    # there's too many mem object passes. 
                    # might be better to reconstruct

    def saveProjectFile(self):
        #checks file exists
        projectDir = self.PC.getProjectDirectory() # base directory for file and results dir
        projectFile = self.PC.getProjectName()
        resultsDir = self.PC.getResultsDirectory() #the project export file base dir
        filepath = os.path.join(projectDir, projectFile)

        #check if directories exist for results. create if needed
        self.checkProjectDirsExist(resultsDir)

        #check if file exists. create if needed
        self.checkProjectFileExists(filepath)

        #write out to file
        ## set to dictionary, convert to df
        PC_export = {            
            'df_DC': [copy.deepcopy(self.DC.export_DC())],
            'df_PC' : [copy.deepcopy(self.PC.export_PC())],
            'df_SO': [copy.deepcopy(self.SO.export_SO())]}
           

        data_df = pd.DataFrame(PC_export)
        data_df.to_pickle(filepath)


    def saveProjectFileAs(self, filepath):
        #make new project
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

        #save project
        #checks file exists
        filepath = os.path.join(resultsDir, catFile)

        #write out to file
        #TODO: switch this to the real format
        self.saveTempDebugInfo(filepath)


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

    def checkProjectFileExists(self, filepath):
        #create an empty antennaCAT project file if doesnt exist
        if os.path.exists(filepath) == False:            
            with open(filepath, 'w') as fp:
                pass

    def saveTempDebugInfo(self, filepath):
        emSOFTWARE = str(self.PC.getSimulationSoftware())
        emPath = str(self.PC.getSimulationSoftwarePath())
        numLicenses = str(self.PC.getNumSimulationLicenses())
        with open(filepath, 'w') as fp:
            fp.writelines(emSOFTWARE + '\n')
            fp.writelines(emPath + '\n')
            fp.writelines(numLicenses + '\n')


    def writeHeader(self):
        pass


    def writeProjectConfig(self):
        pass


    def writeDesignConfig(self):
        pass