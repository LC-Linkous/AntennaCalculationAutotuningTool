##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   'main.py'
#   Main class for project
#    
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import wx
import wx.lib.mixins.inspection as wit
from gui.gui_main.gui_main import GFrame


def main():
 
        app = wit.InspectableApp()
        GUIFrame = GFrame(None, title='AntennaCAT v2024.0')
        GUIFrame.Show()
        app.MainLoop()


if __name__ == '__main__':
    main()

# to update dependencies in requirements.txt:
# for i in $(pip list -o | awk 'NR > 2 {print $1}'); do pip install -U $i; done && pip freeze > requirements.txt
# updating pip:
# python.exe -m pip install --upgrade pip