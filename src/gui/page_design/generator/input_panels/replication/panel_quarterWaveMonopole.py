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
DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_QUARTER_MONOPOLE

class QuarterWaveMonopoleOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)


        lblWireRadius = wx.StaticText(self, label="Wire Radius (mm):")
        self.fieldWireRadius = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWireRadius.SetValue(".15")
        lblGroundPlaneRadius = wx.StaticText(self, label="Ground Plane Radius (mm):")
        self.fieldGroundPlaneRadius = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGroundPlaneRadius.SetValue("50")
        lblFeedGap = wx.StaticText(self, label="Gap (mm):")
        self.fieldFeedGap = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedGap.SetValue("1.5")
        lblLength = wx.StaticText(self, label="Total Length(mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("60")
        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY)
        self.conductorDropDown.SetValue('copper')

        #image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG) #, wx.BITMAP_TYPE_ANY)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(150, 200, wx.IMAGE_QUALITY_HIGH)
        antennaImg = wx.StaticBitmap(img_panel, wx.ID_ANY)
        antennaImg.SetBitmap(img.ConvertToBitmap())       

        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblWireRadius, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblGroundPlaneRadius, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblFeedGap, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldWireRadius, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldGroundPlaneRadius, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldFeedGap, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=15)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=15)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxInputSizer, 0, wx.ALL|wx.EXPAND, border=5)
        pageSizer.Add(img_panel, 0, wx.ALL|wx.CENTER, border=5)
        self.SetSizer(pageSizer)

    def getFeatures(self):  #cannot change names without issues with the lead chars for scripting
        features = [["substrate_material", None],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self): #numerical vals
        l = float(self.fieldLength.GetValue())
        conductorRad = float(self.fieldWireRadius.GetValue())
        gpRad = float(self.fieldGroundPlaneRadius.GetValue())
        feedGap = float(self.fieldFeedGap.GetValue())

        paramArr = [["conductor_radius", conductorRad],
                    ["ground_plane_radius", gpRad],
                    ["feed_gap", feedGap],
                    ["length", l ],
                    # ["substrate_width", None],
                    # ["substrate_length", None],
                    # ["ground_plane_width", None],
                    # ["ground_plane_length", None],
                    #["conductor_height", None],
                    # ["substrate_height", None]
                    ]
             # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return paramArr



        