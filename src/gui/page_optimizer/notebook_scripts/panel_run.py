##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_optimizer/notebook_scripts/panel_run.py'
#   Class for run script settings for batch page
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 6, 2023
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class RunPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # options for looping
        ## batch just keeps the window open to faster edit/run/save
        boxRunOptions = wx.StaticBox(self, label='Run Options')
        self.rbtnOpenRun = wx.RadioButton(boxRunOptions, label = 'Keep Window Open While Script Running') 
        
        # if using multiple licenses 
        boxLicenses = wx.StaticBox(self, label='License Options')
        ### style = wx.RB_GROUP flag causes all following to be part of 1 group
        self.rbtnSingle = wx.RadioButton(boxLicenses,11, label = 'Use Single License', style = wx.RB_GROUP) 
        self.rbtnMultiple = wx.RadioButton(boxLicenses,22, label = 'Use Multiple Licenses') 
        self.stNumLicenses = wx.StaticText(boxLicenses, style=wx.ALIGN_LEFT,  label="Num Licenses:")
        self.spinText = wx.TextCtrl(boxLicenses, value="1")
        self.spinMultiple = wx.SpinButton(boxLicenses, style=wx.SP_VERTICAL, size=(-1,25))
        self.spinMultiple.Bind(wx.EVT_SPIN, self.spinLicenses)
        self.spinMultiple.SetRange(1, 5)
        self.spinMultiple.SetValue(1)

        self.btnRun = wx.Button(self, label="Run Simulations")
        self.btnRun.Bind(wx.EVT_BUTTON, self.btnRunClicked)

        # run options sizer
        runSizer = wx.BoxSizer(wx.VERTICAL)
        runSizer.AddSpacer(15)
        runSizer.Add(self.rbtnOpenRun, 0, wx.ALL, border=5)
        boxRunOptions.SetSizer(runSizer)

        # script split options
        middleSizer = wx.BoxSizer(wx.VERTICAL)
        middleSizer.AddSpacer(15)
        middleSizer.Add(self.rbtnSingle, 0, wx.ALL, border=5)
        middleSizer.Add(self.rbtnMultiple, 0, wx.ALL, border=5)
        middleSizer.AddSpacer(5)
        numLicenseSizer = wx.BoxSizer(wx.HORIZONTAL)
        numLicenseSizer.AddSpacer(15)
        numLicenseSizer.Add(self.stNumLicenses, 0, wx.ALL, border=5)
        numLicenseSizer.Add(self.spinText, 0, wx.ALL, border=0)
        numLicenseSizer.Add(self.spinMultiple, 0, wx.ALL, border=0)
        middleSizer.Add(numLicenseSizer, 0, wx.ALL|wx.EXPAND, border=0)
        boxLicenses.SetSizer(middleSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.AddSpacer(10)
        pageSizer.Add(boxRunOptions, 1, wx.ALL|wx.EXPAND, border=5)
        pageSizer.AddSpacer(10)
        pageSizer.Add(boxLicenses, 0, wx.ALL|wx.EXPAND, border=5)
        pageSizer.AddStretchSpacer()
        pageSizer.Add(self.btnRun, 0, wx.ALL|wx.ALIGN_RIGHT, border=10)
        self.SetSizer(pageSizer)


    def spinLicenses(self, evt=None):
        self.spinText.SetValue(str(evt.GetPosition()))


    def btnRunClicked(self, evt=None):
        self.parent.btnRunClicked(evt)


    def getSettings(self):
        #returns bool, float
        useSingleBool = self.rbtnSingle.GetValue()
        return useSingleBool, float(self.spinText.GetValue())

    def applyLoadedProjectSettings(self, PC):
        pass