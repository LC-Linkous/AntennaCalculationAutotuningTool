##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_simulation/notebook_reports/panel_dataTable.py'
#   Class for EM sim software other report settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx 

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
ALTERNATE_COLORS = c.ALTERNATE_COLORS

class ReportsDataTable(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.modalFeaturesList = []
        # self.modalFunctionsList = []
        self.terminalFeaturesList = []
        # self.terminalFunctionsList = []
        self.farfieldFeaturesList = []

        # modal
        boxModal= wx.StaticBox(self, label="Modal Solution")
        # features
        boxModalFeatures= wx.StaticBox(boxModal, label="Features")        
        cbMSVariables = wx.CheckBox(boxModalFeatures, id=10, label="Variables")
        cbMSVariables.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFeaturesList)
        cbMSSParams = wx.CheckBox(boxModalFeatures, id=11, label="S Parameters (dB)")
        cbMSSParams.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFeaturesList)
        cbMSZParams = wx.CheckBox(boxModalFeatures, id=12, label="Z Parameters (real, imaginary)")
        cbMSZParams.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFeaturesList)

        # functions
        # boxModalFunctions= wx.StaticBox(boxModal, label="Functions")  
        # cbMSNone = wx.CheckBox(boxModalFunctions, id=21, label="none")
        # cbMSNone.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFunctionList)     
        # cbMSDB = wx.CheckBox(boxModalFunctions, id=22, label="dB")
        # cbMSDB.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFunctionList)
        # cbMSIM = wx.CheckBox(boxModalFunctions, id=23, label="imaginary")
        # cbMSIM.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFunctionList)
        # cbMSRE = wx.CheckBox(boxModalFunctions, id=24, label="real")
        # cbMSRE.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFunctionList)
        # cbMSMAG = wx.CheckBox(boxModalFunctions, id=25, label="magnitude")
        # cbMSMAG.Bind(wx.EVT_CHECKBOX, self.cbSelectModalFunctionList)

        # terminal
        boxTerminal= wx.StaticBox(self, label="Terminal Solution")
        # features
        boxTerminalFeatures= wx.StaticBox(boxTerminal, label="Features")
        cbTSVariables = wx.CheckBox(boxTerminalFeatures, id=30, label="Variables")
        cbTSVariables.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFeaturesList)  
        cbTSSParams = wx.CheckBox(boxTerminalFeatures, id=31, label="S Parameters (dB)")
        cbTSSParams.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFeaturesList)  
        cbTSZParams = wx.CheckBox(boxTerminalFeatures, id=32, label="Z Parameters (real, imaginary)")
        cbTSZParams.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFeaturesList)  
        # # functions
        # boxTerminalFunctions= wx.StaticBox(boxTerminal, label="Functions")
        # cbTSNone = wx.CheckBox(boxTerminalFunctions, id=41, label="none")
        # cbTSNone.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFunctionList)     
        # cbTSDB = wx.CheckBox(boxTerminalFunctions, id=42, label="dB")
        # cbTSDB.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFunctionList)
        # cbTSIM = wx.CheckBox(boxTerminalFunctions, id=43, label="imaginary")
        # cbTSIM.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFunctionList)
        # cbTSRE = wx.CheckBox(boxTerminalFunctions, id=44, label="real")
        # cbTSRE.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFunctionList)
        # cbTSMAG = wx.CheckBox(boxTerminalFunctions, id=45, label="magnitude")
        # cbTSMAG.Bind(wx.EVT_CHECKBOX, self.cbSelectTerminalFunctionList)

        # far field
        boxFarField= wx.StaticBox(self, label="Far Field")
        # features
        # boxFFFeatures = wx.StaticBox(boxFarField, label="Features")
        boxFFVariables = wx.StaticBox(boxFarField, label="Variables")
        cbFFVariables = wx.CheckBox(boxFFVariables, id=51, label="Controllable Parameters")
        cbFFVariables.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)
        boxFFGain = wx.StaticBox(boxFarField, label="Gain (dB)")
        cbFFGainTotal = wx.CheckBox(boxFFGain, id=61, label="Gain Total")
        cbFFGainTotal.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)
        cbFFGainPhi = wx.CheckBox(boxFFGain, id=62, label="Gain Phi")
        cbFFGainPhi.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)
        cbFFGainTheta = wx.CheckBox(boxFFGain, id=61, label="Gain Theta")
        cbFFGainTheta.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)       
        boxFFDirectivity = wx.StaticBox(boxFarField, label="Directivity (dB)")
        cbFFDirTotal = wx.CheckBox(boxFFDirectivity, id=71, label="Directivity Total")
        cbFFDirTotal.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)
        cbFFDirPhi = wx.CheckBox(boxFFDirectivity, id=72, label="Directivity Phi")
        cbFFDirPhi.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)
        cbFFDirTheta = wx.CheckBox(boxFFDirectivity, id=73, label="Directivity Theta")
        cbFFDirTheta.Bind(wx.EVT_CHECKBOX, self.cbSelectFarFieldFeaturesList)

        #modal sizers
        boxModalFeaturesSizer = wx.BoxSizer(wx.VERTICAL)      
        boxModalFeaturesSizer.AddSpacer(15)  
        boxModalFeaturesSizer.Add(cbMSVariables, 0, wx.ALL | wx.EXPAND, border=3)        
        boxModalFeaturesSizer.Add(cbMSSParams, 0, wx.ALL | wx.EXPAND, border=3)        
        boxModalFeaturesSizer.Add(cbMSZParams, 0, wx.ALL | wx.EXPAND, border=3)  
        boxModalFeatures.SetSizer(boxModalFeaturesSizer)
        boxModalFunctionsSizer = wx.BoxSizer(wx.VERTICAL)      
        # boxModalFunctionsSizer.AddSpacer(15)  
        # boxModalFunctionsSizer.Add(cbMSNone, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxModalFunctionsSizer.Add(cbMSDB, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxModalFunctionsSizer.Add(cbMSIM, 0, wx.ALL | wx.EXPAND, border=3)  
        # boxModalFunctionsSizer.Add(cbMSRE, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxModalFunctionsSizer.Add(cbMSMAG, 0, wx.ALL | wx.EXPAND, border=3) 
        # boxModalFunctions.SetSizer(boxModalFunctionsSizer)
        modalTopRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        modalTopRowSizer.Add(boxModalFeatures, 0, wx.ALL | wx.EXPAND, border=5) 
        # modalTopRowSizer.Add(boxModalFunctions, 0, wx.ALL | wx.EXPAND, border=5) 
        boxModalSizer = wx.BoxSizer(wx.VERTICAL)
        boxModalSizer.AddSpacer(15)
        boxModalSizer.Add(modalTopRowSizer, 0, wx.ALL | wx.EXPAND, border=0)
        boxModal.SetSizer(boxModalSizer)

        # terminal sizers        
        boxTerminalFeaturesSizer = wx.BoxSizer(wx.VERTICAL) 
        boxTerminalFeaturesSizer.AddSpacer(15)       
        boxTerminalFeaturesSizer.Add(cbTSVariables, 0, wx.ALL | wx.EXPAND, border=3)        
        boxTerminalFeaturesSizer.Add(cbTSSParams, 0, wx.ALL | wx.EXPAND, border=3)        
        boxTerminalFeaturesSizer.Add(cbTSZParams, 0, wx.ALL | wx.EXPAND, border=3)  
        boxTerminalFeatures.SetSizer(boxTerminalFeaturesSizer)
        # boxTerminalFunctionsSizer = wx.BoxSizer(wx.VERTICAL)    
        # boxTerminalFunctionsSizer.AddSpacer(15)    
        # boxTerminalFunctionsSizer.Add(cbTSNone, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxTerminalFunctionsSizer.Add(cbTSDB, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxTerminalFunctionsSizer.Add(cbTSIM, 0, wx.ALL | wx.EXPAND, border=3)  
        # boxTerminalFunctionsSizer.Add(cbTSRE, 0, wx.ALL | wx.EXPAND, border=3)        
        # boxTerminalFunctionsSizer.Add(cbTSMAG, 0, wx.ALL | wx.EXPAND, border=3) 
        # boxTerminalFunctions.SetSizer(boxTerminalFunctionsSizer)
        terminalTopRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        terminalTopRowSizer.Add(boxTerminalFeatures, 0, wx.ALL | wx.EXPAND, border=5) 
        # terminalTopRowSizer.Add(boxTerminalFunctions, 0, wx.ALL | wx.EXPAND, border=5) 
        boxTerminalSizer = wx.BoxSizer(wx.VERTICAL)
        boxTerminalSizer.AddSpacer(15)
        boxTerminalSizer.Add(terminalTopRowSizer, 0, wx.ALL | wx.EXPAND, border=0)
        boxTerminal.SetSizer(boxTerminalSizer)

        # far field sizer
        boxFFVariablesSizer = wx.BoxSizer(wx.VERTICAL)
        boxFFVariablesSizer.AddSpacer(15)
        boxFFVariablesSizer.Add(cbFFVariables, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFVariables.SetSizer(boxFFVariablesSizer)
        boxFFGainSizer = wx.BoxSizer(wx.VERTICAL)
        boxFFGainSizer.AddSpacer(15)
        boxFFGainSizer.Add(cbFFGainTotal, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFGainSizer.Add(cbFFGainPhi, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFGainSizer.Add(cbFFGainTheta, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFGain.SetSizer(boxFFGainSizer)
        boxFFDirectivitySizer = wx.BoxSizer(wx.VERTICAL)
        boxFFDirectivitySizer.AddSpacer(15)
        boxFFDirectivitySizer.Add(cbFFDirTotal, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFDirectivitySizer.Add(cbFFDirPhi, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFDirectivitySizer.Add(cbFFDirTheta, 0, wx.ALL | wx.EXPAND, border=3)
        boxFFDirectivity.SetSizer(boxFFDirectivitySizer)
        FFFeaturesTopRow = wx.BoxSizer(wx.HORIZONTAL)
        FFFeaturesTopRow.Add(boxFFVariables, 0, wx.ALL | wx.EXPAND, border=5) 
        FFFeaturesTopRow.Add(boxFFGain, 0, wx.ALL | wx.EXPAND, border=5) 
        FFFeaturesTopRow.Add(boxFFDirectivity, 0, wx.ALL | wx.EXPAND, border=5) 
        boxFarFieldSizer = wx.BoxSizer(wx.VERTICAL)
        boxFarFieldSizer.AddSpacer(15)
        boxFarFieldSizer.Add(FFFeaturesTopRow, 0, wx.ALL | wx.EXPAND, border=0) 
        boxFarField.SetSizer(boxFarFieldSizer)
        
        #
        topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRowSizer.Add(boxModal, 1, wx.ALL | wx.EXPAND, border=5)
        topRowSizer.Add(boxTerminal, 1, wx.ALL | wx.EXPAND, border=5)

        bottomRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomRowSizer.Add(boxFarField, 1, wx.ALL | wx.EXPAND, border=0)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(topRowSizer, 1, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(bottomRowSizer, 1, wx.ALL | wx.EXPAND, border=5)
        # pageSizer.Add(boxFarField, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    def cbSelectModalFeaturesList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            self.modalFeaturesList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.modalFeaturesList.remove(evt.GetEventObject().GetLabel())

    # def cbSelectModalFunctionList(self, evt):
    #     # add report types to list
    #     if evt.GetEventObject().IsChecked():
    #         self.modalFunctionsList.append(evt.GetEventObject().GetLabel())
    #     elif evt.GetEventObject().IsChecked() == False:
    #         self.modalFunctionsList.remove(evt.GetEventObject().GetLabel())

    def cbSelectTerminalFeaturesList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            self.terminalFeaturesList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.terminalFeaturesList.remove(evt.GetEventObject().GetLabel())

    # def cbSelectTerminalFunctionList(self, evt):
    #     # add report types to list
    #     if evt.GetEventObject().IsChecked():
    #         self.terminalFunctionsList.append(evt.GetEventObject().GetLabel())
    #     elif evt.GetEventObject().IsChecked() == False:
    #         self.terminalFunctionsList.remove(evt.GetEventObject().GetLabel())

    def cbSelectFarFieldFeaturesList(self, evt):
        # add report types to list
        if evt.GetEventObject().IsChecked():
            self.farfieldFeaturesList.append(evt.GetEventObject().GetLabel())
        elif evt.GetEventObject().IsChecked() == False:
            self.farfieldFeaturesList.remove(evt.GetEventObject().GetLabel())


    def getReportList(self):
        return self.modalFeaturesList, self.terminalFeaturesList, self.farfieldFeaturesList
        # return self.modalFeaturesList, self.modalFunctionsList, \
        #         self.terminalFeaturesList, self.terminalFunctionsList, self.farfieldFeaturesList


    def applyLoadedProjectSettings(self, PC):
        pass

