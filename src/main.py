##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   'main.py'
#   Main class for AntennaCAT. 
#       This is the default entry point for the program
#    
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 5, 2025
##--------------------------------------------------------------------\

from gui.antennacat_gui import AntennaCATGUI
from project.config.antennaCAT_config import ANTENNACAT_VERSION

def main():
       
       t = "AntennaCAT " + str(ANTENNACAT_VERSION)
       anCATgui = AntennaCATGUI(None, title=t)
 
if __name__ == '__main__':
    main()

