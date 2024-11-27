##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_settings/panel_clean.py'
#   Class for project settings - clean options to reset scripts/proj vars
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class CleanNotebookPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        #check boxes 
        boxScriptClean = wx.StaticBox(self, label='Script Clean Options')
        self.ckbxDesign = wx.CheckBox(boxScriptClean, label="Clear Design Script")
        self.ckbxSimulation = wx.CheckBox(boxScriptClean, label="Clear Simulation Script ")
        self.ckbxParamAndReport = wx.CheckBox(boxScriptClean, label="Clear Batch and Optimizer Script")
        self.btnClear = wx.Button(boxScriptClean, label="Clear")
        self.btnClear.Bind(wx.EVT_BUTTON, self.btnClearClicked)
        lblNote = wx.StaticText(boxScriptClean, label="This action cannot be undone. Deleted scripts are unrecoverable.")
        lblNote.Wrap(-1)

        cleanSizer = wx.BoxSizer(wx.VERTICAL)
        cleanSizer.AddSpacer(15)
        cleanSizer.Add(self.ckbxDesign, 0, wx.ALL| wx.EXPAND, border=7)
        cleanSizer.Add(self.ckbxSimulation, 0, wx.ALL| wx.EXPAND, border=7)
        cleanSizer.Add(self.ckbxParamAndReport, 0, wx.ALL| wx.EXPAND, border=7)
        cleanSizer.Add(self.btnClear, 0, wx.ALL|wx.ALIGN_RIGHT, border=7)
        cleanSizer.Add(lblNote, 1, wx.ALL| wx.EXPAND, border=10)
        boxScriptClean.SetSizer(cleanSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxScriptClean, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    def btnClearClicked(self, evt=None):
        self.parent.btnClearClicked()

    def getCheckboxValues(self):
        d = self.ckbxDesign.GetValue()
        s = self.ckbxSimulation.GetValue()
        pr = self.ckbxParamAndReport.GetValue()
        return d, s, pr

    def applyLoadedProjectSettings(self, PC):
        pass