##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/sweep_settings_panels/panel_sweep_random.py'
#   Class for inputs for the sweep optimizer, using the random sampling method
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 29, 2024
##--------------------------------------------------------------------\



import wx
import os
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 50
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

OPT_RANDOM_SWEEP = c.OPT_RANDOM_SWEEP

class Random_Sweep_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH #115 if things look weird

        #class variables
        self.numParticles = 2               # Number of Particles in the swarm
        self.searchType = 2                 # Random Sweep Constant
        self.minRes =  0.1                  # Minimum resolution for search (grid)
        self.maxRes = 1.1                   # Maximum resolution for search (grid)
        self.maxIter = 3000                 # Maximum allowed iterations
        self.toleranceVal = 10e-6           # Convergence Tolerance

        boxTuning = wx.StaticBox(self)
        stParticles = wx.StaticText(boxTuning, label="No. of Particles")
        self.fieldnumParticles = wx.TextCtrl(boxTuning, value=str(self.numParticles), size=(self.defaultBoxWidth,-1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1))


  # tuning
        col1TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col1TuningSizer.AddSpacer(10)
        col1TuningSizer.Add(stParticles, 0, wx.ALL, border=5)

        col2TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col2TuningSizer.AddSpacer(10)
        col2TuningSizer.Add(self.fieldnumParticles, 0, wx.ALL, border=3)

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
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter = self.fieldMaxIter.GetValue()
        except Exception as e:
            print("ERROR in panel_multiglods getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self, is_surrogate=False):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            if is_surrogate == False:
                df['num_particles'] = pd.Series(self.numParticles)
                df['search_selection'] = pd.Series(self.searchType)
                df['min_res'] = pd.Series([self.minRes])
                df['max_res'] = pd.Series(self.maxRes)
                df['tolerance'] = pd.Series(self.toleranceVal)
                df['max_iterations'] = pd.Series(self.maxIter)
                df['optimizer_name'] = pd.Series([OPT_RANDOM_SWEEP])
            else:
                df['sm_num_particles'] = pd.Series(self.numParticles)
                df['sm_search_selection'] = pd.Series(self.searchType)
                df['sm_min_res'] = pd.Series([self.minRes])
                df['sm_max_res'] = pd.Series(self.maxRes)
                df['sm_tolerance'] = pd.Series(self.toleranceVal)
                df['sm_max_iterations'] = pd.Series(self.maxIter)
                df['sm_optimizer_name'] = pd.Series([OPT_RANDOM_SWEEP])

        return df, noError
    
