##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/gui/page_optimizer/notebook_summary/notebook_summary.py'
#   Class for the notebook with pages for script splitting and export
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 6, 2023
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_batch.notebook_summary.panel_messageDisplay import MessageDisplay


MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SummaryNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(500, -1))
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.page_status = MessageDisplay(self)
        self.page_details = MessageDisplay(self)

        self.AddPage(self.page_status, "Status")
        self.AddPage(self.page_details, "Design Details") 


    def updateStatusText(self, t):
        self.page_status.updateText(t)


    def clearStatus(self):
        self.page_status.clearText()


    def updateDetailsText(self, t):
        self.page_details.updateText(t)


    def clearDetails(self):
        self.page_details.clearText()

    def applyLoadedProjectSettings(self, PC):
        self.page_status.applyLoadedProjectSettings(PC) 
        self.page_details.applyLoadedProjectSettings(PC)
