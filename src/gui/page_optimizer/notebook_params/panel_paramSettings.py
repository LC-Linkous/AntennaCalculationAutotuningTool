##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_optimizer/notebook_params/panel_paramSettings.py'
#   Class for user controlled settings for param detection 
#       (rounding, %variation, etc)
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 7, 2023
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled

import project.config.antennaCAT_config as c
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class ParamSettingsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.defaultBoxWidth = 100
        self.defaultDelta = 1
        self.defaultVariation = 0.05

   