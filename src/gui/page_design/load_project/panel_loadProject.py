##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_design/load_project/panel_loadProject.py'
#   Class for loading project and indicating changable parameters 
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c
from gui.page_design.load_project.panel_paramDynamicScroll import ParamDynamicScrollPanel

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class LoadProjectNotebookPage(wx.Panel):
    def __init__(self, parent, DC, PC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.DC = DC
        self.PC = PC

        #class vars
        self.loadFilePath = None
        self.script = [] #full file
        self.paramList = []
        self.paramValLst = []
  
        ## select simulation project to load in
        boxSelect = wx.StaticBox(self, label='Select project file to modify:', size=(-1, 50))
        self.fieldFile = wx.TextCtrl(boxSelect, value="", size=(400, 20))
        self.btnOpenFile = wx.Button(boxSelect, label="Browse")
        self.btnOpenFile.Bind(wx.EVT_BUTTON, self.btnBrowseClicked)

        #detected parameters file
        boxDetected = wx.StaticBox(self, label='Add parameters to modify:', size=(-1, 400))
        self.ckbxSimIncluded = wx.CheckBox(boxDetected, label="script includes simulation setup")#select if script includes a simulation setup
        self.detectedScrollPanel = ParamDynamicScrollPanel(boxDetected)
        self.btnSet = wx.Button(boxDetected, label="Set")
        self.btnSet.Bind(wx.EVT_BUTTON, self.btnSetClicked)

        ## file selection sizer
        boxSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSelectionSizer.Add(self.fieldFile, 1, wx.ALL, border=15)
        boxSelectionSizer.Add(self.btnOpenFile, 1, wx.ALL, border=15)
        boxSelect.SetSizer(boxSelectionSizer)

        ## detected param sizer
        boxDetectedSizer = wx.BoxSizer(wx.VERTICAL)
        boxDetectedSizer.Add(self.detectedScrollPanel, 1, wx.ALL|wx.EXPAND, border=15)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.ckbxSimIncluded, 0, wx.ALL, border=15)
        btnSizer.Add(self.btnSet, 0, wx.ALL, border=15)
        boxDetectedSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=15)
        boxDetected.SetSizer(boxDetectedSizer)

        ## main sizer
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.Add(boxSelect, 0, wx.ALL, border=5)
        self.pageSizer.Add(boxDetected, 0, wx.ALL|wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)
        

    def btnSetClicked(self, evt=None):
        self.PC.setImportedProjectPath(self.loadFilePath) #get the EM project path


        self.PC.useImportedProjectDesign() #using a loaded design, takes priority 
        # the design script is just the open file base
        # but set the design parameters based on the inputs
        self.DC.clearParams() #clear old vars
        designParams = self.detectedScrollPanel.getParams()
        self.DC.setAllParamsByName(designParams)
        msg = "Setting " + str(len(designParams)) + " parameters"
        self.updateSummaryText(msg)        
        if len(designParams) == 0:
            msg = "No parameters were set. In order for AntennaCAT to control parameters for an imported project, \
                  you must manually add them in the window under the 'Import Project' tab. Include units. \
                 mm is assumed in most cases, but is not enforced by this program."
            self.updateSummaryText(msg)   

        
        if self.ckbxSimIncluded.GetValue() == True:
            msg = "Simulation setup exists in imported script."
            self.updateSummaryText(msg) 
            self.PC.setImportedSimulationConfigBool(True)#can bypass the sim setup. DOES NOT mean antennaCAT parses setup

    def btnBrowseClicked(self, evt=None):
        #user selects save location. any sub-folders are generated as needed in this location
        with wx.FileDialog(self, "Select File Location", "",
                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            fpath = str(fileDialog.GetPath())
            self.fieldFile.SetValue(fpath)
            tmp = repr(fpath) # this is an interesting bug that only pops up on some systems. We're narrowing in on why this conversion NOT happening 
                                # causes issues with paths in some systems. Might have been because running 3x versions of Windows with 5x versions of HFSS
            self.loadFilePath = str(tmp)[1:-1]#strip extra quotes
            msg = "file loaded from " + str(fpath)
            self.updateSummaryText(msg)

    
    def updateSummaryText(self, t):
        self.parent.updateSummaryText(t)

