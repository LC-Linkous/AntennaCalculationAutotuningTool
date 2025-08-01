##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_optimizer/notebook_optimizer/notebook_optimizer.py'
#   Notebook for selecting and managing optimizers
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 10, 2025
##--------------------------------------------------------------------\

import os
import wx

from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_simulationSettings import SolutionSettingsPanel
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_SWEEP import SWEEPPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_GLODS import GLODSPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_SWARM import SWARMPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_QUANTUM import QUANTUMPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_BAYESIAN import BAYESIANPage
from gui.page_optimizer.notebook_optimizer.optimizer_panels.panel_SURROGATE import SURROGATEPage


import project.config.antennaCAT_config as c

#static vars for cosmetic features
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
#dictionary for calculator integration (not enough vals to move yet)
ANTENNA_TYPE_DICT = c.ANTENNA_TYPE_DICT


class OptimizerNotebook(wx.Notebook):
    def __init__(self, parent, DC, PC, SO):
        wx.Notebook.__init__(self, parent=parent, size=(390, -1))
        self.parent = parent #parent used for sizer layouts in level above
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        

        # these pages are being grouped/consolidated to make navigation easier

        self.page_simulation = SolutionSettingsPanel(self, self.DC, self.PC)
        self.page_SWARM = SWARMPage(self, self.DC, self.PC, self.SO)
        self.page_QUANTUM = QUANTUMPage(self, self.DC, self.PC, self.SO)
        self.page_GLODS = GLODSPage(self, self.DC, self.PC, self.SO)
        self.page_BAYESIAN = BAYESIANPage(self, self.DC, self.PC, self.SO)
        self.page_SWEEP = SWEEPPage(self, self.DC, self.PC, self.SO)
        self.page_SURROGATE=SURROGATEPage(self, self.DC, self.PC, self.SO)


        self.AddPage(self.page_simulation, "Simulation Setup")
        self.AddPage(self.page_SWARM, "Swarm Based")
        self.AddPage(self.page_QUANTUM, "Quantum Inspired")
        self.AddPage(self.page_GLODS, "MultiGLODS")
        self.AddPage(self.page_BAYESIAN, "Bayesian")
        self.AddPage(self.page_SWEEP, "Sweep and Random")
        self.AddPage(self.page_SURROGATE, "Surrogate Optimization")
        
        


#######################################################
# Status update to main page
#######################################################
          
    def updateStatusText(self, t):
        self.parent.updateStatusText(t)

#######################################################
# Button Events
#######################################################

    def btnRunClicked(self):
        self.parent.btnRunClicked()

    def btnStopClicked(self):
        self.parent.btnStopClicked()

    def btnOpenClicked(self):
        #called from panel_OPTIMIZERNAME
        self.parent.btnOpenClicked()
    
    def btnSelectClicked(self, optimizerName, noError=True):
        self.parent.btnSelectClicked(optimizerName, noError)

    def btnExportClicked(self):
        self.parent.btnExportClicked()


#######################################################
# Getters
#######################################################


#######################################################
# Page Events
#######################################################

    def parameterSummaryUpdate(self, numControllable, paramInput):
        self.page_SWARM.parameterSummaryUpdate(numControllable, paramInput)
        self.page_QUANTUM.parameterSummaryUpdate(numControllable, paramInput)       
        self.page_GLODS.parameterSummaryUpdate(numControllable, paramInput)
        self.page_BAYESIAN.parameterSummaryUpdate(numControllable, paramInput)
        self.page_SWEEP.parameterSummaryUpdate(numControllable, paramInput)
        self.page_SURROGATE.parameterSummaryUpdate(numControllable, paramInput)


    def updateSimulationSettingsBoxes(self):
        self.page_simulation.updateAutoGenValues()
        


    def getDataCollectionBools(self):
        return self.page_simulation.getDataCollectionBools()