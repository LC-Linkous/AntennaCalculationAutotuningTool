##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_configuration/panel_simulation.py'
#   Class for project settings - project simulation looping/view options
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SimulationNotebookPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        boxSimulationRun = wx.StaticBox(self, label='Simulation Run Options')
        self.rbFirst = wx.RadioButton(boxSimulationRun, label = 'Wait on First Simulation', style = wx.RB_GROUP) 
        self.rbEvery = wx.RadioButton(boxSimulationRun, label = 'Wait on Every Simulation')
        self.rbAutomated = wx.RadioButton(boxSimulationRun, label = 'Automated Control')
        lblNote = wx.StaticText(boxSimulationRun, label="Selecting a 'wait' option will require the simulaiton software to be manually closed before the next will run")
        lblNote.Wrap(-1)

        runSizer = wx.BoxSizer(wx.VERTICAL)
        runSizer.AddSpacer(15)
        runSizer.Add(self.rbFirst, 0, wx.ALL| wx.EXPAND, border=7)
        runSizer.Add(self.rbEvery, 0, wx.ALL| wx.EXPAND, border=7)
        runSizer.Add(self.rbAutomated, 0, wx.ALL| wx.EXPAND, border=7)
        runSizer.Add(lblNote, 1, wx.ALL| wx.EXPAND, border=10)
        boxSimulationRun.SetSizer(runSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxSimulationRun, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    def applyLoadedProjectSettings(self, PC):
        pass