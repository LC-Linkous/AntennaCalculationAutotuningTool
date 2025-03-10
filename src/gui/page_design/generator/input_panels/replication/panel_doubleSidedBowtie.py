##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_planarBowtie.py'
#   Class interfacing with the replicator class
#
#   paper:
#   [1] T. Karacolak and E. Topsakal, "A Double-Sided Rounded Bow-Tie Antenna (DSRBA) for UWB Communication," in IEEE Antennas and Wireless Propagation Letters, vol. 5, pp. 446-449, 2006, doi: 10.1109/LAWP.2006.885013.
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

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_TWO_SIDED_BOWTIE

class DoubleSidedBowtieOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblSubstrateHeight = wx.StaticText(self, label="Substrate Height (mm):")
        self.fieldSubstrateHeight = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateHeight.SetValue("1.27")
        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY) # size=(INPUT_BOX_WIDTH, 20),
        self.conductorDropDown.SetValue('copper')
        self.conductorDropDown.Bind(wx.EVT_COMBOBOX, self.conductorSelected)
        lblSimSubstrate = wx.StaticText(self, label="Substrate Material (simulation req):")
        substrateTypes = list(materials_dict.keys())
        self.substrateDropDown = wx.ComboBox(self, choices=substrateTypes,  style=wx.CB_READONLY) #size=(INPUT_BOX_WIDTH, 20),
        self.substrateDropDown.SetValue('Rogers RO3210 (tm)')


        lblSubstrateWidth = wx.StaticText(self, label="Substrate Width (mm): ")
        self.fieldSubstrateWidth  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateWidth.SetValue("36")
        lblSubstrateLength = wx.StaticText(self, label="Substrate Length (mm): ")
        self.fieldSubstrateLength  = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateLength.SetValue("36")
        lblW2 = wx.StaticText(self, label="W2 (mm):")
        self.fieldW2 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW2.SetValue("1.87")
        lblW3 = wx.StaticText(self, label="W3 (mm):")
        self.fieldW3 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW3.SetValue("2.8")
        lblW4 = wx.StaticText(self, label="W4 (mm):")
        self.fieldW4 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW4.SetValue("2.6")
        lblW5 = wx.StaticText(self, label="W5 (mm):")
        self.fieldW5 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW5.SetValue("1.4")
        lblW6 = wx.StaticText(self, label="W6 (mm):")
        self.fieldW6 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW6.SetValue("2.3")
        lblW7 = wx.StaticText(self, label="W7 (mm):")
        self.fieldW7 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW7.SetValue("9")
        lblW8 = wx.StaticText(self, label="W8 (mm):")
        self.fieldW8 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldW8.SetValue("1")

        lblL2 = wx.StaticText(self, label="L2 (mm):")
        self.fieldL2 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL2.SetValue("6")
        lblL3 = wx.StaticText(self, label="L3 (mm):")
        self.fieldL3 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL3.SetValue("4.6")
        lblL4 = wx.StaticText(self, label="L4 (mm):")
        self.fieldL4 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL4.SetValue("11.9")
        lblL5 = wx.StaticText(self, label="L5 (mm):")
        self.fieldL5 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL5.SetValue("3.2")
        lblL6 = wx.StaticText(self, label="L6 (mm):")
        self.fieldL6 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL6.SetValue("12")
        lblL7 = wx.StaticText(self, label="L7  (mm):")
        self.fieldL7 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldL7.SetValue("0.8")

        self.ckbxRoundedBowTie = wx.CheckBox(self, label="rounded edges", size=(-1, 20))
        self.ckbxRoundedBowTie.SetValue(True)
        self.ckbxRoundedBowTie.Disable()

        #patch image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(335, 255, wx.IMAGE_QUALITY_HIGH)
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
        boxSmallInput5 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput6 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput7 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput8 = wx.BoxSizer(wx.VERTICAL)

        boxSmallInput1.Add(lblW2, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblW3, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblW4, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblW5, 0, wx.ALL, border=5) 
        boxSmallInput1.Add(lblW6, 0, wx.ALL, border=5)

        boxSmallInput2.Add(self.fieldW2, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldW3, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldW4, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldW5, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldW6, 0, wx.ALL, border=3)
       
        boxSmallInput3.Add(lblW7, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblW8, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblL2, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblL3, 0, wx.ALL, border=5)

        boxSmallInput4.Add(self.fieldW7, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldW8, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldL2, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldL3, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.ckbxRoundedBowTie, 0, wx.ALL|wx.EXPAND, border=3)
        
        boxSmallInput5.Add(lblL4, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblL5, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblL6, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblL7, 0, wx.ALL, border=5)
        boxSmallInput6.Add(self.fieldL4, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldL5, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldL6, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldL7, 0, wx.ALL, border=3)


        boxSmallInputSizer.Add(boxSmallInput1, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput2, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput3, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput4, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput5, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput6, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput7, 0, wx.ALL|wx.EXPAND,border=0)
        boxSmallInputSizer.Add(boxSmallInput8, 0, wx.ALL|wx.EXPAND,border=0)

        # 2 cols
        boxMiddleInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxMiddleInput1 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput2 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput3 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput4 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput5 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput6 = wx.BoxSizer(wx.VERTICAL)


        boxMiddleInput1.Add(lblSubstrateLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput2.Add(self.fieldSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)

        boxMiddleInput3.Add(lblSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput4.Add(self.fieldSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=3)
        
        boxMiddleInputSizer.Add(boxMiddleInput1, 0, wx.ALL|wx.EXPAND,border=5)
        boxMiddleInputSizer.Add(boxMiddleInput2, 0, wx.ALL|wx.EXPAND,border=5)
        boxMiddleInputSizer.Add(boxMiddleInput3, 0, wx.ALL|wx.EXPAND,border=5)
        boxMiddleInputSizer.Add(boxMiddleInput4, 0, wx.ALL|wx.EXPAND,border=5)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxInputSizer, 0, wx.ALL|wx.EXPAND, border=0)
        pageSizer.Add(boxMiddleInputSizer, 0, wx.ALL|wx.CENTER, border=0)
        pageSizer.Add(boxSmallInputSizer, 0, wx.ALL|wx.CENTER, border=0)
        pageSizer.Add(img_panel, 0, wx.ALL|wx.CENTER, border=0)
        self.SetSizer(pageSizer)
        

    def conductorSelected(self,evt):
        txt = str(materials_dict[self.conductorDropDown.GetValue()])
        # self.fieldDi.SetValue(txt)

    def getFeatures(self):  #cannot change names without issues with the lead chars for scripting
        features = [["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    
    def getParams(self):
        paramArr = []
        w2 = float(self.fieldW2.GetValue())
        w3 = float(self.fieldW3.GetValue())
        w4= float(self.fieldW4.GetValue())
        w5 = float(self.fieldW5.GetValue())
        w6 = float(self.fieldW6.GetValue())
        w7 = float(self.fieldW7.GetValue())
        w8 = float(self.fieldW8.GetValue())
        l2 = float(self.fieldL2.GetValue())
        l3 = float(self.fieldL3.GetValue())
        l4 = float(self.fieldL4.GetValue())
        l5 = float(self.fieldL5.GetValue())
        l6 = float(self.fieldL6.GetValue())
        l7 = float(self.fieldL7.GetValue())
        subLength = float(self.fieldSubstrateLength.GetValue())
        subWidth = float(self.fieldSubstrateWidth.GetValue())
        subHeight = float(self.fieldSubstrateHeight.GetValue())


        paramArr = [["W2", w2],
                    ["W3", w3],
                    ["W4", w4],
                    ["W5", w5],
                    ["W6", w6],
                    ["W7", w7],
                    ["W8", w8],
                    ["L2", l2],
                    ["L3", l3],
                    ["L4", l4],
                    ["L5", l5],
                    ["L6", l6],
                    ["L7", l7],    
                    ["substrate_width", subWidth],
                    ["substrate_length", subLength],
                    ["ground_plane_width", subWidth],
                    ["ground_plane_length", subLength],
                    #["conductor_height", None],
                    ["substrate_height", subHeight]]
        return paramArr

    