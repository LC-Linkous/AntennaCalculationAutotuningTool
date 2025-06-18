##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_BAYESIAN.py'
#   Class configuring the BAYESIAN optimzer and surrogate models
#       Contains widgets for optimizer settings and exports
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 10, 2025
##--------------------------------------------------------------------\

import wx
import os
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_parameterSummary import ParameterSummaryPanel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_optimizationMetric import OptimizationMetricPanel

from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_decision_tree_regression import DecisionTreeRegression_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_gaussian_process import GaussianProcess_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_knn_regression import KNNRegression_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_kriging_regression import Kriging_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_polynomial_chaos_expansion import PolynomialChaos_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_polynomial_regression import PolynomialRegression_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.bayesian_settings_panels.panel_rbf_network import RBFNetwork_Panel

#directories

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

SURROGATE_LIST = c.SURROGATE_LIST
BOUNDARY_LIST = c.BOUNDARY_LIST
OPT_BAYESIAN = c.OPT_BAYESIAN
SM_RADIAL_BASIS_FUNC = c.SM_RADIAL_BASIS_FUNC # this is unstable, so it's been temp removed from menu
SM_GAUSSIAN_PROCESS = c.SM_GAUSSIAN_PROCESS
SM_KRIGING = c.SM_KRIGING
SM_POLY_REGRESSION = c.SM_POLY_REGRESSION
SM_POLY_CHAOS_REGRESSION = c.SM_POLY_CHAOS_REGRESSION
SM_KNN = c.SM_KNN
SM_DECISION_TREE_REGRESSION = c.SM_DECISION_TREE_REGRESSION

class BAYESIANPage(wx.Panel):
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
        self.optimizerName = OPT_BAYESIAN #set optimizer name with the dropdown
        self.surrogateName = None # does not have surrogate model by default. ALSO, BAYESIAN does not use a surrogate model optimizer
        self.modelApproximatorName = SM_GAUSSIAN_PROCESS
        
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

        boxSelect = wx.StaticBox(self, label='Select a Surrogate Model Kernel:', size=(300, -1))
        surrogateTypes = SURROGATE_LIST
        self.surrogateDropDown = wx.ComboBox(boxSelect, choices=surrogateTypes, id=1,style=wx.CB_READONLY, size=(280, -1))
        self.surrogateDropDown.SetValue(surrogateTypes[0])
        self.surrogateDropDown.Bind(wx.EVT_COMBOBOX, self.optimizerDesignSelectionChange)

        boxBoundary = wx.StaticBox(self, label="Select a Boundary Type:")
        bndTypes = BOUNDARY_LIST# getting dictionary keys throws an err
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
        boxSelectSizer.Add(self.surrogateDropDown, 0, wx.ALL|wx.EXPAND, border=7)
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
    
    def btnOpenClicked(self):
        self.parent.btnOpenClicked()
    
    def btnSelectClicked(self, evt=None):
        # call the optimizer inputs from the child class
         #ONLY optimizer where self.modelApproximatorName replaces self.optimizerName here. 
        df1, noError = self.notebook_settings.getOptimizerInputs(self.modelApproximatorName)
        # call the optimizer inputs from the page
        df2, noError = self.getPageOptimizerInputs()        

        # merge the data frames
        df = pd.concat([df1, df2], axis=1)


        #print(df)
        #assign

        self.DC.setOptimizerParameters(df)
        self.parent.btnSelectClicked(self.optimizerName, noError) 


        # df, noError = self.getOptimizerInputs()
        # self.DC.setOptimizerParameters(df)
        # self.parent.btnSelectClicked(self.optimizerName, noError) 
        # print(df)

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
            print("Error: No boundary selected!")
           
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
        self.RBF_panel = RBFNetwork_Panel(self) # default show
        self.GP_panel = GaussianProcess_Panel(self)
        self.kriging_panel = Kriging_Panel(self)
        self.PR_panel = PolynomialRegression_Panel(self)
        self.PChaos_panel = PolynomialChaos_Panel(self)
        self.KNN_panel = KNNRegression_Panel(self)
        self.DTR_panel = DecisionTreeRegression_Panel(self)

        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(self.RBF_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.GP_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.kriging_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.PR_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.PChaos_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.KNN_panel, 1, wx.ALL|wx.EXPAND, border=3)
        pageSizer.Add(self.DTR_panel, 1, wx.ALL|wx.EXPAND, border=3)
        self.SetSizer(pageSizer)

        
        self.kriging_panel.Hide()
        self.PR_panel.Hide()
        self.PChaos_panel.Hide()
        self.KNN_panel.Hide()
        self.DTR_panel.Hide()
        self.RBF_panel.Hide()  
        self.GP_panel.Show()#default show


    def set_optimizer_tuning_panel(self, txt):

        #uses self.modelApproximatorName to change panels.
        # this distinction is important because versions that use surrogate models
        # in other optimizers will operate more similar to this in the 2025.0 update

        optimizerName = OPT_BAYESIAN
        if txt == 'Radial_Basis_Function':
            self.hideEverythingAndShowSinglePanel(self.RBF_panel)
            modelApproximatorName = SM_RADIAL_BASIS_FUNC
        elif txt == 'Gaussian_Process':
            self.hideEverythingAndShowSinglePanel(self.GP_panel)
            modelApproximatorName = SM_GAUSSIAN_PROCESS
        elif txt == 'Kriging':
            self.hideEverythingAndShowSinglePanel(self.kriging_panel)
            modelApproximatorName = SM_KRIGING
        elif txt == 'Polynomial_Regression':
            self.hideEverythingAndShowSinglePanel(self.PR_panel)
            modelApproximatorName = SM_POLY_REGRESSION
        elif txt == 'Polynomial_Chaos_Expansion':
            self.hideEverythingAndShowSinglePanel(self.PChaos_panel)
            modelApproximatorName = SM_POLY_CHAOS_REGRESSION
        elif txt == 'K_Nearest_Neighbors':
            self.hideEverythingAndShowSinglePanel(self.KNN_panel)
            modelApproximatorName = SM_KNN
        elif txt == 'Decision_Tree_Regression':
            self.hideEverythingAndShowSinglePanel(self.DTR_panel)
            modelApproximatorName = SM_DECISION_TREE_REGRESSION
        else:
            print("ERROR in panel_bayesian.py unknown model approximator selected")
            optimizerName = OPT_BAYESIAN
            modelApproximatorName = None

        return optimizerName, modelApproximatorName


    def getOptimizerInputs(self, modelApproximatorName):
        noError = False
        df = None

        # call the optimizer inputs from the child class
        # this uses the surrogate names to make the formatting easier across optimizers
        
        if modelApproximatorName == SM_RADIAL_BASIS_FUNC:
            df, noError = self.RBF_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_GAUSSIAN_PROCESS:
            df, noError = self.GP_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_KRIGING:
            df, noError = self.kriging_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_POLY_REGRESSION:
            df, noError = self.PR_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_POLY_CHAOS_REGRESSION:
            df, noError = self.PChaos_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_KNN:
            df, noError = self.KNN_panel.getOptimizerInputs()
        elif modelApproximatorName == SM_DECISION_TREE_REGRESSION:
            df, noError = self.DTR_panel.getOptimizerInputs()
        else:
            print("SURROGATE MODEL APPROXIMATOR NAME")
            print(modelApproximatorName)
            print("ERROR: name not recognized in panel_BAYESIAN. Select an option from the dropdown menu to continue!")


        if noError == False:
            print("ERROR: error in optimizer input values. check inputs.")    


        return df, noError


    def hideEverythingAndShowSinglePanel(self, showPanel):
        # hide everything
        self.RBF_panel.Hide()
        self.GP_panel.Hide()
        self.kriging_panel.Hide()
        self.PR_panel.Hide()
        self.PChaos_panel.Hide()
        self.KNN_panel.Hide()
        self.DTR_panel.Hide()
        #show the selected panel
        showPanel.Show()

        self.Layout()

class SettingsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent #parent used for sizer layouts in level above

        self.page_tuning = TuningPage(self)
        self.AddPage(self.page_tuning, "Optimizer Parameters")
        

    def set_optimizer_tuning_panel(self, boxText):
        optimizerName = self.page_tuning.set_optimizer_tuning_panel(boxText)
        return optimizerName


    def getOptimizerInputs(self, optimizerName):
        df, noError = self.page_tuning.getOptimizerInputs(optimizerName)
        return df, noError
        

