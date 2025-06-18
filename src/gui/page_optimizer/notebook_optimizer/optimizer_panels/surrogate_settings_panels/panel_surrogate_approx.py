##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/surrogate_settings_panels/panel_surrogate_approx.py'
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

SURROGATE_LIST = c.SURROGATE_LIST

SM_RADIAL_BASIS_FUNC = c.SM_RADIAL_BASIS_FUNC # this is unstable, so it's been temp removed from menu
SM_GAUSSIAN_PROCESS = c.SM_GAUSSIAN_PROCESS
SM_KRIGING = c.SM_KRIGING
SM_POLY_REGRESSION = c.SM_POLY_REGRESSION
SM_POLY_CHAOS_REGRESSION = c.SM_POLY_CHAOS_REGRESSION
SM_KNN = c.SM_KNN
SM_DECISION_TREE_REGRESSION = c.SM_DECISION_TREE_REGRESSION


class SurrogateApproxPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent


        # default names
        self.optimizerName = SM_GAUSSIAN_PROCESS  #This MUST match the initial menu val if using default setup

        # all panel options
        self.RBF_panel = RBFNetwork_Panel(self) # default show
        self.GP_panel = GaussianProcess_Panel(self)
        self.kriging_panel = Kriging_Panel(self)
        self.PR_panel = PolynomialRegression_Panel(self)
        self.PChaos_panel = PolynomialChaos_Panel(self)
        self.KNN_panel = KNNRegression_Panel(self)
        self.DTR_panel = DecisionTreeRegression_Panel(self)


        boxSelect = wx.StaticBox(self, label='Select a Surrogate Model Kernel:', size=(100, -1))
        surrogateTypes = SURROGATE_LIST
        self.surrogateDropDown = wx.ComboBox(boxSelect, choices=surrogateTypes, id=1,style=wx.CB_READONLY, size=(150, -1))
        self.surrogateDropDown.SetValue(surrogateTypes[0])
        self.surrogateDropDown.Bind(wx.EVT_COMBOBOX, self.optimizerDesignSelectionChange)
        boxSelect.SetMaxSize(wx.Size(-1, 100))  # width: 150 pixels

        #sizer setup
        pageSizer = wx.BoxSizer(wx.VERTICAL)

        # dropdown menus
        boxSelectSizer = wx.BoxSizer(wx.VERTICAL)
        boxSelectSizer.AddSpacer(10)
        boxSelectSizer.Add(self.surrogateDropDown, 0, wx.ALL|wx.EXPAND, border=7)
        boxSelect.SetSizer(boxSelectSizer)

        # config sizers
        configBoxSizer = wx.BoxSizer(wx.VERTICAL)
        configBoxSizer.Add(self.RBF_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.GP_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.kriging_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.PR_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.PChaos_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.KNN_panel, 1, wx.ALL|wx.EXPAND, border=3)
        configBoxSizer.Add(self.DTR_panel, 1, wx.ALL|wx.EXPAND, border=3)

        # set sizers to page
        pageSizer.Add(boxSelect, 1, wx.ALL|wx.EXPAND, border=7)
        pageSizer.Add(configBoxSizer, 1, wx.ALL|wx.EXPAND, border=3)
        self.SetSizer(pageSizer)

        self.GP_panel.Hide()
        self.kriging_panel.Hide()
        self.PR_panel.Hide()
        self.PChaos_panel.Hide()
        self.KNN_panel.Hide()
        self.DTR_panel.Hide()
        self.RBF_panel.Hide()  
        self.GP_panel.Show()#default show


    def optimizerDesignSelectionChange(self, evt):
            # should be : surrogateDesignSelectionChange
            boxText = evt.GetEventObject().GetValue()
            self.optimizerName = self.set_optimizer_tuning_panel(boxText)
            
            self.Layout() 


    def getOptimizerName(self):
        return self.optimizerName
    

    def set_optimizer_tuning_panel(self, txt):

        #uses self.modelApproximatorName to change panels.
        # this distinction is important because versions that use surrogate models
        # in other optimizers will operate more similar to this in the 2025+ update
        txt = str(txt)
        if txt == 'Radial_Basis_Function':
            self.hideEverythingAndShowSinglePanel(self.RBF_panel)
            surrogateAproxName = SM_RADIAL_BASIS_FUNC
        elif txt == 'Gaussian_Process':
            self.hideEverythingAndShowSinglePanel(self.GP_panel)
            surrogateAproxName = SM_GAUSSIAN_PROCESS
        elif txt == 'Kriging':
            self.hideEverythingAndShowSinglePanel(self.kriging_panel)
            surrogateAproxName = SM_KRIGING  
        elif txt == 'Polynomial_Regression':
            self.hideEverythingAndShowSinglePanel(self.PR_panel)
            surrogateAproxName = SM_POLY_REGRESSION
        elif txt == 'Polynomial_Chaos_Expansion':
            self.hideEverythingAndShowSinglePanel(self.PChaos_panel)
            surrogateAproxName = SM_POLY_CHAOS_REGRESSION     
        elif txt == 'K_Nearest_Neighbors':
            self.hideEverythingAndShowSinglePanel(self.KNN_panel)
            surrogateAproxName = SM_KNN
        elif txt == 'Decision_Tree_Regression':
            self.hideEverythingAndShowSinglePanel(self.DTR_panel)
            surrogateAproxName = SM_DECISION_TREE_REGRESSION
        else:
            print("ERROR in panel_surrogate.py unknown surrogate approx selected")

        return surrogateAproxName


    def getOptimizerInputs(self, modelApproximatorName, is_surrogate=False):
        noError = False
        df = None

        # call the optimizer inputs from the child class
        # this uses the surrogate names to make the formatting easier across optimizers
        
        if modelApproximatorName == SM_RADIAL_BASIS_FUNC:
            df, noError = self.RBF_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_GAUSSIAN_PROCESS:
            df, noError = self.GP_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_KRIGING:
            df, noError = self.kriging_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_POLY_REGRESSION:
            df, noError = self.PR_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_POLY_CHAOS_REGRESSION:
            df, noError = self.PChaos_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_KNN:
            df, noError = self.KNN_panel.getOptimizerInputs(is_surrogate)
        elif modelApproximatorName == SM_DECISION_TREE_REGRESSION:
            df, noError = self.DTR_panel.getOptimizerInputs(is_surrogate)
        else:
            print("SURROGATE MODEL APPROXIMATOR NAME")
            print(modelApproximatorName)
            print("ERROR: name not recognized in panel_surrogate_approx.py. Select an option from the dropdown menu to continue!")

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

