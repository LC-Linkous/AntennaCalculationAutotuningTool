##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/user_settings/notebook_userSettings.py'
#   Class for project settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_settings.user_settings.panel_userInformation import UserInfoNotebookPage

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class UserSettingsNotebook(wx.Notebook):
    def __init__(self, parent, PC):
        wx.Notebook.__init__(self, parent=parent, size=(450, -1))
        self.parent = parent
        self.PC = PC
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
               
        self.page_userInformation = UserInfoNotebookPage(self) 

        self.AddPage(self.page_userInformation, "User Info")
          
    def getUserSettings(self):
        return self.page_userInformation.getValues()


    def applyLoadedProjectSettings(self, PC):        
        self.page_userInformation.applyLoadedProjectSettings(PC)


