##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_information/project_information.py'
#   Class for project settings - displayed, uneditable project information
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ProjectInformationPage(wx.Panel):
    def __init__(self, parent, DC, PC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.lblName = wx.StaticText(self, label="Name: ")

        boxProperties = wx.StaticBox(self, label='Properties')
        self.lblPath = wx.StaticText(boxProperties, label="Path: ")
        self.lblSize = wx.StaticText(boxProperties, label="Size: ")
        self.lblAuthor = wx.StaticText(boxProperties, label="Author: ")

        boxDates = wx.StaticBox(self, label='Related Dates')
        self.lblDateModified = wx.StaticText(boxDates, label="Last Modified: ")
        self.lblDateCreated = wx.StaticText(boxDates, label="Created: ")


        # sizers
        # properties box sizer
        propertiesSizer = wx.BoxSizer(wx.VERTICAL)
        propertiesSizer.AddSpacer(10)
        propertiesSizer.Add(self.lblPath, 0, wx.ALL| wx.EXPAND, border=10)
        propertiesSizer.Add(self.lblSize, 0, wx.ALL| wx.EXPAND, border=10)
        propertiesSizer.Add(self.lblAuthor, 0, wx.ALL| wx.EXPAND, border=10)
        boxProperties.SetSizer(propertiesSizer)

        # comments
        dateSizer = wx.BoxSizer(wx.VERTICAL)
        dateSizer.AddSpacer(10)
        dateSizer.Add(self.lblDateModified, 0, wx.ALL| wx.EXPAND, border=10)
        dateSizer.Add(self.lblDateCreated, 0, wx.ALL| wx.EXPAND, border=10)
        boxDates.SetSizer(dateSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(self.lblName, 0, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxProperties, 0, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxDates, 0, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    
    def setProjectName(self, t):
        self.lblName.SetLabel(t)
    
    def setProjectPath(self, t):
        self.lblPath.SetLabel(t)
    
    def setProjectSize(self, t):
        self.lblSize.SetLabel(t)

    def setAuthor(self, t):
        self.lblAuthor.SetLabel(t)

    def setDateModified(self, t):
        self.lblDateModified.SetLabel(t)

    def setDateCreated(self, t):
        self.lblDateCreated.SetLabel(t)        

    def applyLoadedProjectSettings(self, PC):
        pass