##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/notebook_solution/notebook_solution.py'
#   Class for project settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c
from gui.page_simulation.notebook_solution.panel_simulationSettings import SolutionSettingsPanel

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SolutionSetupNotebook(wx.Notebook):
    def __init__(self, parent, mainGUI, DC, PC):
        wx.Notebook.__init__(self, parent=parent, size=(-1, 250))
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        self.parent = parent
        self.mainGUI = mainGUI
        self.DC = DC
        self.PC = PC
        self.page_simSetup = SolutionSettingsPanel(self, self.mainGUI, self.DC, self.PC)

        self.AddPage(self.page_simSetup, "Solution Setup")


    def updateSummaryText(self, t):
        self.parent.updateSummaryText(t)

    def updateSimulationAutoGenValues(self):
        self.page_simSetup.updateAutoGenValues()

    def updateSimulationSetupValues(self):
        #returns 'noErrors' bool
        return self.page_simSetup.updateDCValsFromUI()

    def applyLoadedProjectSettings(self, PC):
        self.page_simSetup.applyLoadedProjectSettings(PC)




