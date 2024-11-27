##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/config/antennaCAT_config.py'
#   Class for global vars for program functionality. 
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os #for dealing with windows/linux path differences
import wx

# debug messages printed to terminal
DEBUG = True


# GUI visuals
## default frame/panel sizes
WIDTH = 1300
HEIGHT =810
PANEL_HEIGHT = 450
PANEL_WIDTH = 400
SIDEBAR_COLOR ='Thistle'
#pale_turquoise = wx.Colour(175, 238, 238) 
robin_egg_blue = wx.Colour(176, 224, 230) #Not an eyesore
light_blue = wx.Colour(190, 238, 230)
antennaCAT_default_blue = wx.Colour(190, 220, 220) #'Light Blue', but a little warmer
MAIN_BACKGROUND_COLOR=  antennaCAT_default_blue
ALTERNATE_COLORS = ['Medium Goldenrod','Pale Green', 'Light Green', 'Light Steel Blue']
DEFAULT_COLORS = ['blue','orange','green','red','purple','brown','pink','grey',
                  'olive','cyan']

#media
ANTENNACAT_ICON_FILE = os.path.join('src','media','antennaCAT-icons','transparent-antennaCAT-icon.png')
#".//src//media//antennaCAT-icons//transparent-antennaCAT-icon.png"
ANTENNACAT_LOGO_FILE =os.path.join('src','media','antennaCAT-icons','transparent-antennaCAT-logo.png')
#".//src//media//antennaCAT-icons//transparent-antennaCAT-logo.png"
ANTENNACAT_NEW_PROJECT_FILE = os.path.join('src','media','antennaCAT-icons','new_project_text.png')
ANTENNACAT_OPEN_PROJECT_FILE = os.path.join('src','media','antennaCAT-icons','open_project_text.png')

DESIGN_REPLICATION_DIPOLE = os.path.join('src','media','design-images','design-dipole.png')
DESIGN_REPLICATION_RECTANGULAR_PATCH = os.path.join('src','media','design-images','design-rectangular-patch.png')
DESIGN_REPLICATION_E = os.path.join('src','media','design-images','design-E.png')
DESIGN_REPLICATION_SLOTTED_PATCH = os.path.join('src','media','design-images','design-slotted-patch.png')
DESIGN_REPLICATION_SERPENTINE = os.path.join('src','media','design-images','design-serpentine-patch.png')
DESIGN_REPLICATION_CIRCULAR_LOOP = os.path.join('src','media','design-images','design-circular-loop.png')

# Static project filepaths
## base directories
OUTPUT_DIR = "output"
SCRIPTS_DIR = os.path.join(OUTPUT_DIR, "scripts")
BATCH_OUTPUT = os.path.join(OUTPUT_DIR, "batch")
TMP_DIR = os.path.join(OUTPUT_DIR, "tmp")
OPTIMIZER_DIR =  os.path.join(OUTPUT_DIR, "optimizer")

SOURCE_CODE_DIR = "./src"
ANSYS_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "ANSYS")
COMSOL_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "COMSOL")
CST_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "CST")
EMPIRE_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "EMPIRE")
FEKO_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "FEKO")

## list for directories - used for error checking. If anything else is missing, there are other issues
DIR_LIST = {OUTPUT_DIR, SCRIPTS_DIR, TMP_DIR, OPTIMIZER_DIR}

## default names for logging and data saving
DEFAULT_OUTPUT_DIRECTORY = SOURCE_CODE_DIR + OUTPUT_DIR
#logs
SIMULATION_OUTPUT_LOG_NAME = "SIMULATION_SOFTWARE_LOG.log"
PLOT_HISTORY_LOG_NAME = "PLOT_HISTORY_LOG.log"
TUNING_HISTORY_LOG_NAME = "TUNING_HISTORY_LOG.log" #"TuningLog.txt"
BATCH_HISTORY_LOG_NAME = "BATCH_HISTORY_LOG.log"
#batch defaults
BATCH_SUMMARY_FILE = "batchSummary.txt"
BATCH_PLOT_HIST_FILE = "batchPlotHistory.txt"
#genetic defaults
##particle swarm optimization (PSO)
PSO_SAVE_FILE = "save.json"
PSO_SUMMARY_FILE = "organismSummary.txt"
GENETIC_CHECKPOINT_IMAGE = "outputImage.bmp"


#software paths
## default software path for simulation softwares
# #name of the exe - this will be searched for with new project creation to get accurate paths
# KEEP THESE HERE FOR NOW
ANSYS_EXECUTABLE = "ansysedt.exe"
COMSOL_EXECUTABLE = None
CST_EXECUTABLE = None
EMPIRE_EXECUTABLE = None
FEKO_EXECUTABLE = None

# Shared dictionaries and lists
## dictionary for calculator integration (not enough vals to move yet)
ANTENNA_TYPE_DICT = {
    '(calculate) Rectangular Patch': 'rectangular_patch',
    '(calculate) Half Wave Dipole': 'half_wave_dipole',
    '(calculate) Quarter Wave Monopole': 'quarter_wave_monopole',
    '(replicate) Rectangular Patch': 'rep_rectangular_patch',
    '(replicate) Half Wave Dipole': 'rep_half_wave_dipole',
    '(replicate) E': 'rep_E',
    '(replicate) Slotted Rectangular Patch': 'rep_slotted_r_patch',
    '(replicate) Dual Band Serpentine': 'rep_db_serpentine'
}


FEED_TYPE_DICT = {'microstrip': 'microstrip', 'probe': 'probe'}

#list of topologies that can be exported
CALCULATOR_EXPORT_LIST = ['rectangular_patch', 'rep_rectangular_patch', 'rep_E']



