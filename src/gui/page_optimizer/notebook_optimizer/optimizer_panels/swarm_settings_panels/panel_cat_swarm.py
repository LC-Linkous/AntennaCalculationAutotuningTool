##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/swarm_settings_panels/panel_cat_swarm.py'
#   Class for inputs for cat swarm optimizer
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

class Cat_Swarm_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH

        #default swarm variables
        self.numParticles = 5               # Number of Particles in the swarm
        self.weights =  2                   # weights for curr vec, local min vec, global min vec
        self.vlim = 1.5                     # Limit of initialized velocity
        self.toleranceVal = 10e-6           # Convergence Tolerance
        self.maxIter = 10000               # Maximum allowed iterations
        # cat swarm vars
        self.MR = .02                    # Mixture Ratio (MR). Small value for tracing population %.
        self.SMP = 5                     # Seeking memory pool. Num copies of cats made.
        self.SRD = .45                   # Seeking range of the selected dimension. 
        self.CDC = 2                     # Counts of dimension to change. mutation.
        self.SPC = True                  # self-position consideration. boolean.

        boxTuning = wx.StaticBox(self, size=(300, -1))
        stParticles = wx.StaticText(boxTuning, label="No. of Particles")
        self.fieldnumParticles = wx.TextCtrl(boxTuning, value=str(self.numParticles), size=(self.defaultBoxWidth,-1))
        stWeights1 = wx.StaticText(boxTuning, label="Tracing Weight")
        self.fieldWeights1 = wx.TextCtrl(boxTuning, value=str(self.weights), size=(self.defaultBoxWidth,-1))
        stVlim = wx.StaticText(boxTuning, label="Initial Velocity Limit")
        self.fieldVlim = wx.TextCtrl(boxTuning, value=str(self.vlim), size=(self.defaultBoxWidth,-1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1)) 

        stMR = wx.StaticText(boxTuning, label="Mixture Ratio (MR)")
        self.fieldMR = wx.TextCtrl(boxTuning, value=str(self.MR), size=(self.defaultBoxWidth,-1)) 
        stSPM = wx.StaticText(boxTuning, label="Seeking Memory Pool")
        self.fieldSMP = wx.TextCtrl(boxTuning, value=str(self.SMP), size=(self.defaultBoxWidth,-1))
        stSRD = wx.StaticText(boxTuning, label="Seeking Range")
        self.fieldSRD = wx.TextCtrl(boxTuning, value=str(self.SRD), size=(self.defaultBoxWidth,-1)) 
        stCDC = wx.StaticText(boxTuning, label="Mutation Dim")
        self.fieldCDC = wx.TextCtrl(boxTuning, value=str(self.CDC), size=(self.defaultBoxWidth,-1)) 
        SPCvals = ['True', 'False']
        stSPC = wx.StaticText(boxTuning, label="Self Position")
        self.fieldSPC = wx.ComboBox(boxTuning, choices=SPCvals, id=1,style=wx.CB_READONLY, size=(self.defaultBoxWidth, -1))
        self.fieldSPC.SetValue(SPCvals[0])


        # tuning
        col1TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col1TuningSizer.AddSpacer(10)
        col1TuningSizer.Add(stParticles, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stWeights1, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stVlim, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stMR, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stSPM, 0, wx.ALL, border=5)

        col2TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col2TuningSizer.AddSpacer(10)
        col2TuningSizer.Add(self.fieldnumParticles, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldWeights1, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldVlim, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldMR, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldSMP, 0, wx.ALL, border=3)

        col3TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col3TuningSizer.AddSpacer(10)
        col3TuningSizer.Add(stTolerance, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stSRD, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stCDC, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stSPC, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stMaxIter, 0, wx.ALL, border=5)


        col4TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col4TuningSizer.AddSpacer(10)
        col4TuningSizer.Add(self.fieldTolerance, 0, wx.ALL, border=3)
        col4TuningSizer.Add(self.fieldSRD, 0, wx.ALL, border=3)   
        col4TuningSizer.Add(self.fieldCDC, 0, wx.ALL, border=3)
        col4TuningSizer.Add(self.fieldSPC, 0, wx.ALL, border=3)
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
            self.weights = self.fieldWeights1.GetValue()
            self.vlim = self.fieldVlim.GetValue()
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter = self.fieldMaxIter.GetValue()
            self.MR = self.fieldMR.GetValue()
            self.SMP = self.fieldSMP.GetValue()
            self.SRD = self.fieldSRD.GetValue()
            self.CDC = self.fieldCDC.GetValue()
            self.SPC = self.fieldSPC.GetValue()
        except Exception as e:
            print("ERROR in panel_cat_swarm getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['num_particles'] = pd.Series(self.numParticles)
            df['weights'] = pd.Series(self.weights) #singular value
            df['velocity_limit'] = pd.Series(self.vlim)
            df['tolerance'] = pd.Series(self.toleranceVal)
            df['max_iterations'] = pd.Series(self.maxIter)
            df['mixture_ratio'] = pd.Series(self.MR) #was []
            df['seeking_pool'] = pd.Series(self.SMP)
            df['seeking_range'] = pd.Series(self.SRD)
            df['mutation_dim'] = pd.Series(self.CDC)
            df['self_position'] = pd.Series(self.SPC)            

        return df, noError
    