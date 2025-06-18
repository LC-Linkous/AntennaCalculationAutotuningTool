##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/surrogate_settings_panels/panel_internal_optimizer.py'
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

#directories

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

# static lists
INTERNAL_OPTIMIZERS_LIST =   c.INTERNAL_OPTIMIZERS_LIST
BOUNDARY_LIST = c.BOUNDARY_LIST

OPT_SELECTION = c.OPT_SELECTION
OPT_RULES = c.OPT_RULES
OPT_PSO_BASIC = c.OPT_PSO_BASIC
OPT_PSO_PYTHON = c.OPT_PSO_PYTHON
OPT_PSO_QUANTUM = c.OPT_PSO_QUANTUM
OPT_CAT_SWARM = c.OPT_CAT_SWARM
OPT_SAND_CAT_SWARM = c.OPT_SAND_CAT_SWARM
OPT_CAT_QUANTUM = c.OPT_CAT_QUANTUM
OPT_CHICKEN_SWARM = c.OPT_CHICKEN_SWARM
OPT_CHICKEN_2015 = c.OPT_CHICKEN_2015
OPT_CHICKEN_QUANTUM = c.OPT_CHICKEN_QUANTUM
OPT_MULTI_GLODS = c.OPT_MULTI_GLODS
OPT_BAYESIAN = c.OPT_BAYESIAN
OPT_GRID_SWEEP = c.OPT_GRID_SWEEP
OPT_RANDOM_SWEEP = c.OPT_RANDOM_SWEEP




class InternalOptimizerPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent


        # default names
        self.optimizerName = OPT_PSO_BASIC  #This MUST match the initial menu val if using default setup

        # all panel options
        self.pso_basic_panel = PSO_Basic_Panel(self) # default show
        self.pso_python_panel = PSO_Python_Panel(self)
        self.cat_swarm_panel = Cat_Swarm_Panel(self)
        self.sand_cat_panel = Sand_Cat_Panel(self)
        self.chicken_swarm_panel = Chicken_Swarm_Panel(self)
        self.chicken_swarm_2015_panel = Chicken_Swarm_2015_Panel(self)
        self.pso_quantum_panel = PSO_Quantum_Panel(self) 
        self.cat_quantum_panel = Cat_Quantum_Panel(self)
        self.chicken_quantum_panel = Chicken_Quantum_Panel(self)

        boxOptimizer = wx.StaticBox(self, label="Select an Optimizer:")
        optTypes = INTERNAL_OPTIMIZERS_LIST # getting dictionary keys throws an err
        self.optimizerDropDown = wx.ComboBox(boxOptimizer, choices=optTypes, id=3, style=wx.CB_READONLY, size=(280, -1))
        self.optimizerDropDown.SetValue(optTypes[0])
        self.optimizerDropDown.Bind(wx.EVT_COMBOBOX, self.optimizerDesignSelectionChange) 

        boxBoundary = wx.StaticBox(self, label="Select a Boundary Type:")
        bndTypes = BOUNDARY_LIST
        self.boundaryDropDown = wx.ComboBox(boxBoundary, choices=bndTypes, id=2, style=wx.CB_READONLY, size=(280, -1))
        self.boundaryDropDown.SetValue(bndTypes[0])
        self.boundaryDropDown.Bind(wx.EVT_COMBOBOX, self.boundarySelection) 

        # sizer setup
        # page sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)

        #optimizer selection
        optimizerSizer = wx.BoxSizer(wx.VERTICAL)
        optimizerSizer.AddSpacer(10)
        optimizerSizer.Add(self.optimizerDropDown, 0, wx.ALL|wx.EXPAND, border=4)
        boxOptimizer.SetSizer(optimizerSizer)

        # boundary selection
        boundarySizer = wx.BoxSizer(wx.VERTICAL)
        boundarySizer.AddSpacer(10)
        boundarySizer.Add(self.boundaryDropDown, 0, wx.ALL|wx.EXPAND, border=4)
        boxBoundary.SetSizer(boundarySizer)

        # optimizer configs settings
        optConfigSizer = wx.BoxSizer(wx.VERTICAL)
        optConfigSizer.Add(self.pso_basic_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.pso_python_panel, 1, wx.ALL|wx.EXPAND, border=3) 
        optConfigSizer.Add(self.cat_swarm_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.sand_cat_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.chicken_swarm_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.chicken_swarm_2015_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.pso_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.cat_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
        optConfigSizer.Add(self.chicken_quantum_panel, 1, wx.ALL|wx.EXPAND, border=3)
                
        # set sizers to page
        pageSizer.Add(boxOptimizer, 0, wx.ALL|wx.EXPAND, border=3)   
        pageSizer.Add(boxBoundary, 0, wx.ALL|wx.EXPAND, border=3)
        # pageSizer.Add(boxBoundary, 0, wx.ALL|wx.EXPAND, border=7)
        pageSizer.Add(optConfigSizer, 0, wx.ALL|wx.EXPAND, border=3)
        self.SetSizer(pageSizer)
        
        self.pso_python_panel.Hide()
        self.cat_swarm_panel.Hide()
        self.sand_cat_panel.Hide()
        self.chicken_swarm_panel.Hide()
        self.chicken_swarm_2015_panel.Hide()
        self.chicken_quantum_panel.Hide()
        self.cat_quantum_panel.Hide()
        self.pso_quantum_panel.Hide()
        self.pso_basic_panel.Show()


    def boundarySelection(self, evt=None):       
        boxText = self.boundaryDropDown.GetValue()#evt.GetEventObject().GetValue()
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

    def getBoundarySelection(self):
        self.boundarySelection(None)
        return self.boundary

    def optimizerDesignSelectionChange(self, evt):
            boxText = evt.GetEventObject().GetValue()
            self.optimizerName = self.set_optimizer_tuning_panel(boxText)
            
            self.Layout() 

    def getOptimizerName(self):
        return self.optimizerName

    def set_optimizer_tuning_panel(self, txt):
        if txt == "PSO_basic":
            self.hideEverythingAndShowSinglePanel(self.pso_basic_panel)
            optimizerName = OPT_PSO_BASIC
        elif txt == 'PSO_time_modulation':
            self.hideEverythingAndShowSinglePanel(self.pso_python_panel)
            optimizerName = OPT_PSO_PYTHON
        elif txt == 'cat_swarm':
            self.hideEverythingAndShowSinglePanel(self.cat_swarm_panel)
            optimizerName = OPT_CAT_SWARM      
        elif txt == 'sand_cat_swarm':
            self.hideEverythingAndShowSinglePanel(self.sand_cat_panel)
            optimizerName = OPT_SAND_CAT_SWARM
        elif txt == 'chicken_swarm':
            self.hideEverythingAndShowSinglePanel(self.chicken_swarm_panel)
            optimizerName = OPT_CHICKEN_SWARM      
        elif txt == 'improved_chicken_2015':
            self.hideEverythingAndShowSinglePanel(self.chicken_swarm_2015_panel)
            optimizerName = OPT_CHICKEN_2015
        elif txt == "quantum_PSO":
            self.hideEverythingAndShowSinglePanel(self.pso_quantum_panel)
            optimizerName = OPT_PSO_QUANTUM
        elif txt == 'quantum_cat_swarm':
            self.hideEverythingAndShowSinglePanel(self.cat_quantum_panel)
            optimizerName = OPT_CAT_QUANTUM
        elif txt == 'quantum_chicken_swarm':
            self.hideEverythingAndShowSinglePanel(self.chicken_quantum_panel)
            optimizerName = OPT_CHICKEN_QUANTUM  

        #ADD MULTIGLODS AND BAYES


        else:
            print("ERROR in panel_surrogate.py unknown optimizer selected")

        # print("PANEL_SWARM.PY self.optimizerName set based on dropdown selection")
        # print(optimizerName)
        return optimizerName
    
    def getOptimizerInputs(self, optimizerName, is_surrogate=True):
        noError = False
        df = None

        # call the optimizer inputs from the child class
        if optimizerName == OPT_PSO_BASIC:
            df, noError = self.pso_basic_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_PSO_PYTHON:
            df, noError = self.pso_python_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_CAT_SWARM:
            df, noError = self.cat_swarm_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_SAND_CAT_SWARM:
            df, noError = self.sand_cat_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_CHICKEN_SWARM:
            df, noError = self.chicken_swarm_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_CHICKEN_2015:
            df, noError = self.chicken_swarm_2015_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_PSO_QUANTUM:
            df, noError = self.pso_quantum_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_CAT_QUANTUM:
            df, noError = self.cat_quantum_panel.getOptimizerInputs(is_surrogate)
        elif optimizerName == OPT_CHICKEN_QUANTUM:
            df, noError = self.chicken_quantum_panel.getOptimizerInputs(is_surrogate)
        else:
            print("ERROR: optimizer name not recognized in panel_internal_optimizer. Select an option from the dropdown menu to continue!")
            print("selected optimizer: " + str(optimizerName))

        if noError == False:
            print("ERROR: error in optimizer input values. check inputs.")    


        return df, noError


    def hideEverythingAndShowSinglePanel(self, showPanel):
        # hide everything
        self.pso_basic_panel.Hide()
        self.pso_python_panel.Hide()
        self.cat_swarm_panel.Hide()
        self.sand_cat_panel.Hide()
        self.chicken_swarm_panel.Hide()
        self.chicken_swarm_2015_panel.Hide()
        self.chicken_quantum_panel.Hide()
        self.cat_quantum_panel.Hide()
        self.pso_quantum_panel.Hide()
        #show the selected panel
        showPanel.Show()

        self.Layout()


