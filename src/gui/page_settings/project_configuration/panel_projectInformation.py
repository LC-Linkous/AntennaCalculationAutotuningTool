##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_configuration/project_information.py'
#   Class for project settings - displayed, uneditable project information
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import os
import wx
import time
from pathlib import Path
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

        self.lblPath = wx.StaticText(boxProperties, label="Project Location: ")
        self.lblResults = wx.StaticText(boxProperties, label="Results Location: ")
        self.lblSize = wx.StaticText(boxProperties, label="Project Size: ")

        boxDates = wx.StaticBox(self, label='Related Dates')
        self.lblDateModified = wx.StaticText(boxDates, label="Modified: ")
        self.lblDateCreated = wx.StaticText(boxDates, label="Created: ")


        # sizers
        # properties box sizer
        propertiesSizer = wx.BoxSizer(wx.VERTICAL)
        propertiesSizer.AddSpacer(15)
        propertiesSizer.Add(self.lblPath, 0, wx.ALL| wx.EXPAND, border=3)
        propertiesSizer.Add(self.lblResults, 0, wx.ALL| wx.EXPAND, border=3)
        propertiesSizer.Add(self.lblSize, 0, wx.ALL| wx.EXPAND, border=3)
        boxProperties.SetSizer(propertiesSizer)

        # comments
        dateSizer = wx.BoxSizer(wx.VERTICAL)
        dateSizer.AddSpacer(15)
        dateSizer.Add(self.lblDateModified, 0, wx.ALL| wx.EXPAND, border=3)
        dateSizer.Add(self.lblDateCreated, 0, wx.ALL| wx.EXPAND, border=3)
        boxDates.SetSizer(dateSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(self.lblName, 0, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxProperties, 0, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxDates, 0, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    
    def setProjectName(self, t):
        s = "Name: " + str(t)
        self.lblName.SetLabel(s)
    
    def setProjectPath(self, t):
        s = "Project Location: " + str(t)
        self.lblPath.SetLabel(s)
    
    def setResultsPath(self, t):
        s = "Results Location: " + str(t)
        self.lblResults.SetLabel(s)

    def setProjectSize(self, t):
        s = "Project Size: " + str(t)
        self.lblSize.SetLabel(s)
        # this should probably be the FOLDER size, but that's a TODO list item

    def setDateModified(self, t):
        s = "Modified: " + str(t)
        self.lblDateModified.SetLabel(s)

    def setDateCreated(self, t):
        s = "Created: " + str(t)
        self.lblDateCreated.SetLabel(s)        


    def updateSettingsProjectInformation(self):
        a = self.PC.getFullPath() #full path to the ancat file
        b = self.PC.getResultsDirectory() # get the project folder
        if a == None:
            pass
        else:
            path = Path(a)
            if not path.exists():
                # check again inscase there was an error up stream
                return None
            resPath = Path(b)
            # Get stat info
            stat_info = path.stat()
            # split up the strings and  set
            self.setProjectName(path.name)
            self.setProjectPath(str(path.absolute()))
            self.setResultsPath(str(resPath.absolute()))

            s = 0
            # get size
            for path, dirs, files in os.walk(resPath):
                for f in files:
                    fp = os.path.join(path, f)
                    s += os.path.getsize(fp)

            sz = str(s/1000) + " kb" # this will be more intelligent later
            self.setProjectSize(sz) # in kb for now
            self.setDateModified( time.ctime(stat_info.st_mtime))
            self.setDateCreated(time.ctime(stat_info.st_birthtime))


    def applyLoadedProjectSettings(self, PC):
        pass