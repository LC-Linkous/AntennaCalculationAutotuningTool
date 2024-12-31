##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/bayesian_settings_panels/panel_rbf_network.py'
#   Class for inputs for Bayesian optimizer
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 5, 2024
##--------------------------------------------------------------------\



import wx
import numpy as np
import pandas as pd

import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 50
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class RBFNetwork_Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = INPUT_BOX_WIDTH #115 if things look weird


        #surrogate ID vars
        self.surrogateModel = 0


        #class variables
        self.toleranceVal = 1e-4            # Convergence Tolerance
        self.initialNumPts = 1              # Initial number of points (set minimum)
        self.xi = 0.01                      # Exploration weight
        self.numRestarts = 20               # number of sample points generated to avoid local minima
        self.maxIter = 3000                 # Maximum allowed iterations


        self.RBF_kernel  = 'gaussian' #options: 'gaussian', 'multiquadric'
        self.RBF_epsilon = 1.0



        boxTuning = wx.StaticBox(self)
        # bayesian
        stNumSamples = wx.StaticText(boxTuning, label="Initial Num. Samples")
        self.fieldNumSamples = wx.TextCtrl(boxTuning, value=str(self.initialNumPts), size=(self.defaultBoxWidth,-1))
        stXI = wx.StaticText(boxTuning, label="Exploration Balance")
        self.fieldXI = wx.TextCtrl(boxTuning, value=str(self.xi), size=(self.defaultBoxWidth,-1))
        stNumRestarts = wx.StaticText(boxTuning, label="Num. Restarts")
        self.fieldNumRestarts = wx.TextCtrl(boxTuning, value=str(self.numRestarts), size=(self.defaultBoxWidth,-1))
        stTolerance = wx.StaticText(boxTuning, label="Tolerance") 
        self.fieldTolerance = wx.TextCtrl(boxTuning, value=str(self.toleranceVal), size=(self.defaultBoxWidth,-1))
        stMaxIter = wx.StaticText(boxTuning, label="Max Iterations")
        self.fieldMaxIter = wx.TextCtrl(boxTuning, value=str(self.maxIter), size=(self.defaultBoxWidth,-1))
        #surrogate model specific
        stKernelType = wx.StaticText(boxTuning, label="Kernel Type")
        kernelTypes = ['gaussian', 'multiquadric']
        self.kernelDropDown = wx.ComboBox(boxTuning, choices=kernelTypes, id=1,style=wx.CB_READONLY, size=(280, -1))
        self.kernelDropDown.SetValue(kernelTypes[0])
        stEpsilon = wx.StaticText(boxTuning, label="Epsilon")
        self.fieldEpsilon = wx.TextCtrl(boxTuning, value=str(self.xi), size=(self.defaultBoxWidth,-1))

        # tuning
        col1TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col1TuningSizer.AddSpacer(10)
        col1TuningSizer.Add(stNumSamples, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stXI, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stNumRestarts, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stTolerance, 0, wx.ALL, border=5)
        col1TuningSizer.AddSpacer(4)
        col1TuningSizer.Add(stMaxIter, 0, wx.ALL, border=5)

        col2TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col2TuningSizer.AddSpacer(10)
        col2TuningSizer.Add(self.fieldNumSamples, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldXI, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldNumRestarts, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldTolerance, 0, wx.ALL, border=3)
        col2TuningSizer.Add(self.fieldMaxIter, 0, wx.ALL, border=3)

        col3TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col3TuningSizer.AddSpacer(10)
        col3TuningSizer.Add(stKernelType, 0, wx.ALL, border=5)
        col3TuningSizer.AddSpacer(4)
        col3TuningSizer.Add(stEpsilon, 0, wx.ALL, border=5)

        col4TuningSizer = wx.BoxSizer(wx.VERTICAL)
        col4TuningSizer.AddSpacer(10)
        col4TuningSizer.Add(self.kernelDropDown, 0, wx.ALL, border=3)
        col4TuningSizer.Add(self.fieldEpsilon, 0, wx.ALL, border=3)


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
            self.initialNumPts = self.fieldNumSamples.GetValue()
            self.xi = self.fieldXI.GetValue()
            self.numRestarts = self.fieldNumRestarts.GetValue()
            self.toleranceVal = self.fieldTolerance.GetValue()
            self.maxIter = self.fieldMaxIter.GetValue()
            self.RBF_kernel = self.kernelDropDown.GetValue()
            self.RBF_epsilon = self.fieldEpsilon.GetValue()

        except Exception as e:
            print("ERROR in panel_rbf_network getting user input")
            print(e)
            noError = False   
        
        return noError


    def getOptimizerInputs(self):
        noError = self.getInputFields()
        df = pd.DataFrame({})
        if noError == True:   
            df['surrogate_model'] = pd.Series(self.surrogateModel)  
            df['init_samples'] = pd.Series(self.initialNumPts)
            df['xi'] = pd.Series([self.xi])
            df['num_restarts'] = pd.Series(self.numRestarts)
            df['tolerance'] = pd.Series(self.toleranceVal)
            df['max_iterations'] = pd.Series(self.maxIter)
            df['rbf_kernel'] = pd.Series(self.RBF_kernel)
            df['rbf_epsilon'] = pd.Series(self.RBF_epsilon)    
        return df, noError
    
    