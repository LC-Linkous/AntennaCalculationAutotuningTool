##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/gui/page_optimizer/notebook_params/notebook_params.py'
#   Class for the notebook for param detection and manipulation
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 7, 2023
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

from gui.page_optimizer.notebook_params.panel_detectedParamDynamicScroll import DetectedBoundaryParameterDynamicScrollPanel
from gui.page_optimizer.notebook_params.panel_paramSettings import ParamSettingsPanel

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ParamsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent) #, size=(500, -1))
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.page_parameters = DetectedBoundaryParameterDynamicScrollPanel(self)
        self.page_settings = ParamSettingsPanel(self)

        self.AddPage(self.page_parameters, "Controllable Parameters")
        self.AddPage(self.page_settings, "Settings") 
    
    def btnDetectClicked(self, evt=None):
        self.parent.btnDetectClicked(evt)
        
    def btnApplyClicked(self, evt=None):
        self.parent.btnApplyClicked(evt)

    def clearPanelRows(self):
        self.page_parameters.clearRows()
    
    def getParamInputBoxVals(self):
        return self.page_parameters.getInputBoxVals()
                
    def addParamRows(self, paramList, paramValLst):
        self.page_parameters.addRows(paramList, paramValLst)

    def applyLoadedProjectSettings(self, PC):
        pass 

    def getNumControllableParams(self):
        return self.page_parameters.getNumControllableParams()