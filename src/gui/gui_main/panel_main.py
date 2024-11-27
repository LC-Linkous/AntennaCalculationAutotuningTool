##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/gui/gui_main/panel_main.py'
#   Class for GUI layout and basic functionality - main gui interaction panel
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './gui')
from gui.page_batch.page_batch import BatchPage
from gui.page_design.page_design import DesignPage
from gui.page_settings.page_settings import SettingsPage
from gui.page_simulation.page_simulation import SimulationPage
from gui.page_optimizer.page_optimizer import OptimizerPage
from gui.page_project.page_project import ProjectPage

class MainPanel(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO

        # pages in the mainUI panel
        self.panel_project = ProjectPage(self, self.DC, self.PC, self.SO)
        self.panel_design = DesignPage(self, self.DC, self.PC, self.SO)
        self.panel_simulation = SimulationPage(self, self.DC, self.PC, self.SO)
        self.panel_batch = BatchPage(self, self.DC, self.PC, self.SO)
        self.panel_settings = SettingsPage(self, self.DC, self.PC, self.SO)
        self.panel_optimizer = OptimizerPage(self, self.DC, self.PC, self.SO)

        self.panel_project.Show()# shown by default
        self.panel_design.Hide()  
        self.panel_simulation.Hide()
        self.panel_batch.Hide()
        self.panel_settings.Hide()
        self.panel_optimizer.Hide()

        self.mainUIpanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainUIpanelSizer.Add(self.panel_project, 1, wx.EXPAND)
        self.mainUIpanelSizer.Add(self.panel_design, 1, wx.EXPAND)
        self.mainUIpanelSizer.Add(self.panel_simulation, 1, wx.EXPAND)
        self.mainUIpanelSizer.Add(self.panel_batch, 1, wx.EXPAND)
        self.mainUIpanelSizer.Add(self.panel_settings, 1, wx.EXPAND)
        self.mainUIpanelSizer.Add(self.panel_optimizer, 1, wx.EXPAND)

        self.SetSizer(self.mainUIpanelSizer)

    def btnNewProjectClicked(self, evt=None):
        self.parent.btnNewProjectClicked(evt)

    def btnOpenProjectClicked(self, evt=None):
        self.parent.btnOpenProjectClicked(evt)

    def applyLoadedProjectSettings(self):
        self.panel_project.applyLoadedProjectSettings(self.PC)
        self.panel_simulation.applyLoadedProjectSettings(self.PC) 
        self.panel_batch.applyLoadedProjectSettings(self.PC)
        self.panel_settings.applyLoadedProjectSettings(self.PC) #passing so everything is working off a copy and not modding

    def updateProjectValues(self):
        # triggers the auto update events that tie widgets/values together
        #can be called by applyLoadedProjectSettings() after PC and DC are set
        # OR can be called during update events on the design page
        self.panel_simulation.updateSimulationSettingsBoxes()