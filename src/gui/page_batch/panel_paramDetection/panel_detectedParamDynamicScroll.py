##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_batch/panel_paramDetection/panel_detectedParamDynamicScroll.py'
#   Class for dynamic scroll for detecting params
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
import wx.lib.scrolledpanel as scrolled

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class DetectedBoundaryParameterDynamicScrollPanel(wx.Panel):
    def __init__(self, parent, DC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        
        self.defaultBoxWidth = 135
        self.defaultDelta = 1
        self.defaultVariation = 0.01 #use 0.12 in real testing
        self.originalVal = []
        self.paramFields = []
        self.typeFields = []
        self.percentVar = []
        self.valFields= []
        self.unitVal = []
        self.deltaVals = []
        self.ignoreVal=[]

        self.scrolled_panel = scrolled.ScrolledPanel(self, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()

        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        
        self.scrolled_panel.SetSizer(self.vSizer, wx.EXPAND)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        self.SetSizer(panelSizer)


    def addRows(self,keyTxt=None, valTxt=None):
        #add top row labels
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, border=3)

        # vals for dropdown
        dataTypes = ['Range','Constant','Parameter','Materials']
        dataUnits = ['m', 'cm', 'mm']
        
        ctr = 0
        for t in keyTxt:
            t = t.replace(" ", "")
            vt = valTxt[ctr].replace(" mm", "")
            vt = vt.strip()
            hSizer = wx.BoxSizer(wx.HORIZONTAL)
            tcParam = wx.TextCtrl(self.scrolled_panel, value=t, style=wx.TE_READONLY, size=(self.defaultBoxWidth, -1))
            rVal, ignoreVal = self.setRangeValues(vt, self.defaultVariation)
            oVal = self.formatDisplay(vt)
            origVal = wx.TextCtrl(self.scrolled_panel, value=oVal, size=(self.defaultBoxWidth, -1)) 
            unitsDropDown = wx.ComboBox(self.scrolled_panel, choices=dataUnits)
            unitsDropDown.SetValue(dataUnits[2]) #mm is default
            typeDropDown = wx.ComboBox(self.scrolled_panel, choices=dataTypes, size=(self.defaultBoxWidth-15, -1))
            if ignoreVal == True: #probably a material or parameter - TODO need to check if in list of materials
                typeDropDown.SetValue(dataTypes[2]) 
            else: #edited to be a range
                typeDropDown.SetValue(dataTypes[0])
            pVar = wx.TextCtrl(self.scrolled_panel, value=str(self.defaultVariation), size=(self.defaultBoxWidth-40, -1))
            pVar.Bind(wx.EVT_KILL_FOCUS, self.variationTextChanged)  
            # wx.EVT_KILL_FOCUS(pVar, self.variationTextChanged)  
            tcVal = wx.TextCtrl(self.scrolled_panel, value=rVal, size=(self.defaultBoxWidth, -1)) 
            delVal = wx.TextCtrl(self.scrolled_panel, value=str(self.defaultDelta), size=(50, -1))
            cbIgnoreVal = wx.CheckBox(self.scrolled_panel, label='use original')
            cbIgnoreVal.SetValue(ignoreVal)

            self.paramFields.append(tcParam)
            self.originalVal.append(origVal)
            self.unitVal.append(unitsDropDown)
            self.typeFields.append(typeDropDown)
            self.percentVar.append(pVar)
            self.valFields.append(tcVal)
            self.deltaVals.append(delVal)
            self.ignoreVal.append(cbIgnoreVal)

            hSizer.Add(tcParam, border=3)
            hSizer.Add(origVal, border=3)     
            hSizer.Add(unitsDropDown, border=3)       
            hSizer.Add(typeDropDown, border=3)
            hSizer.Add(pVar, border=3)
            hSizer.Add(tcVal, border=3)
            hSizer.Add(delVal, border=3)
            hSizer.Add(cbIgnoreVal, border=5)
            self.vSizer.Add(hSizer, border=3)
            ctr=ctr+1
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout


    def addLabelsToTop(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        lblParamName = wx.StaticText(self.scrolled_panel, label='Parameter', size=(self.defaultBoxWidth, 20))
        lblOriginalVal = wx.StaticText(self.scrolled_panel, label='|   Original', size=(self.defaultBoxWidth, 20))
        lblUnits = wx.StaticText(self.scrolled_panel, label='|  Units   ', size=(50, 20))
        lblType = wx.StaticText(self.scrolled_panel, label= '|  Type', size=(self.defaultBoxWidth-10, 20))
        lblPercentVar = wx.StaticText(self.scrolled_panel, label= '| +- Variation%', size=(self.defaultBoxWidth-47, 20))
        lblVariations = wx.StaticText(self.scrolled_panel, label=' |  Variation Range ', size=(self.defaultBoxWidth, 20))
        lblDelta = wx.StaticText(self.scrolled_panel, label='|  Δ  ', size=(50, 20))
        lblIgnoreVal = wx.StaticText(self.scrolled_panel, label='|  Ignore')

        hSizer.Add(lblParamName, 0, wx.ALL, border=0)
        hSizer.Add(lblOriginalVal, 0, wx.ALL, border=0)
        hSizer.Add(lblUnits, 0, wx.ALL, border=0)
        hSizer.Add(lblType, 0, wx.ALL, border=0)
        hSizer.Add(lblPercentVar, 0, wx.ALL, border=0)
        hSizer.Add(lblVariations, 0, wx.ALL, border=0)
        hSizer.Add(lblDelta, 0, wx.ALL, border=0)
        hSizer.Add(lblIgnoreVal, 0, wx.ALL, border=0)

        return hSizer
    
    
    def variationTextChanged(self, evt=None):
        evt.Skip() #so UI doesn't hang
        
        #get the index in the list where the change was made
        if evt.GetEventObject() in self.percentVar:
            idx = self.percentVar.index(evt.GetEventObject())
            #get original value
            oVal = self.originalVal[idx].GetValue()
            #get value of new % variaion
            pVar = evt.GetEventObject().GetValue()
            #get string for the range values
            t, ignoreVal = self.setRangeValues(oVal, pVar)
            #set in the val field
            self.valFields[idx].SetValue(t)
                          

    def getInputBoxVals(self):
        return self.paramFields, self.originalVal,  self.unitVal, self.typeFields, self.percentVar, self.valFields, self.deltaVals, self.ignoreVal


    def setRangeValues(self, t, varPercent = .15):
        t = t.strip('\"')
        varPercent = float(varPercent)
        decimalPrecision = self.DC.getNumericalPrecision()
        try:
            if (t == None) or (t =="None"):
                ignoreVal == True
            else:
                n = float(t)
                minN = n * (1-varPercent)
                maxN = n * (1+varPercent)
                minN = round(minN, decimalPrecision)
                maxN = round(maxN, decimalPrecision)
                t = "[" + str(minN) + ", " + str(maxN) + "]"
                ignoreVal=False
        except:
            ignoreVal = True
        return t, ignoreVal


    def formatDisplay(self, t):
        t = t.strip('\"')
        decimalPrecision = self.DC.getNumericalPrecision()
        try:
            n = float(t)
            t = str(round(n, decimalPrecision))
        except:
            pass
        return t


    def clearRows(self):
        self.vSizer.Clear(True)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.ctr = 0
        self.originalVal = []
        self.paramFields = []
        self.typeFields = []
        self.valFields= []
        self.percentVar = []
        self.unitVal = []
        self.deltaVals = []
        self.ignoreVal=[]

        self.Layout()#force update for layout


    def applyLoadedProjectSettings(self, PC):
        pass