##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/calculator/input_panels/panel_rectangularPatch.py'
#   Class interfacing with the internal antenna calculator
#       Contains widgets for rectangular patch antenna input
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

class RectangularPatchOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblTarget = wx.StaticText(self, label="Target Frequency (Hz):")
        self.fieldFrequency = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFrequency.SetValue("2.4e9")
        lblDielectric = wx.StaticText(self, label="Dielectric Constant:")
        self.fieldDielectric = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldDielectric.SetValue("4.4")
        lblSubstrateHeight = wx.StaticText(self, label="Substrate Height (mm):")
        self.fieldSubstrateHeight = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateHeight.SetValue("1.6")
        lblFeed = wx.StaticText(self, label="Feed Method (simulation req):")
        feedTypes = ['microstrip', 'probe']
        self.feedDropDown = wx.ComboBox(self, choices=feedTypes, style=wx.CB_READONLY) #, size=(INPUT_BOX_WIDTH, 20)
        self.feedDropDown.SetValue(feedTypes[0])
        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY) # size=(INPUT_BOX_WIDTH, 20),
        self.conductorDropDown.SetValue('copper')
        lblSimSubstrate = wx.StaticText(self, label="Substrate Material (simulation req):")
        substrateTypes = list(materials_dict.keys())
        self.substrateDropDown = wx.ComboBox(self, choices=substrateTypes,  style=wx.CB_READONLY) #size=(INPUT_BOX_WIDTH, 20),
        self.substrateDropDown.SetValue('FR4_epoxy')
        self.substrateDropDown.Bind(wx.EVT_COMBOBOX, self.substrateSelected)
        lblGap = wx.StaticText(self, label="Gap (optional, mm):")
        self.fieldGap = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGap.SetValue("1")
        lblStripWidth = wx.StaticText(self, label="Strip Width (optional, mm):")
        self.fieldStripWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldStripWidth.SetValue("3.06")
        self.ckbX0 = wx.CheckBox(self, label="Use L/4 for probe feed X0")

        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        
        boxInputLeft.Add(lblFeed, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblSimSubstrate, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblTarget, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblDielectric, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblGap, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblStripWidth, 0, wx.ALL|wx.EXPAND, border=7)


        boxInputRight.Add(self.feedDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.substrateDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldFrequency, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldDielectric, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldGap, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldStripWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.ckbX0, 0, wx.ALL|wx.EXPAND, border=3)

        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=15)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=15)


        self.SetSizer(boxInputSizer)
        

    def conductorSelected(self,evt):
        txt = str(materials_dict[self.conductorDropDown.GetValue()])
        self.fieldDielectric.SetValue(txt)

    def substrateSelected(self,evt):
        txt = str(materials_dict[self.substrateDropDown.GetValue()])
        self.fieldDielectric.SetValue(txt)

    def getFeatures(self):

        ft = self.feedDropDown.GetValue()
        
        if ft == 'microstrip': #strip fed 
            features = [["feed_type", self.feedDropDown.GetValue()],
                        ["dielectric", self.fieldDielectric.GetValue()],
                        ["substrate_material", self.substrateDropDown.GetValue()],
                        ["conductor_material", self.conductorDropDown.GetValue()],
                        #["conductor_height", None],
                        ["substrate_height", self.fieldSubstrateHeight.GetValue()],
                        ["simulation_frequency", self.fieldFrequency.GetValue()],
                        ["gap", self.fieldGap.GetValue()],
                        ["strip_width", self.fieldStripWidth.GetValue()]]

        else: # probe fed

            features = [["feed_type", self.feedDropDown.GetValue()],
                        ["dielectric", self.fieldDielectric.GetValue()],
                        ["substrate_material", self.substrateDropDown.GetValue()],
                        ["conductor_material", self.conductorDropDown.GetValue()],
                        #["conductor_height", None],
                        ["substrate_height", self.fieldSubstrateHeight.GetValue()],
                        ["simulation_frequency", self.fieldFrequency.GetValue()],
                        #["gap", self.fieldGap.GetValue()]
                        ]
               # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return features
    
    def getUseLengthForX0(self):
        return self.ckbX0.GetValue()


        