##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_slottedPatch.py'
#   Class interfacing with the replicator class
#
#   This replicates the antenna used in: 
#       A. Aldhafeeri and Y. Rahmat-Samii, "Brain Storm Optimization for Electromagnetic 
#        Applications: Continuous and Discrete," in IEEE Transactions on Antennas and Propagation, 
#        vol. 67, no. 4, pp. 2710-2722, April 2019, doi: 10.1109/TAP.2019.2894318.
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 5, 2023
##--------------------------------------------------------------------\

import sys
import wx

sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.configs_materials import materials_dict
import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 70
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_SLOTTED_PATCH

class SlottedPatchOptionsPage(wx.Panel):
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


        lblLr = wx.StaticText(self, label="Lr (mm):")
        self.fieldLr = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLr.SetValue("6.82")
        lblLh = wx.StaticText(self, label="Lh (mm):")
        self.fieldLh = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLh.SetValue("54.1")
        lblLv = wx.StaticText(self, label="Lv (mm):")
        self.fieldLv = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLv.SetValue("22.85")
        lblLength = wx.StaticText(self, label="Length (mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("60.45")
        lblSubstrateLength = wx.StaticText(self, label="Substrate Length (mm):")
        self.fieldSubstrateLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateLength.SetValue("125")
        lblfx = wx.StaticText(self, label="fx (mm):")
        self.fieldfx = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldfx.SetValue("22.43")

        lblPr = wx.StaticText(self, label="Pr (mm):")
        self.fieldPr = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPr.SetValue("-5.21")
        lblWr = wx.StaticText(self, label="Wr (mm):")
        self.fieldWr = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWr.SetValue("6.45")
        lblWu = wx.StaticText(self, label="Wu (mm):")
        self.fieldWu = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWu.SetValue("7.04")
        lblWidth = wx.StaticText(self, label="Width (mm):")
        self.fieldWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("65.96")
        lblSubstrateWidth = wx.StaticText(self, label="Substrate Width (mm):")
        self.fieldSubstrateWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateWidth.SetValue("150")
        lblfy = wx.StaticText(self, label="fy (mm):")
        self.fieldfy = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldfy.SetValue("7.69")


        #patch image
        img_panel = wx.Panel(self, wx.ID_ANY)
        img_panel.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        imgFile = DESIGN_REPLICATION_ANTENNA
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(275, 250, wx.IMAGE_QUALITY_HIGH)
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
        # 3 cols
        boxSmallInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSmallInput1 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput2 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput3 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput4 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput5 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput6 = wx.BoxSizer(wx.VERTICAL)

        boxSmallInput1.Add(lblLr, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput1.Add(lblLh, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput2.Add(self.fieldLr, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldLh, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInput3.Add(lblLv, 0, wx.ALL|wx.EXPAND, border=5)  
        boxSmallInput3.Add(lblPr, 0, wx.ALL|wx.EXPAND, border=5) 
        boxSmallInput4.Add(self.fieldLv, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldPr, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInput5.Add(lblWr, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput5.Add(lblWu, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput6.Add(self.fieldWr, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput6.Add(self.fieldWu, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInputSizer.Add(boxSmallInput1, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput2, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput3, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput4, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput5, 0, wx.ALL|wx.EXPAND,border=5)
        boxSmallInputSizer.Add(boxSmallInput6, 0, wx.ALL|wx.EXPAND,border=5)

        # 2 cols
        boxMiddleInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxMiddleInput1 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput2 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput3 = wx.BoxSizer(wx.VERTICAL)
        boxMiddleInput4 = wx.BoxSizer(wx.VERTICAL)

        boxMiddleInput1.Add(lblSubstrateLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput1.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput1.Add(lblfx, 0, wx.ALL|wx.EXPAND, border=5)   

        boxMiddleInput2.Add(self.fieldSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxMiddleInput2.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxMiddleInput2.Add(self.fieldfx, 0, wx.ALL|wx.EXPAND, border=3)

        boxMiddleInput3.Add(lblSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput3.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput3.Add(lblfy, 0, wx.ALL|wx.EXPAND, border=5)

        boxMiddleInput4.Add(self.fieldSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=3)
        boxMiddleInput4.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)       
        boxMiddleInput4.Add(self.fieldfy, 0, wx.ALL|wx.EXPAND, border=3)

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

    def getFeatures(self):
        features = [["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):  #cannot change names without issues with the lead chars for scripting
        paramArr = []
        d = float(self.fieldSubstrateHeight.GetValue())
        lr = float(self.fieldLr.GetValue())
        lh = float(self.fieldLh.GetValue())
        Lv = float(self.fieldLv.GetValue())
        l = float(self.fieldLength.GetValue())
        fx = float(self.fieldfx.GetValue())

        Pr = float(self.fieldPr.GetValue())
        Wr = float(self.fieldWr.GetValue())
        Wu = float(self.fieldWu.GetValue())
        w = float(self.fieldWidth.GetValue())
        
        Lg= float(self.fieldSubstrateLength.GetValue())
        Wg = float(self.fieldSubstrateWidth.GetValue()) #ground is always the size of the substrate
                                            # so this is now in the template to reduce unused dimensionality
        fy = float(self.fieldfy.GetValue())

        paramArr = [["Lr", lr],
                    ["Lh", lh],
                    ["Lv", Lv],
                    ["L", l],
                    ["Pr", Pr],
                    ["Wr", Wr],
                    ["Wu", Wu],
                    ["W", w],
                    ["fx", fx],
                    ["fy", fy],
                    ["substrate_width", Wg],
                    ["substrate_length", Lg],
                    # ["ground_plane_width", Wg],
                    # ["ground_plane_length", Lg], #ground is always the size of the substrate
                                            # so this is now in the template to reduce unused dimensionality
                    #["conductor_height", None],
                    ["substrate_height", d]]
               # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return paramArr


    