##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_GLODS.py'
#   Class interfacing with the GLODS optimizer
#       Contains widgets for optimizer settings and exports
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 15, 2023
##--------------------------------------------------------------------\

import wx
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_parameterSummary import ParameterSummaryPanel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_optimizationMetric import OptimizationMetricPanel


#directories

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class SWEEPPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        #UI vars
        self.defaultBoxWidth = 115
        #data management
        self.optimizerName = "SWEEP"
        #
        self.paramInput = pd.DataFrame({})
        #class variables
        self.toleranceVal = 10e-3           # Search Tolerance
        self.lowerBoundsArr = None          # Lower boundaries
        self.upperBoundsArr = None          # Upper Boundaries
        self.stepSize = 0.01                # Increment for variable values
        self.outputVariables = None         # Number of output variables
        
        # widgets
        self.paramSummary = ParameterSummaryPanel(self)

        self.optimizerMetrics = OptimizationMetricPanel(self)
        
        boxTuning = wx.StaticBox(self, label="Tuning Parameters", size=(300, -1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stStepSize = wx.StaticText(boxTuning, label="Step Size")
        self.fieldStepSize = wx.TextCtrl(boxTuning, value=str(self.stepSize), size=(self.defaultBoxWidth,-1))

        ## buttons
        self.btnOpen = wx.Button(self, label="Open Saved")
        self.btnOpen.Bind(wx.EVT_BUTTON, self.btnOpenClicked)
        self.btnSelect = wx.Button(self, label="Select Optimizer")
        self.btnSelect.Bind(wx.EVT_BUTTON, self.btnSelectClicked)
        self.btnExport = wx.Button(self, label="Export State")
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)


        # sizers
        # tuning
        leftTuningSizer = wx.BoxSizer(wx.VERTICAL)
        leftTuningSizer.AddSpacer(10)
        leftTuningSizer.Add(stTolerance, 0, wx.ALL, border=5)
        leftTuningSizer.AddSpacer(4)
        leftTuningSizer.Add(stStepSize, 0, wx.ALL, border=5)

        rightTuningSizer = wx.BoxSizer(wx.VERTICAL)
        rightTuningSizer.AddSpacer(10)
        rightTuningSizer.Add(self.fieldTolerance, 0, wx.ALL, border=3)
        rightTuningSizer.Add(self.fieldStepSize, 0, wx.ALL, border=3)

        boxTuningSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxTuningSizer.Add(leftTuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuningSizer.Add(rightTuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuning.SetSizer(boxTuningSizer)

        # panel sizer
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.paramSummary, 0, wx.ALL|wx.EXPAND, border=10)
        panelSizer.Add(self.optimizerMetrics, 0, wx.ALL|wx.EXPAND, border=10)
        panelSizer.Add(boxTuning, 0, wx.ALL|wx.EXPAND, border=10)

        # btn sizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnOpen, 0, wx.ALL, border=10)
        btnSizer.Add(self.btnSelect, 0, wx.ALL, border=10)
        btnSizer.Add(self.btnExport, 0, wx.ALL, border=10)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        # pageSizer.AddStretchSpacer()
        pageSizer.Add(panelSizer, 1, wx.ALL|wx.EXPAND, border=10)
        pageSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=10)
        self.SetSizer(pageSizer)


#######################################################
# Button Events
#######################################################
    
    def btnOpenClicked(self):
        self.parent.btnOpenClicked()
    
    def btnSelectClicked(self, evt=None):
        df, noError = self.getOptimizerInputs()
        self.DC.setOptimizerParameters(df)
        self.parent.btnSelectClicked(self.optimizerName, noError) 
        print(df)

    def btnExportClicked(self, evt=None):
        self.parent.btnExportClicked()
        
#######################################################
# Status update to main page
#######################################################

    def updateStatusText(self, t):
        self.parent.updateStatusText(t)


#######################################################
# Optimizer save/directory management
#######################################################
    
    def getOptimizerName(self):
         return self.optimizerName
    
#######################################################
# Error checking
#######################################################

    def checkFieldInput(self):
        #check all values can be converted to floats
        #check that lower, upper, and target arrays are comma seperated
        pass

#######################################################
# Setters and Getters
#######################################################
    def getInputFields(self):
        # get input fields and check if target selected
        # inclides basic error checking
        noError = True
        
        #from optimizer scroll - returns ref to widgets
        metricTxt, targetTxt, checkedBxs = self.optimizerMetrics.getInputBoxVals() 

        ctr = 0
        metricVals = []
        targetVals = []
        for cb in checkedBxs:
            useMetric = cb.GetValue()
            if useMetric == True:
                mt = metricTxt[ctr].GetValue()
                mt = mt.split(" ")
                metricVals.append(mt[0])
                t =  targetTxt[ctr].GetValue()
                targetVals.append(t)
            ctr = ctr + 1
             
        self.metricArr = metricVals
        self.targetArr = targetVals
        self.outputVariables = np.shape(targetVals)

        #get from local textbxs
        self.toleranceVal = float(self.fieldTolerance.GetValue())
        self.stepSize =  float(self.fieldStepSize.GetValue())

           
        if (self.upperBoundsArr == None):
            msg = "ERROR: apply parameter configuration to continue"
            self.updateStatusText(msg)
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            noError = False
            return noError
        
        if len(self.metricArr) < 1:
            msg = "ERROR: select at least one optimization metric"
            self.updateStatusText(msg)
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            noError = False
            return noError
        
        return noError

    def getOptimizerInputs(self):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['tolerance'] = pd.Series(self.toleranceVal)
            df['lower_bounds'] = pd.Series([self.lowerBoundsArr])
            df['upper_bounds'] = pd.Series([self.upperBoundsArr])
            df['search_frequency'] = pd.Series(self.stepSize)
            df['num_output'] = pd.Series(self.outputVariables)
            df['target_metrics'] = pd.Series([self.metricArr])
            df['target_values'] = pd.Series([self.targetArr])
        return df, noError

#######################################################
# Page Events
#######################################################
    def parameterSummaryUpdate(self, numControllable, paramInput):
        #parse params from detected params into form optimizer takes
        self.paramInput = paramInput

        self.numInputVariables = numControllable # number total input vars

        pName = []
        lbArr = []
        ubArr = []

        for p in paramInput:
            val = paramInput[p]
            # check if 'ignore' selected
            if val[4] == False: 
                pName.append(p)
                lbArr.append(float(val[2]))
                ubArr.append(float(val[3]))

        self.lowerBoundsArr = lbArr
        self.upperBoundsArr = ubArr
        # msg = str(len(self.lowerBoundsArr)) + " parameters selected for optimization."
        # self.updateStatusText(msg)

        self.paramSummary.setParameterSummaryText(self.numInputVariables, \
                                                  pName, lbArr, ubArr)
       

    def applyLoadedProjectSettings(self, PC):
        pass
   