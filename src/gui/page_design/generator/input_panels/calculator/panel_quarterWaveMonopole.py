##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/calculator/input_panels/panel_quarterWaveMonopole.py'
#   Class interfacing with the internal antenna calculator
#       Contains widgets for quarter wave monopole antenna input
#   Antenna calculator from: https://github.com/Dollarhyde/AntennaCalculator
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.configs_materials import materials_dict
import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class QuarterWaveMonopoleOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblTarget = wx.StaticText(self, label="Target Frequency (Hz):")
        self.fieldFrequency = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFrequency.SetValue("2.4e9")
        lblWireRadius = wx.StaticText(self, label="Wire Radius (mm):")
        self.fieldWireRadius = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWireRadius.SetValue(".15")
        lblGroundPlaneRadius = wx.StaticText(self, label="Ground Plane Radius (mm):")
        self.fieldGroundPlaneRadius = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGroundPlaneRadius.SetValue("50")
        lblFeedGap = wx.StaticText(self, label="Feed Gap (mm):")
        self.fieldFeedGap = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedGap.SetValue("1.5")
        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY)
        self.conductorDropDown.SetValue('copper')

        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)

        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblTarget, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblWireRadius, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblGroundPlaneRadius, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblFeedGap, 0, wx.ALL|wx.EXPAND, border=5)        
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldFrequency, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldWireRadius, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldGroundPlaneRadius, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldFeedGap, 0, wx.ALL|wx.EXPAND, border=3)
        
        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=15)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=15)

        self.SetSizer(boxInputSizer)

    def getFeatures(self):
        features = [["conductor_material", self.conductorDropDown.GetValue()],
                    ["conductor_radius", self.fieldWireRadius.GetValue()],
                    ["ground_plane_radius", self.fieldGroundPlaneRadius.GetValue()],
                    ["feed_gap", self.fieldFeedGap.GetValue()],
                    ["simulation_frequency", self.fieldFrequency.GetValue()]]
        return features
    


        