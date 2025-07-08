##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_configuration/notebook_projectSettings.py'
#   Class for project settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_settings.ancat_info.panel_ancat import AnCATNotebookPage
from gui.page_settings.ancat_info.panel_license import LicenseNotebookPage

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class AnCATInformationNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(450, -1))
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
       
        self.page_ancat = AnCATNotebookPage(self) 
        self.page_license = LicenseNotebookPage(self) 

        
        self.AddPage(self.page_ancat, "AntennaCAT")
        self.AddPage(self.page_license, "License")




    def updateSettingsProjectInformation(self):
        pass

    def applyLoadedProjectSettings(self, PC):        
        pass



