##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_halfWaveDipole.py'
#   Class interfacing with the replicator class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 7, 2023
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.configs_materials import materials_dict

import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_DIPOLE

class HalfWaveDipoleOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblLength = wx.StaticText(self, label="Total Length(mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("60")
        lblWireRadius = wx.StaticText(self, label="Wire Radius (mm):")
        self.fieldWireRadius = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWireRadius.SetValue("1")
        lblFeedGap = wx.StaticText(self, label="Feed Gap (mm):")
        self.fieldFeedGap = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedGap.SetValue("5")
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
        img = img.Scale(100, 300, wx.IMAGE_QUALITY_HIGH)
        antennaImg = wx.StaticBitmap(img_panel, wx.ID_ANY)
        antennaImg.SetBitmap(img.ConvertToBitmap())       

        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblWireRadius, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputLeft.Add(lblFeedGap, 0, wx.ALL|wx.EXPAND, border=5)
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldWireRadius, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldFeedGap, 0, wx.ALL|wx.EXPAND, border=3)
        
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
        feedGap = float(self.fieldFeedGap.GetValue())

        paramArr = [["length", l],
                    ["half_length", l/2],
                    ["conductor_radius", conductorRad],
                    ["feed_gap", feedGap],
                    ["substrate_width", None],
                    ["substrate_length", None],
                    ["ground_plane_width", None],
                    ["ground_plane_length", None],
                    #["conductor_height", None],
                    ["substrate_height", None]]
                
        return paramArr