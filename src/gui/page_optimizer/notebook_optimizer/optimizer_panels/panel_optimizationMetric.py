##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_optimizationMetric.py'
#   Class for dynamic scroll for detecting params
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 15, 2023
##--------------------------------------------------------------------\

import wx

import wx.lib.scrolledpanel as scrolled

import project.config.antennaCAT_config as c
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class OptimizationMetricPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(325,-1))
        self.parent = parent

        #feed in key and value arguments to the dynamic target scroll box
        # optimizerKeyArr = ["S₁₁        (dB)", "Gain    (dB)", "BW      (Hz)", "Directivity (dB)", "Efficiency"]
        # changing to S_11 bc of an encoding err exporting log file
        optimizerKeyArr = ["S_11        (dB)", "Gain    (dB)", "BW      (Hz)", "Directivity (dB)", "Efficiency"]
        optimizerTargetArr = ["-10", "3", "0", "0", "0"]

        self.defaultBoxWidth = 115
        self.metricFields = []  #names of metric (gain, s11)
        self.targetValFields=[] #value of detected parameters
        self.checkedVals = []

        boxOptimizer = wx.StaticBox(self, label="Optimizer Targets")

        self.scrolled_panel = scrolled.ScrolledPanel(boxOptimizer, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
       
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer, wx.EXPAND)

        boxOptimizerSizer = wx.BoxSizer(wx.VERTICAL)
        boxOptimizerSizer.AddSpacer(10)
        boxOptimizerSizer.Add(self.scrolled_panel, 1, wx.ALL|wx.EXPAND, border=10)
        boxOptimizer.SetSizer(boxOptimizerSizer)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(boxOptimizer, 1, wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(panelSizer)

        self.addRows( optimizerKeyArr, optimizerTargetArr)
    
    def clearRows(self):
        self.metricFields = []  #names of metric (gain, s11)
        self.targetValFields=[] #value of detected parameters
        self.checkedVals = []
        self.vSizer.Clear(True)
        hSizer=self.addLabelsToTop()
        self.vSizer.Add(hSizer, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout

    def addLabelsToTop(self):
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        lblParamName = wx.StaticText(self.scrolled_panel, label='  Metric ', size=(self.defaultBoxWidth, 20))
        lblParamValue= wx.StaticText(self.scrolled_panel, label= '|     Value', size=(self.defaultBoxWidth-20, 20))

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
            tcParam = wx.TextCtrl(self.scrolled_panel, value=t,  size=(self.defaultBoxWidth,-1), style=wx.TE_READONLY)

            vTxt = valTxt[ctr]
            tcVal= wx.TextCtrl(self.scrolled_panel, value=str(vTxt), size=(self.defaultBoxWidth-20,-1))

            cbUseVal = wx.CheckBox(self.scrolled_panel, label='select')
            cbUseVal.SetValue(False)

            self.metricFields.append(tcParam)
            self.targetValFields.append(tcVal)
            self.checkedVals.append(cbUseVal)

            hSizer.Add(tcParam, border=3)
            # hSizer.AddSpacer(3)
            hSizer.Add(tcVal, border=3)
            hSizer.AddSpacer(3)
            hSizer.Add(cbUseVal, border=7)
            self.vSizer.Add(hSizer, border=3)
            ctr=ctr+1
        self.scrolled_panel.SetSizer(self.vSizer)
        self.Layout()#force update for layout


    def getInputBoxVals(self):
        return self.metricFields, self.targetValFields, self.checkedVals
    

