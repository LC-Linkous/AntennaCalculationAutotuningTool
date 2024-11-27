##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_rectangularPatch.py'
#   Class interfacing with the replicator class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 1, 2023
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.configs_materials import materials_dict
import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 70
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_RECTANGULAR_PATCH

class RectangularPatchOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

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
        self.conductorDropDown.Bind(wx.EVT_COMBOBOX, self.conductorSelected)
        lblSimSubstrate = wx.StaticText(self, label="Substrate Material (simulation req):")
        substrateTypes = list(materials_dict.keys())
        self.substrateDropDown = wx.ComboBox(self, choices=substrateTypes,  style=wx.CB_READONLY) #size=(INPUT_BOX_WIDTH, 20),
        self.substrateDropDown.SetValue('FR4_epoxy')
        lblLength = wx.StaticText(self, label="Length (mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("29.44")
        lblWidth = wx.StaticText(self, label="Width (mm):")
        self.fieldWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("38.04")
        lblX0 = wx.StaticText(self, label="X0 (mm):")
        self.fieldX0 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldX0.SetValue("11.32")
        lblY0 = wx.StaticText(self, label="Y0 (mm):")
        self.fieldY0 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldY0.SetValue("19.02")
        lblGap = wx.StaticText(self, label="Gap (mm):")
        self.fieldGap = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGap.SetValue("1")
        lblStripWidth = wx.StaticText(self, label="Strip Width (mm):")
        self.fieldStripWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldStripWidth.SetValue("3.06")

        #patch image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG) #, wx.BITMAP_TYPE_ANY)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(250, 250, wx.IMAGE_QUALITY_HIGH)
        antennaImg = wx.StaticBitmap(img_panel, wx.ID_ANY)
        antennaImg.SetBitmap(img.ConvertToBitmap()) 


        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        boxInputLeft.Add(lblFeed, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblSimSubstrate, 0, wx.ALL|wx.EXPAND, border=7)

        boxInputRight.Add(self.feedDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.substrateDropDown, 0, wx.ALL|wx.EXPAND, border=3)

        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=10)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=10)

        #small input sizer
        boxSmallInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSmallInput1 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput2 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput3 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput4 = wx.BoxSizer(wx.VERTICAL)

        boxSmallInput1.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput1.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblGap, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblDielectric, 0, wx.ALL|wx.EXPAND, border=5)

        boxSmallInput2.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldGap, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldDielectric, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInput3.Add(lblX0, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblY0, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblStripWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=5)

        boxSmallInput4.Add(self.fieldX0, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldY0, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldStripWidth, 0, wx.ALL|wx.EXPAND, border=3)       
        boxSmallInput4.Add(self.fieldSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInputSizer.Add(boxSmallInput1, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput2, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput3, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput4, 0, wx.ALL|wx.EXPAND,border=5)


        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxInputSizer, 0, wx.ALL|wx.EXPAND, border=0)
        pageSizer.Add(boxSmallInputSizer, 0, wx.ALL|wx.CENTER, border=0)
        pageSizer.Add(img_panel, 0, wx.ALL|wx.CENTER, border=5)
        self.SetSizer(pageSizer)
        

    def conductorSelected(self,evt):
        txt = str(materials_dict[self.conductorDropDown.GetValue()])
        self.fieldDielectric.SetValue(txt)

    def getFeatures(self):
        features = [["feed_type", self.feedDropDown.GetValue()],
                    ["dielectric", self.fieldDielectric.GetValue()],
                    ["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["conductor_height", None],
                    ["substrate_height", self.fieldSubstrateHeight.GetValue()],
                    ["gap", self.fieldGap.GetValue()],
                    ["strip_width", self.fieldStripWidth.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):
        paramArr = []
        width = float(self.fieldWidth.GetValue())
        length = float(self.fieldLength.GetValue())
        x0 = float(self.fieldX0.GetValue())
        y0 = float(self.fieldY0.GetValue())
        gap = float(self.fieldGap.GetValue())

        if self.feedDropDown.GetValue() == 'microstrip':
            paramArr = [["width", width],
                        ["length", length],
                        ["x0", x0],
                        ["y0", y0],
                        ["gap", gap],
                        ["strip_width", float(self.fieldStripWidth.GetValue())]]
        else:
            paramArr = [["width", width],
                        ["length", length],
                        ["x0", x0],
                        ["y0", y0],
                        ["gap", gap]]
        return paramArr

    