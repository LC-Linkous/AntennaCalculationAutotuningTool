##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   'main.py'
#   Main class for AntennaCAT. 
#       This is the default entry point for the program
#    
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 30, 2024
##--------------------------------------------------------------------\

from gui.antennacat_gui import AntennaCATGUI


def main():

       anCATgui = AntennaCATGUI(None, title='AntennaCAT v2024.0')
 
if __name__ == '__main__':
    main()

