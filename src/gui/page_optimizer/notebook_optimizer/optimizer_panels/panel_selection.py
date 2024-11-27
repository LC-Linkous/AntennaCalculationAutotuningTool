##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_selection.py'
#   Class for antennaCAT's 'help me choose' optimizer selection
#       Contains widgets for optimizer settings and exports
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 12, 2023
##--------------------------------------------------------------------\

import wx
import sys
import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SelectionPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # buttons
        self.btnHelp = wx.Button(self, label="Help Choose an Optimizer")
        self.btnHelp.Bind(wx.EVT_BUTTON, self.btnHelpClicked)
        self.btnOpen = wx.Button(self, label="Open a Previous Save State")
        self.btnOpen.Bind(wx.EVT_BUTTON, self.btnOpenClicked)

        ## btnSizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnHelp, 0, wx.ALL, border=10)
        btnSizer.Add(self.btnOpen, 0, wx.ALL, border=10)
        # btnSizer.Add(self.btnSave, 0, wx.ALL, border=10)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.AddStretchSpacer()
        pageSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=10)
        self.SetSizer(pageSizer)

#######################################################
# Button Events
#######################################################
    
    def btnOpenClicked(self):
        # self.parent.btnOpenUnknownClicked()
        pass

    def btnHelpClicked(self):
        # self.parent.btnHelpMeChooseClicked()
        pass
    
    
#######################################################
# Page Events
#######################################################
    def parameterSummaryUpdate(self, paramInput):
        #parse params from detected params into form optimizer takes
        pass

