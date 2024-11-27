##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_project/notebook_recent/notebook_recent.py'
#   Class for the notebook with pages for recent and pinned projects
#
#   NOTE: this functionality pulled for the early release so the config/save files are only updated once
#   THIS IS A QUICK ADD-IN, DO THIS FIRST as soon as the project configs/save configs are back in agreement
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_project.notebook_recent.panel_projectList import ProjectListPage


MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class RecentProjectNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(-1, 300))
        self.parent = parent #parent used for sizer layouts in level above
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        font = wx.Font(12,  wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,)
        self.SetFont(font)


        self.page_recent = ProjectListPage(self)
        self.page_pinned = ProjectListPage(self)

        self.AddPage(self.page_recent, "Recent")
        self.AddPage(self.page_pinned, "Pinned") 

    def applyLoadedProjectSettings(self, PC):
        self.page_recent.applyLoadedProjectSettings(PC)
        self.page_pinned.applyLoadedProjectSettings(PC)