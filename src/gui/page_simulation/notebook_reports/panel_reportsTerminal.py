##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_simulation/notebook_reports/panel_reportsTerminal.py'
#   Class for EM sim software terminal report settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx 

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ALTERNATE_COLORS = c.ALTERNATE_COLORS


class ReportsTerminal(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.reportList = []
        self.featuresList = []
        # self.functionsList = []

        # 'create terminal solution data report' menu
        boxReports = wx.StaticBox(self, label="Reports")
        boxTerminal = wx.StaticBox(boxReports)
        cbRect = wx.CheckBox(boxTerminal, id=10, label="Rectangular Plot")
        cbRect.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbRectStacked = wx.CheckBox(boxTerminal, id=11, label="Rectangular Stacked Plot")
        cbRectStacked.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbPolar = wx.CheckBox(boxTerminal, id=12, label="Polar Plot")
        cbPolar.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbTable = wx.CheckBox(boxTerminal, id=13, label="Data Table (default)")
        cbTable.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbSmith = wx.CheckBox(boxTerminal, id=14, label="Smith Chart")
        cbSmith.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        boxTerminal3D = wx.StaticBox(boxReports)
        cb3DRect = wx.CheckBox(boxTerminal3D, id=20, label="3D Rectangular Plot")
        cb3DRect.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cb3DRectBar = wx.CheckBox(boxTerminal3D, id=21, label="3D Rectangular Bar Plot")
        cb3DRectBar.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cb3DPolar = wx.CheckBox(boxTerminal3D, id=22, label="3D Polar Plot")
        cb3DPolar.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cb3DSphere = wx.CheckBox(boxTerminal3D, id=23, label="3D Spherical Plot")
        cb3DSphere.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        boxTerminalContour = wx.StaticBox(boxReports)
        cbRectContour = wx.CheckBox(boxTerminalContour, id=30, label="Rectangular Contour Plot")
        cbRectContour.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbSmithContour = wx.CheckBox(boxTerminalContour, id=31, label="Smith Contour Plot")
        cbSmithContour.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        #boxes for report details
        boxFeatures = wx.StaticBox(self, label="Features")
        boxCategory = wx.StaticBox(boxFeatures, label="Parameter Category")
        cbSParam = wx.CheckBox(boxCategory, id=51, label="Terminal S (dB)")
        cbSParam.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)
        cbZParam = wx.CheckBox(boxCategory, id=52, label="Terminal Z (real, imaginary)")
        cbZParam.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)

        # self.radio1 = wx.RadioButton(panel, label="A", pos=(20,40), style=wx.RB_GROUP)

        # boxFunction = wx.StaticBox(boxFeatures, label="Function")
        # cbDB = wx.CheckBox(boxFunction, id=61, label="dB")
        # cbDB.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbIM = wx.CheckBox(boxFunction, id=62, label="imaginary")
        # cbIM.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbRE = wx.CheckBox(boxFunction, id=63, label="real")
        # cbRE.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbMAG = wx.CheckBox(boxFunction, id=64, label="magnitude")
        # cbMAG.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)


        # sizers
        # terminal solution spacer
        boxTerminalSizer = wx.BoxSizer(wx.VERTICAL)
        boxTerminalSizer.AddSpacer(15)
        boxTerminalSizer.Add(cbRect, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalSizer.Add(cbRectStacked, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalSizer.Add(cbPolar, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalSizer.Add(cbTable, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalSizer.Add(cbSmith, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminal.SetSizer(boxTerminalSizer)
        #
        boxTerminal3DSizer = wx.BoxSizer(wx.VERTICAL)
        boxTerminal3DSizer.AddSpacer(15)
        boxTerminal3DSizer.Add(cb3DRect, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminal3DSizer.Add(cb3DRectBar, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminal3DSizer.Add(cb3DPolar, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminal3DSizer.Add(cb3DSphere, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminal3D.SetSizer(boxTerminal3DSizer)
        #
        boxTerminalContourSizer = wx.BoxSizer(wx.VERTICAL)
        boxTerminalContourSizer.AddSpacer(15)
        boxTerminalContourSizer.Add(cbRectContour, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalContourSizer.Add(cbSmithContour, 0, wx.ALL | wx.EXPAND, border=3)
        boxTerminalContour.SetSizer(boxTerminalContourSizer)
        #
        boxCategorySizer = wx.BoxSizer(wx.VERTICAL)
        boxCategorySizer.AddSpacer(15)
        boxCategorySizer.Add(cbSParam, 0, wx.ALL | wx.EXPAND, border=3)
        boxCategorySizer.Add(cbZParam, 0, wx.ALL | wx.EXPAND, border=3)
        boxCategory.SetSizer(boxCategorySizer)
        #
        # boxFunctionSizer = wx.BoxSizer(wx.VERTICAL)
        # boxFunctionSizer.AddSpacer(15)
        # boxFunctionSizer.Add(cbDB, 0, wx.ALL | wx.EXPAND, border=3)
        # boxFunctionSizer.Add(cbIM, 0, wx.ALL | wx.EXPAND, border=3)
        # boxFunctionSizer.Add(cbRE, 0, wx.ALL | wx.EXPAND, border=3)
        # boxFunctionSizer.Add(cbMAG, 0, wx.ALL | wx.EXPAND, border=3) 
        # boxFunction.SetSizer(boxFunctionSizer)
        #top row sizer
        topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRowSizer.AddSpacer(5)
        topRowSizer.Add(boxTerminal, 0, wx.ALL | wx.EXPAND, border=3)
        topRowSizer.Add(boxTerminal3D, 0, wx.ALL | wx.EXPAND, border=3)
        topRowSizer.Add(boxTerminalContour, 0, wx.ALL | wx.EXPAND, border=3)
        boxReportsSizer = wx.BoxSizer(wx.VERTICAL)
        boxReportsSizer.AddSpacer(10)
        boxReportsSizer.Add(topRowSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxReports.SetSizer(boxReportsSizer)
        #bottom row sizer
        bottomRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomRowSizer.AddSpacer(5)
        bottomRowSizer.Add(boxCategory, 0, wx.ALL | wx.EXPAND, border=3)
        # bottomRowSizer.Add(boxFunction, 0, wx.ALL | wx.EXPAND, border=3)
        boxFeaturesSizer = wx.BoxSizer(wx.VERTICAL)
        boxFeaturesSizer.AddSpacer(10)
        boxFeaturesSizer.Add(bottomRowSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxFeatures.SetSizer(boxFeaturesSizer)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxReports, 1, wx.ALL | wx.EXPAND, border=5)
        # pageSizer.Add(topRowSizer, 1, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxFeatures, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    def cbSelectReportList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            #print(evt.GetEventObject().GetLabel())
            self.reportList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.reportList.remove(evt.GetEventObject().GetLabel())

    def cbSelectFeaturesList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            self.featuresList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.featuresList.remove(evt.GetEventObject().GetLabel())

    # def cbSelectFunctionsList(self, evt):
    #     # add report types to list
    #     if evt.GetEventObject().IsChecked():
    #         self.functionsList.append(evt.GetEventObject().GetLabel())
    #     elif evt.GetEventObject().IsChecked() == False:
    #         self.functionsList.remove(evt.GetEventObject().GetLabel())


    def getReportList(self):
        return self.reportList, self.featuresList #, self.functionsList

    def applyLoadedProjectSettings(self, PC):
        pass