##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_project/notebook_recent/panel_projectList.py'
#   Class for showing linkable antennaCAT project files
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled
import time

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ProjectListPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        designScroll = scrolled.ScrolledPanel(self, 1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        designScroll.SetAutoLayout(1)
        designScroll.SetupScrolling()
        self.designTxt = wx.TextCtrl(designScroll, style=wx.TE_MULTILINE|wx.TE_RICH)
        self.designTxt.SetValue("temporary panel page")

        ## main sizer
        scrollSizer = wx.BoxSizer(wx.VERTICAL)
        scrollSizer.Add(self.designTxt, 1, wx.ALL|wx.EXPAND, border=0)
        designScroll.SetSizer(scrollSizer)
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.Add(designScroll, 1, wx.ALL|wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)

    def applyLoadedProjectSettings(self, PC):
        pass