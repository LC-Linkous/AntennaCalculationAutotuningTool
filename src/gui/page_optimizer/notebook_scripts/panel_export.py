##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_optimizer/notebook_scripts/panel_export.py'
#   Class for export script settings for batch page
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 6, 2023
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ExportPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
       
        # splitting script options 
        boxScripts = wx.StaticBox(self, label='Split Scripts')
        ### style = wx.RB_GROUP flag causes all following to be part of 1 group
        self.rbtnSingle = wx.RadioButton(boxScripts,11, label = 'Use Single Script', style = wx.RB_GROUP) 
        self.rbtnMultiple = wx.RadioButton(boxScripts,22, label = 'Use Multiple Scripts') 
        self.stNumScripts = wx.StaticText(boxScripts, style=wx.ALIGN_LEFT,  label="Num Scripts:")
        self.spinText = wx.TextCtrl(boxScripts, value="1")
        self.spinMultiple = wx.SpinButton(boxScripts, style=wx.SP_VERTICAL, size=(-1,25))
        self.spinMultiple.Bind(wx.EVT_SPIN, self.spinScripts)
        self.spinMultiple.SetRange(1, 5)
        self.spinMultiple.SetValue(1)

        self.btnExport = wx.Button(self, label="Export Scripts")
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)

        # liscense options sizer
        middleSizer = wx.BoxSizer(wx.VERTICAL)
        middleSizer.AddSpacer(15)
        middleSizer.Add(self.rbtnSingle, 0, wx.ALL, border=5)
        middleSizer.Add(self.rbtnMultiple, 0, wx.ALL, border=5)
        middleSizer.AddSpacer(5)
        numLicenseSizer = wx.BoxSizer(wx.HORIZONTAL)
        numLicenseSizer.AddSpacer(15)
        numLicenseSizer.Add(self.stNumScripts, 0, wx.ALL, border=5)
        numLicenseSizer.Add(self.spinText, 0, wx.ALL, border=0)
        numLicenseSizer.Add(self.spinMultiple, 0, wx.ALL, border=0)
        middleSizer.Add(numLicenseSizer, 0, wx.ALL|wx.EXPAND, border=0)
        boxScripts.SetSizer(middleSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.AddSpacer(10)
        pageSizer.Add(boxScripts, 1, wx.ALL|wx.EXPAND, border=5)
        pageSizer.AddStretchSpacer()
        pageSizer.Add(self.btnExport, 0, wx.ALL|wx.ALIGN_RIGHT, border=10)
        self.SetSizer(pageSizer)

    def setMaxSpin(self, nMax):
        # TO DO set this based on user input on settings page/PC settings
        self.spinMultiple.SetRange(1, nMax)


    def spinScripts(self, evt=None):
        self.spinText.SetValue(str(evt.GetPosition()))


    def btnExportClicked(self, evt=None):
        self.parent.btnExportClicked(evt)

        
    def getSettings(self):
        #returns bool, float
        useSingleBool = self.rbtnSingle.GetValue()
        return useSingleBool, float(self.spinText.GetValue())
    

    def applyLoadedProjectSettings(self, PC):
        pass