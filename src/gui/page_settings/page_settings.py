##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_settings/page_settings.py'
#   Class for user settings and config inputs
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: October 25, 2023
##--------------------------------------------------------------------\

# system level imports
import os
import sys
import wx #pip install wxpython
import wx.aui
import wx.lib.newevent

# local imports
import project.config.antennaCAT_config as c
from gui.page_settings.em_software.notebook_EMSoftware import EMSoftwareNotebook
from gui.page_settings.user_settings.notebook_userSettings import UserSettingsNotebook
from gui.page_settings.project_information.panel_projectInformation import ProjectInformationPage
from gui.page_settings.project_settings.notebook_projectSettings import ProjectSettingsNotebook

sys.path.insert(0, './project/')
from project.antennaCAT_project import AntennaCATProject

MAIN_BACKGROUND_COLOR= c.MAIN_BACKGROUND_COLOR

class SettingsPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)


        # upper left EM settings notebok
        boxSoftwareSettings = wx.StaticBox(self, label='EM Software Settings')
        self.notebook_softwareSettings = EMSoftwareNotebook(boxSoftwareSettings)

        # upper right project information
        boxProjectInformation = wx.StaticBox(self, label='Project Information')
        self.panel_projectInformation = ProjectInformationPage(boxProjectInformation, self.DC, self.PC)

        # lower left user settings
        boxUserSettings = wx.StaticBox(self, label='User Settings')
        self.notebook_userSettings = UserSettingsNotebook(boxUserSettings, self.PC)
        
        # lower right project settings
        boxProjectSettings= wx.StaticBox(self, label='Project Settings')
        self.notebook_projectSettings = ProjectSettingsNotebook(boxProjectSettings, self.DC, self.PC)

        #TODO: make panel for:
        # "show me first simulation"  "always autorun" "parallel simulations"
        # include in batch and tuning tabs?

        # save button in bottom right
        self.saveBtn = wx.Button(self, label="Save")
        self.saveBtn.Bind(wx.EVT_BUTTON, self.btnSaveClicked)

        # sizers
        # emsoftware sizer
        softwareSettingSizer = wx.BoxSizer(wx.VERTICAL)
        softwareSettingSizer.AddSpacer(15) #so tabs dont overlap name of static box
        softwareSettingSizer.Add(self.notebook_softwareSettings, 1, wx.ALL | wx.EXPAND, border=10)
        boxSoftwareSettings.SetSizer(softwareSettingSizer)
        
        # project info sizer
        projectInfoSizer = wx.BoxSizer(wx.VERTICAL)
        projectInfoSizer.AddSpacer(15)
        projectInfoSizer.Add(self.panel_projectInformation, 1, wx.ALL | wx.EXPAND, border=10)
        boxProjectInformation.SetSizer(projectInfoSizer)

        # user settings sizer
        userSettingsSizer = wx.BoxSizer(wx.VERTICAL)
        userSettingsSizer.AddSpacer(15)
        userSettingsSizer.Add(self.notebook_userSettings, 1, wx.ALL | wx.EXPAND, border=10)
        boxUserSettings.SetSizer(userSettingsSizer)

        # project setting sizer
        projectSettingSizer = wx.BoxSizer(wx.VERTICAL)
        projectSettingSizer.AddSpacer(15)
        projectSettingSizer.Add(self.notebook_projectSettings, 1, wx.ALL | wx.EXPAND, border=10)
        boxProjectSettings.SetSizer(projectSettingSizer)

        # btn sizer 
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        btnSizer.Add(self.saveBtn, 0, wx.ALL, border=15)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(boxSoftwareSettings, 1, wx.ALL | wx.EXPAND, border=15)
        topSizer.Add(boxProjectInformation, 1, wx.ALL | wx.EXPAND, border=15)
        
        middleSizer = wx.BoxSizer(wx.HORIZONTAL)
        middleSizer.Add(boxUserSettings, 1, wx.ALL | wx.EXPAND, border=15)
        middleSizer.Add(boxProjectSettings, 1, wx.ALL | wx.EXPAND, border=15)

        pageSizer.Add(topSizer, 1, wx.ALL | wx.EXPAND, border=0)
        pageSizer.Add(middleSizer, 1, wx.ALL | wx.EXPAND, border=0)
        pageSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, border=0)
       
        self.SetSizer(pageSizer)


    def btnSaveClicked(self, evt=None):
        if self.PC.getProjectDirectory()== None:
            with wx.FileDialog(self, "Save antennaCAT project", wildcard="AntennaCAT files (*.ancat)|*.ancat",
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # user cancelled
                pathname = fileDialog.GetPath()
                try:
                    acp = AntennaCATProject(self.DC, self.PC, self.SO)
                    acp.createNewProject(pathname)
                except Exception as e:
                    print(e)


        #TODO: read everything into PC properly
        # still need the author, comments, save options, run options, etc

        #get the EM software choices
        ems = self.notebook_softwareSettings.getDefaultEMSoftware()
        softwareSelection, softwarePath, numLicenses, useSingle, defaultSoftware = self.notebook_softwareSettings.getEMSettings() #return a dataFrame to write to PC
        self.PC.setSimulationSoftware(ems)
        self.PC.setSimulationSoftwarePath(str(softwarePath))
        self.PC.setNumSimulationLicenses(float(numLicenses))
        self.PC.setUseSingleLicense(useSingle)
        self.PC.setDefaultEMSoftware(defaultSoftware)      

        self.SO.setupSI(softwareSelection, softwarePath, float(numLicenses))

        #project save
        acp = AntennaCATProject(self.DC, self.PC, self.SO)
        acp.saveProject()

        print("EM software saved in page_settings.py")    

    def applyLoadedProjectSettings(self, PC):
        self.notebook_softwareSettings.applyLoadedProjectSettings(PC)
        self.panel_projectInformation.applyLoadedProjectSettings(PC)
        self.notebook_userSettings.applyLoadedProjectSettings(PC)        
        self.notebook_projectSettings.applyLoadedProjectSettings(PC)

    


            



