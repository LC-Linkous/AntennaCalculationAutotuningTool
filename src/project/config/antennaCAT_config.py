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
ANTENNACAT_EXE = False  #update to TRUE to use the exe path configs

ANTENNACAT_VERSION = "2025.1.1" #W11 patch


# GUI visuals
## default frame/panel sizes
WIDTH = 1300
HEIGHT = 810
PANEL_HEIGHT = 450
PANEL_WIDTH = 400
SIDEBAR_COLOR ='Thistle'
#pale_turquoise = wx.Colour(175, 238, 238) 
robin_egg_blue = wx.Colour(176, 224, 230) #Not an eyesore
light_blue = wx.Colour(190, 238, 230)
antennaCAT_default_blue = wx.Colour(190, 220, 220) #'Light Blue', but a little warmer
MAIN_BACKGROUND_COLOR =  antennaCAT_default_blue
GREY_BACKGROUND_COLOR = wx.Colour(234, 234, 234)
ALTERNATE_COLORS = ['Medium Goldenrod','Pale Green', 'Light Green', 'Light Steel Blue']
DEFAULT_COLORS = ['blue','orange','green','red','purple','brown','pink','grey',
                  'olive','cyan']

#media
ANTENNACAT_SPLASH_FILE = os.path.join('src','media','antennaCAT-icons','splashscreen_2024.png')
ANTENNACAT_ICON_FILE = os.path.join('src','media','antennaCAT-icons','transparent-antennaCAT-icon.png')
#".//src//media//antennaCAT-icons//transparent-antennaCAT-icon.png"
ANTENNACAT_LOGO_FILE =os.path.join('src','media','antennaCAT-icons','transparent-antennaCAT-logo.png')
#".//src//media//antennaCAT-icons//transparent-antennaCAT-logo.png"
ANTENNACAT_NEW_PROJECT_FILE = os.path.join('src','media','antennaCAT-icons','new_project_text.png')
ANTENNACAT_OPEN_PROJECT_FILE = os.path.join('src','media','antennaCAT-icons','open_project_text.png')


DESIGN_REPLICATION_CIRCULAR_LOOP = os.path.join('src','media','design-images','design-circular-loop.png')
DESIGN_REPLICATION_DIPOLE = os.path.join('src','media','design-images','design-dipole.png')
DESIGN_REPLICATION_E = os.path.join('src','media','design-images','design-E.png')
DESIGN_REPLICATION_COPLANAR_KEYHOLE = os.path.join('src','media','design-images','design-coplanar-keyhole.png')
DESIGN_REPLICATION_QUARTER_MONOPOLE = os.path.join('src','media','design-images','design-monopole.png')
DESIGN_REPLICATION_PLANAR_BOWTIE = os.path.join('src','media','design-images','design-planar-bowtie.png')
DESIGN_REPLICATION_RECTANGULAR_PATCH = os.path.join('src','media','design-images','design-rectangular-patch.png')
DESIGN_REPLICATION_SERPENTINE = os.path.join('src','media','design-images','design-serpentine-patch.png')
DESIGN_REPLICATION_SLOTTED_PATCH = os.path.join('src','media','design-images','design-slotted-patch.png')
DESIGN_REPLICATION_SQUARE_LOOP = os.path.join('src','media','design-images','design-square-loop.png')
DESIGN_REPLICATION_TWO_ARM_SQUARE_SPIRAL = os.path.join('src','media','design-images','design-two-arm-square-spiral.png')
DESIGN_REPLICATION_TWO_SIDED_BOWTIE = os.path.join('src','media','design-images','design-two-sided-bowtie.png')

# Static user-created PROJECT filepaths
## base directories
OUTPUT_DIR = "output"
SCRIPTS_DIR = os.path.join(OUTPUT_DIR, "scripts")
BATCH_OUTPUT = os.path.join(OUTPUT_DIR, "batch")
TMP_DIR = os.path.join(OUTPUT_DIR, "tmp")
OPTIMIZER_DIR =  os.path.join(OUTPUT_DIR, "optimizer")

## list for directories - used for error checking. If anything else is missing, there are other issues
DIR_LIST = {OUTPUT_DIR, SCRIPTS_DIR, TMP_DIR, OPTIMIZER_DIR}

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


# ANTENNACAT SOFTWARE PATHS
## EM hardcoded paths to main template and integrator folders
SOURCE_CODE_DIR = "./src"
ANSYS_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "ANSYS")
COMSOL_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "COMSOL")
CST_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "CST")
EMPIRE_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "EMPIRE")
FEKO_DIR = os.path.join(SOURCE_CODE_DIR, "simulation_integrator", "FEKO")


## AntennaCAT software files for cache and other user memory files
# starts from current working directory FOR NOW
# TODO: update toggle for the .exe version
if ANTENNACAT_EXE == True:
    #might need to load in file depending on how the .exe locs can be saved
    pass

else:
    #use current working directory
    ROOT_PATH = os.getcwd()


PROG_TEMP_PATH = os.path.join(ROOT_PATH, "tmp")
PROG_CONFIG_PATH = os.path.join(ROOT_PATH, "config")
PROG_DIR_LIST = {PROG_TEMP_PATH, PROG_CONFIG_PATH}

# cache files
PROG_RECENTS_FILE = os.path.join(PROG_TEMP_PATH, "recent_local.json") #project files
PROG_CONFIG_FILE = os.path.join(PROG_CONFIG_PATH, "config_local.json") #user and other program config
PROG_FILES_LIST = {PROG_RECENTS_FILE,PROG_CONFIG_FILE}


#SOFTWARE PATHS
## default software path for simulation softwares
# #name of the exe - this will be searched for with new project creation to get accurate paths
# KEEP THESE HERE FOR NOW
ANSYS_EXECUTABLE = "ansysedt.exe"
COMSOL_EXECUTABLE = None
CST_EXECUTABLE = None
EMPIRE_EXECUTABLE = None
FEKO_EXECUTABLE = None

# SHARED DICTIONARIES AND LISTS
## dictionary for calculator integration (not enough vals to move yet)
ANTENNA_TYPE_DICT = {
    '(calculate) Rectangular Patch': 'rectangular_patch',
    '(calculate) Half Wave Dipole': 'half_wave_dipole',
    '(calculate) Quarter Wave Monopole': 'quarter_wave_monopole',
    '(replicate) Rectangular Patch': 'rep_rectangular_patch',
    '(replicate) Half Wave Dipole': 'rep_half_wave_dipole',
    '(replicate) Quarter Wave Monopole': 'rep_quarter_wave_monopole',
    'PLANAR': 'placeholder',
    '(replicate) E': 'rep_E',
    '(replicate) Slotted Rectangular Patch': 'rep_slotted_r_patch',
    '(replicate) Dual Band Serpentine': 'rep_db_serpentine',
    '(replicate) Planar Bowtie': 'rep_planar_bowtie',
    '(replicate) Two Arm Square Spiral': 'rep_two_arm_square_spiral',
    'LOOP AND COIL': 'placeholder',
    '(replicate) Coplanar Keyhole': 'rep_coplanar_keyhole',
    '(replicate) Circular Loop': 'rep_circular_loop',
    '(replicate) Square Loop': 'rep_square_loop',
    'TWO SIDED': 'placeholder',
    '(replicate) Double Sided Bowtie': 'rep_double_sided_bowtie'
}





FEED_TYPE_DICT = {'microstrip': 'microstrip', 'probe': 'probe'}

#list of topologies that can be exported
CALCULATOR_EXPORT_LIST = ['rectangular_patch', 'rep_rectangular_patch']


# optimizer lists and combinations
# (some of these can be turned into dictionaties on their respective pages for modularity)
BASE_OPTIMIZERS_LIST =  ['PSO_basic', 'PSO_time_modulation', 'cat_swarm', 
                    'sand_cat_swarm', 'chicken_swarm', 'improved_chicken_2015',
                    'quantum_PSO','quantum_cat_swarm','quantum_chicken_swarm']


INTERNAL_OPTIMIZERS_LIST =   ['PSO_basic', 'PSO_time_modulation', 'cat_swarm', 
                    'sand_cat_swarm', 'chicken_swarm', 'improved_chicken_2015',
                    'quantum_PSO','quantum_cat_swarm','quantum_chicken_swarm']

SURROGATE_LIST =['Gaussian_Process', 'Kriging', 'Polynomial_Regression',
                            'Polynomial_Chaos_Expansion', 
                            'K_Nearest_Neighbors',  'Decision_Tree_Regression']
# RBF is unstable with small matrix value sin stress testing. it needs some extra error correction. 
# Works fine for Bayesian prediction

# ['Radial_Basis_Function', 'Gaussian_Process', 
#                           'Kriging', 'Polynomial_Regression',
#                             'Polynomial_Chaos_Expansion', 
#                             'K_Nearest_Neighbors',  'Decision_Tree_Regression']


BOUNDARY_LIST = ['Random', 'Reflection', 'Absorption', 'Invisible'] # getting dictionary keys throws an err

# names of optimizers used in integration/settings
OPT_SELECTION = "SELECTION"
OPT_RULES = "RULES"
OPT_PSO_BASIC = "PSO_BASIC"
OPT_PSO_PYTHON = "PSO_PYTHON"
OPT_PSO_QUANTUM = "PSO_QUANTUM"
OPT_CAT_SWARM = "CAT_SWARM"
OPT_SAND_CAT_SWARM = "SAND_CAT_SWARM"
OPT_CAT_QUANTUM = "CAT_QUANTUM"
OPT_CHICKEN_SWARM = "CHICKEN_SWARM"
OPT_CHICKEN_2015 = "CHICKEN_2015"
OPT_CHICKEN_QUANTUM = "CHICKEN_QUANTUM"
OPT_MULTI_GLODS = "MULTI_GLODS"
OPT_BAYESIAN = "BAYESIAN"
OPT_GRID_SWEEP = "GRID_SWEEP"
OPT_RANDOM_SWEEP = "RANDOM_SWEEP"

# # surrogate model approximator options
SM_RADIAL_BASIS_FUNC = "RADIAL_BASIS_FUNC"
SM_GAUSSIAN_PROCESS = "GAUSSIAN_PROCESS"
SM_KRIGING = "KRIGING"
SM_POLY_REGRESSION = "POLY_REGRESSION"
SM_POLY_CHAOS_REGRESSION = "POLY_CHAOS_REGRESSION"
SM_KNN = "KNN"
SM_DECISION_TREE_REGRESSION = "DECISION_TREE_REGRESSION"

