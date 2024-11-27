##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/load_script/panel_detectedParamDynamicScroll.py'
#   Class for dynamic scroll for detecting params
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled

import project.config.antennaCAT_config as c
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class DetectedParameterDynamicScrollPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = 110
        self.paramFields = [] #names of detected parameters
        self.valFields=[] #value of detected parameters

        self.scrolled_panel = scrolled.ScrolledPanel(self, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
       
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer, wx.EXPAND)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolled_panel, 1, wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(panelSizer)
    
    def clearRows(self):
        self.paramFields = [] #names of detected parameters
        self.valFields=[] #value of detected parameters
        self.vSizer.Clear(True)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout

    def addLabelsToTop(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        lblParamName = wx.StaticText(self.scrolled_panel, label='  Parameter Name ', size=(self.defaultBoxWidth, 20))
        lblParamValue= wx.StaticText(self.scrolled_panel, label= '|     Value', size=(self.defaultBoxWidth, 20))

        hSizer.Add(lblParamName, 0, wx.ALL, border=1)
        hSizer.Add(lblParamValue, 0, wx.ALL, border=1)

        return hSizer

    def addRows(self,keyTxt=None, valTxt=None):
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = self.addLabelsToTop()
        self.vSizer.Add(topSizer, border=3)
        ctr = 0
        for t in keyTxt:
            hSizer = wx.BoxSizer(wx.HORIZONTAL)
            tcParam = wx.TextCtrl(self.scrolled_panel, value=t, style=wx.TE_READONLY)

            vTxt = valTxt[ctr] 
            tcVal= wx.TextCtrl(self.scrolled_panel, value=vTxt, size=(180,-1), style=wx.TE_READONLY)

            self.paramFields.append(tcParam)
            self.valFields.append(tcVal)

            hSizer.Add(tcParam, border=3)
            hSizer.Add(tcVal, border=3)
            self.vSizer.Add(hSizer, border=3)
            ctr=ctr+1
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout


    def getInputBoxVals(self):
        return self.paramFields, self.valFields

