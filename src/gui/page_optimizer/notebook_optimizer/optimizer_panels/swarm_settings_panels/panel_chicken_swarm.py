##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/swarm_settings_panels/panel_chicken_swarm.py'
#   Class for inputs for chicken swarm optimizer
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

class Chicken_Swarm_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH

        #default swarm variables
        self.toleranceVal = 10e-6           # Convergence Tolerance
        self.maxIter = 10000               # Maximum allowed iterations
        self.boundary = 1                   # Boundary Type 1 - Random, 2 - Reflection, 3 - Absorption, 4 - Invisible Wall
        self.metricArr = []
        self.RN = 2                       # Total number of roosters
        self.HN = 3                       # Total number of hens
        self.MN = 2                       # Number of mother hens in total hens
        self.CN = 5                       # Total number of chicks
        self.G = 70                        # Reorganize groups every G steps 

        boxTuning = wx.StaticBox(self, size=(300, -1))
        stRN = wx.StaticText(boxTuning, label="No. of Roosters")
        self.fieldnumRoosters = wx.TextCtrl(boxTuning, value=str(self.RN), size=(self.defaultBoxWidth,-1))
        stHN = wx.StaticText(boxTuning, label="No. of Hens")
        self.fieldnumHens = wx.TextCtrl(boxTuning, value=str(self.HN), size=(self.defaultBoxWidth,-1))
        stMN = wx.StaticText(boxTuning, label="No. of Mothers")
        self.fieldnumMother = wx.TextCtrl(boxTuning, value=str(self.MN), size=(self.defaultBoxWidth,-1))
        stCN = wx.StaticText(boxTuning, label="No. of Chicks")
        self.fieldnumChicks = wx.TextCtrl(boxTuning, value=str(self.CN), size=(self.defaultBoxWidth,-1))
        stG = wx.StaticText(boxTuning, label="Generation Length")
        self.fieldnumGenerations = wx.TextCtrl(boxTuning, value=str(self.G), size=(self.defaultBoxWidth,-1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1)) 


        # tuning
        col1TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col1TuningSizer.AddSpacer(10)
        col1TuningSizer.Add(stRN, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stHN, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stMN, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stCN, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stG, 0, wx.ALL, border=5)

        col2TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col2TuningSizer.AddSpacer(10)
        col2TuningSizer.Add(self.fieldnumRoosters, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldnumHens, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldnumMother, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldnumChicks, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldnumGenerations, 0, wx.ALL, border=3)

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
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter  = self.fieldMaxIter.GetValue()
            self.RN = self.fieldnumRoosters.GetValue()
            self.HN = self.fieldnumHens.GetValue()
            self.MN = self.fieldnumMother.GetValue()
            self.CN = self.fieldnumChicks.GetValue()
            self.G = self.fieldnumGenerations.GetValue()
        
        except Exception as e:
            print("ERROR in panel_chicke_swarm getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['tolerance'] = pd.Series(self.toleranceVal)
            df['max_iterations'] = pd.Series(self.maxIter)
            df['rooster_number'] = pd.Series(self.RN)
            df['hen_number'] = pd.Series(self.HN)
            df['mother_number'] = pd.Series(self.MN)
            df['chick_number'] = pd.Series(self.CN)
            df['generation'] = pd.Series(self.G)
        
        return df, noError
