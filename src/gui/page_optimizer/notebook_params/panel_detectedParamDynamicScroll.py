##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_optimizer/notebook_params/panel_detectedParamDynamicScroll.py'
#   Class for dynamic scroll for detecting params
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 8, 2023
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c
import wx.lib.scrolledpanel as scrolled

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class DetectedBoundaryParameterDynamicScrollPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.numRows = 0

        self.defaultBoxWidth = 110
        self.defaultDelta = 1
        self.defaultVariation = 0.05
        self.originalVal = []
        self.paramFields = []
        self.lowerFields= []
        self.upperFields= []
        self.unitVal = []
        self.ignoreVal=[]

        self.scrolled_panel = scrolled.ScrolledPanel(self, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()

        # btns
        self.btnDetect = wx.Button(self, label="Detect")
        self.btnDetect.Bind(wx.EVT_BUTTON, self.btnDetectClicked)
        self.btnApply= wx.Button(self, label="Apply Configuration")
        self.btnApply.Bind(wx.EVT_BUTTON, self.btnApplyClicked)

        # sizers
        # btn sizer
        boxBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxBtnSizer.AddStretchSpacer()
        boxBtnSizer.Add(self.btnDetect, 0, wx.ALL|wx.RIGHT, border=5)
        boxBtnSizer.Add(self.btnApply, 0, wx.ALL|wx.RIGHT, border=5)


        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        
        
        self.scrolled_panel.SetSizer(self.vSizer, wx.EXPAND)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        panelSizer.Add(boxBtnSizer, 0, wx.EXPAND)
        self.SetSizer(panelSizer)

    def btnDetectClicked(self, evt=None):
        self.parent.btnDetectClicked(evt)
        
    def btnApplyClicked(self, evt=None):
        self.parent.btnApplyClicked(evt)

    def getNumControllableParams(self):
        return self.numRows


    def addRows(self,keyTxt=None, valTxt=None):
        #add top row labels
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, border=3)

        # vals for dropdown
        dataUnits = ['m', 'cm', 'mm']
        
        ctr = 0
        self.numRows = 0
        for t in keyTxt:
            t = t.replace(" ", "")
            vt = valTxt[ctr].replace(" mm", "")
            vt = vt.strip()
            hSizer = wx.BoxSizer(wx.HORIZONTAL)

            tcParam = wx.TextCtrl(self.scrolled_panel, value=str(t), style=wx.TE_READONLY, size=(self.defaultBoxWidth, -1))
            minN, maxN, ignoreVal = self.setRangeValues(vt, self.defaultVariation)
            oVal = self.formatDisplay(vt)
            origVal = wx.TextCtrl(self.scrolled_panel, value=str(oVal), style=wx.TE_READONLY, size=(self.defaultBoxWidth-15, -1)) 
            unitsDropDown = wx.ComboBox(self.scrolled_panel, choices=dataUnits)
            unitsDropDown.SetValue(dataUnits[2]) #mm is default
            lbVal = wx.TextCtrl(self.scrolled_panel, value=str(minN), size=(self.defaultBoxWidth, -1)) 
            ubVal = wx.TextCtrl(self.scrolled_panel, value=str(maxN), size=(self.defaultBoxWidth, -1)) 
            cbIgnoreVal = wx.CheckBox(self.scrolled_panel, label='ignore')
            cbIgnoreVal.SetValue(ignoreVal)

            self.paramFields.append(tcParam)
            self.originalVal.append(origVal)
            self.unitVal.append(unitsDropDown)
            self.lowerFields.append(lbVal)
            self.upperFields.append(ubVal)
            self.ignoreVal.append(cbIgnoreVal)

            hSizer.Add(tcParam, border=3)
            hSizer.Add(origVal, border=3)     
            hSizer.Add(unitsDropDown, border=3)       
            hSizer.Add(lbVal, border=3)
            hSizer.Add(ubVal, border=3)
            hSizer.AddSpacer(3)
            hSizer.Add(cbIgnoreVal, border=5)
            self.vSizer.Add(hSizer, border=3)
            ctr=ctr+1
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout
        self.numRows = ctr


    def addLabelsToTop(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        lblParamName = wx.StaticText(self.scrolled_panel, label='Parameter', size=(self.defaultBoxWidth, 20))
        lblOriginalVal = wx.StaticText(self.scrolled_panel, label='|   Original', size=(self.defaultBoxWidth-15, 20))
        lblUnits = wx.StaticText(self.scrolled_panel, label='|  Units   ', size=(50, 20))
        lblLower = wx.StaticText(self.scrolled_panel, label=' |  Lower Bounds', size=(self.defaultBoxWidth , 20))
        lblUpper = wx.StaticText(self.scrolled_panel, label=' |  Upper Bounds ', size=(self.defaultBoxWidth , 20))
        # lblIgnoreVal = wx.StaticText(self.scrolled_panel, label='|  Ignore')

        hSizer.Add(lblParamName, 0, wx.ALL, border=0)
        hSizer.Add(lblOriginalVal, 0, wx.ALL, border=0)
        hSizer.Add(lblUnits, 0, wx.ALL, border=0)
        hSizer.Add(lblLower, 0, wx.ALL, border=0)
        hSizer.Add(lblUpper, 0, wx.ALL, border=0)
        # hSizer.Add(lblIgnoreVal, 0, wx.ALL, border=0)

        return hSizer
    
    def getInputBoxVals(self):
        return self.paramFields, self.originalVal,  self.unitVal, self.lowerFields, self.upperFields, self.ignoreVal


    def setRangeValues(self, t, varPercent = .15):
        t = t.strip('\"')
        minN = 0
        maxN = 0
        varPercent = float(varPercent)
        try:
            if (t == None) or (t=="None"):
                ignoreVal == True
            else:
                n = float(t)
                minN = n * (1-varPercent)
                maxN = n * (1+varPercent)
                minN = format(minN, '.5f')
                maxN = format(maxN, '.5f')
                ignoreVal=False
        except:
            ignoreVal = True
        return minN, maxN, ignoreVal


    def formatDisplay(self, t):
        t = t.strip('\"')
        try:
            n = float(t)
            t = format(n, '.5f')
            ignoreVal=False
        except:
            ignoreVal = True
        return t


    def clearRows(self):
        self.vSizer.Clear(True)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.ctr = 0
        self.originalVal = []
        self.paramFields = []
        self.lowerFields= []
        self.upperFields= []
        self.unitVal = []
        self.ignoreVal=[]
        self.Layout()#force update for layout


    def applyLoadedProjectSettings(self, PC):
        pass