##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_simulation/page_simulation.py'
#   Class for EM software simulation + report settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import wx

import project.config.antennaCAT_config as c
import helper_func.fileIO_helperFuncs as fIO

from gui.page_simulation.notebook_reports.notebook_reports import ReportsNotebook
from gui.page_simulation.notebook_solution.notebook_solution import SolutionSetupNotebook
from gui.page_simulation.panel_messageDisplay import MessageDisplay

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ALTERNATE_COLORS = c.ALTERNATE_COLORS

class SimulationPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # left size of page
        # simulation settings
        boxSimulationSettings = wx.StaticBox(self, label='Simulation Settings')
        self.notebook_simSettings = SolutionSetupNotebook(boxSimulationSettings, self, self.DC, self.PC)
        # check boxes for reports to be returned
        boxReports = wx.StaticBox(self, label='Report Settings')
        self.notebook_reportSettings = ReportsNotebook(boxReports)

        # right side of page
        # summary panel to report output
        boxSummary = wx.StaticBox(self, label='Simulation Configuration Summary')
        self.txtSummary = MessageDisplay(boxSummary)

        #buttons
        boxBtns = wx.StaticBox(self)
        self.btnGenerate = wx.Button(boxBtns, label="Generate Script")
        self.btnGenerate.Bind(wx.EVT_BUTTON, self.btnGenerateClicked)
        self.btnExport = wx.Button(boxBtns, label="Export Script")
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)
        self.btnRun = wx.Button(boxBtns, label="Run Simulation")
        self.btnRun.Bind(wx.EVT_BUTTON, self.btnRunClicked)

        # simulation settings sizer
        boxSimulationSettingsSizer = wx.BoxSizer(wx.VERTICAL)
        boxSimulationSettingsSizer.Add(self.notebook_simSettings, 0, wx.ALL|wx.EXPAND, border=15)
        boxSimulationSettings.SetSizer(boxSimulationSettingsSizer)
        # report settings sizer
        boxReportSettingsSizer = wx.BoxSizer(wx.VERTICAL)
        boxReportSettingsSizer.Add(self.notebook_reportSettings, 0, wx.ALL|wx.EXPAND, border=15)
        boxReports.SetSizer(boxReportSettingsSizer)
        # config summary sizer
        boxSummarySizer = wx.BoxSizer(wx.VERTICAL)
        boxSummarySizer.Add(self.txtSummary, 1, wx.ALL|wx.EXPAND, border=15)
        boxSummary.SetSizer(boxSummarySizer)

        # btn sizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnRun, 0, wx.RIGHT, border=10)  
        btnSizer.Add(self.btnExport, 0, wx.RIGHT, border=10)              
        btnSizer.Add(self.btnGenerate, 0, wx.RIGHT, border=10)
        boxBtns.SetSizer(btnSizer)
        
        ## main sizer
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(boxSimulationSettings, 0, wx.ALL|wx.EXPAND, border=5)
        leftSizer.Add(boxReports, 0, wx.ALL|wx.EXPAND, border=5)
        topSizer.Add(leftSizer, 0, wx.ALL|wx.EXPAND, border=0)
        topSizer.Add(boxSummary, 1, wx.ALL|wx.EXPAND, border=5)

        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(topSizer, 0, wx.ALL|wx.EXPAND, border=0)
        pageSizer.AddStretchSpacer()
        pageSizer.Add(boxBtns,0, wx.ALL| wx.ALIGN_RIGHT, border=5)
        self.SetSizer(pageSizer)

        self.Layout()

    def updateSimulationSettingsBoxes(self):
        self.notebook_simSettings.updateSimulationAutoGenValues()
        self.notebook_simSettings.updateSimulationSetupValues()


    def updateSummaryText(self, t):
        self.txtSummary.updateText(str(t))
   
    def btnRunClicked (self, evt=None):
        if self.PC.getSimulationConfigBool() == False:
            msg = "Generate script before running"
            self.updateSummaryText(msg)
            return
        if self.errorCheck() == False:
            return
        pth = self.PC.getSimulationScriptPath()
        msg = "simulation script path: " + str(pth)
        self.updateSummaryText(msg)
        scriptTxt = self.combineDesignAndSimScripts()
        noErrors = fIO.writeOut(pth, scriptTxt)
        if noErrors == False:
            msg = "ERROR: unable to write design and sim script out to file at " + str(pth)
            self.updateSummaryText(msg)
        #run simulation using file last written out
        self.SO.runWithScript(pth) #sim script running here is a "build and run" so HFSS doesn't have to close
                
    def btnGenerateClicked(self, evt=None):
        if (self.PC.getSimulationSoftware() == None):
            msg = "no EM simulation software detected. Configure this in settings"
            self.updateSummaryText(msg)
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            return
        # set project configs, save files for use in HFSS
        #set the values from the panels (TODO: custom panel update)
        noErrors = self.notebook_simSettings.updateSimulationSetupValues()#sets the user input to self.PC
        if noErrors == False:
            msg = "ERROR: issue with simulation values. check user input"
            self.updateSummaryText(msg)
            return noErrors

        noErrors = self.errorCheck()
        if noErrors == True:
            #get vals and set to design config
            self.setUserValsToDesignConfig()
            self.PC.setSimulationConfigBool(True)
            self.SO.simulationTemplateGen(createNew=True)
            #script can now be exported
            msg = "Simulate script generated"
            self.updateSummaryText(msg)
        else:
            msg = "ERROR: generate button clicked. error check failed"
            self.updateSummaryText(msg)
        return noErrors
    
    def btnExportClicked(self, evt=None):
        if self.PC.getDesignScriptCreatedBool() == False:
            msg = "No design script detected to export"
            self.updateSummaryText(msg)
            return
        if self.PC.getSimulationConfigBool() == False:
            msg ="Generating simulation script before export"
            self.updateSummaryText(msg)
            noError = self.btnGenerateClicked()
            if noError == False:
                msg ="Simulation script not exported"
                self.updateSummaryText(msg)
                return

        scriptTxt = self.combineDesignAndSimScripts()
        #export to scripts folder
        #write out to the scripts file  in the antennaCAT project
        try:
            pathname = self.PC.getScriptDirectory()
            fileExt = self.SO.getExpectedScriptFileExtension()
            pathname = os.path.join(pathname, "exported-design-and-simulation" + str(fileExt))
            fIO.writeOut(pathname, scriptTxt)
            msg = "file exported to " + str(pathname)
            self.updateSummaryText(msg)
        except Exception as e:
                msg = "Cannot save current data in file " + str(pathname)
                self.updateSummaryText(msg)
                self.updateSummaryText(e)
        
    def combineDesignAndSimScripts(self):
        txtDesign = self.DC.getDesignScript()
        # txtSim = []
        # if script or project import has sim setup, skip this
        txtSim = []
        if self.PC.getImportedSimulationConfigBool() == False:
            txtSim = self.DC.getSimulationScript()
        txtReports = self.DC.getReportsScript()
        txt = txtDesign + txtSim + txtReports
        return txt

    def errorCheck(self):
        noErrors = True
        if self.PC.getDesignConfigBool()==False:
            noErrors = False
            msg = "No antenna configuration detected. Either design or import a file."
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            self.updateSummaryText(msg)
        fpath= str(self.PC.getResultsDirectory())
        if fpath == "":
            noErrors = False
            msg = "Invalid file path. Select a valid directory to save project"
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            self.updateSummaryText(msg)
        return noErrors
    
    def setUserValsToDesignConfig(self):
        # solution notebook
        freq = self.DC.getSimulationFreq()
        numMultF = len(freq)
        useMultF = self.DC.getUseMultipleFreq()
        minFreq= self.DC.getMinSimRange()
        maxFreq= self.DC.getMaxSimRange()
        numPasses = self.DC.getNumPasses()
        maxDelta = self.DC.getMaxDelta()
        useMultD = self.DC.getUseMultipleDelta()
        numPoints = self.DC.getNumSimPts()
        self.DC.setSimulationSettingsDF(freq, useMultF, numMultF, minFreq, maxFreq, numPasses, maxDelta, useMultD, numPoints)

        # reports notebook 
        modalReports, modalFeatures = self.notebook_reportSettings.getModalReportList()
        terminalReports, terminalFeatures = self.notebook_reportSettings.getTerminalReportList()
        farFieldReports, farFieldFeatures = self.notebook_reportSettings.getFarFieldReportList()
        DTMFeats, DTTFeats, FFFeats = self.notebook_reportSettings.getDataTableList()
        antennaParamFeats = self.notebook_reportSettings.getAntennaParamsTableList()
        self.DC.setModalReportList(modalReports, modalFeatures)
        self.DC.setTerminalReportList(terminalReports, terminalFeatures)
        self.DC.setFarFieldReportList(farFieldReports, farFieldFeatures)
        self.DC.setDataTableReportList(DTMFeats, DTTFeats, FFFeats)
        self.DC.setAntennaParamTableList(antennaParamFeats) 
        
    def applyLoadedProjectSettings(self, PC):
        self.notebook_simSettings.applyLoadedProjectSettings(PC)
        self.notebook_reportSettings.applyLoadedProjectSettings(PC)
        self.txtSummary.applyLoadedProjectSettings(PC)