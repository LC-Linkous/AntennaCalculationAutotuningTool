##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/EM_software/panel_EMSoftwareConfig.py'
#   Class for project settings
#
#   NOTE: add hooks back in for the other EM sim softwares here post 2024.0
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import os
import wx

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class EMSoftwareConfigNotebookPage(wx.Panel):
    def __init__(self, parent, EMSoftwareIRD, executable):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.EMSoftwareID = EMSoftwareIRD
        self.executable = executable #use this to search and set path automtically 
        self.defaultNoExe = "no//executable//path//set"
        self.fullExePath= None
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        #detected executable + browse button (if wrong file found)
        boxExecutable = wx.StaticBox(self, label='Detected Executable')
        self.fieldExecutableDir = wx.TextCtrl(boxExecutable, value=self.defaultNoExe, size=(300, -1))

        self.btnAutodetect = wx.Button(boxExecutable, label="Autodetect")
        self.btnAutodetect.Bind(wx.EVT_BUTTON, self.btnAutodetectClicked)
        self.btnBrowseExecutable = wx.Button(boxExecutable, label="Browse")
        self.btnBrowseExecutable.Bind(wx.EVT_BUTTON, self.btnBrowseClicked)

        #licenses
        boxLicense = wx.StaticBox(self, label='License Options')
        lblNumLicenses = wx.StaticText(boxLicense, label="Max Number of Licenses for Simulation Software: ")
        self.fieldNumLicenses = wx.TextCtrl(boxLicense, value=str(int(1)), size=(-1, 20))
        self.ckbxUseSingleLicense = wx.CheckBox(boxLicense, label="Limit Simulations to Single License")
        self.ckbxUseStudentVersion = wx.CheckBox(boxLicense, label="Use Student Version")
        self.ckbxUseSingleLicense.SetValue(True)
        self.ckbxUseStudentVersion.SetValue(False)
        self.ckbxUseStudentVersion.Bind(wx.EVT_CHECKBOX, self.ckbxUseStudentVersionChecked)


        #default
        self.ckbxUseAsDefaultSoftware = wx.CheckBox(self, label="Use as Default EM Simulation Software")
        self.ckbxUseAsDefaultSoftware.SetValue(False)
        self.ckbxUseAsDefaultSoftware.Bind(wx.EVT_CHECKBOX, self.ckbxUseAsDefaultSoftwareChecked)

        # 


        # sizers
        # btn sizers
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnAutodetect, 0, wx.ALL, border=10)
        btnSizer.Add(self.btnBrowseExecutable, 0, wx.ALL, border=10)

        # EM software settings sizer
        executableSizer = wx.BoxSizer(wx.VERTICAL)
        executableSizer.AddSpacer(10)
        executableSizer.Add(self.fieldExecutableDir, 0, wx.ALL|wx.EXPAND, border=10)
        executableSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=10)
        boxExecutable.SetSizer(executableSizer)

        #license sizer
        licenseSizer = wx.BoxSizer(wx.VERTICAL)
        topLicenseSizer = wx.BoxSizer(wx.HORIZONTAL)
        topLicenseSizer.AddSpacer(15)
        topLicenseSizer.Add(lblNumLicenses, 1, wx.ALL|wx.EXPAND, border=5)
        topLicenseSizer.AddSpacer(10)
        topLicenseSizer.Add(self.fieldNumLicenses, 1, wx.ALL, border=5)
        bottomLicenseSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomLicenseSizer.AddSpacer(15)
        bottomLicenseSizer.Add(self.ckbxUseSingleLicense, 1, wx.ALL|wx.EXPAND, border=5)
        bottomLicenseSizer.Add(self.ckbxUseStudentVersion, 1, wx.ALL|wx.EXPAND, border=5)
        licenseSizer.AddSpacer(10)
        licenseSizer.Add(topLicenseSizer, 1, wx.ALL|wx.EXPAND, border=0)
        licenseSizer.Add(bottomLicenseSizer, 1, wx.ALL|wx.EXPAND, border=0)
        boxLicense.SetSizer(licenseSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxExecutable, 1, wx.ALL|wx.EXPAND, border=5)
        pageSizer.Add(boxLicense, 1, wx.ALL|wx.EXPAND, border=5)
        pageSizer.Add(self.ckbxUseAsDefaultSoftware, 0, wx.ALL | wx.EXPAND, border=15)
        self.SetSizer(pageSizer)

    
    def btnBrowseClicked(self, evt):
        #select executable (should not be the default - only if the detected executable is wrong)
        with wx.FileDialog(self, "Select EM Software Executable", wildcard="software executable (*.exe)|*.exe",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # user cancelled
            # save the current contents in the file
            pathname= fileDialog.GetPath()
            self.executable = pathname
            self.fieldExecutableDir.SetLabel(pathname)

    def btnAutodetectClicked(self, evt=None):
        self.btnAutodetect.SetLabel("Searching")
        exPath = self.detectExectuablePath()
        self.fieldExecutableDir.SetValue(str(exPath))
        self.btnAutodetect.SetLabel("Autodetect")

    def detectExectuablePath(self):
        # TODO: make this non-blocking (maybe with asyncio)
        if self.executable is not None:
            rootPath = os.path.abspath(os.sep)
            for root, dirs, files in os.walk(rootPath):
                if self.executable  in files:
                    fullPath = os.path.join(root, self.executable )
                    self.fullExePath = fullPath
                    # do not autosave
                    return fullPath
        return self.defaultNoExe

    def ckbxUseAsDefaultSoftwareChecked(self, evt):
        #uses parent class to uncheck the other EMsoftwares
        if self.ckbxUseAsDefaultSoftware.GetValue()==True:
            self.parent.setDefaultEM(self.EMSoftwareID)
        
    def checkMakeDefaultEMSoftware(self):
        self.ckbxUseAsDefaultSoftware.SetValue(True)

    def uncheckMakeDefaultEMSoftware(self):
        #called from parent class when another software is selected as default
        self.ckbxUseAsDefaultSoftware.SetValue(False)

    def getValues(self):
        #returns ID, full path, int, bool, bool (redundant)
        numLicenses = float(self.fieldNumLicenses.GetValue())
        useSingle = self.ckbxUseSingleLicense.GetValue()
        defaultSoftware = self.ckbxUseAsDefaultSoftware.GetValue()
        return self.EMSoftwareID, self.fullExePath, numLicenses, useSingle, defaultSoftware

    def applyLoadedProjectSettings(self, PC):
        # print("apply loaded settings - panel from panel_EMSoftwareConfig.py")
        if PC.getSimulationSoftware() == self.EMSoftwareID:
            self.fieldExecutableDir.SetValue(str(PC.getSimulationSoftwarePath()))
            self.fieldNumLicenses.SetValue(str(int(PC.getNumSimulationLicenses())))
            #TODO: set rest of features

    def ckbxUseStudentVersionChecked(self, evt):
        # TODO:
        # update as other em sim softwares are integrated. 
        if self.executable == "ansysedt.exe":
            self.executable = "ansysedtsv.exe"
        elif self.executable == "ansysedtsv.exe":
            self.executable = "ansysedt.exe"

        




