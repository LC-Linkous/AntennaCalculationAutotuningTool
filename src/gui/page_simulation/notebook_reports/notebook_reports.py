##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_simulation/notebook_reports/notebook_reports.py'
#   Class for project settings
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_simulation.notebook_reports.panel_reportsModal import ReportsModal
from gui.page_simulation.notebook_reports.panel_reportsFarField import ReportsFarField
from gui.page_simulation.notebook_reports.panel_reportsTerminal import ReportsTerminal
from gui.page_simulation.notebook_reports.panel_dataTable import ReportsDataTable
from gui.page_simulation.notebook_reports.panel_reportsAntennaParams import ReportsAntennaParams

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ReportsNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent, size=(-1, 325))
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
       
        self.page_reportModal = ReportsModal(self)
        self.page_reportFarField = ReportsFarField(self)
        self.page_dataTable = ReportsDataTable(self)
        self.page_reportTerminal = ReportsTerminal(self)
        self.page_antennaParams = ReportsAntennaParams(self)

        self.AddPage(self.page_reportModal, "Modal Solution")
        self.AddPage(self.page_reportTerminal, "Terminal Solution") 
        self.AddPage(self.page_reportFarField, "Far Field")
        self.AddPage(self.page_dataTable, "Data Table")
        self.AddPage(self.page_antennaParams, "Antenna Parameters")              


    def getTerminalReportList(self):
        return self.page_reportTerminal.getReportList()
    
    def getFarFieldReportList(self):
        return self.page_reportFarField.getReportList()

    def getModalReportList(self):
        return self.page_reportModal.getReportList()

    def getDataTableList(self):
        return self.page_dataTable.getReportList()
    
    def getAntennaParamsTableList(self):
        return self.page_antennaParams.getReportList()
          

    def applyLoadedProjectSettings(self, PC):
        self.page_reportModal.applyLoadedProjectSettings(PC)
        self.page_reportTerminal.applyLoadedProjectSettings(PC)
        self.page_reportFarField.applyLoadedProjectSettings(PC)
        self.page_dataTable.applyLoadedProjectSettings(PC)
        self.page_antennaParams.applyLoadedProjectSettings(PC)
        




