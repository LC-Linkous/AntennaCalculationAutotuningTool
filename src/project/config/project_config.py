##--------------------------------------------------------------------\
#   Antenna Calculation andAutotuning Tool
#   './src/config/project_config.py'
#   Class for storing user input project values and error checking
#   This class handles everything needed for manipulating the program/files
#   at the topmost levels
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\
import os
import pandas as pd
import project.config.antennaCAT_config as c

OUTPUT_DIR = c.OUTPUT_DIR
SCRIPTS_DIR = c.SCRIPTS_DIR
BATCH_OUTPUT = c.BATCH_OUTPUT
TMP_DIR = c.TMP_DIR
OPTIMIZER_DIR = c.OPTIMIZER_DIR

class ProjectConfiguration:
    def __init__(self):

        #simulation software information
        self.simulationSoftwarePath = None  
        self.simulationSoftware = None
        self.numSimulationLicenses = None
        self.useSingleLicense = False
        self.defaultEMSoftware = None
        #optimizer memory
        self.optimizer = None
        # path information
        ## the project directory
        self.projectDir = None
        self.projectResultsDir = None
        self.projectName = None 
        self.emSoftwareProjectName = None
        self.fullPath = None # this is the path as returned from the browser. used for err check
        #script file information
        # design and loop scripts have been broken up into several scripts
        # 1) the model design
        self.designConfigCreated = False  ## the design creation/3D model script created
        self.designScriptCreated = False
        self.designScriptPath = None #full file path to the antenna script
        self.designFileName = None# DESIGN_NAME
        # 2) the simulation script (setup sim)
        ## the simulation script - primarily used for setup
        self.simulationConfigCreated = False## bool for checking that there's a configuration
        self.simulationImportedConfigCreated = False
        self.simulationScriptPath = None #full file path
        self.simulationFileName = None#SIMULATION_NAME
        # 3) editing parameters
        self.parameterEditConfigCreated = False## bool for checking that there's a configuration
        self.parameterEditScriptPath = None #full file path
        self.parameterEditFileName = None #PARAM_EDIT_NAME
        # 4) run reports + export
        ## reports generated from simulation - no simulation, just creates the reports
        self.reportExportConfigCreated = False## bool for checking that there's a configuration
        self.reportExportPath = None #full file path
        self.reportExportFileName = None#REPORT_EXPORT_NAME

        #user options
        self.ImportedProjectPath = None
        self.importedDXFPath = None

        #for layers - if F&F, then NO conductor
        self.useCalculatedConductor = False
        self.useImportedConductor = False

        self.designOptions = pd.DataFrame({})
        self.designOptions["antenna_generator"] = pd.Series(False) 
        self.designOptions["custom_conductor"] = pd.Series(False)
        self.designOptions["custom_layers"] = pd.Series(False)
        self.designOptions["custom_shape"] = pd.Series(False)
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(False)


    #################################################
    # simulation software information
    #################################################

    def setSimulationSoftwarePath(self, p=None):
        self.simulationSoftwarePath = p
    
    def getSimulationSoftwarePath(self):
        return self.simulationSoftwarePath
    
    def setSimulationSoftware(self, s):
        self.simulationSoftware = s
        
    def getSimulationSoftware(self):
        return self.simulationSoftware
    
    def setNumSimulationLicenses(self, s):
        self.numSimulationLicenses = s

    def getNumSimulationLicenses(self):
        return self.numSimulationLicenses
    
    def setUseSingleLicense(self, s):
        self.useSingleLicense = s

    def getUseSingleLicense(self):
        return self.useSingleLicense
    
    def setDefaultEMSoftware(self, s):
        self.defaultEMSoftware = s

    def getDefaultEMSoftware(self):
        return self.defaultEMSoftware    

    def setOptimizerSelection(self, s):
        self.optimizer = s
    
    def getOptimizerSelection(self):
        return self.optimizer

    #################################################
    # Root Project/Dir paths
    # project directory: this is where the antennaCAT project file is saved
    # results directory: this is where everything generated from the project is saved
    # project name: includes the file extension, but not the path
    #################################################

    def setFullPath(self, s):
        self.fullPath = s

    def getFullPath(self):
        return self.fullPath

    def setProjectDirectory(self, s):
        self.projectDir = s

    def getProjectDirectory(self):
        return self.projectDir
    
    def setResultsDirectory(self, s):
        self.projectResultsDir = s

    def getResultsDirectory(self):
        return self.projectResultsDir
   
    def setProjectName(self, n):
        self.projectName = n

    def getProjectName(self):
        #antenna cat project name
        #includes file extension
        return self.projectName     
    
    def setEMSoftwareProjectName(self, n):
        self.emSoftwareProjectName = n
    
        # self.PC.getResultsDirectory() + name

    def getEMSoftwareProjectName(self):
        return self.emSoftwareProjectName
   
    def setDefaultScriptPaths(self, desFile, simFile, parFile, repFile):
        #these are the files used by antennaCAT for automating simulations
        # must always point to the most recent save dir
        self.designFileName = desFile
        self.simulationFileName = simFile
        self.parameterEditFileName = parFile
        self.reportExportFileName = repFile
        p = self.getScriptDirectory()
        self.designScriptPath = os.path.join(p, self.designFileName)
        self.simulationScriptPath = os.path.join(p, self.simulationFileName)
        self.parameterEditScriptPath = os.path.join(p, self.parameterEditFileName)
        self.reportExportPath = os.path.join(p, self.reportExportFileName)
    
    #################################################
    # standard project export paths
    # used for automated exports and looping
    #################################################
   
    def getOutputDirectory(self):
        d = os.path.join(self.projectResultsDir, OUTPUT_DIR)
        self.checkDirAndCreate(d)
        return d  

    def getScriptDirectory(self):
        d = os.path.join(self.projectResultsDir, SCRIPTS_DIR)
        self.checkDirAndCreate(d)
        return d  
    
    def getBatchDirectory(self):
        d = os.path.join(self.projectResultsDir, BATCH_OUTPUT)
        self.checkDirAndCreate(d)
        return d    

    def getTmpDirectory(self):
        d = os.path.join(self.projectResultsDir, TMP_DIR)
        self.checkDirAndCreate(d)
        return d  
    
    def getOptimizerDirectory(self):
        d = os.path.join(self.projectResultsDir, OPTIMIZER_DIR)
        self.checkDirAndCreate(d)
        return d  

    def checkDirAndCreate(self, dirPath):
        if os.path.exists(dirPath) == False:
            os.makedirs(dirPath)

    ################################################
    # Set bools for control flow of scripting
    #  handles some compatability issues
    ################################################

    def useAntennaGeneratorDesign(self):
        # this new choice takes priority over everything
        # even though the custom_x options can use the calculator
        # this allows for a switch back to 'calculator only' versions
        self.designOptions["antenna_generator"] = pd.Series(True)
        self.designOptions["custom_conductor"] = pd.Series(False)
        self.designOptions["custom_layers"] = pd.Series(False)
        self.designOptions["custom_shape"] = pd.Series(False)
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(False)
        self.setDesignConfigBool(True)

    def useCustomConductorDesign(self):
        #the other custom options can chain, so don't change those
        #but we're not using the antenna calculator
        self.designOptions["antenna_generator"] = pd.Series(False)
        self.designOptions["custom_conductor"] = pd.Series(True)
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(False)
        self.setDesignConfigBool(True)

    def useCustomLayersDesign(self, useCalculatedConductor, useImportedConductor):
        #the other custom options can chain, so don't change those
        #but we're not using the antenna calculator
        self.useCalculatedConductor = useCalculatedConductor
        self.useImportedConductor = useImportedConductor
        self.designOptions["antenna_generator"] = pd.Series(False) 
        self.designOptions["custom_layers"] = pd.Series(True) # bools are only checked when this is true
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(False)
        self.setDesignConfigBool(True)

    def useCustomShapeDesign(self):
        #the other custom options can chain, so don't change those
        #but we're not using the antenna calculator
        self.designOptions["antenna_generator"] = pd.Series(False) 
        self.designOptions["custom_shape"] = pd.Series(True)
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(False)

    def useImportedScriptDesign(self):
        self.designOptions["antenna_generator"] = pd.Series(False) 
        self.designOptions["custom_conductor"] = pd.Series(False)
        self.designOptions["custom_layers"] = pd.Series(False)
        self.designOptions["custom_shape"] = pd.Series(False)
        self.designOptions["import_script"] = pd.Series(True)
        self.designOptions["import_project"] = pd.Series(False)
        self.setDesignConfigBool(True)

    def useImportedProjectDesign(self):
        self.designOptions["antenna_generator"] = pd.Series(False) 
        self.designOptions["custom_conductor"] = pd.Series(False)
        self.designOptions["custom_layers"] = pd.Series(False)
        self.designOptions["custom_shape"] = pd.Series(False)
        self.designOptions["import_script"] = pd.Series(False)
        self.designOptions["import_project"] = pd.Series(True)
        self.setDesignConfigBool(True)


    def getDesignOptionBoolByName(self, designOpt):
        return self.designOptions[str(designOpt)][0]    
    
    def getAntennaGeneratorBoolean(self):
        return self.designOptions["antenna_generator"][0]    

    def getCustomConductorBoolean(self):
        return self.designOptions["custom_conductor"][0]    

    def getCustomLayersBoolean(self):
        return self.designOptions["custom_layers"][0]

    def getCustomShapeBoolean(self):
        return self.designOptions["custom_shape"][0]    

    def getImportScriptBoolean(self):
        return self.designOptions["import_script"][0]    

    def getImportProjectBoolean(self):
        return self.designOptions["import_project"][0]
    
    def checkDesignCreated(self):
        #check if any DESIGN is set
        # not included:
        # customShape - doesnt stand alone
        self.designConfigCreated  = False
        a = self.getAntennaGeneratorBoolean()
        b = self.getCustomConductorBoolean()
        c = self.getCustomLayersBoolean()
        d = self.getImportScriptBoolean()
        e = self.getImportProjectBoolean()
        if (a) or (b) or (c) or (d) or (e):
            self.setDesignConfigBool(True)
        return self.designConfigCreated 

     
    #################################################
    # 
    #   Paths  for handling input method type
    #################################################
      
    def setImportedScriptBoolean(self, b):
        self.useImportedScript = b 
    
    def getImportedScriptBoolean(self):
        return self.useImportedScript

    #imported
    def setImportedProjectPath(self, n):
        self.importedProjectPath = str(n)
    
    def getImportedProjectPath(self):
        return self.importedProjectPath
    
    # DXF import
    def setImportedDXFPath(self, n):
        self.importedProjectPath = n
    
    def getImportedDXFPath(self):
        return self.importedProjectPath
    
    #################################################
    # setters and getters for script creation
    # bools - has script been created?
    # path - full file path
    #################################################

    # design 
    def setDesignConfigBool(self, b):
        self.designConfigCreated = b

    def getDesignConfigBool(self):
        return self.designConfigCreated
    
    def setDesignScriptCreatedBool(self, b):
        self.designScriptCreated = b

    def getDesignScriptCreatedBool(self):
        return self.designScriptCreated

    def getDesignScriptPath(self):
        return self.designScriptPath
    
    # simulation 
    def setSimulationConfigBool(self, b):
        self.simulationConfigCreated = b

    def getSimulationConfigBool(self):
        return self.simulationConfigCreated

    def getSimulationScriptPath(self):
        return self.simulationScriptPath    

    def setImportedSimulationConfigBool(self, b):
        self.simulationImportedConfigCreated = b

    def getImportedSimulationConfigBool(self):
        return self.simulationImportedConfigCreated

    # parameter 
    def setParameterEditConfigBool(self, b):
        self.parameterEditConfigCreated = b

    def getParameterEditConfigBool(self):
        return self.parameterEditConfigCreated

    def getParameterEditScriptPath(self):
        return self.parameterEditScriptPath    

    # reports 
    def setReportExportConfigBool(self, b):
        self.reportExportConfigCreated = b

    def getReportExportConfigBool(self):
        return self.reportExportConfigCreated

    def getReportExportScriptPath(self):
        return self.reportExportPath    
    



#############################################
# clearing and reseting scripts
##############################################
    def resetDesignBool(self):
        self.setDesignConfigBool(False)
        self.setDesignScriptCreatedBool(False)

    def resetSimulationBool(self):
         self.setSimulationConfigBool(False)
         self.setImportedSimulationConfigBool(False)

    def resetParametersBool(self):
        self.setParameterEditConfigBool(False)

    def resetReportsBool(self):
        self.setReportExportConfigBool(False)
