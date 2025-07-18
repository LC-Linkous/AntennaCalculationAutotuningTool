##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_planarBowtie.py'
#   Class interfacing with the replicator class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 28, 2023
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.configs_materials import materials_dict
import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 70
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_PLANAR_BOWTIE

class PlanarBowtieOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblSubstrateHeight = wx.StaticText(self, label="Substrate Height (mm):")
        self.fieldSubstrateHeight = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateHeight.SetValue("1.6")
        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY) # size=(INPUT_BOX_WIDTH, 20),
        self.conductorDropDown.SetValue('copper')
        self.conductorDropDown.Bind(wx.EVT_COMBOBOX, self.conductorSelected)
        lblSimSubstrate = wx.StaticText(self, label="Substrate Material (simulation req):")
        substrateTypes = list(materials_dict.keys())
        self.substrateDropDown = wx.ComboBox(self, choices=substrateTypes,  style=wx.CB_READONLY) #size=(INPUT_BOX_WIDTH, 20),
        self.substrateDropDown.SetValue('FR4_epoxy')
        lblLength = wx.StaticText(self, label="Length (mm): ")
        self.fieldLength  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("31.25")
        lblWidth = wx.StaticText(self, label="Width (mm): ")
        self.fieldWidth  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("46.875")
        lblFeedWidth = wx.StaticText(self, label="Feed Width (mm): ")
        self.fieldFeedWidth  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedWidth.SetValue("3")
        lblGapDistance = wx.StaticText(self, label="Gap Distance (mm): ")
        self.fieldGapDistance  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGapDistance.SetValue("1.5")
        lblSubstrateWidth = wx.StaticText(self, label="Substrate Width (mm): ")
        self.fieldSubstrateWidth  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateWidth.SetValue("150")
        lblSubstrateLength = wx.StaticText(self, label="Substrate Length (mm): ")
        self.fieldSubstrateLength  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateLength.SetValue("100")



  

        #patch image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG) #, wx.BITMAP_TYPE_ANY)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(350, 250, wx.IMAGE_QUALITY_HIGH)
        antennaImg = wx.StaticBitmap(img_panel, wx.ID_ANY)
        antennaImg.SetBitmap(img.ConvertToBitmap()) 


        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        boxInputLeft.Add(lblConductor, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblSimSubstrate, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=5)        
        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.substrateDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldSubstrateHeight, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=10)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=10)

        #small input sizer
        boxSmallInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSmallInput1 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput2 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput3 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput4 = wx.BoxSizer(wx.VERTICAL)

        boxSmallInput1.Add(lblSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput1.Add(lblFeedWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput2.Add(self.fieldSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldFeedWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput3.Add(lblSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblGapDistance, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput4.Add(self.fieldSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldGapDistance, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
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

    def getFeatures(self):  #cannot change names without issues with the lead chars for scripting
        features = [["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):

        paramArr = []
        length = float(self.fieldLength.GetValue())
        width = float(self.fieldWidth.GetValue())
        feedWidth = float(self.fieldFeedWidth.GetValue())
        gapDist = float(self.fieldGapDistance.GetValue())
        subWidth =float(self.fieldSubstrateWidth.GetValue())
        subLength =float(self.fieldSubstrateLength.GetValue())  
        subHeight = float(self.fieldSubstrateHeight.GetValue())


        paramArr = [["length", length],
                    ["width", width],
                    ["feed_width", feedWidth],
                    ["gap_distance", gapDist],
                    ["substrate_width", subWidth],
                    ["substrate_length", subLength],
                    # ["ground_plane_width", subWidth],
                    # ["ground_plane_length", subLength], #GP is ALWAYS substrate size, template has 2 vars tho
                    #["conductor_height", None],
                    ["substrate_height", subHeight]]

               # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return paramArr
