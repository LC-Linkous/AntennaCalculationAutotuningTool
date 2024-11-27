##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_batch/notebook_summary/panel_messageDisplay.py'
#   Class for displaying detail text on notebook page 
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import time

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class MessageDisplay(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.summaryTxt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH|wx.BORDER_SUNKEN)
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.Add(self.summaryTxt, 1, wx.ALL|wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)

    def clearText(self):
        self.summaryTxt.SetValue("")
        
    def updateText(self, t):
        if t is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(t)  + "\n"
        self.summaryTxt.AppendText(msg)

    def applyLoadedProjectSettings(self, PC):
        pass