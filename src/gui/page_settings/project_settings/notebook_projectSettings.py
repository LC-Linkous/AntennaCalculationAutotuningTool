##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_settings/notebook_projectSettings.py'
#   Class for project settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_settings.project_settings.panel_save import SaveNotebookPage
from gui.page_settings.project_settings.panel_simuation import SimulationNotebookPage
from gui.page_settings.project_settings.panel_clean import CleanNotebookPage

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ProjectSettingsNotebook(wx.Notebook):
    def __init__(self, parent, DC, PC):
        wx.Notebook.__init__(self, parent=parent, size=(450, -1))
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
       
        self.page_simulation = SimulationNotebookPage(self) 
        self.page_save = SaveNotebookPage(self)
        self.page_clean = CleanNotebookPage(self) 

        self.AddPage(self.page_simulation, "Simulation Control")
        self.AddPage(self.page_save, "Save Options")
        self.AddPage(self.page_clean, "Clean Project")
          

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
        return self.page_clean.getCheckboxValues()

    def applyLoadedProjectSettings(self, PC):        
        self.page_simulation.applyLoadedProjectSettings(PC)
        self.page_save.applyLoadedProjectSettings(PC)




