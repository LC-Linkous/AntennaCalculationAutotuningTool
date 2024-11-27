##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_simulation/notebook_reports/panel_reportsFarFields.py'
#   Class for EM sim software far field report settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ALTERNATE_COLORS = c.ALTERNATE_COLORS

class ReportsFarField(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.reportList = []
        self.featuresList = []
        # self.functionsList = []


        # 'create faf field data report' menu
        boxReports = wx.StaticBox(self, label="Reports")
        boxFarField = wx.StaticBox(boxReports)
        cbFFRect = wx.CheckBox(boxFarField, id=10, label="Rectangular Plot")
        cbFFRect.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFFRectStacked = wx.CheckBox(boxFarField, id=11, label="Rectangular Stacked Plot")
        cbFFRectStacked.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFFRadiation = wx.CheckBox(boxFarField, id=12, label="Radiation Pattern")
        cbFFRadiation.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFFTable = wx.CheckBox(boxFarField, id=13, label="Data Table (default)")
        cbFFTable.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        boxFarField3D = wx.StaticBox(boxReports)
        cbFF3DRect = wx.CheckBox(boxFarField3D, id=10, label="3D Rectangular Plot")
        cbFF3DRect.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFF3DRectBar = wx.CheckBox(boxFarField3D, id=11, label="3D Rectangular Bar Plot")
        cbFF3DRectBar.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFF3DPolar = wx.CheckBox(boxFarField3D, id=12, label="3D Polar Plot")
        cbFF3DPolar.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)
        cbFF3DSphere = wx.CheckBox(boxFarField3D, id=13, label="3D Spherical Plot")
        cbFF3DSphere.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        boxFarFieldContour = wx.StaticBox(boxReports)
        cbFFRectContour = wx.CheckBox(boxFarFieldContour, id=10, label="Rectangular Contour Plot")
        cbFFRectContour.Bind(wx.EVT_CHECKBOX, self.cbSelectReportList)

        #boxes for report details
        boxFeatures = wx.StaticBox(self, label="Features")
        boxGain = wx.StaticBox(boxFeatures, label="Gain (dB)")
        cbGainTotal = wx.CheckBox(boxGain, id=31, label="Gain Total")
        cbGainTotal.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)
        cbGainPhi = wx.CheckBox(boxGain, id=32, label="Gain Phi")
        cbGainPhi.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)
        cbGainTheta = wx.CheckBox(boxGain, id=33, label="Gain Theta")
        cbGainTheta.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)

        
        boxDirectivity = wx.StaticBox(boxFeatures, label="Directivity (dB)")
        cbDirTotal = wx.CheckBox(boxDirectivity, id=41, label="Directivity Total")
        cbDirTotal.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)
        cbDirPhi = wx.CheckBox(boxDirectivity, id=42, label="Directivity Phi")
        cbDirPhi.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)
        cbDirTheta = wx.CheckBox(boxDirectivity, id=43, label="Directivity Theta")
        cbDirTheta.Bind(wx.EVT_CHECKBOX, self.cbSelectFeaturesList)

        
        # boxFunction = wx.StaticBox(boxFeatures, label="Function")
        # cbDB = wx.CheckBox(boxFunction, id=51, label="dB")
        # cbDB.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbIM = wx.CheckBox(boxFunction, id=52, label="imaginary")
        # cbIM.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbRE = wx.CheckBox(boxFunction, id=53, label="real")
        # cbRE.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)
        # cbMAG = wx.CheckBox(boxFunction, id=54, label="magnitude")
        # cbMAG.Bind(wx.EVT_CHECKBOX, self.cbSelectFunctionsList)


        boxFarFieldSizer = wx.BoxSizer(wx.VERTICAL)
        boxFarFieldSizer.AddSpacer(15)
        boxFarFieldSizer.Add(cbFFRect, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarFieldSizer.Add(cbFFRectStacked, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarFieldSizer.Add(cbFFRadiation, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarFieldSizer.Add(cbFFTable, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarField.SetSizer(boxFarFieldSizer)
        #
        boxFarField3DSizer = wx.BoxSizer(wx.VERTICAL)
        boxFarField3DSizer.AddSpacer(15)
        boxFarField3DSizer.Add(cbFF3DRect, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarField3DSizer.Add(cbFF3DRectBar, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarField3DSizer.Add(cbFF3DPolar, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarField3DSizer.Add(cbFF3DSphere, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarField3D.SetSizer(boxFarField3DSizer)
        #
        boxFarFieldContourSizer = wx.BoxSizer(wx.VERTICAL)
        boxFarFieldContourSizer.AddSpacer(15)
        boxFarFieldContourSizer.Add(cbFFRectContour, 0, wx.ALL | wx.EXPAND, border=3)
        boxFarFieldContour.SetSizer(boxFarFieldContourSizer)
        #
        boxGainSizer = wx.BoxSizer(wx.VERTICAL)
        boxGainSizer.AddSpacer(15)
        boxGainSizer.Add(cbGainTotal, 0, wx.ALL | wx.EXPAND, border=3)
        boxGainSizer.Add(cbGainPhi, 0, wx.ALL | wx.EXPAND, border=3)
        boxGainSizer.Add(cbGainTheta, 0, wx.ALL | wx.EXPAND, border=3)
        boxGain.SetSizer(boxGainSizer)
        #
        boxDirectivitySizer = wx.BoxSizer(wx.VERTICAL)
        boxDirectivitySizer.AddSpacer(15)
        boxDirectivitySizer.Add(cbDirTotal, 0, wx.ALL | wx.EXPAND, border=3)
        boxDirectivitySizer.Add(cbDirPhi, 0, wx.ALL | wx.EXPAND, border=3)
        boxDirectivitySizer.Add(cbDirTheta, 0, wx.ALL | wx.EXPAND, border=3)
        boxDirectivity.SetSizer(boxDirectivitySizer)
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
        topRowSizer.Add(boxFarField, 0, wx.ALL | wx.EXPAND, border=3)
        topRowSizer.Add(boxFarField3D, 0, wx.ALL | wx.EXPAND, border=3)
        topRowSizer.Add(boxFarFieldContour, 0, wx.ALL | wx.EXPAND, border=3)
        boxReportsSizer = wx.BoxSizer(wx.VERTICAL)
        boxReportsSizer.AddSpacer(10)
        boxReportsSizer.Add(topRowSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxReports.SetSizer(boxReportsSizer)
        #bottom row sizer
        bottomRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomRowSizer.Add(boxGain, 0, wx.ALL | wx.EXPAND, border=3)
        bottomRowSizer.Add(boxDirectivity, 0, wx.ALL | wx.EXPAND, border=3)
        # bottomRowSizer.Add(boxFunction, 0, wx.ALL | wx.EXPAND, border=3)
        boxFeaturesSizer = wx.BoxSizer(wx.VERTICAL)
        boxFeaturesSizer.AddSpacer(10)
        boxFeaturesSizer.Add(bottomRowSizer, 0, wx.ALL | wx.EXPAND, border=3)
        boxFeatures.SetSizer(boxFeaturesSizer)


        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxReports, 1, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxFeatures, 1, wx.ALL | wx.EXPAND, border=5)
        # pageSizer.Add(boxFarField, 1, wx.ALL | wx.EXPAND, border=5)
        # pageSizer.Add(boxFarField3D, 1, wx.ALL | wx.EXPAND, border=5)
        # pageSizer.Add(boxFarFieldContour, 1, wx.ALL | wx.EXPAND, border=5)
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