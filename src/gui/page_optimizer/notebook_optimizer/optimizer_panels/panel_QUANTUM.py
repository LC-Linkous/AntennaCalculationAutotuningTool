##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_QUANTUM.py'
#   Class configuring the quantum inspired optimzers 
#       Contains widgets for optimizer settings and exports
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 17, 2024
##--------------------------------------------------------------------\

import wx
import os
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_parameterSummary import ParameterSummaryPanel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_optimizationMetric import OptimizationMetricPanel

from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_cat_quantum import Cat_Quantum_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_chicken_quantum import Chicken_Quantum_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_pso_quantum import PSO_Quantum_Panel


#directories

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR


OPT_PSO_QUANTUM = c.OPT_PSO_QUANTUM
OPT_CAT_QUANTUM = c.OPT_CAT_QUANTUM
OPT_CHICKEN_QUANTUM = c.OPT_CHICKEN_QUANTUM


class QUANTUMPage(wx.Panel):
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
        self.optimizerName = OPT_PSO_QUANTUM #set base optimizer name with the dropdown
        self.surrogateName = None # Default internal optimizer is None
        self.modelApproximatorName = None # Default surrogate model approx. is None
        #
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
        optimizerTypes = ['quantum_PSO', 'quantum_cat_swarm', 'quantum_chicken_swarm']
        self.optimizerDropDown = wx.ComboBox(boxSelect, choices=optimizerTypes, id=1,style=wx.CB_READONLY, size=(280, -1))
        self.optimizerDropDown.SetValue(optimizerTypes[0])
        self.optimizerDropDown.Bind(wx.EVT_COMBOBOX, self.optimizerDesignSelectionChange)

        boxBoundary = wx.StaticBox(self, label="Select a Boundary Type:")
        bndTypes = ['Random', 'Reflection',
                    'Absorption', 'Invisible'] # getting dictionary keys throws an err
        self.boundaryDropDown = wx.ComboBox(boxBoundary, choices=bndTypes, id=2, style=wx.CB_READONLY, size=(280, -1))
        self.boundaryDropDown.SetValue(bndTypes[0])
        self.boundaryDropDown.Bind(wx.EVT_COMBOBOX, self.boundarySelection) 

        # widgets
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

        # add the boundary dropdown to boxBoundary
        boxBoundarySizer = wx.BoxSizer(wx.VERTICAL)
        boxBoundarySizer.AddSpacer(10)
        boxBoundarySizer.Add(self.boundaryDropDown, 0, wx.ALL|wx.EXPAND, border=7)
        boxBoundary.SetSizer(boxBoundarySizer)
     


        # last column vert sizer
        rightSizeSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizeSizer.Add(boxSelect, 0, wx.ALL|wx.EXPAND, border=7)
        rightSizeSizer.Add(boxBoundary, 0, wx.ALL|wx.EXPAND, border=7)
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
    
    def btnOpenClicked(self, evt=None):
        self.parent.btnOpenClicked()
    
    def btnSelectClicked(self, evt=None):
        # call the optimizer inputs from the child class
        df1, noError = self.notebook_settings.getOptimizerInputs(self.optimizerName)
        # call the optimizer inputs from the page
        df2, noError = self.getPageOptimizerInputs()        

        # merge the data frames
        df = result = pd.concat([df1, df2], axis=1)


        #print(df)
        #assign

        self.DC.setOptimizerParameters(df)
        self.parent.btnSelectClicked(self.optimizerName, noError) 


    def btnExportClicked(self, evt=None):
        self.parent.btnExportClicked()
        
    def optimizerDesignSelectionChange(self, evt):
            boxText = evt.GetEventObject().GetValue()
            self.optimizerName = self.notebook_settings.set_optimizer_tuning_panel(boxText)
            
            self.Layout() 
    
    def boundarySelection(self, evt):       
        boxText = evt.GetEventObject().GetValue()
        if boxText == 'Random':
            self.boundary = 1
        elif boxText == 'Reflection':
            self.boundary = 2
        elif boxText == 'Absorption':
            self.boundary = 3
        elif boxText == 'Invisible':
            self.boundary = 4
        else:
            print("Error: No boundary selected!")

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

        boxText = self.boundaryDropDown.GetValue()
        if boxText == 'Random':
            self.boundary = 1
        elif boxText == 'Reflection':
            self.boundary = 2
        elif boxText == 'Absorption':
            self.boundary = 3
        elif boxText == 'Invisible':
            self.boundary = 4
        else:
            print("Error: No boundary selected! Random boundary used by default")
            self.boundary = 1
           
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
            df['lower_bounds'] = pd.Series([self.lowerBoundsArr])
            df['upper_bounds'] = pd.Series([self.upperBoundsArr])
            df['num_output'] = pd.Series(self.outputVariables)
            df['target_metrics'] = pd.Series([self.metricArr])
            df['target_values'] = pd.Series([self.targetArr])
            df['target_threshold'] = pd.Series([self.thresholdArr])
            df['boundary'] = pd.Series(self.boundary)
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
        # msg = str(len(self.lowerBoundsArr)) + " parameters selected for optimization."
        # self.updateStatusText(msg)

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


        # all panel options
        self.pso_quantum_panel = PSO_Quantum_Panel(self) # default show
        self.cat_quantum_panel = Cat_Quantum_Panel(self)
        self.chicken_quantum_panel = Chicken_Quantum_Panel(self)

        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(self.pso_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.cat_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.chicken_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
        self.SetSizer(pageSizer)

        self.chicken_quantum_panel.Hide()
        self.cat_quantum_panel.Hide()
        self.pso_quantum_panel.Show()


    def set_optimizer_tuning_panel(self, txt):
        if txt == "quantum_PSO":
            self.hideEverythingAndShowSinglePanel(self.pso_quantum_panel)
            optimizerName = OPT_PSO_QUANTUM
        elif txt == 'quantum_cat_swarm':
            self.hideEverythingAndShowSinglePanel(self.cat_quantum_panel)
            optimizerName = OPT_CAT_QUANTUM
        elif txt == 'quantum_chicken_swarm':
            self.hideEverythingAndShowSinglePanel(self.chicken_quantum_panel)
            optimizerName = OPT_CHICKEN_QUANTUM     
        else:
            print("ERROR in panel_QUANTUM.py unknown optimizer selected")

        return optimizerName
    
    def getOptimizerInputs(self, optimizerName):
        noError = False
        df = None


        # call the optimizer inputs from the child class
        if optimizerName == OPT_PSO_QUANTUM:
            df, noError = self.pso_quantum_panel.getOptimizerInputs()
        elif optimizerName == OPT_CAT_QUANTUM:
            df, noError = self.cat_quantum_panel.getOptimizerInputs()
        elif optimizerName == OPT_CHICKEN_QUANTUM:
            df, noError = self.chicken_quantum_panel.getOptimizerInputs()
        else:
            print("ERROR: optimizer name not recognized in panel_QUANTUM. Select an option from the dropdown menu to continue!")


        if noError == False:
            print("ERROR: error in optimizer input values. check inputs.")    


        return df, noError


    def hideEverythingAndShowSinglePanel(self, showPanel):
        # hide everything
        self.chicken_quantum_panel.Hide()
        self.cat_quantum_panel.Hide()
        self.pso_quantum_panel.Hide()
        #show the selected panel
        showPanel.Show()

        self.Layout()


class SettingsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent #parent used for sizer layouts in level above

        self.page_tuning = TuningPage(self)
        #self.page_surrogate = SurrogatePage(self)

        self.AddPage(self.page_tuning, "Optimizer Parameters")
        
        #unhooked here, but the code also hasn't been ported over to this version
        #self.AddPage(self.page_surrogate, "Surrogate Model")
        #self.AddPage(self.page_surrogate, "Help Me Choose")

    def set_optimizer_tuning_panel(self, boxText):
        optimizerName = self.page_tuning.set_optimizer_tuning_panel(boxText)
        return optimizerName

    # def set_surrogate_params_panel(self, boxText):
    #     self.page_surrogate.set_surrogate_params_panel(boxText)

    def getOptimizerInputs(self, optimizerName):
        df, noError = self.page_tuning.getOptimizerInputs(optimizerName)
        return df, noError
        

