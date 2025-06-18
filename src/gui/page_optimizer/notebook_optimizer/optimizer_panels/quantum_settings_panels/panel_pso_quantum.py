##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/swarm_settings_panels/panel_pso_quantum.py'
#   Class for inputs for quantum inspired PSO
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import wx
import os
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 50
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

OPT_PSO_QUANTUM = c.OPT_PSO_QUANTUM

class PSO_Quantum_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH

        #default swarm variables
        self.numParticles = 10              # Number of Particles in the swarm
        self.weights =  [0.7, 1.5, 0.5]     # weights for curr vec, local min vec, global min vec
        self.toleranceVal = 10e-6           # Convergence Tolerance
        self.maxIter = 10000                # Maximum allowed iterations
        self.boundary = 1                   # Boundary Type 1 - Random, 2 - Reflection, 3 - Absorption, 4 - Invisible Wall
        self.metricArr = []
        self.betaVal = 0.5                  # balance between local and global min

        boxTuning = wx.StaticBox(self, size=(300, -1))
        stParticles = wx.StaticText(boxTuning, label="No. of Particles")
        self.fieldnumParticles = wx.TextCtrl(boxTuning, value=str(self.numParticles), size=(self.defaultBoxWidth,-1))
        stWeights1 = wx.StaticText(boxTuning, label="Curr Vel Weight")
        self.fieldWeights1 = wx.TextCtrl(boxTuning, value=str(self.weights[0]), size=(self.defaultBoxWidth,-1))
        stWeights2 = wx.StaticText(boxTuning, label="Local Min Weight")
        self.fieldWeights2 = wx.TextCtrl(boxTuning, value=str(self.weights[1]), size=(self.defaultBoxWidth,-1))
        stWeights3 = wx.StaticText(boxTuning, label="Global Min Weight")
        self.fieldWeights3 = wx.TextCtrl(boxTuning, value=str(self.weights[2]), size=(self.defaultBoxWidth,-1))
        
        
        stBetaVal = wx.StaticText(boxTuning, label="Beta Value")
        self.fieldBetaVal = wx.TextCtrl(boxTuning, value=str(self.betaVal), size=(self.defaultBoxWidth,-1)) 
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1)) 


        # tuning
        col1TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col1TuningSizer.AddSpacer(10)
        col1TuningSizer.Add(stParticles, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stWeights1, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stWeights2, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stWeights3, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stBetaVal, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)

        col2TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col2TuningSizer.AddSpacer(10)
        col2TuningSizer.Add(self.fieldnumParticles, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldWeights1, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldWeights2, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldWeights3, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldBetaVal, 0, wx.ALL, border=3)

        col3TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col3TuningSizer.AddSpacer(10)
        col3TuningSizer.Add(stTolerance, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stMaxIter, 0, wx.ALL, border=5)

        col4TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col4TuningSizer.AddSpacer(10)
        col4TuningSizer.Add(self.fieldTolerance, 0, wx.ALL, border=3)
        col4TuningSizer.Add(self.fieldMaxIter, 0, wx.ALL, border=3)   



        boxTuningSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxTuningSizer.Add(col1TuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuningSizer.Add(col2TuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuningSizer.Add(col3TuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuningSizer.Add(col4TuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuning.SetSizer(boxTuningSizer)


        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxTuning, 0, wx.ALL|wx.EXPAND, border=5)
        self.SetSizer(pageSizer)


    def getInputFields(self):
        noError = True
        try:
            self.numParticles = self.fieldnumParticles.GetValue()
            self.weights = [self.fieldWeights1.GetValue(),
                            self.fieldWeights2.GetValue(), 
                            self.fieldWeights3.GetValue()]
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter = self.fieldMaxIter.GetValue()
            self.betaVal = self.fieldBetaVal.GetValue()
        except Exception as e:
            print("ERROR in panel_pso_basic getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self, is_surrogate=False):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            if is_surrogate == False:
                df['num_particles'] = pd.Series(self.numParticles)
                df['weights'] = pd.Series([self.weights])
                df['tolerance'] = pd.Series(self.toleranceVal)
                df['max_iterations'] = pd.Series(self.maxIter)
                df['beta'] = pd.Series(self.betaVal)
                df['optimizer_name'] = pd.Series([OPT_PSO_QUANTUM])
            else:
                df['sm_num_particles'] = pd.Series(self.numParticles)
                df['sm_weights'] = pd.Series([self.weights])
                df['sm_tolerance'] = pd.Series(self.toleranceVal)
                df['sm_max_iterations'] = pd.Series(self.maxIter)
                df['sm_beta'] = pd.Series(self.betaVal)
                df['sm_optimizer_name'] = pd.Series([OPT_PSO_QUANTUM])
        return df, noError
    
