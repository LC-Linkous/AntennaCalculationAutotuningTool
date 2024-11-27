##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/gui/gui_main/panel_buttonMenu.py'
#   Class for GUI layout and basic functionality - sidebar of buttons
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx
import project.config.antennaCAT_config as c

# default frame/panel sizes and visuals
#CHANGE IN CONSTANTS.PY FOR CONSISTENCY ACROSS PROJECT
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
SIDEBAR_COLOR = c.SIDEBAR_COLOR
ANTENNACAT_LOGO_FILE = c.ANTENNACAT_LOGO_FILE

class ButtonMenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(120, -1))
        self.parent = parent
        self.SetBackgroundColour(SIDEBAR_COLOR)

        #top corner panel
        top_panel = wx.Panel(self, wx.ID_ANY)
        top_panel.SetBackgroundColour(SIDEBAR_COLOR)
        #cat image
        imgFile = ANTENNACAT_LOGO_FILE
        bMap = wx.Bitmap(imgFile, wx.BITMAP_TYPE_PNG)
        img = wx.Bitmap.ConvertToImage(bMap)
        img = img.Scale(110, 200, wx.IMAGE_QUALITY_HIGH)
        antennaCATLogo = wx.StaticBitmap(top_panel, wx.ID_ANY)
        antennaCATLogo.SetBitmap(img.ConvertToBitmap())        

        #panel with sidebar buttons
        button_panel = wx.Panel(self, wx.ID_ANY)
        button_panel.SetBackgroundColour(SIDEBAR_COLOR)
        #buttons
        font = wx.Font(14, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        btnDesign = wx.Button(button_panel, id=1, label='Design', style=wx.BU_LEFT)
        btnDesign.SetFont(font)
        btnDesign.Bind(wx.EVT_BUTTON, self.btnClick)
        btnSimulate = wx.Button(button_panel, id=2, label='Simulate', style=wx.BU_LEFT)
        btnSimulate.SetFont(font)
        btnSimulate.Bind(wx.EVT_BUTTON, self.btnClick)
        btnBatch = wx.Button(button_panel, id=3, label='Batch', style=wx.BU_LEFT)
        btnBatch.SetFont(font)
        btnBatch.Bind(wx.EVT_BUTTON, self.btnClick)
        btnSettings = wx.Button(button_panel, id=6, label='Settings', style=wx.BU_LEFT)
        btnSettings.SetFont(font)
        btnSettings.Bind(wx.EVT_BUTTON, self.btnClick)
        btnOptimizer = wx.Button(button_panel, id=9, label='Optimizer', style=wx.BU_LEFT)
        btnOptimizer.SetFont(font)
        btnOptimizer.Bind(wx.EVT_BUTTON, self.btnClick)

        #button sizer
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(btnDesign, 0, wx.ALL|wx.EXPAND, border=5)
        buttonSizer.Add(btnSimulate, 0, wx.ALL|wx.EXPAND, border=5)
        buttonSizer.Add(btnBatch, 0, wx.ALL|wx.EXPAND, border=5)
        buttonSizer.Add(btnOptimizer, 0, wx.ALL|wx.EXPAND, border=5)
        buttonSizer.Add(btnSettings, 0, wx.ALL|wx.EXPAND, border=5)
        button_panel.SetSizer(buttonSizer)

        #panel sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddSpacer(10)
        mainSizer.Add(top_panel, 1, wx.ALL|wx.EXPAND, border=5)
        mainSizer.AddSpacer(10)
        mainSizer.Add(button_panel, 3, wx.ALL, border=5)
        self.SetSizer(mainSizer)

    def btnClick(self, evt):
        id = evt.GetEventObject().GetId()
        if id == 1: # design panel
            self.btnDesignClicked()

        elif id == 2: # simulation panel
            self.btnSimulationClicked()

        elif id == 3: # batch panel
            self.btnBatchClicked()

        elif id == 6: #settings panel
            self.btnSettingsClicked()

        elif id == 9: #Optimizer panel
            self.btnOptimizerClicked()
        
    
#individual button events so they can be triggered programmatically
    def btnProjectClicked(self):
        self.parent.panel_mainUI.panel_project.Show()
        self.parent.panel_mainUI.panel_design.Hide()
        self.parent.panel_mainUI.panel_simulation.Hide()
        self.parent.panel_mainUI.panel_batch.Hide()
        self.parent.panel_mainUI.panel_settings.Hide()
        self.parent.panel_mainUI.panel_optimizer.Hide()
        self.parent.Layout() 

    def btnDesignClicked(self):
        self.parent.panel_mainUI.panel_project.Hide()
        self.parent.panel_mainUI.panel_design.Show()
        self.parent.panel_mainUI.panel_simulation.Hide()
        self.parent.panel_mainUI.panel_batch.Hide()
        self.parent.panel_mainUI.panel_settings.Hide()
        self.parent.panel_mainUI.panel_optimizer.Hide()
        self.parent.Layout() 

    def btnSimulationClicked(self):
        self.parent.panel_mainUI.panel_project.Hide()
        self.parent.panel_mainUI.panel_design.Hide()
        self.parent.panel_mainUI.panel_simulation.Show()
        self.parent.panel_mainUI.panel_simulation.updateSimulationSettingsBoxes()
        self.parent.panel_mainUI.panel_batch.Hide()
        self.parent.panel_mainUI.panel_settings.Hide()
        self.parent.panel_mainUI.panel_optimizer.Hide()
        self.parent.Layout() 


    def btnBatchClicked(self):
        self.parent.panel_mainUI.panel_project.Hide()
        self.parent.panel_mainUI.panel_design.Hide()
        self.parent.panel_mainUI.panel_simulation.Hide()
        self.parent.panel_mainUI.panel_batch.Show()
        self.parent.panel_mainUI.panel_settings.Hide()
        self.parent.panel_mainUI.panel_optimizer.Hide()
        self.parent.Layout() 

    def btnSettingsClicked(self):
        self.parent.panel_mainUI.panel_project.Hide()
        self.parent.panel_mainUI.panel_design.Hide()
        self.parent.panel_mainUI.panel_simulation.Hide()
        self.parent.panel_mainUI.panel_batch.Hide()
        self.parent.panel_mainUI.panel_settings.Show()
        self.parent.panel_mainUI.panel_optimizer.Hide()
        self.parent.Layout() 

    def btnOptimizerClicked(self):
        self.parent.panel_mainUI.panel_project.Hide()
        self.parent.panel_mainUI.panel_design.Hide()
        self.parent.panel_mainUI.panel_simulation.Hide()
        self.parent.panel_mainUI.panel_batch.Hide()
        self.parent.panel_mainUI.panel_settings.Hide()
        self.parent.panel_mainUI.panel_optimizer.Show()
        self.parent.panel_mainUI.panel_optimizer.updateSimulationSettingsBoxes()
        self.parent.Layout() 
