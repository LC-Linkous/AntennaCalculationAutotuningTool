##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_batch/page_batch.py'
#   Class for batch data collection page
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\
# system level imports
import wx
import wx.aui
import wx.lib.newevent
import pandas as pd

# local imports
import project.config.antennaCAT_config as c
from batch.batch import Batch
from gui.page_batch.panel_paramDetection.panel_detectedParamDynamicScroll import DetectedBoundaryParameterDynamicScrollPanel
from gui.page_batch.notebook_summary.notebook_summary import SummaryNotebook
from gui.page_batch.notebook_scripts.notebook_scripts import ScriptsNotebook

# default frame/panel sizes
#CHANGE IN CONSTANTS.PY FOR CONSISTENCY ACROSS PROJECT
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
PANEL_HEIGHT = c.PANEL_HEIGHT
PANEL_WIDTH = c.PANEL_WIDTH
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class BatchPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO        
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        
        self.batchFunc = Batch(self, self.DC, self.PC, self.SO)        

        self.paramList = []
        self.paramValLst = []
        self.paramInput = []

        # controllable parameters panel (dynamically populated) (top left)
        boxControl = wx.StaticBox(self, label='Controllable Parameters', size=(-1, 150))
        self.scrollPanel = DetectedBoundaryParameterDynamicScrollPanel(boxControl, self.DC)

        # settings and summary notebooks
        self.notebook_summary = SummaryNotebook(self)
        self.notebook_scripts = ScriptsNotebook(self)
        
        # btns
        self.btnDetect = wx.Button(boxControl, label="Detect")
        self.btnDetect.Bind(wx.EVT_BUTTON, self.btnDetectClicked)
        self.btnApply= wx.Button(boxControl, label="Apply Configuration")
        self.btnApply.Bind(wx.EVT_BUTTON, self.btnApplyClicked)

        # sizers
        # btn sizer
        boxBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxBtnSizer.AddStretchSpacer()
        boxBtnSizer.Add(self.btnDetect, 0, wx.ALL|wx.RIGHT, border=5)
        boxBtnSizer.Add(self.btnApply, 0, wx.ALL|wx.RIGHT, border=5)

        # controllable param box
        boxControlSizer = wx.BoxSizer(wx.VERTICAL)
        boxControlSizer.AddSpacer(15)
        boxControlSizer.Add(self.scrollPanel, 4, flag=wx.ALL | wx.EXPAND, border=5)
        boxControlSizer.Add(boxBtnSizer, 0, flag=wx.ALL | wx.EXPAND, border=5)
        boxControl.SetSizer(boxControlSizer)

        # top sizer with params and summary
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(boxControl, 1, wx.ALL | wx.EXPAND, border=5)

        # bottom window sizer with script settings and status
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(self.notebook_scripts, 1, wx.ALL | wx.EXPAND, border=5)
        bottomSizer.Add(self.notebook_summary , 1, wx.ALL | wx.EXPAND, border=5)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(topSizer, 1, wx.ALL | wx.EXPAND, border=0)
        pageSizer.Add(bottomSizer, 1, wx.ALL | wx.EXPAND, border=0)
        self.SetSizer(pageSizer)

    def updateStatusText(self, t):
        if t is None:
            return
        self.notebook_summary.updateStatusText(t)

    def updateDetailsText(self, t):
        if t is None:
            return
        self.notebook_summary.updateDetailsText(t)

    def clearTextWindows(self):
        self.notebook_summary.clearStatus()
        self.notebook_summary.clearDetails()

    def clearCurrent(self):
        self.paramList = []
        self.paramValLst = []
        self.paramInput = []
        #clear old rows
        self.scrollPanel.clearRows()

    def btnDetectClicked(self, evt=None):
        # check that a design was created
        if self.PC.getDesignConfigBool() == False:
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        #clear old rows
        self.clearCurrent()
        
        #if design was created, then there's something in:
        # 1) design script (even if it's just a call to open a file)
        # and 2) self.DC.self.designParams <- any provided/calculated params
        # future expansion: self.DC.designFeatures <- like layer height (to make substrate dynamic)

        designParams = self.DC.getParams()
       
        self.populateDetectedKeywords(designParams)
        if self.paramList == [] or self.paramList == None:
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)            
        else:
            self.scrollPanel.addRows(self.paramList, self.paramValLst)

    def btnApplyClicked(self, evt=None):
        # use the batch object to combine all parameters and check if too many combinations to handle
        
        #check that there's either a loaded design, or that the param list isn't empty
        if (self.PC.getDesignConfigBool() == False) or (self.paramList == [] or self.paramList == None):
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)
            return        
        #get the vals from the scrollbox
        # set vals to array/tuple
        self.paramInput = pd.DataFrame({})
        paramFields, originalVal, unitVal, typeFields, percentFields, valFields, delVal, ignoreVal = self.scrollPanel.getInputBoxVals()
        for i in range(0, len(paramFields)):
            a = paramFields[i].GetValue()
            b = originalVal[i].GetValue()
            c = unitVal[i].GetValue()
            d = typeFields[i].GetValue()
            e = percentFields[i].GetValue()
            f = valFields[i].GetValue()
            g = delVal[i].GetValue()
            h = ignoreVal[i].IsChecked()
            self.paramInput[str(a)] = pd.Series([b,c,d,e,f,g,h])
        #put into batch object.
            #batch function will sort for processing
            #displays and handles any warnings that need user action
        self.batchFunc.setInputParams(self.paramInput)
        self.batchFunc.createCombinationsDataFrame()

    def errorCheck(self):
        #checks that a design and simulation script exists
        #you can generate parameters without the scripts (preview),
        #  but not export or run
        noErrors = False
        # check design script
        if self.PC.getDesignScriptCreatedBool() == False:
            msg = "No design script created. Generate design script to use the Batch functionality."
            self.updateStatusText(msg)
            return noErrors
        # check simulation script
        if self.PC.getSimulationConfigBool() == False:
            msg = "No simulation script created. Configure simulation options to use Batch functionality."
            self.updateStatusText(msg)
            return noErrors
        noErrors = True
        return noErrors
        

    def btnExportClicked(self, evt=None):
        # check if design and simulation scripts exist
        noErrors = self.errorCheck()
        if noErrors == False:
            return
        # get the values from the panel_export
        # loc and vals to script gen in batch incase script needs to be split
        useSingleBool, numScripts = self.notebook_scripts.getExportSettings()
        if useSingleBool == True:
            numScripts = 1 #use just one license 
            
        # generate and export scripts in Batch
        self.batchFunc.generateBatchScripts(numScripts)
            

    def btnRunClicked(self, evt=None):
        # check if design and simulation scripts exist
        noErrors = self.errorCheck()
        if noErrors == False:
            return

        # triggered from notebook scripts, panel_run
        useSingleBool, numScripts = self.notebook_scripts.getRunSettings()
        if useSingleBool == True:
            numScripts = 1 #use just one license 
            
        # generate and export scripts in Batch
        scriptNames = self.batchFunc.generateBatchScripts(numScripts)
        
        # loop through the file paths and run each
        msg = "Begining batch simulation process"
        self.updateStatusText(msg)
        msg = str(len(scriptNames)) + " scripts will be run automatically, with the simulation "+\
            "software remaining open."
        self.updateStatusText(msg)
        
        self.SO.runBatchAndExit(files=scriptNames, numLicenses=1)

    def populateDetectedKeywords(self, paramVals):
        #read design params into class variables
        for p in paramVals:
           self.paramList.append(str(p)) #name in list
           val = paramVals[str(p)][0] # get value by name
           self.paramValLst.append(str(val)) #set val to list

    def applyLoadedProjectSettings(self, PC):
        self.scrollPanel.applyLoadedProjectSettings(PC) 
        self.notebook_summary.applyLoadedProjectSettings(PC)
        self.notebook_scripts.applyLoadedProjectSettings(PC)

