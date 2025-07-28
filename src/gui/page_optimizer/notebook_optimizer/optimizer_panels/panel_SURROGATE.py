##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_SURROGATE.py'
#   Class configuring the base and surroagte optimzera and surrogate models approximators
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

#  SurrogateApproxPage:     surrogate model maker
#  BaseOptimizerPage:       page for the main optimizer
#  InternalOptimizerPage:   page for the internal optimizer 
#                               that works with the surogate model
from gui.page_optimizer.notebook_optimizer.optimizer_panels.surrogate_settings_panels.panel_base_optimizer import BaseOptimizerPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.surrogate_settings_panels.panel_internal_optimizer import InternalOptimizerPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.surrogate_settings_panels.panel_surrogate_approx import SurrogateApproxPage

# OPTIMIZERS 
    # there's options for both BASE and INTERNAL optimizer in the dropdown creation
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_pso_python import PSO_Python_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_pso_basic import PSO_Basic_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_cat_swarm import Cat_Swarm_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_sand_cat import Sand_Cat_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_chicken_swarm import Chicken_Swarm_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.swarm_settings_panels.panel_chicken_swarm_2015 import Chicken_Swarm_2015_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_cat_quantum import Cat_Quantum_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_chicken_quantum import Chicken_Quantum_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.quantum_settings_panels.panel_pso_quantum import PSO_Quantum_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.glods_settings_panels.panel_multiglods import MultiGLODS_Panel
# INSERT BAyesiaN
from gui.page_optimizer.notebook_optimizer.optimizer_panels.sweep_settings_panels.panel_sweep_grid import Grid_Sweep_Panel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.sweep_settings_panels.panel_sweep_random import Random_Sweep_Panel


# SURROGATE MODEL APPROXIMATORS
    # these are used to create a surrogate model for the INTERNAL optimizer to solve
    # Bayesian optimization already uses these, so there's some framework that already exists
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


# static lists

BASE_OPTIMIZERS_LIST = c.BASE_OPTIMIZERS_LIST
INTERNAL_OPTIMIZERS_LIST =   c.INTERNAL_OPTIMIZERS_LIST
SURROGATE_LIST = c.SURROGATE_LIST
BOUNDARY_LIST = c.BOUNDARY_LIST


OPT_PSO_BASIC = c.OPT_PSO_BASIC
SM_RADIAL_BASIS_FUNC = c.SM_RADIAL_BASIS_FUNC


class SURROGATEPage(wx.Panel):
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
        self.baseOptimizerName = OPT_PSO_BASIC #set optimizer name with the dropdown
        self.internalOptimizerName = OPT_PSO_BASIC  # default internal optimizer name
        self.modelApproximatorName = SM_RADIAL_BASIS_FUNC # default option for approximating surrogate model
        
        # 
        self.paramInput = pd.DataFrame({})

        #local vars
        self.lowerBoundsArr = None
        self.upperBoundsArr = None
        self.metricArr = None
        self.thresholdArr = None
        self.targetArr = None
        self.outputVariables = None
        self.boundary = 1


        # widgets
        self.paramSummary = ParameterSummaryPanel(self)
        self.optimizerMetrics = OptimizationMetricPanel(self)
        self.notebook_settings = SettingsNotebook(self)

        # widgets
        ## buttons
        self.btnOpen = wx.Button(self, label="Open Saved")
        self.btnOpen.Bind(wx.EVT_BUTTON, self.btnOpenClicked)
        self.btnSelect = wx.Button(self, label="Select Optimizer")
        self.btnSelect.Bind(wx.EVT_BUTTON, self.btnSelectClicked)
        self.btnExport = wx.Button(self, label="Export State")
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)

        # last column vert sizer
        rightSizeSizer = wx.BoxSizer(wx.VERTICAL)
        # rightSizeSizer.Add(boxBoundary, 0, wx.ALL|wx.EXPAND, border=7)
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
         
        # this is the major difference between the other panels and this one
        # the Help Me Choose will have different hooks when it's added back 
        # (to prevent cross-writing with no error checking)


        self.baseOptimizerName, self.internalOptimizerName, self.modelApproximatorName = self.notebook_settings.getOptimizerNames()

        

        #Get the combined df for all 3 setings. ONLY place theres more than 1 arg for this
        #df1, noError = self.notebook_settings.getOptimizerInputs(self.modelApproximatorName)
        df1, noError = self.notebook_settings.getOptimizerInputs(baseOpt=self.baseOptimizerName, 
                                                                 innerOpt=self.internalOptimizerName, 
                                                                 surgModel=self.modelApproximatorName)
        # call the optimizer inputs from the page
        df2, noError = self.getPageOptimizerInputs()        

        # merge the data frames
        df = pd.concat([df1, df2], axis=1)

        self.DC.setOptimizerParameters(df)
        self.parent.btnSelectClicked(self.baseOptimizerName, noError) 
        # this set will trigger the check for the 'using surrogate bool' 


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
    

#######################################################
# Setters and Getters
#######################################################   

    def getOptimizerName(self):
         # this is the name of the BASE optimizer,
         # it is used to set the directory name for where
         # everything is saved
         return self.baseOptimizerName

    def getInternalOptimizerName(self):
         return self.internalOptimizerName

    def getSurrogateApproxName(self):
         return self.modelApproximatorName



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
        # these are the values used for the BASE optimizer. 
        # Most of these are going to be shared across the layered models (inner/outer optimization model)

        noError = self.getPageInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            #
            df['lower_bounds'] = pd.Series([self.lowerBoundsArr])
            df['upper_bounds'] = pd.Series([self.upperBoundsArr])
            df['num_output'] = pd.Series(self.outputVariables)
            df['target_metrics'] = pd.Series([self.metricArr])
            df['target_threshold'] = pd.Series([self.thresholdArr])
            df['target_values'] = pd.Series([self.targetArr])
            df['target_threshold'] = pd.Series([self.thresholdArr])
            
            df['use_surrogate_bool'] = pd.Series([True])

            #pull the boundary option from the panel because it's
            # NOT connected to the optimizer configs, but is a 
            # seperate widget
            self.boundary, sm_bounds = self.notebook_settings.getBoundaries()
            df['boundary'] = pd.Series(self.boundary)
            df['sm_boundary'] = pd.Series(sm_bounds)

        return df, noError
    
        # the other vals are all called with the funcs below. This keeps everything streamlined with the other pages
        # and keeps it modular for other optimizer integration
        # * getOptimizerInputs()
        # * set_optimizer_tuning_panel() is now getOptimizerNames()


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
   


class SettingsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(410, -1))
        self.parent = parent #parent used for sizer layouts in level above
        self.SetMaxSize(wx.Size(500, 320))

        self.page_surrogate = SurrogateApproxPage(self)
        self.page_baseOptimizer = BaseOptimizerPage(self)
        self.page_internalOptimizer = InternalOptimizerPage(self)

        self.AddPage(self.page_baseOptimizer, "Base Optimizer")
        self.AddPage(self.page_internalOptimizer, "Internal Optimizer")
        self.AddPage(self.page_surrogate, "Surrogate Model")
        

    def getBoundaries(self):
        base_boundary = self.page_baseOptimizer.getBoundarySelection()
        sm_boundary = self.page_internalOptimizer.getBoundarySelection()
        return base_boundary, sm_boundary


    def getOptimizerNames(self):

        # naming convention kept to compare between optimizers. This would typically get the
        # text from the dropdown box and set. but because this is 3 pages, this is triggered 
        # a little bit backwards. This calling the bound function for the dropdown menu


        # base optimizer
        optimizerName = self.page_baseOptimizer.getOptimizerName()
        # internal optimizer
        internalName = self.page_internalOptimizer.getOptimizerName()
        # surrogate model approximator
        surrogateName = self.page_surrogate.getOptimizerName()

        return optimizerName, internalName, surrogateName


    def getOptimizerInputs(self, baseOpt, innerOpt, surgModel):

        # this needs to GET and CONSOLIDATE all 3 pages
        df = pd.DataFrame({})

        dfBase, noError = self.page_baseOptimizer.getOptimizerInputs(baseOpt, is_surrogate=False)
        if noError == False:
            return df, noError
            
        dfInner, noError = self.page_internalOptimizer.getOptimizerInputs(innerOpt, is_surrogate=True) #IS SURROGATE/INTERNAL OPTIMIZER
        if noError == False:
            return df, noError
            
        combined_df = dfBase.combine_first(dfInner)               
        dfSurrogate, noError = self.page_surrogate.getOptimizerInputs(surgModel, is_surrogate=False)

        if noError == False:
            return df, noError

        df = combined_df.combine_first(dfSurrogate)   

        return df, noError
        
