##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/optimizer_panels/panel_parameterSummary.py'
#   Class 
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 15, 2023
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c

#directories

#static vars for cosmetic features
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ParameterSummaryPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(320, 300))
        self.parent = parent

        # widgets
        boxParametersSummary = wx.StaticBox(self, label="Parameter Summary")
        self.stParameterSummary = wx.TextCtrl(boxParametersSummary, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH|wx.BORDER_SUNKEN)
        font = wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Lucida Console")
        self.stParameterSummary.SetFont(font)
        self.clearParameterSummaryText()

        # sizer
        boxParametersSummarySizer = wx.BoxSizer(wx.VERTICAL)
        boxParametersSummarySizer.AddSpacer(10)
        boxParametersSummarySizer.Add(self.stParameterSummary, 1, wx.ALL|wx.EXPAND, border=10)
        boxParametersSummary.SetSizer(boxParametersSummarySizer)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxParametersSummary, 1, wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(pageSizer)


    def setParameterSummaryText(self, numPar, namePar, lbArr, ubArr):
        txt = "\n"
        try:
            numTxt = "# Controllable Input Parameters: " + str(int(numPar)) + "\n"
        except:
            numTxt = "# Controllable Input Parameters: " + str(numPar) + "\n"

        mutableTxt = "# Selected Parameters: " + str(len(lbArr)) + "\n"
        lbTxt = ""
        ubTxt = ""
        
        if lbArr == []:
            pass
        else:
            ctr = 0
            for lb in lbArr:
                tmpTxt = str(namePar[ctr]) 
                lbTxt = lbTxt + f"{str(tmpTxt)[:25]:<25}{str(lb):<15}\n" # + tmpTxt  + "\n"
                ctr = ctr + 1

            ctr = 0
            for ub in ubArr:
                tmpTxt = str(namePar[ctr]) #+ ": \t\t" + str(ub)
                ubTxt = ubTxt + f"{str(tmpTxt)[:25]:<25}{str(ub):<15}\n" # + tmpTxt  + "\n"#+ tmpTxt  + "\n"
                ctr = ctr + 1

        txt = numTxt + \
            "\n" + \
            mutableTxt+ \
            "\n" + \
            "Lower Bounds Set: \n" + \
            lbTxt + "\n" + \
            "Upper Bounds Set: \n" + \
            ubTxt + "\n"
        self.stParameterSummary.SetLabel(txt)


    def clearParameterSummaryText(self):
        self.stParameterSummary.SetLabel("")
        self.setParameterSummaryText("", [], [], [])

