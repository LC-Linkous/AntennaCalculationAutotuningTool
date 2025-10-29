##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_project/page_project.py'
#   Class for creating or opening an AntennaCAT project
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_project.notebook_recent.notebook_recent import RecentProjectNotebook

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ANTENNACAT_NEW_PROJECT_FILE = c.ANTENNACAT_NEW_PROJECT_FILE
ANTENNACAT_OPEN_PROJECT_FILE = c.ANTENNACAT_OPEN_PROJECT_FILE


class ProjectPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SimObj = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)


        # header text
        font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        self.txtWelcome = wx.StaticText(self, label='Welcome to AntennaCAT')
        self.txtWelcome.SetFont(font)

        # large buttons for New and Open
        newBtnBitmap = wx.Bitmap(ANTENNACAT_NEW_PROJECT_FILE, wx.BITMAP_TYPE_PNG) # create wx.Bitmap object  
        newImg = wx.Bitmap.ConvertToImage(newBtnBitmap)
        newImg = newImg.Scale(175, 145, wx.IMAGE_QUALITY_HIGH)
        self.btnNew = wx.Button(self, size =(250, 250))  
        self.btnNew.SetBitmap(newImg.ConvertToBitmap())
        self.btnNew.Bind(wx.EVT_BUTTON, self.btnNewClicked)   

        openBtnBitmap = wx.Bitmap(ANTENNACAT_OPEN_PROJECT_FILE, wx.BITMAP_TYPE_PNG)
        openImg = wx.Bitmap.ConvertToImage(openBtnBitmap)
        openImg = openImg.Scale(180, 190, wx.IMAGE_QUALITY_HIGH)
        self.btnOpen = wx.Button(self, size =(250, 250))
        self.btnOpen.SetBitmap(openImg.ConvertToBitmap())
        self.btnOpen.Bind(wx.EVT_BUTTON, self.btnOpenClicked)   

        # notebook for 'recent' and 'pinned'
        self.notebook_project = RecentProjectNotebook(self)


        #sizers
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnNew, 1, wx.ALL, border=5)
        btnSizer.AddSpacer(50)
        btnSizer.Add(self.btnOpen, 1, wx.ALL, border=5)

        ## main sizer
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.AddSpacer(20)
        self.pageSizer.Add(self.txtWelcome, 1, wx.ALL | wx.ALIGN_LEFT, border=5)
        self.pageSizer.Add(btnSizer, 1, wx.ALL | wx.CENTER, border=5)
        self.pageSizer.AddStretchSpacer()
        self.pageSizer.Add(self.notebook_project , 1, wx.ALL |wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)



    def btnNewClicked(self, evt=None):
        self.parent.btnNewProjectClicked()

    def btnOpenClicked(self, evt=None):
        self.parent.btnOpenProjectClicked()


    def applyLoadedProjectSettings(self, PC):
        self.notebook_project.applyLoadedProjectSettings(PC)



