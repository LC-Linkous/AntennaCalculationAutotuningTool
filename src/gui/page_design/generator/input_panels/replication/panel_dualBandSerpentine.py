##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_rectangularPatch.py'
#   Class interfacing with the replicator class
#
#   This class replicates the antenna found here:
#       T. Karacolak, A. Z. Hood and E. Topsakal, "Design of a Dual-Band Implantable Antenna 
#        and Development of Skin Mimicking Gels for Continuous Glucose Monitoring," in IEEE Transactions
#       on Microwave Theory and Techniques, vol. 56, no. 4, pp. 1001-1008, April 2008,
#       doi: 10.1109/TMTT.2008.919373.
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
INPUT_BOX_WIDTH = 45
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_SERPENTINE

class DualBandSerpentineOptionsPage(wx.Panel):
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
        self.substrateDropDown.SetValue('Rogers RO3210 (tm)')

        lblPs1 = wx.StaticText(self, label="Ps1 (mm):")
        self.fieldPs1 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPs1.SetValue("-7.0")
        lblLs1 = wx.StaticText(self, label="Ls1 (mm):")
        self.fieldLs1 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLs1.SetValue("19.1")
        lblWs1 = wx.StaticText(self, label="Ws1 (mm):")
        self.fieldWs1 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWs1.SetValue("2.7")

        lblPs2 = wx.StaticText(self, label="Ps2 (mm):")
        self.fieldPs2 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPs2.SetValue("-3.9")
        lblLs2 = wx.StaticText(self, label="Ls2 (mm):")
        self.fieldLs2 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLs2.SetValue("20.1")
        lblWs2 = wx.StaticText(self, label="Ws2 (mm):")
        self.fieldWs2 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWs2.SetValue("0.5")

        lblPs3 = wx.StaticText(self, label="Ps3 (mm):")
        self.fieldPs3 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPs3.SetValue("0.5")
        lblLs3 = wx.StaticText(self, label="Ls3 (mm):")
        self.fieldLs3 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLs3.SetValue("18.0")
        lblWs3 = wx.StaticText(self, label="Ws3 (mm):")
        self.fieldWs3 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWs3.SetValue("2.0")

        lblPs4 = wx.StaticText(self, label="Ps4 (mm):")
        self.fieldPs4 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPs4.SetValue("3.5")
        lblLs4 = wx.StaticText(self, label="Ls4 (mm):")
        self.fieldLs4 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLs4.SetValue("17.5")
        lblWs4 = wx.StaticText(self, label="Ws4 (mm):")
        self.fieldWs4 = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWs4.SetValue("0.6")

        lblLength = wx.StaticText(self, label="Lp (mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("22.0")
        lblSubstrateLength = wx.StaticText(self, label="Lsub (mm):")
        self.fieldSubstrateLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateLength.SetValue("22.5")
        lblPx = wx.StaticText(self, label="Px (mm):")
        self.fieldPx = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPx.SetValue("0.2")

        lblWidth = wx.StaticText(self, label="Wp (mm):")
        self.fieldWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("17.75")
        lblSubstrateWidth = wx.StaticText(self, label="Wsub (mm):")
        self.fieldSubstrateWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldSubstrateWidth.SetValue("22.5")
        lblPy = wx.StaticText(self, label="Py (mm):")
        self.fieldPy = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPy.SetValue("0.2")

        lblFy = wx.StaticText(self, label="Fy (mm):")
        self.fieldFy = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldFy.SetValue("0.1")

        lblLc = wx.StaticText(self, label="Lc (mm):")
        self.fieldLc = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLc.SetValue("9.6")


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

        boxSmallInput1.Add(lblPs1, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblPs2, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblPs3, 0, wx.ALL, border=5)
        boxSmallInput1.Add(lblPs4, 0, wx.ALL, border=5) 
        boxSmallInput2.Add(self.fieldPs1, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldPs2, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldPs3, 0, wx.ALL, border=3)
        boxSmallInput2.Add(self.fieldPs4, 0, wx.ALL, border=3)

        boxSmallInput3.Add(lblLs1, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblLs2, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblLs3, 0, wx.ALL, border=5)
        boxSmallInput3.Add(lblLs4, 0, wx.ALL, border=5)
        boxSmallInput4.Add(self.fieldLs1, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldLs2, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldLs3, 0, wx.ALL, border=3)
        boxSmallInput4.Add(self.fieldLs4, 0, wx.ALL, border=3)

        boxSmallInput5.Add(lblWs1, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblWs2, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblWs3, 0, wx.ALL, border=5)
        boxSmallInput5.Add(lblWs4, 0, wx.ALL, border=5)
        boxSmallInput6.Add(self.fieldWs1, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldWs2, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldWs3, 0, wx.ALL, border=3)
        boxSmallInput6.Add(self.fieldWs4, 0, wx.ALL, border=3)


        
        boxSmallInput7.Add(lblPx, 0, wx.ALL, border=5)
        boxSmallInput7.Add(lblPy, 0, wx.ALL, border=5)
        boxSmallInput7.Add(lblFy, 0, wx.ALL, border=5)
        boxSmallInput7.Add(lblLc, 0, wx.ALL, border=5)
        boxSmallInput8.Add(self.fieldPx, 0, wx.ALL, border=3)
        boxSmallInput8.Add(self.fieldPy, 0, wx.ALL, border=3)
        boxSmallInput8.Add(self.fieldFy, 0, wx.ALL, border=3)
        boxSmallInput8.Add(self.fieldLc, 0, wx.ALL, border=3)

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
        boxMiddleInput1.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput2.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxMiddleInput2.Add(self.fieldSubstrateLength, 0, wx.ALL|wx.EXPAND, border=3)

        boxMiddleInput3.Add(lblSubstrateWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput3.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxMiddleInput4.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)       
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

    def getFeatures(self): #cannot change names without issues with the lead chars for scripting
        features = [["substrate_material", self.substrateDropDown.GetValue()],
                    ["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):
        paramArr = []
        d = float(self.fieldSubstrateHeight.GetValue())
        lp = float(self.fieldLength.GetValue())
        subLength= float(self.fieldSubstrateLength.GetValue())
        wp = float(self.fieldWidth.GetValue())
        subWidth = float(self.fieldSubstrateWidth.GetValue())
        ps1 = float(self.fieldPs1.GetValue())
        ls1 = float(self.fieldLs1.GetValue())
        ws1 = float(self.fieldWs1.GetValue())
        ps2 = float(self.fieldPs2.GetValue())
        ls2 = float(self.fieldLs2.GetValue())
        ws2 = float(self.fieldWs2.GetValue())
        ps3 = float(self.fieldPs3.GetValue())
        ls3 = float(self.fieldLs3.GetValue())
        ws3 = float(self.fieldWs3.GetValue())
        ps4 = float(self.fieldPs4.GetValue())
        ls4 = float(self.fieldLs4.GetValue())
        ws4 = float(self.fieldWs4.GetValue())
        Px = float(self.fieldPx.GetValue())
        Py = float(self.fieldPy.GetValue())
        Fy = float(self.fieldFy.GetValue())
        Lc = float(self.fieldLc.GetValue())


        paramArr = [["Lp", lp],
                    ["Wp", wp],
                    ["Ps1", ps1],
                    ["Ls1", ls1],
                    ["Ws1", ws1],
                    ["Ps2", ps2],
                    ["Ls2", ls2],
                    ["Ws2", ws2],
                    ["Ps3", ps3],
                    ["Ls3", ls3],
                    ["Ws3", ws3],    
                    ["Ps4", ps4],
                    ["Ls4", ls4],
                    ["Ws4", ws4],
                    ["Lc", Lc],
                    ["Fy", Fy],
                    ["Px", Px],
                    ["Py", Py],
                    ["substrate_width", subWidth],
                    ["substrate_length", subLength],
                    # ["ground_plane_width", subWidth], #template has var. GP is substrate size by default
                    # ["ground_plane_length", subLength],
                    #["conductor_height", None],
                    ["substrate_height", d]]
               # THESE NAMES WILL NEED TO MATCH THE TEMPLATE EXACTLY
        return paramArr

    