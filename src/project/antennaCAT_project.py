##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/project/antennaCAT_project.py'
#   Class for batch configuration setup to be passed to sim object
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import project.config.antennaCAT_config as c
#these actions are broken up for easier future expansion
from project.antennaCAT_new import NewAntennaCATProject
from project.antennaCAT_open import OpenAntennaCATProject
from project.antennaCAT_save import SaveAntennaCATProject

class AntennaCATProject():
    def __init__(self, DC, PC, SO):
        self.DC = DC  
        self.PC = PC
        self.SO = SO

        self.currentActionObj = None #new, save, open obj switch

    def createNewProject(self, pathname):
        self.currentActionObj = NewAntennaCATProject(self.PC)
        self.currentActionObj.createProjectFile(pathname)

    def openExistingProject(self, pathname):
        self.currentActionObj = OpenAntennaCATProject(self.DC, self.PC, self.SO)
        self.currentActionObj.openProjectFile(pathname)

    def saveProject(self):
        self.currentActionObj = SaveAntennaCATProject(self.DC, self.PC, self.SO)
        self.currentActionObj.saveProjectFile()

    def saveAsProject(self, pathname):
        self.currentActionObj = SaveAntennaCATProject(self.DC, self.PC, self.SO)
        self.currentActionObj.saveProjectFileAs(pathname)
               

