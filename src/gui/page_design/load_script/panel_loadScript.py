##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/load_script/panel_loadScript.py'
#   Class for loading scripts and detecting changable parameters 
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_design.load_script.panel_detectedParamDynamicScroll import DetectedParameterDynamicScrollPanel
from gui.page_design.load_script.parsers.parser_ANSYS import ImportANSYSScript
from gui.page_design.load_script.parsers.parser_COMSOL import ImportCOMSOLScript
from gui.page_design.load_script.parsers.parser_CST import ImportCSTScript
from gui.page_design.load_script.parsers.parser_EMPIRE import ImportEMPIREScript
from gui.page_design.load_script.parsers.parser_FEKO import ImportFEKOScript

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class LoadScriptNotebookPage(wx.Panel):
    def __init__(self, parent, DC, PC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.DC = DC
        self.PC = PC

        #class vars
        self.loadFilePath = None
        self.script = [] #full file as 2D arr of strings
        self.paramList = []
        self.paramValLst = []
        self.designParams = []

        ## select simulation script to load in
        boxSelect = wx.StaticBox(self, label='Select antenna script file:', size=(-1, 50))
        self.fieldFile = wx.TextCtrl(boxSelect, value="", size=(400, 20))
        self.btnOpenFile = wx.Button(boxSelect, label="Browse")
        self.btnOpenFile.Bind(wx.EVT_BUTTON, self.btnBrowseClicked)


        #detected parameters file
        boxDetected = wx.StaticBox(self, label='Detected parameters', size=(-1, 340))
        self.detectedScrollPanel = DetectedParameterDynamicScrollPanel(boxDetected)            
        self.ckbxSimIncluded = wx.CheckBox(boxDetected, label="script includes simulation setup")#select if script includes a simulation setup
        self.btnClear = wx.Button(boxDetected, label="Clear")
        self.btnClear.Bind(wx.EVT_BUTTON, self.btnClearClicked)
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
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.ckbxSimIncluded, 0, wx.ALL, border=15)
        bottomSizer.Add(self.btnClear, 0, wx.ALL, border=15)
        bottomSizer.Add(self.btnSet, 0, wx.ALL, border=15)
        boxDetectedSizer.Add(bottomSizer, 0, wx.ALL|wx.ALIGN_RIGHT)
        boxDetected.SetSizer(boxDetectedSizer)

        ## main sizer
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.Add(boxSelect, 0, wx.ALL, border=5)
        self.pageSizer.Add(boxDetected, 0, wx.ALL|wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)

    def updateSummaryText(self, t):
        self.parent.updateSummaryText(t)

    def btnClearClicked(self, evt=None):
        self.updateSummaryText("Clearing parameters from memory")
        self.PC.setImportedScriptBoolean(False)
        self.DC.clearImportedScript()
        self.DC.clearParams()
        self.fieldFile.SetValue("")
        self.loadFilePath = None
        self.detectedScrollPanel.clearRows()    
      

    def btnBrowseClicked(self, evt=None):
        #user selects save location. any sub-folders are generated as needed in this location
        with wx.FileDialog(self, "Select File Location", "",
                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            fpath = str(fileDialog.GetPath())
            self.fieldFile.SetValue(fpath)
            self.loadFilePath = fpath
            self.DC.clearParams() #clear old vars
            self.detectParams()
            self.updateSummaryText("Importing parameters from " + str(fpath))

           
    def btnSetClicked(self, evt=None):
        self.PC.useImportedScriptDesign() #what type of project
        self.DC.setImportedScript(self.script) #the design text to start with
        self.DC.setAllParamsByName(self.designParams)
        msg = str(len(self.designParams))  + " set to design configuration"
        self.updateSummaryText(msg)

        # check if using sim setup from script
        if self.ckbxSimIncluded.GetValue() == True:
            msg = "Simulation setup exists in imported script."
            self.updateSummaryText(msg) 
            self.PC.setImportedSimulationConfigBool(True)#can bypass the sim setup. DOES NOT mean antennaCAT parses setup


    def detectParams(self):
        if self.loadFilePath == None:
            #return error message in popup
            self.updateSummaryText("self.loadFilePath has no file")
            return
        self.readInFile()


    def readInFile(self):
        DEBUG_EMSOFTWARE = "ANSYS" #replace this with DEFAULT_EM_WHATEVER  

        if DEBUG_EMSOFTWARE == "ANSYS":
            inScript= ImportANSYSScript(self.loadFilePath)

        elif DEBUG_EMSOFTWARE == "COMSOL":
            inScript= ImportCOMSOLScript(self.loadFilePath)

        elif DEBUG_EMSOFTWARE == "CST":
            inScript= ImportCSTScript(self.loadFilePath)

        elif DEBUG_EMSOFTWARE == "EMPIRE":
            inScript= ImportEMPIREScript(self.loadFilePath)

        elif DEBUG_EMSOFTWARE == "FEKO":
            inScript= ImportFEKOScript(self.loadFilePath)
        else:
            wx.MessageBox('No software set or detected.', 'Error', wx.OK | wx.ICON_ERROR)    
            return
    
        self.paramList, self.paramValLst, self.script = inScript.importScript()

        if self.paramList == [] or self.paramList == None:
            wx.MessageBox('No parameters detected.', 'Error', wx.OK | wx.ICON_ERROR)
            self.updateSummaryText("No identifiable parameters detected from script")            
        else:
            self.detectedScrollPanel.addRows(self.paramList, self.paramValLst)
        self.designParams = list(zip(self.paramList, self.paramValLst))
        msg = str(len(self.paramList)) + " parameters detected in script"
        self.updateSummaryText(msg)
