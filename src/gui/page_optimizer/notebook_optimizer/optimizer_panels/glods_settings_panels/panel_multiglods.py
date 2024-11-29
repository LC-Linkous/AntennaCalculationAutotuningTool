##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/multiglods_settings_panels/panel_multiglods.py'
#   Class for inputs for multiGLODS optimizer
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

class MultiGLODS_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH #115 if things look weird

        #class variables
        self.toleranceVal = 1e-4            # Convergence Tolerance
        self.betaVal =  0.9                 # Beta Par
        self.gammaVal = 1.1                 # Gamma Par
        self.searchFreq = 2                 # Search Frequency
        self.maxIter = 3000                 # Maximum allowed iterations


        boxTuning = wx.StaticBox(self)
        stBeta = wx.StaticText(boxTuning, label="Beta")
        self.fieldBeta = wx.TextCtrl(boxTuning, value=str(self.betaVal), size=(self.defaultBoxWidth,-1))
        stGamma = wx.StaticText(boxTuning, label="Gamma")
        self.fieldGamma = wx.TextCtrl(boxTuning, value=str(self.gammaVal), size=(self.defaultBoxWidth,-1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stSearchFreq = wx.StaticText(boxTuning, label="Search Frequency")
        self.fieldSearchFreq = wx.TextCtrl(boxTuning, value=str(self.searchFreq), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1))


        leftTuningSizer = wx.BoxSizer(wx.VERTICAL)
        leftTuningSizer.AddSpacer(10)
        leftTuningSizer.Add(stBeta, 0, wx.ALL, border=5)
        leftTuningSizer.AddSpacer(4)
        leftTuningSizer.Add(stGamma, 0, wx.ALL, border=5)
        leftTuningSizer.AddSpacer(4)
        leftTuningSizer.Add(stTolerance, 0, wx.ALL, border=5)
        leftTuningSizer.AddSpacer(4)
        leftTuningSizer.Add(stSearchFreq, 0, wx.ALL, border=5)
        leftTuningSizer.AddSpacer(4)
        leftTuningSizer.Add(stMaxIter, 0, wx.ALL, border=5)

        rightTuningSizer = wx.BoxSizer(wx.VERTICAL)
        rightTuningSizer.AddSpacer(10)
        rightTuningSizer.Add(self.fieldBeta, 0, wx.ALL, border=3)
        rightTuningSizer.Add(self.fieldGamma, 0, wx.ALL, border=3)
        rightTuningSizer.Add(self.fieldTolerance, 0, wx.ALL, border=3)
        rightTuningSizer.Add(self.fieldSearchFreq, 0, wx.ALL, border=3)
        rightTuningSizer.Add(self.fieldMaxIter, 0, wx.ALL, border=3)

        boxTuningSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxTuningSizer.Add(leftTuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuningSizer.Add(rightTuningSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxTuning.SetSizer(boxTuningSizer)


        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        # pageSizer.AddStretchSpacer()
        pageSizer.Add(boxTuning, 0, wx.ALL|wx.EXPAND, border=10)
        self.SetSizer(pageSizer)



    def getInputFields(self):
        noError = True

        try:
            self.betaVal = self.fieldBeta.GetValue()
            self.gammaVal = self.fieldGamma.GetValue()
            self.searchFreq = self.fieldSearchFreq.GetValue()
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter = self.fieldMaxIter.GetValue()
        except Exception as e:
            print("ERROR in panel_multiglods getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['beta'] = pd.Series(self.betaVal)
            df['gamma'] = pd.Series([self.gammaVal])
            df['search_frequency'] = pd.Series(self.searchFreq)
            df['tolerance'] = pd.Series(self.toleranceVal)
            df['max_iterations'] = pd.Series(self.maxIter)
        return df, noError
    
    
