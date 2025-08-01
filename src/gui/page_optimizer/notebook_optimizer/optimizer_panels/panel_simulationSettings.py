##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_simulation/notebook_optimizer/panel_simulationSettings.py'
#   Class opimizer simulation settings notebook page
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 3, 2023
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SolutionSettingsPanel(wx.Panel):
    def __init__(self, parent, DC, PC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        self.DC = DC
        self.PC = PC

        self.freq = None
        self.minFreq = None
        self.maxFreq = None


        # Solution Settings
        boxSolutionSetup = wx.StaticBox(self, label="Solution Setup")
        #target frequency settings
        lblFrequency = wx.StaticText(boxSolutionSetup, label="Frequency (Hz): ")
        self.fieldFrequency = wx.TextCtrl(boxSolutionSetup, value=" ", size=(250, 20))
        self.ckbxMultipleFrequencies = wx.CheckBox(boxSolutionSetup, label="Use Multiple Frequencies")        
        #num passes settings
        lblMaxPasses= wx.StaticText(boxSolutionSetup, label="Maximum No. of Passes (1-100): ")
        self.fieldPasses = wx.TextCtrl(boxSolutionSetup, value=" ", size=(50, 20))
        self.fieldPasses.SetValue(str(6))
        # #delta settings
        lblMaxDelta = wx.StaticText(boxSolutionSetup, label="Maximum Delta S:         ")
        self.fieldDelta = wx.TextCtrl(boxSolutionSetup, value="", size=(100, 20))
        self.fieldDelta.SetValue(str(0.02))
        self.ckbxMultipleDelta = wx.CheckBox(boxSolutionSetup, label="Use Multiple Delta") 
        # #Freq sweep settings
        boxFrequencySweep = wx.StaticBox(boxSolutionSetup, label='Frequency Sweep')
        lblStart = wx.StaticText(boxFrequencySweep, label="Start (Hz): ")
        self.fieldStart = wx.TextCtrl(boxFrequencySweep, value="", size=(100, 20))
        lblStop= wx.StaticText(boxFrequencySweep, label="Stop (Hz): ")
        self.fieldStop = wx.TextCtrl(boxFrequencySweep, value="", size=(100, 20))
        lblNumPts = wx.StaticText(boxFrequencySweep, label="Number of Points: ")
        self.fieldPoints = wx.TextCtrl(boxFrequencySweep, value="", size=(60, 20))
        self.fieldPoints.SetValue(str(401))
        #set button to remember freq settings, but not generate script
        btnApply = wx.Button(boxSolutionSetup, label='Apply')
        btnApply.Bind(wx.EVT_BUTTON, self.btnApplyClicked)

        # Data Collection Setup
        boxDataCollectionSetup = wx.StaticBox(self, label="Data Collection Setup")
        boxLogFiles = wx.StaticBox(boxDataCollectionSetup, label="Log File Options")
        self.cbCreateSimulationLog = wx.CheckBox(boxLogFiles, label='log simulation data to file')
        self.cbCreateSimulationLog.SetValue(True)
        self.cbCreateOptimizerLog = wx.CheckBox(boxLogFiles, label='log optimizer data to file')
        self.cbCreateOptimizerLog.SetValue(False)

        boxReportOptions = wx.StaticBox(boxDataCollectionSetup, label="Data Options")
        self.cbSaveReports = wx.CheckBox(boxReportOptions, label='save copies of report data')
        self.cbSaveReports.SetValue(False)
   
        #Sizers
        ##frequency
        freqSizer = wx.BoxSizer(wx.HORIZONTAL)
        freqSizer.Add(lblFrequency, 0, wx.ALL, border=3)
        freqSizer.Add(self.fieldFrequency, 0, wx.ALL, border=3)
        freqSizer.Add(self.ckbxMultipleFrequencies, 0, wx.ALL, border=5)        
        ##passes
        passesSizer = wx.BoxSizer(wx.HORIZONTAL)
        passesSizer.Add(lblMaxPasses, 0, wx.ALL, border=3)
        passesSizer.Add(self.fieldPasses, 0, wx.ALL, border=3)
        # ##delta
        deltaSizer = wx.BoxSizer(wx.HORIZONTAL)
        deltaSizer.Add(lblMaxDelta, 0, wx.ALL, border=3)
        deltaSizer.Add(self.fieldDelta, 0, wx.ALL, border=3)
        deltaSizer.Add(self.ckbxMultipleDelta, 0, wx.ALL, border=5)
        ##frequencysweep
        sweepSizer = wx.BoxSizer(wx.VERTICAL)
        ###start
        startSizer = wx.BoxSizer(wx.HORIZONTAL)
        startSizer.Add(lblStart, 0, wx.ALL, border=3)
        startSizer.Add(self.fieldStart, 0, wx.ALL, border=3)
        startSizer.Add(lblStop, 0, wx.ALL, border=3)
        startSizer.Add(self.fieldStop, 0, wx.ALL, border=3)
        startSizer.Add(lblNumPts, 0, wx.ALL, border=3)
        startSizer.Add(self.fieldPoints, 0, wx.ALL, border=3)
        sweepSizer.AddSpacer(12)
        sweepSizer.Add(startSizer, 0, wx.ALL)
        boxFrequencySweep.SetSizer(sweepSizer)
        ## Solution setup box
        boxSolutionSetupSizer = wx.BoxSizer(wx.VERTICAL)
        boxSolutionSetupSizer.AddSpacer(15)
        boxSolutionSetupSizer.Add(freqSizer, 0, wx.ALL, border=2)
        boxSolutionSetupSizer.Add(passesSizer, 0, wx.ALL, border=2)
        boxSolutionSetupSizer.Add(deltaSizer, 0, wx.ALL, border=2)
        boxSolutionSetupSizer.Add(boxFrequencySweep, 0, wx.ALL, border=10)
        boxSolutionSetupSizer.Add(btnApply, 0, wx.ALL|wx.ALIGN_RIGHT, border=15)
        boxSolutionSetup.SetSizer(boxSolutionSetupSizer) 
        
        ## data collection setup box
        boxLogFilesSizer =  wx.BoxSizer(wx.VERTICAL)
        boxLogFilesSizer.AddSpacer(15)
        boxLogFilesSizer.Add(self.cbCreateSimulationLog, 0, wx.ALL, border=10)
        boxLogFilesSizer.Add(self.cbCreateOptimizerLog, 0, wx.ALL, border=10)
        boxLogFiles.SetSizer(boxLogFilesSizer)
        boxReportOptionsSizer =  wx.BoxSizer(wx.VERTICAL)
        boxReportOptionsSizer.AddSpacer(15)
        boxReportOptionsSizer.Add(self.cbSaveReports, 0, wx.ALL, border=10)
        boxReportOptions.SetSizer(boxReportOptionsSizer)
        boxDataCollectionSetupSizer = wx.BoxSizer(wx.VERTICAL)
        boxDataCollectionSetupSizer.AddSpacer(15)
        boxDataCollectionSetupSizer.Add(boxLogFiles, 0, wx.ALL, border=10)
        boxDataCollectionSetupSizer.Add(boxReportOptions, 0, wx.ALL, border=10)
        boxDataCollectionSetup.SetSizer(boxDataCollectionSetupSizer)

        #left size sizer
        leftSideSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSideSizer.Add(boxSolutionSetup, 0, wx.ALL, border=15)
        leftSideSizer.Add(boxDataCollectionSetup, 0, wx.ALL|wx.EXPAND, border=15)

        #right size sizer
        rightSideSizer = wx.BoxSizer(wx.VERTICAL)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(leftSideSizer, 0, wx.ALL, border=0)
        pageSizer.Add(rightSideSizer, 0, wx.ALL, border=0)
        self.SetSizer(pageSizer)


          
    def updateStatusText(self, t):
        self.parent.updateStatusText(t)

    def getDataCollectionBools(self):
        saveLog = self.cbCreateSimulationLog.GetValue()
        saveOptimizer = self.cbCreateOptimizerLog.GetValue()
        saveData = self.cbSaveReports.GetValue()
        return saveLog, saveOptimizer, saveData

    def btnApplyClicked(self, evt=None):
        #get vals from fields and set to DC
        self.updateDCValsFromUI()
        #self.updateAutoGenValues()
        msg = "applying solution setup"
        self.updateStatusText(msg)
        msg = self.solutionSummaryCheck()
        self.updateStatusText(msg)

    def solutionSummaryCheck(self):
        msg = ""
        # frequencies
        numFreqVals = self.DC.getNumMultipleFreq()
        freqs = self.DC.getSimulationFreq()
        if numFreqVals > 1:
            freqs = [float(x.strip()) for x in freqs.split(',')]
            msg = msg + "Multiple frequency solution added: " + str(self.DC.getSimulationFreq()) + "\n"
            minFreq = min(freqs)
            maxFreq = max(freqs)
        else:
            msg = msg + "Single frequency solution added: " + str(self.DC.getSimulationFreq()) + "\n"
            minFreq = float(freqs)
            maxFreq = float(freqs)

        if minFreq < float(self.DC.getMinSimRange()):
            msg = msg + "WARNING: simulation frequency is lower than the minimum range \n"
        if maxFreq > float(self.DC.getMaxSimRange()):
            msg = msg + "WARNING: simulation frequency is higher than the max range \n"

        return msg


    def updateAutoGenValues(self):
        template = "{:.3e}"
        if self.DC.getUseMultipleFreq() == False:
            if self.DC.getSimulationFreq() is not None:
                self.ckbxMultipleFrequencies.SetValue(False)
                centerFreq = template.format(float(self.DC.getSimulationFreq())).replace("e+", "e")
                minFreq = template.format(float(self.DC.getSimulationFreq())/2).replace("e+", "e")
                maxFreq = template.format(float(self.DC.getSimulationFreq())*1.5).replace("e+", "e")
                self.freq = centerFreq
                self.minFreq = minFreq
                self.maxFreq = maxFreq
                multiFreqBool = False
        else:
            centerFreq = self.DC.getSimulationFreq().split(',') #template.format(self.DC.getSimulationFreq()).replace("e+", "e")
            freqLst = list(centerFreq)
            freqLst = [float(l) for l in freqLst]
            #convert these to sci notation 
            minFreq = min(freqLst)/2
            maxFreq = max(freqLst)*1.5
            self.freq = self.DC.getSimulationFreq()
            self.minFreq = minFreq
            self.maxFreq = maxFreq
            multiFreqBool = True


        self.fieldFrequency.SetValue(self.freq)
        self.ckbxMultipleFrequencies.SetValue(multiFreqBool)
        self.fieldStart.SetValue(str(self.minFreq))
        self.fieldStop.SetValue(str(self.maxFreq))
        #update DC 
        # noErrors = self.updateDCValsFromUI()
        # return noErrors

    def updateDCValsFromUI(self):
        noError, numFreqVals = self.checkFrequencyCompatability()
        # print("num freq vals in panel_simulationSettings.py")
        # print(numFreqVals)
        
        if noError == False:
            return False
    
        if self.checkDeltaCompatability() == False: #noErrors == False
            return False

        self.DC.setUseMultipleFreq(self.ckbxMultipleFrequencies.GetValue())
        self.DC.setNumMultipleFreq(numFreqVals)
        self.DC.setSimulationFreq(self.fieldFrequency.GetValue())
        self.DC.setMinSimRange(self.fieldStart.GetValue())
        self.DC.setMaxSimRange(self.fieldStop.GetValue())
        self.DC.setNumPasses(self.fieldPasses.GetValue())
        self.DC.setMaxDelta(self.fieldDelta.GetValue())
        self.DC.setNumSimPts(self.fieldPoints.GetValue())
        return True

    def setProjectValues(self): #called from parent
        self.fieldFrequency.SetValue(float(self.DC.getSimulationFreq()))
        self.ckbxMultipleFrequencies.SetValue(self.DC.getUseMultipleFreq())
        self.fieldStart.SetValue(float(self.DC.getMinSimRange()))
        self.fieldStop.SetValue(float(self.DC.getMaxSimRange()))
        self.fieldPasses.SetValue(float(self.DC.getNumPasses()))
        self.fieldDelta.SetValue(float(self.DC.getMaxDelta()))
        self.fieldPoints.SetValue(float(self.DC.getNumSimPts()))

    def checkFrequencyCompatability(self):
        # check that if the multi-freq box isn't checked, user hasn't put in multiple frequencies
        freqInput = self.fieldFrequency.GetValue()
        multiBool = self.ckbxMultipleFrequencies.GetValue()
        #remove leading and trailing whitespace
        freqInput = freqInput.strip() 

        #check if free floating comma
        splitComma = freqInput.split(",")
        if "" in splitComma:
            msg = "select 'use multiple frequencies' or use single entry in simulation frequency box"
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            return False, 0

        #check if multi-checkbox and UI field match       
        if multiBool == False:
            if len(splitComma) > 1:
                msg = "select 'use multiple frequencies' or use single entry in simulation frequency box"
                wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
                return False, len(splitComma)
        else:
            splitComma = freqInput.split(",") 
            if len(splitComma) < 2:
                msg = "enter comma seperated values to use multi-frequency mode"
                wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
                return False, len(splitComma)                
        return True, len(splitComma)

    

    def checkDeltaCompatability(self):
        # check that if the multi-freq box isn't checked, user hasn't put in multiple frequencies
        deltaInput = self.fieldDelta.GetValue()
        multiBool = self.ckbxMultipleDelta.GetValue()
        multiFreqBool = self.ckbxMultipleFrequencies.GetValue()
        #remove leading and trailing whitespace
        deltaInput = deltaInput.strip() 

        #check if free floating comma
        splitComma = deltaInput.split(",")
        if "" in splitComma:
            msg = "select 'use multiple frequencies' to enable multiple deltas"
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            return False

        #check if multi-checkbox and UI field match       
        if multiBool == False:
            if len(splitComma) > 1:
                if multiFreqBool == False:
                    msg = "select 'use multiple frequencies' to enable multiple deltas"
                else:
                    msg = "select 'Use Multiple Delta' to use this feature"
                wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
                return False
        else:
            splitComma = deltaInput.split(",") 
            if len(splitComma) < 2:
                msg = "enter comma seperated values to use multi-frequency mode with multiple deltas"
                wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
                return False
        return True


    def applyLoadedProjectSettings(self, PC):
        pass


   