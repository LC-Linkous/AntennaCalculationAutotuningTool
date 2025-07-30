##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/project_configuration/panel_simulation.py'
#   Class for project settings - project simulation looping/view options
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 16, 2025
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

#static vars for cosmetic features
INPUT_BOX_WIDTH = 50
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class PrecisionNotebookPage(wx.Panel):
    def __init__(self, parent, DC):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        #self.PC = PC
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)


        boxPrecision = wx.StaticBox(self, label='Numeric Precision')
        
        
        # default units
        # dropdown, just mm for now
        lblUnit = wx.StaticText(boxPrecision, label="Default Unit:")
        unitTypes = ['mm']
        self.unitDropDown = wx.ComboBox(boxPrecision, choices=unitTypes, style=wx.CB_READONLY) #, size=(INPUT_BOX_WIDTH, 20)
        self.unitDropDown.SetValue(unitTypes[0])

        # Calculated value precision - for the calculator values
        # label and text box. 4 after decimal is default
        # lblCalcPrecision = wx.StaticText(boxPrecision, label="Calculator Decimal Precision:")
        # self.fieldCalcPrecision = wx.TextCtrl(boxPrecision, value="", size=(INPUT_BOX_WIDTH, 20))
        # self.fieldCalcPrecision.SetValue("4")


        # optimizer value precision 
        # label and text box. 4 after the decimal is default
        lblOptPrecision = wx.StaticText(boxPrecision, label="Optimizer Decimal Precision:")
        self.fieldOptPrecision = wx.TextCtrl(boxPrecision, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldOptPrecision.SetValue("4")



        boxInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxInputLeft = wx.BoxSizer(wx.VERTICAL)
        boxInputRight = wx.BoxSizer(wx.VERTICAL)
        
        boxInputLeft.Add(lblUnit, 0, wx.ALL|wx.EXPAND, border=7)
        #boxInputLeft.Add(lblCalcPrecision, 0, wx.ALL|wx.EXPAND, border=7)
        boxInputLeft.Add(lblOptPrecision, 0, wx.ALL|wx.EXPAND, border=7)

        boxInputRight.Add(self.unitDropDown, 0, wx.ALL|wx.EXPAND, border=3)
        #boxInputRight.Add(self.fieldCalcPrecision, 0, wx.ALL|wx.EXPAND, border=3)
        boxInputRight.Add(self.fieldOptPrecision, 0, wx.ALL|wx.EXPAND, border=3)


        boxInputSizer.Add(boxInputLeft, 0, wx.ALL|wx.EXPAND,border=15)
        boxInputSizer.Add(boxInputRight, 0, wx.ALL|wx.EXPAND,border=15)


        boxPrecision.SetSizer(boxInputSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxPrecision, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)


    def setNumericPrecisionSettings(self):
        try:
            unitdd = self.unitDropDown.GetValue()
            
        except:
            unitdd = 'mm'

        self.DC.setDefaultUnits(unitdd)


        try:
            numPrecis = int(self.fieldOptPrecision.GetValue())
        except:
            numPrecis = 4
            # todo, error message

        self.DC.setNumericalPrecision(numPrecis)



    def applyLoadedProjectSettings(self):
        # don't need to set any class vars bc these are only saved with a button
        # based on what is currently in the widget.
        unitval = self.DC.getDefaultUnits()
        decVal = int(self.DC.getNumericalPrecision())

        self.unitDropDown.SetValue(str(unitval))
        self.fieldOptPrecision.SetValue(str(decVal))