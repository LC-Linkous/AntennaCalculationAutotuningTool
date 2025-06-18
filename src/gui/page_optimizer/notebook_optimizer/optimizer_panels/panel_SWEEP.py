##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_SWEEP.py'
#   Class interfacing with the SWEEP optimizer
#       Contains widgets for optimizer settings and exports
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 27, 2024
##--------------------------------------------------------------------\

import wx
import os
import pandas as pd
import numpy as np
import project.config.antennaCAT_config as c
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_parameterSummary import ParameterSummaryPanel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_optimizationMetric import OptimizationMetricPanel



# other SWEEP algorithms to be added
from gui.page_optimizer.notebook_optimizer.optimizer_panels.sweep_settings_panels.panel_sweep_grid import Grid_Sweep_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.sweep_settings_panels.panel_sweep_random import Random_Sweep_Panel

#directories

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

OPT_GRID_SWEEP = c.OPT_GRID_SWEEP
OPT_RANDOM_SWEEP = c.OPT_RANDOM_SWEEP




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
        self.optimizerName = OPT_GRID_SWEEP
        self.surrogateName = None # Default internal optimizer is None
        self.modelApproximatorName = None # Default surrogate model approx. is None
        #
        self.paramInput = pd.DataFrame({})

        #local vars
        self.lowerBoundsArr = None
        self.upperBoundsArr = None
        self.metricArr = None
        self.targetArr = None
        self.outputVariables = None
        self.boundary = 1



        # widgets
        self.paramSummary = ParameterSummaryPanel(self)
        self.optimizerMetrics = OptimizationMetricPanel(self)
        self.notebook_settings = SettingsNotebook(self)


        boxSelect = wx.StaticBox(self, label='Select an Optimizer:', size=(300, -1))
        optimizerTypes = ['grid_sweep', 'random_sweep']
        self.optimizerDropDown = wx.ComboBox(boxSelect, choices=optimizerTypes, id=1,style=wx.CB_READONLY, size=(280, -1))
        self.optimizerDropDown.SetValue(optimizerTypes[0])
        self.optimizerDropDown.Bind(wx.EVT_COMBOBOX, self.optimizerDesignSelectionChange)



        ## buttons
        self.btnOpen = wx.Button(self, label="Open Saved")
        self.btnOpen.Bind(wx.EVT_BUTTON, self.btnOpenClicked)
        self.btnSelect = wx.Button(self, label="Select Optimizer")
        self.btnSelect.Bind(wx.EVT_BUTTON, self.btnSelectClicked)
        self.btnExport = wx.Button(self, label="Export State")
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)


       # add the dropdown to  boxSelect
        boxSelectSizer = wx.BoxSizer(wx.VERTICAL)
        boxSelectSizer.AddSpacer(10)
        boxSelectSizer.Add(self.optimizerDropDown, 0, wx.ALL|wx.EXPAND, border=7)
        boxSelect.SetSizer(boxSelectSizer)


        # last column vert sizer
        rightSizeSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizeSizer.Add(boxSelect, 0, wx.ALL|wx.EXPAND, border=7)
        rightSizeSizer.Add(self.notebook_settings, 0, wx.ALL, border=10)
        

        # panel sizer
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.paramSummary, 0, wx.ALL|wx.EXPAND, border=5)
        panelSizer.Add(self.optimizerMetrics, 0, wx.ALL|wx.EXPAND, border=5)
        panelSizer.Add(rightSizeSizer, 0, wx.ALL|wx.EXPAND, border=5)

        # btn sizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnOpen, 0, wx.ALL, border=3)
        btnSizer.Add(self.btnSelect, 0, wx.ALL, border=3)
        btnSizer.Add(self.btnExport, 0, wx.ALL, border=3)
        btnSizer.AddSpacer(50)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        # pageSizer.AddStretchSpacer()
        pageSizer.Add(panelSizer, 0, wx.ALL|wx.EXPAND, border=10)
        pageSizer.AddStretchSpacer()
        pageSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=3)
        self.SetSizer(pageSizer)

#######################################################
# Button Events
#######################################################
    
    def btnOpenClicked(self):
        self.parent.btnOpenClicked()
    
    def btnSelectClicked(self, evt=None):
        # call the optimizer inputs from the child class
        df1, noError = self.notebook_settings.getOptimizerInputs(self.optimizerName)
        # call the optimizer inputs from the page
        df2, noError = self.getPageOptimizerInputs()        

        # merge the data frames
        df = pd.concat([df1, df2], axis=1)

        #assign

        self.DC.setOptimizerParameters(df)
        self.parent.btnSelectClicked(self.optimizerName, noError) 


    def btnExportClicked(self, evt=None):
        self.parent.btnExportClicked()


    def optimizerDesignSelectionChange(self, evt):
            boxText = evt.GetEventObject().GetValue()
            self.optimizerName = self.notebook_settings.set_optimizer_tuning_panel(boxText)
            
            self.Layout() 
    


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

    def getPageInputFields(self):
        # get input fields and check if target selected
        # inclides basic error checking
        noError = True
        
        #from optimizer scroll - returns ref to widgets
        metricTxt, tresholdTxt, targetTxt, checkedBxs = self.optimizerMetrics.getInputBoxVals() 

        ctr = 0
        metricVals = []
        thresholdVals = []
        targetVals = []
        for cb in checkedBxs:
            useMetric = cb.GetValue()
            if useMetric == True:
                mt = metricTxt[ctr].GetValue()
                mt = mt.split(" ")
                metricVals.append(mt[0])
                th = tresholdTxt[ctr].GetValue()
                thresholdVals.append(th)
                t =  targetTxt[ctr].GetValue()
                targetVals.append(t)
            ctr = ctr + 1
             
        self.metricArr = metricVals
        self.thresholdArr = thresholdVals
        self.targetArr = targetVals
        self.outputVariables = np.shape(targetVals)

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


    def getPageOptimizerInputs(self):
        noError = self.getPageInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['num_input'] = pd.Series(self.numInputVariables)
            df['lower_bounds'] = pd.Series([self.lowerBoundsArr])
            df['upper_bounds'] = pd.Series([self.upperBoundsArr])
            df['num_output'] = pd.Series(self.outputVariables)
            df['target_metrics'] = pd.Series([self.metricArr])
            df['target_values'] = pd.Series([self.targetArr])
            df['target_threshold'] = pd.Series([self.thresholdArr])
            df['use_surrogate_bool'] = pd.Series([False])

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


        self.paramSummary.setParameterSummaryText(self.numInputVariables, \
                                                  pName, lbArr, ubArr)
       
    def applyLoadedProjectSettings(self, PC):
        pass
   

#############################################################
#  sub-pages. move these to another file when there's time
# 
# ###########################################################   
class TuningPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent


        self.grid_sweep_panel = Grid_Sweep_Panel(self) #default
        self.random_sweep_panel = Random_Sweep_Panel(self)

        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(self.grid_sweep_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.random_sweep_panel, 1, wx.ALL|wx.EXPAND, border=3)
        self.SetSizer(pageSizer)


        self.random_sweep_panel.Hide()
        self.grid_sweep_panel.Show()



    def set_optimizer_tuning_panel(self, txt="grid_sweep"):
        # add if/else here when adding more options
        if txt == "grid_sweep":
            self.hideEverythingAndShowSinglePanel(self.grid_sweep_panel)
            optimizerName = OPT_GRID_SWEEP
        elif txt == "random_sweep":
            self.hideEverythingAndShowSinglePanel(self.random_sweep_panel)
            optimizerName = OPT_RANDOM_SWEEP

        else:
            print("ERROR in panel_SWEEP.py unknown optimizer selected")

        return optimizerName
    
    def getOptimizerInputs(self, optimizerName):
        noError = False
        df = None

        if optimizerName == OPT_GRID_SWEEP:
            df, noError = self.grid_sweep_panel.getOptimizerInputs()
        elif optimizerName == OPT_RANDOM_SWEEP:
            df, noError = self.random_sweep_panel.getOptimizerInputs()
        else:
            print("ERROR: optimizer name not recognized in panel_SWEEP. Select an option from the dropdown menu to continue!")


        if noError == False:
            print("ERROR: error in optimizer input values. check inputs.")    


        return df, noError

    def hideEverythingAndShowSinglePanel(self, showPanel):
        # hide everything
        self.grid_sweep_panel.Hide()
        self.random_sweep_panel.Hide()
        #show the selected panel
        showPanel.Show()

        self.Layout()

        
class SettingsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent #parent used for sizer layouts in level above
        self.page_tuning = TuningPage(self)
        self.AddPage(self.page_tuning, "Optimizer Parameters")
        #NOTE: sweep&random does NOT have a surrogate model option
       

    def set_optimizer_tuning_panel(self, boxText):
        optimizerName = self.page_tuning.set_optimizer_tuning_panel(boxText)
        return optimizerName

    def getOptimizerInputs(self, optimizerName):
        df, noError = self.page_tuning.getOptimizerInputs(optimizerName)
        return df, noError
    
