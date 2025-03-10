##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   'gui_setup.py'
#   placeholder file for mini-restructure to incorporate:
#       * splash screen during setup
#       * AntennaCAT cache file loading
#       * transistion to stand-alone .exe
#    
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 30, 2024
##--------------------------------------------------------------------\

import sys
import wx
import wx.adv
import wx.lib.mixins.inspection as wit

sys.path.insert(0, './gui')
from gui.gui_main.gui_main import GFrame


sys.path.insert(0, './project/')
import project.config.antennaCAT_config as c
ANTENNACAT_SPLASH_FILE = c.ANTENNACAT_SPLASH_FILE

class AntennaCATGUI():
    def __init__(self, parent, title):
        app = wit.InspectableApp()

        #splash img
        # bmap = wx.Bitmap(ANTENNACAT_SPLASH_FILE, wx.BITMAP_TYPE_PNG)
        # img = wx.Bitmap.ConvertToImage(bmap)
        # img = img.Scale(735, 400, wx.IMAGE_QUALITY_HIGH)
        # splash = wx.adv.SplashScreen(img.ConvertToBitmap(), wx.adv.SPLASH_CENTER_ON_SCREEN|wx.adv.SPLASH_TIMEOUT, 
        #              15000,  None, -1, wx.DefaultPosition, wx.DefaultSize,wx.BORDER_NONE)
        # splash.Show()


        # while splash screen is up, create the GUI
        GUIFrame = GFrame(parent, title=title)

        # show the GUI and destory the splash when thread is free
        GUIFrame.Show()
        #splash.Destroy()

        # add app to the main loop to keep program open
        app.MainLoop()
