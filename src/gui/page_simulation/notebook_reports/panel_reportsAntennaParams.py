##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_simulation/notebook_reports/panel_reportsAntennaParams.py'
#   Class for EM sim software other report settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx 

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ALTERNATE_COLORS = c.ALTERNATE_COLORS

class ReportsAntennaParams(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.antennaParametersList = []

        boxAntennaParams = wx.StaticBox(self, label="Data Table")        
        cbPeakDir = wx.CheckBox(boxAntennaParams, id=10, label="Peak Directivity (dB)")
        cbPeakDir.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbPeakGain = wx.CheckBox(boxAntennaParams, id=11, label="Peak Gain (dB)")
        cbPeakGain.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbRadEff = wx.CheckBox(boxAntennaParams, id=12, label="Radiation Efficiency")
        cbRadEff.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbTotalEff = wx.CheckBox(boxAntennaParams, id=12, label="Total Efficiency")
        cbTotalEff.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbRadPower = wx.CheckBox(boxAntennaParams, id=10, label="Radiated Power (dB)")
        cbRadPower.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbIncidentPower = wx.CheckBox(boxAntennaParams, id=10, label="Incident Power (dB)")
        cbIncidentPower.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbBeamArea = wx.CheckBox(boxAntennaParams, id=11, label="Beam Area")
        cbBeamArea.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)
        cbFrontToBack = wx.CheckBox(boxAntennaParams, id=12, label="Front To Back Ratio")
        cbFrontToBack.Bind(wx.EVT_CHECKBOX, self.cbSelectAntennaParameterFeaturesList)

        #sizers
        leftSizer = wx.BoxSizer(wx.VERTICAL)      
        leftSizer.AddSpacer(15)  
        leftSizer.Add(cbPeakDir, 0, wx.ALL | wx.EXPAND, border=3)        
        leftSizer.Add(cbPeakGain, 0, wx.ALL | wx.EXPAND, border=3)        
        leftSizer.Add(cbRadEff, 0, wx.ALL | wx.EXPAND, border=3)  
        leftSizer.Add(cbTotalEff, 0, wx.ALL | wx.EXPAND, border=3) 
        rightSizer = wx.BoxSizer(wx.VERTICAL)      
        rightSizer.AddSpacer(15)  
        rightSizer.Add(cbRadPower, 0, wx.ALL | wx.EXPAND, border=3)        
        rightSizer.Add(cbIncidentPower, 0, wx.ALL | wx.EXPAND, border=3)        
        rightSizer.Add(cbBeamArea, 0, wx.ALL | wx.EXPAND, border=3)  
        rightSizer.Add(cbFrontToBack, 0, wx.ALL | wx.EXPAND, border=3) 


        boxAntennaParamsSizer = wx.BoxSizer(wx.HORIZONTAL)     
        boxAntennaParamsSizer.Add(leftSizer, 0, wx.ALL | wx.EXPAND, border=3)        
        boxAntennaParamsSizer.Add(rightSizer, 0, wx.ALL | wx.EXPAND, border=3)        
        boxAntennaParams.SetSizer(boxAntennaParamsSizer)
   

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxAntennaParams, 0, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    def cbSelectAntennaParameterFeaturesList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            self.antennaParametersList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.antennaParametersList.remove(evt.GetEventObject().GetLabel())


    def getReportList(self):
        return self.antennaParametersList


    def applyLoadedProjectSettings(self, PC):
        pass

