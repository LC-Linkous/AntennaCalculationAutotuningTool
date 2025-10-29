##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   'main.py'
#   Main class for AntennaCAT. 
#       This is the default entry point for the program
#    
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: October 29, 2025
##--------------------------------------------------------------------\

import logging
from gui.antennacat_gui import AntennaCATGUI
from project.config.antennaCAT_config import ANTENNACAT_VERSION


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='antennaCAT.log',
        filemode='a' # Use 'a' to append logs, 'w' to overwrite
    )


def main():
       setup_logging()
       logger = logging.getLogger(__name__)
       logger.info("AntennaCAT application started.")
       t = "AntennaCAT " + str(ANTENNACAT_VERSION)
       anCATgui = AntennaCATGUI(None, title=t)
       logger.info("AntennaCAT application closed.")    


if __name__ == '__main__':
    main()

