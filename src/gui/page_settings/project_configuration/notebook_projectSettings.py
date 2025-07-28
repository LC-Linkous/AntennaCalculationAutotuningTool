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
from gui.page_settings.project_configuration.panel_save import SaveNotebookPage
from gui.page_settings.project_configuration.panel_simulation import SimulationNotebookPage
from gui.page_settings.project_configuration.panel_clean import CleanNotebookPage
from gui.page_settings.project_configuration.panel_projectInformation import ProjectInformationPage
from gui.page_settings.project_configuration.panel_userInformation import UserInfoNotebookPage
from gui.page_settings.project_configuration.panel_precision import PrecisionNotebookPage


MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ProjectSettingsNotebook(wx.Notebook):
    def __init__(self, parent, DC, PC):
        wx.Notebook.__init__(self, parent=parent, size=(400, -1))
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
       
        self.page_simulation = SimulationNotebookPage(self) 
        self.page_save = SaveNotebookPage(self)
        # self.page_clean = CleanNotebookPage(self) 
        self.page_projInfo = ProjectInformationPage(self, self.DC, self.PC) 
        self.page_userInfo = UserInfoNotebookPage(self)  
        self.page_precision = PrecisionNotebookPage(self, self.DC)

        
        self.AddPage(self.page_projInfo, "Project Info")
        self.AddPage(self.page_userInfo, "User Info")  
        self.AddPage(self.page_simulation, "Simulation Control")
        self.AddPage(self.page_precision, "Numeric Precision")
        self.AddPage(self.page_save, "Save Options")
        # self.AddPage(self.page_clean, "Clean Project")

    def btnClearClicked(self):
        d, s, pr = self.getClearOptions()
        if d == True:
            #clear the design script
            print("design script cleared in page_settings.py")
            self.DC.clearDesignScript()
            self.PC.resetDesignBool()
    
        if s == True:
            #clear the simulation script
            print("simulation script cleared in page_settings.py")
            self.PC.resetSimulationBool()
        
        if pr == True:
            # clear the other scripts
            print("batch script and report script cleared in page_settings.py")
            self.DC.clearReportsScript()
            self.PC.resetParametersBool()
            self.PC.resetReportsBool()


    def getClearOptions(self):
        #return self.page_clean.getCheckboxValues()
        return []

    def setNumericPrecision(self):
        self.page_precision.setNumericPrecisionSettings()

    def updateSettingsProjectInformation(self):
        self.page_projInfo.updateSettingsProjectInformation()

    def applyLoadedProjectSettings(self, PC):        
        self.page_simulation.applyLoadedProjectSettings(PC)
        self.page_save.applyLoadedProjectSettings(PC)
        self.page_projInfo.applyLoadedProjectSettings(PC)


    def updateProjectSettings(self):
        self.setNumericPrecision()
        # TODO, other functions set by this hook
        



