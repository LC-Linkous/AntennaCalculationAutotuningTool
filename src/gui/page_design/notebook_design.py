##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_design/notebook_design.py'
#   Class for the notebook with pages of design options
#
#   NOTE: this page was stripped down to pull the bend and array functions for the early release
#       START ADDING FUNCS BACK FROM HERE
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c
from gui.page_design.generator.panel_generator import GeneratorNotebookPage
from gui.page_design.load_script.panel_loadScript import LoadScriptNotebookPage
from gui.page_design.load_project.panel_loadProject import LoadProjectNotebookPage


MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class DesignNotebook(wx.Notebook):
    def __init__(self, parent, mainGUI, DC, PC):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent #parent used for sizer layouts in level above
        self.mainGUI = mainGUI
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        self.DC = DC
        self.PC = PC

        self.page_generator = GeneratorNotebookPage(self, self.DC, self.PC)
        self.page_loadScript = LoadScriptNotebookPage(self, self.DC, self.PC)
        self.page_loadProject = LoadProjectNotebookPage(self, self.DC, self.PC)

        self.AddPage(self.page_generator, "Antenna Generator")
        self.AddPage(self.page_loadScript, "Load Script")
        self.AddPage(self.page_loadProject, "Load Project")

    def updateSummaryText(self, t):
        self.mainGUI.updateSummaryText(t)
          
    def updatePreview(self):
        self.mainGUI.draw3DDesignOnCanvas()

    def checkIfExportExtrasSelected(self):
       b1, b2, b3 =  self.page_generator.getExportSelections()
       return (b1 or b2 or b3)
       
