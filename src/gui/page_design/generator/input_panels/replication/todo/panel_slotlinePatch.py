##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replication/input_panels/panel_planarBowtie.py'
#   Class interfacing with the replicator class
#
#   Paper:
#       [1-hourglass] M. Asili, R. Green, S. Seran and E. Topsakal, "A Small Implantable Antenna for MedRadio and ISM Bands," in IEEE Antennas and Wireless Propagation Letters, vol. 11, pp. 1683-1685, 2012, doi: 10.1109/LAWP.2013.2241723.
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

DESIGN_REPLICATION_ANTENNA = c.DESIGN_REPLICATION_E

class SlotlinePatchOptionsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        lblConductor = wx.StaticText(self, label="Conductor Material (simulation req):")
        conductorTypes = list(materials_dict.keys())
        self.conductorDropDown = wx.ComboBox(self, choices=conductorTypes, style=wx.CB_READONLY) # size=(INPUT_BOX_WIDTH, 20),
        self.conductorDropDown.SetValue('copper')
        self.conductorDropDown.Bind(wx.EVT_COMBOBOX, self.conductorSelected)
        lblGroundDist = wx.StaticText(self, label="Distance from Ground Plane (mm):")
        self.fieldGroundDist = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGroundDist.SetValue("15")

        lblX = wx.StaticText(self, label="X (mm):")
        self.fieldX = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldX.SetValue("0")
        lblLs = wx.StaticText(self, label="Ls (mm):")
        self.fieldLs = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLs.SetValue("20")
        lblLength = wx.StaticText(self, label="Length (mm):")
        self.fieldLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldLength.SetValue("30")
        lblGroundplaneLength = wx.StaticText(self, label="Groundplane Length (mm):")
        self.fieldGroundplaneLength = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGroundplaneLength.SetValue("125")


        lblPs = wx.StaticText(self, label="Ps (mm):")
        self.fieldPs = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldPs.SetValue("7.5")
        lblWs = wx.StaticText(self, label="Ws (mm):")
        self.fieldWs = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWs.SetValue("5")
        lblWidth = wx.StaticText(self, label="Width (mm):")
        self.fieldWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldWidth.SetValue("30")
        lblGroundplaneWidth = wx.StaticText(self, label="Groundplane Width (mm):")
        self.fieldGroundplaneWidth = wx.TextCtrl(self, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldGroundplaneWidth.SetValue("150")


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
        boxInputLeft.Add(lblGroundDist, 0, wx.ALL|wx.EXPAND, border=7)

        boxInputRight.Add(self.conductorDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldGroundDist, 0, wx.ALL|wx.EXPAND, border=3)

        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=10)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=10)

        #small input sizer
        boxSmallInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSmallInput1 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput2 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput3 = wx.BoxSizer(wx.VERTICAL)
        boxSmallInput4 = wx.BoxSizer(wx.VERTICAL)

        boxSmallInput1.Add(lblX, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput1.Add(lblLs, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblLength, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput1.Add(lblGroundplaneLength, 0, wx.ALL|wx.EXPAND, border=5)

        boxSmallInput2.Add(self.fieldX, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldLs, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldLength, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput2.Add(self.fieldGroundplaneLength, 0, wx.ALL|wx.EXPAND, border=3)

        boxSmallInput3.Add(lblPs, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblWs, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblWidth, 0, wx.ALL|wx.EXPAND, border=5)
        boxSmallInput3.Add(lblGroundplaneWidth, 0, wx.ALL|wx.EXPAND, border=5)

        boxSmallInput4.Add(self.fieldPs, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldWs, 0, wx.ALL|wx.EXPAND, border=3)
        boxSmallInput4.Add(self.fieldWidth, 0, wx.ALL|wx.EXPAND, border=3)       
        boxSmallInput4.Add(self.fieldGroundplaneWidth, 0, wx.ALL|wx.EXPAND, border=3)

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

    def getFeatures(self):
        features = [["conductor_material", self.conductorDropDown.GetValue()],
                    ["simulation_frequency", -1]]

        return features
    
    def getParams(self):
        paramArr = []
        x = float(self.fieldX.GetValue())
        l = float(self.fieldLength.GetValue())
        Ls = float(self.fieldLs.GetValue())
        Lg= float(self.fieldGroundplaneLength.GetValue())
        Ps = float(self.fieldPs.GetValue())
        Ws = float(self.fieldWs.GetValue())
        w = float(self.fieldWidth.GetValue())
        Wg = float(self.fieldGroundplaneWidth.GetValue())
        h = float(self.fieldGroundDist.GetValue())

        paramArr = [["X", x],
                    ["L", l],
                    ["Ls", Ls],
                    ["Lg", Lg],
                    ["Ps", Ps],
                    ["Ws", Ws],
                    ["W", w],
                    ["Wg", Wg],
                    ["h", h]]
        return paramArr

    