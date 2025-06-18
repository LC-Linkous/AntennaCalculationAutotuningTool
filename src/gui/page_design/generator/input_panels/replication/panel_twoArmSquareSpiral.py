##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_singleLoop.py'
#   Class interfacing with the replicator class
#
#   [1] https://www.mathworks.com/help/antenna/ref/spiralrectangular.html
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
INPUT_BOX_WIDTH = 70
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_TWO_ARM_SQUARE_SPIRAL

class TwoArmSquareSpiralOptionsPage(wx.Panel):
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
        
        lblInitialWidth = wx.StaticText(self, label="Initial Width (mm):")
        self.fieldInitialWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldInitialWidth.SetValue("10")
        lblInitialLength = wx.StaticText(self, label="Initial Length (mm):")
        self.fieldInitialLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldInitialLength.SetValue("10")
        lblWidth = wx.StaticText(self, label="Strip Width (mm):")
        self.fieldWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("2")
        lblSpacing = wx.StaticText(self, label="Spacing (mm):")
        self.fieldSpacing = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSpacing.SetValue("4.5")
        lblFeedX = wx.StaticText(self, label="Feed X (mm):")
        self.fieldFeedX = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedX.SetValue("0")
        lblFeedY = wx.StaticText(self, label="Feed Y (mm):")
        self.fieldFeedY = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFeedY.SetValue("0")
        lblSubstrateWidth = wx.StaticText(self, label="Substrate Width (mm): ")
        self.fieldSubstrateWidth  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateWidth.SetValue("80")
        lblSubstrateLength = wx.StaticText(self, label="Substrate Length (mm): ")
        self.fieldSubstrateLength  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateLength.SetValue("80")


        #patch image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(285, 250, wx.IMAGE_QUALITY_HIGH)
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
        boxSmallInput1.Add(lblInitialWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput1.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblFeedX, 0, wx.ALL|wx.EXPAND, border=5)
        
        boxSmallInput2.Add(self.fieldSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldInitialWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldFeedX, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInput3.Add(lblSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblInitialLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblSpacing, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblFeedY, 0, wx.ALL|wx.EXPAND, border=5)
        
        boxSmallInput4.Add(self.fieldSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldInitialLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldSpacing, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldFeedY, 0, wx.ALL|wx.EXPAND, border=3)


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

        initW = float(self.fieldInitialWidth.GetValue())
        initL = float(self.fieldInitialLength.GetValue())
        stripWidth = float(self.fieldWidth.GetValue())
        feedX = float(self.fieldFeedX.GetValue())
        feedY = float(self.fieldFeedY.GetValue())
        spacing = float(self.fieldSpacing.GetValue())
        subWidth =float(self.fieldSubstrateWidth.GetValue())
        subLength =float(self.fieldSubstrateLength.GetValue())  
        subHeight = float(self.fieldSubstrateHeight.GetValue())


        features = [["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):
        paramArr = []
        initW = float(self.fieldInitialWidth.GetValue())
        initL = float(self.fieldInitialLength.GetValue())
        stripWidth = float(self.fieldWidth.GetValue())
        feedX = float(self.fieldFeedX.GetValue())
        feedY = float(self.fieldFeedY.GetValue())
        spacing = float(self.fieldSpacing.GetValue())
        subWidth =float(self.fieldSubstrateWidth.GetValue())
        subLength =float(self.fieldSubstrateLength.GetValue())  
        subHeight = float(self.fieldSubstrateHeight.GetValue())

        paramArr = [["init_width", initW],
                    ["init_length", initL],
                    ["strip_width", stripWidth],
                    ["feed_x", feedX],
                    ["feed_y", feedY],
                    ["spacing", spacing],
                    ["substrate_width", subWidth],
                    ["substrate_length", subLength],
                    # ["ground_plane_width", subWidth],
                    # ["ground_plane_length", subLength],
                    #["conductor_height", None],
                    ["substrate_height", subHeight]]

               # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return paramArr

