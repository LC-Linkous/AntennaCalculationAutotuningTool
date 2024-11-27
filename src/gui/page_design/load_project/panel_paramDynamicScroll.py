##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_design/load_project/panel_paramDynamicScroll.py'
#   Class for custom material layering scroll panel
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled

# local imports
import project.config.antennaCAT_config as c


class ParamDynamicScrollPanel(wx.Panel):
    def __init__(self, parent, bn="$"):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        # default vals
        self.defaultColors = c.DEFAULT_COLORS
        self.colorMod = len(self.defaultColors)
        self.defaultBoxWidth = 85
        #ctr for indexing
        self.ctr = 0
        #dynamic naming
        self.baseName = bn
        #lists for keeping track of dynamic elements
        self.paramName = []
        self.paramMaterial=[]
        self.paramRemove=[]

        self.scrolled_panel = scrolled.ScrolledPanel(self, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, size=(500,110))
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()   

        self.btnClear = wx.Button(self, label="Clear") #, size=(90, -1))
        self.btnClear.Bind(wx.EVT_BUTTON, self.btnClearParamsClicked)
        self.btnRemove = wx.Button(self, label="Remove") #, size=(90, -1))
        self.btnRemove.Bind(wx.EVT_BUTTON, self.btnRemoveParamsClicked)
        self.btnAdd = wx.Button(self, label="Add") #, size=(90, -1))
        self.btnAdd.Bind(wx.EVT_BUTTON, self.btnAddParamClicked)

        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer, wx.EXPAND)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        btnSizer.AddStretchSpacer()
        btnSizer.Add(self.btnRemove, 0, wx.ALL|wx.RIGHT, border=5)
        btnSizer.Add(self.btnClear, 0, wx.ALL|wx.RIGHT, border=5)
        btnSizer.Add(self.btnAdd, 0, wx.ALL|wx.RIGHT, border=5)
                
        panelSizer.Add(self.scrolled_panel, 1, wx.ALL) #| wx.EXPAND, border=0)
        panelSizer.Add(btnSizer, 0, wx.ALL|wx.EXPAND)
        self.SetSizer(panelSizer)
        self.Layout()#force update for layout

    def btnAddParamClicked(self, evt):
        self.addEmptyRow()

    def btnRemoveParamsClicked(self, evt):
        self.removeParams()

    def btnClearParamsClicked(self, evt):
        self.clearRows()

    def addLabelsToTop(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        lblParamNum = wx.StaticText(self.scrolled_panel, label='#', size=(15, 20))
        lblParamName = wx.StaticText(self.scrolled_panel, label='| Param Name', size=(self.defaultBoxWidth, 20))
        lblParamValue= wx.StaticText(self.scrolled_panel, label= '| Value', size=(self.defaultBoxWidth+25, 20))

        hSizer.Add(lblParamNum, 0, wx.ALL, border=1)
        hSizer.Add(lblParamName, 0, wx.ALL, border=1)
        hSizer.Add(lblParamValue, 0, wx.ALL, border=1)

        return hSizer
    
    def clearRows(self):
        self.vSizer.Clear(True)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.ctr = 0
        self.paramName = []
        self.paramMaterial=[]
        self.paramDepth=[]
        self.paramColor=[]
        self.paramRemove=[]
        self.Layout()#force update for layout

    def removeParams(self):
        #iterate through all checkboxes in collection and get their data
        numElements = len(self.paramName) 
        print(numElements)
        #local vars
        ctr = 0
        paramName = []
        paramVal=[]

        for pR in self.paramRemove:
            if pR.IsChecked() == True: #is checked
                pass
            else:
                paramName.append(self.paramName[ctr].GetValue())
                paramVal.append(self.paramMaterial[ctr].GetValue())
            ctr = ctr+1
        
        self.repopulateRows(paramName, paramVal)

    def repopulateRows(self, pName, pMaterial):
        self.clearRows()
        ctr = 0
        for pn in pName:
            pm = pMaterial[ctr]
            self.addRow(pn, pm)
            ctr = ctr +1
       
    def addRow(self, pn, pm):
        #create new instance of 
        # layer name, material, thickness, 
        self.ctr = self.ctr + 1

        self.vSizer.AddSpacer(2)
        paramNum= wx.StaticText(self.scrolled_panel, label=str(self.ctr), size=(15, 20)) 
        paramName= wx.TextCtrl(self.scrolled_panel, value="", size=(self.defaultBoxWidth, 20))
        paramName.SetValue(pn)
        paramMaterial= wx.TextCtrl(self.scrolled_panel, value="", size=(self.defaultBoxWidth, 20))
        paramMaterial.SetValue(pm)
        removeParam = wx.CheckBox(self.scrolled_panel, label="remove")

        self.paramName.append(paramName)
        self.paramMaterial.append(paramMaterial)
        self.paramRemove.append(removeParam)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(paramNum)
        hSizer.AddSpacer(2)
        hSizer.Add(paramName)
        hSizer.AddSpacer(2)
        hSizer.Add(paramMaterial)
        hSizer.AddSpacer(5)
        hSizer.Add(removeParam)

        self.vSizer.Add(hSizer, border=2)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout

    def addEmptyRow(self):
        self.ctr = self.ctr + 1

        self.vSizer.AddSpacer(2)

        paramNum= wx.StaticText(self.scrolled_panel, label=str(self.ctr), size=(15, 20)) 
        paramName= wx.TextCtrl(self.scrolled_panel, value="", size=(self.defaultBoxWidth, 20))
        pname = self.baseName + str(self.ctr)
        paramName.SetValue(pname)
        paramMaterial= wx.TextCtrl(self.scrolled_panel, value="", size=(self.defaultBoxWidth, 20))
        paramMaterial.SetValue("1")
        removeParam = wx.CheckBox(self.scrolled_panel, label="remove")

        self.paramName.append(paramName)
        self.paramMaterial.append(paramMaterial)
        self.paramRemove.append(removeParam)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(paramNum)
        hSizer.AddSpacer(2)
        hSizer.Add(paramName)
        hSizer.AddSpacer(2)
        hSizer.Add(paramMaterial)
        hSizer.AddSpacer(5)
        hSizer.Add(removeParam)

        self.vSizer.Add(hSizer, border=2)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout

    def getParams(self):
        paramArr = []
        ctr = 0
        for p in self.paramName:
                pn = self.paramName[ctr].GetValue()
                pm = self.paramMaterial[ctr].GetValue()
                paramArr.append([pn, pm])
                ctr = ctr + 1
        return paramArr
 