##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_batch/notebook_scripts/notebook_scripts.py'
#   Class for the notebook with pages for script splitting and export
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_batch.notebook_scripts.panel_export import ExportPage
from gui.page_batch.notebook_scripts.panel_run import RunPage


MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ScriptsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.page_run = RunPage(self)
        self.page_export = ExportPage(self)

        self.AddPage(self.page_run, "Run Settings")
        self.AddPage(self.page_export, "Export Settings") 

    def btnExportClicked(self, evt=None):
        # triggered from notebook scripts, panel_export
        self.parent.btnExportClicked(evt)

    def btnRunClicked(self, evt=None):
        # triggered from notebook scripts, panel_run
        self.parent.btnRunClicked(evt)

    def getExportSettings(self):
        return self.page_export.getSettings()
    
    def getRunSettings(self):
        return self.page_run.getSettings()
    

    def applyLoadedProjectSettings(self, PC):
        self.page_run.applyLoadedProjectSettings(PC) 
        self.page_export.applyLoadedProjectSettings(PC)
