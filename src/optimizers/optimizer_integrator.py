##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/opimizers/optimizer_integrator.py'
#   Main class for managing the optimizer hooks
#   Scripts are NOT written or read to file in this class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: Novmber 29, 2024
##--------------------------------------------------------------------\

import os
import wx
import pandas as pd
import numpy as np

import time


#debug
import project.config.antennaCAT_config as c
DEBUG = False#c.DEBUG

OPT_SELECTION = c.OPT_SELECTION
OPT_RULES = c.OPT_RULES
OPT_PSO_BASIC = c.OPT_PSO_BASIC
OPT_PSO_PYTHON = c.OPT_PSO_PYTHON
OPT_PSO_QUANTUM = c.OPT_PSO_QUANTUM
OPT_CAT_SWARM = c.OPT_CAT_SWARM
OPT_SAND_CAT_SWARM = c.OPT_SAND_CAT_SWARM
OPT_CAT_QUANTUM = c.OPT_CAT_QUANTUM
OPT_CHICKEN_SWARM = c.OPT_CHICKEN_SWARM
OPT_CHICKEN_2015 = c.OPT_CHICKEN_2015
OPT_CHICKEN_QUANTUM = c.OPT_CHICKEN_QUANTUM
OPT_MULTI_GLODS = c.OPT_MULTI_GLODS
OPT_BAYESIAN = c.OPT_BAYESIAN
OPT_GRID_SWEEP = c.OPT_GRID_SWEEP
OPT_RANDOM_SWEEP = c.OPT_RANDOM_SWEEP

SM_RADIAL_BASIS_FUNC = c.SM_RADIAL_BASIS_FUNC
SM_GAUSSIAN_PROCESS = c.SM_GAUSSIAN_PROCESS
SM_KRIGING = c.SM_KRIGING
SM_POLY_REGRESSION = c.SM_POLY_REGRESSION
SM_POLY_CHAOS_REGRESSION = c.SM_POLY_CHAOS_REGRESSION
SM_KNN = c.SM_KNN
SM_DECISION_TREE_REGRESSION = c.SM_DECISION_TREE_REGRESSION





import helper_func.fileIO_helperFuncs as fIO
# from optimizers.data_interpretation. 
## PSO/SWARM optimizers
from optimizers.PSO_PYTHON.controller_PSO_PYTHON import CONTROLLER_PSO_PYTHON
from optimizers.PSO_BASIC.controller_PSO_BASIC import CONTROLLER_PSO_BASIC
from optimizers.CAT_SWARM.controller_CAT_SWARM import CONTROLLER_CAT_SWARM
from optimizers.SAND_CAT_PYTHON.controller_SAND_CAT import CONTROLLER_SAND_CAT
from optimizers.CHICKEN_SWARM.controller_CHICKEN_SWARM import CONTROLLER_CHICKEN_SWARM
from optimizers.CHICKEN_SWARM_2015.controller_CHICKEN_SWARM_2015 import CONTROLLER_CHICKEN_SWARM_2015
## QUANTUM INSPIRED PSO
from optimizers.PSO_QUANTUM.controller_PSO_QUANTUM import CONTROLLER_PSO_QUANTUM
from optimizers.CAT_SWARM_QUANTUM.controller_CAT_QUANTUM import CONTROLLER_CAT_SWARM_QUANTUM
from optimizers.CHICKEN_SWARM_QUANTUM.controller_CHICKEN_QUANTUM import CONTROLLER_CHICKEN_QUANTUM
#BAYESIAN OPTIMIZERS
from optimizers.BAYESIAN.controller_BAYESIAN import CONTROLLER_BAYESIAN
## MULTI GLODS
from optimizers.MULTI_GLODS.controller_MULTI_GLODS import CONTROLLER_MULTI_GLODS
#from optimizers.GLODS_SURROGATE.controller_GLODS_SURROGATE import CONTROLLER_GLODS_SURROGATE
## OTHERS
from optimizers.SWEEP_PYTHON.controller_SWEEP import CONTROLLER_SWEEP

#SURROGATE MODELS (customization to be added)
from optimizers.surrogate_models.RBF_network import RBFNetwork
from optimizers.surrogate_models.gaussian_process import GaussianProcess
from optimizers.surrogate_models.kriging_regression import Kriging
from optimizers.surrogate_models.polynomial_regression import PolynomialRegression
from optimizers.surrogate_models.polynomial_chaos_expansion import PolynomialChaosExpansion
from optimizers.surrogate_models.KNN_regression import KNNRegression
from optimizers.surrogate_models.decision_tree_regression import DecisionTreeRegression


# selection methods
from optimizers.selection.selection import Selection


# data processing
from data_processing.processing_integrator import DataProcessingIntegrator

class OptimizerIntegrator():
    def __init__(self, parent, DC, PC, SO): 
        # class maybe created before config uploaded
        self.parent = parent #for GUI feed back to status page - might remove
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.OO = None #optimizer object. to be selcted 
        self.DP = None # data processing obj. to be selected

        # directories
        self.optimizerDir = None #optimizer directory
        self.dataDir = None #default loc for saving generated data
        self.optimizerScriptPath = None

        # data collection
        self.saveLogBool = True
        self.saveOptimizerData = False
        self.saveReportData = False # this edits the script into the EM software

        # optimizer vals
        self.controllableParams = pd.DataFrame({}) # detected/applied vals from page_optimizer
        self.optimizerParams = pd.DataFrame({}) #params processed for the optimizer
        self.targetMetrics = None # class var so not called once per loop
        self.decimalPrecision = 4 # the default for numbers after the decimal

        self.simRunningBool = False
        self.dataProcessingDone = True

        self.enableRunBool = False
        self.firstRunBool = True
        self.pauseBool = False
        self.stopBool = False

        self.F = None
        self.xNames = []
        self.x = []
        self.stepCounter = 0
        self.simulationCounter = 0

        self.best_eval = 999
        self.iteration = 0
        self.soln_x_vals = []
        self.soln_y_vals = []


        self.objectiveFuncCounter = 0

####################################################
# Interfacing with GUI
####################################################
    
    #general output
    def updateStatusText(self, t):
        self.parent.updateStatusText(t)

    #parsing optimizer vals into display:
    def formatOptimizerDataForDisplay(self, dataLst, paramLst):
        t = "\n"
        ctr = 0
        # print("optimizer_integrator.py")
        # print("paramLst")
        # print(paramLst)
        # print("dataLst")
        # print(dataLst)

        for d in dataLst:
            # tmpStr = str(paramLst[ctr]) + ":\t" + str(d[0]) + "\n"
            tmpStr = str(paramLst[ctr]) + ":\t" + str(d) + "\n"
            t = t + tmpStr
            ctr = ctr + 1

        self.updateStatusText(t)

####################################################
# Setting objects in class memory
####################################################

    def setControllableParams(self, df):
        self.controllableParams = df

    def getControllableParams(self):
        return self.controllableParams
    
    def setOptimizerParams(self,df):
        self.optimizerParams = df

    def getOptimizerParams(self):
        return self.optimizerParams

    def setDataCollectionBools(self, saveLog, saveOptimizer, saveData):
        self.saveLogBool = saveLog
        self.saveOptimizerData = saveOptimizer
        self.saveReportData = saveData
    
    def setPrecision(self, n):
        self.decimalPrecision = int(n)
    
    def getPrecision(self):
        return self.decimalPrecision



####################################################
# Reset vars
####################################################

    # full reset
    def resetVariables(self):
        msg = "resetting simulation"
        self.updateStatusText(msg)

        self.simRunningBool = False
        self.dataProcessingDone = True

        self.enableRunBool = False
        self.firstRunBool = True
        self.pauseBool = False
        self.stopBool = False

        self.F = None
        self.xNames = []
        self.x = []
        self.stepCounter = 0
        self.simulationCounter = 0

    def resetVarsSimError(self):
        msg = "resetting simulation for error recovery"
        self.updateStatusText(msg)

        self.simRunningBool = False
        self.dataProcessingDone = True

        self.enableRunBool = True
        self.firstRunBool = False
        self.pauseBool = False
        self.stopBool = False

####################################################
# Optimizer selection, management, and setup
####################################################

    def selectOptimizer(self, optimizerSelection):
        return self.selectOptimizerIntegrator(optimizerSelection)
    

    def selectOptimizerIntegrator(self,optimizerSelection):
        #reset the bools
        self.enableRunBool = False
        self.firstRunBool = True
        self.pauseBool = False
        self.stopBool = False

        # set up optimizer integrator
        self.OO = self.setOptimizer(optimizerSelection)
        self.setupOptimizerIntegration(optimizerSelection) #setup save directories + SO dirs

        #select the data processor based on the current EM software
        emSoftware = self.PC.getSimulationSoftware()
        self.DP = DataProcessingIntegrator(emSoftware)

        msg = "optimizer set to " + str(optimizerSelection)
        return msg
    

    def setOptimizer(self, optimizerSelection):
        # this is called FIRST by the 'select' button on the panels in the 
        # optimzier notebook to create a CONTROLLER
        # panel_XYZ -> notebook_optimizer -> page_optimizer-> THIS CLASS

        # if a SURROGATE MODEL is used, this will be called a SECOND time
        # by the previously created CONTROLLER. A new controller will be created, 
        # but only to get the optimizer class (via the controller), and have the 
        # optimizer settings unpacked into the df that will be used
        # this DOES NOT need to be called repeatedly, because the class and the df
        # can be REUSED to reset the optimizer when it needs to be created


        if optimizerSelection == OPT_SELECTION:
           OO = Selection(self.DC, self.PC, self.SO)
        elif optimizerSelection == OPT_RULES:
        #    OO = Rules(self.DC, self.PC, self.SO)
            OO = None
        elif optimizerSelection == OPT_PSO_BASIC:
            OO = CONTROLLER_PSO_BASIC(self)
        elif optimizerSelection == OPT_PSO_PYTHON:
            OO = CONTROLLER_PSO_PYTHON(self)
        elif optimizerSelection == OPT_PSO_QUANTUM:
           OO = CONTROLLER_PSO_QUANTUM(self)
        elif optimizerSelection == OPT_CAT_SWARM:
            OO = CONTROLLER_CAT_SWARM(self)
        elif optimizerSelection == OPT_SAND_CAT_SWARM:
            OO = CONTROLLER_SAND_CAT(self)
        elif optimizerSelection == OPT_CAT_QUANTUM:
            OO = CONTROLLER_CAT_SWARM_QUANTUM(self)
        elif optimizerSelection == OPT_CHICKEN_SWARM:
            OO = CONTROLLER_CHICKEN_SWARM(self)
        elif optimizerSelection == OPT_CHICKEN_2015:
            OO = CONTROLLER_CHICKEN_SWARM_2015(self)
        elif optimizerSelection == OPT_CHICKEN_QUANTUM:
            OO = CONTROLLER_CHICKEN_QUANTUM(self)
        elif optimizerSelection == OPT_MULTI_GLODS:
           OO = CONTROLLER_MULTI_GLODS(self)
        elif optimizerSelection == OPT_BAYESIAN:
            OO = CONTROLLER_BAYESIAN(self)
        # these two are the same controller. 
        # same optimizer, different panel options.
        elif optimizerSelection == OPT_GRID_SWEEP:
           OO = CONTROLLER_SWEEP(self)
        elif optimizerSelection == OPT_RANDOM_SWEEP:
           OO = CONTROLLER_SWEEP(self)
        else:
            print("ERROR: unrecognized optimizer object: " + str(optimizerSelection))
            print("check selection in optimizer_integrator.py")
          
        # NOTE: SURROGATE panel doesn't have it's own selection because it's using other optimizers
        # 

        return OO


    def check_model_approximator(self, SURROGATE_MODEL, INIT_SAMPLES, optimizerParams, is_internal_optimizer=False):
        # SURROGATE MODEL VARS
        # inbuilt error correction here. This will be cleaned up in later versions after some testing.

        sm_approx = None
        noError =  False  # must be changed to True
        errMsg = "no surrogate model approximator selected" #will be overwritten


        if SURROGATE_MODEL == SM_RADIAL_BASIS_FUNC:
            # Radial Basis Function Kernel
            # set kernel specific vars
            # if is_internal_optimizer == False:
            RBF_KERNEL = optimizerParams['rbf_kernel'][0]#options: 'gaussian', 'multiquadric'
            RBF_EPSILON = float(optimizerParams['rbf_epsilon'][0]) 
            # else:
            #     RBF_KERNEL = optimizerParams['sm_rbf_kernel'][0]#options: 'gaussian', 'multiquadric'
            #     RBF_EPSILON = float(optimizerParams['sm_rbf_epsilon'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if RBF_KERNEL in ['gaussian', 'multiquadric']:
                pass
            else:
                RBF_KERNEL = 'gaussian'
                msg = "ERROR: unknown RBF kernel. Defaulting to gaussian RBF kernel"
                self.updateStatusText(msg)
           
            # setup
            sm_approx = RBFNetwork(kernel=RBF_KERNEL, epsilon=RBF_EPSILON)  
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES, RBF_KERNEL)

        elif SURROGATE_MODEL == SM_GAUSSIAN_PROCESS:
            # Gaussian Process vars
            # set kernel specific vars
            # if is_internal_optimizer == False:
            GP_NOISE = float(optimizerParams['gp_noise'][0])#1e-10
            GP_LENGTH_SCALE = float(optimizerParams['gp_length_scale'][0]) 
            # else:
            #     GP_NOISE = float(optimizerParams['sm_gp_noise'][0])#1e-10
            #     GP_LENGTH_SCALE = float(optimizerParams['sm_gp_length_scale'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)

            sm_approx = GaussianProcess(length_scale=GP_LENGTH_SCALE,noise=GP_NOISE) 
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == SM_KRIGING:
            # Kriging vars
            # set kernel specific vars
            #if is_internal_optimizer == False:
            K_LENGTH_SCALE = float(optimizerParams['k_length_scale'][0])# 1.0
            K_NOISE = float(optimizerParams['k_noise'][0]) # 1e-10
            # else:
            #     K_LENGTH_SCALE = float(optimizerParams['sm_k_length_scale'][0])# 1.0
            #     K_NOISE = float(optimizerParams['sm_k_noise'][0]) # 1e-10               

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 2:
                INIT_SAMPLES = 2
                msg = "WARNING: a minimum number of 2 initial sample(s) must be used for this kernel. Setting minimum to 2."
                self.updateStatusText(msg)
   
            sm_approx = Kriging(length_scale=K_LENGTH_SCALE, noise=K_NOISE)
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == SM_POLY_REGRESSION:
            # Polynomial Regression vars
            # set kernel specific vars
            # if is_internal_optimizer == False:
            PR_DEGREE = int(optimizerParams['pr_degree'][0])
            # else:
            #     PR_DEGREE = int(optimizerParams['sm_pr_degree'][0])

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if PR_DEGREE < 1:
                PR_DEGREE = 1
                msg = "WARNING: a polynomial degree must be at least 1. Setting to 1."
                self.updateStatusText(msg)
           
            sm_approx = PolynomialRegression(degree=PR_DEGREE)
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == SM_POLY_CHAOS_REGRESSION:
            # Polynomial Chaos Expansion vars
            # set kernel specific vars
            # if is_internal_optimizer == False:
            PC_DEGREE = int(optimizerParams['pc_degree'][0])
            # else:
            #     PC_DEGREE = int(optimizerParams['sm_pc_degree'][0])

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if PR_DEGREE < 1:
                PR_DEGREE = 1
                msg = "WARNING: a polynomial degree must be at least 1. Setting to 1."
                self.updateStatusText(msg)

            sm_approx = PolynomialChaosExpansion(degree=PC_DEGREE)
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == SM_KNN:
            # KNN regression vars
            # set kernel specific vars
            # if is_internal_optimizer == False:
            KNN_WEIGHTS = optimizerParams['knn_weights'][0]#options: 'uniform', 'distance'
            KNN_N_NEIGHBORS = int(optimizerParams['knn_n_neighbors'][0]) 
            # else:
            #     KNN_WEIGHTS = optimizerParams['sm_knn_weights'][0]#options: 'uniform', 'distance'
            #     KNN_N_NEIGHBORS = int(optimizerParams['sm_knn_n_neighbors'][0]) 


            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if KNN_N_NEIGHBORS < 1:
                KNN_N_NEIGHBORS = 1
                msg = "WARNING: a minimum number of 1 neighbors must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if KNN_N_NEIGHBORS < INIT_SAMPLES:
                msg = "WARNING: it is suggested that the number of initial samples be equal to the number of neighbors. \n " +\
                    "This is not a fatal error, but the initial predictions may be incorrect or fail to \n " +\
                    "converge until after meeting the number of neighbors + 1"
            if KNN_WEIGHTS in ['uniform', 'distance']:
                pass
            else:
                KNN_WEIGHTS = 'uniform'
                msg = "ERROR: unknown KNN kernel. Defaulting to uniform KNN kernel"
                self.updateStatusText(msg)
           
            sm_approx = KNNRegression(n_neighbors=KNN_N_NEIGHBORS, weights=KNN_WEIGHTS)
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        elif SURROGATE_MODEL == SM_DECISION_TREE_REGRESSION:
            # Decision Tree Regression vars
            # set kernel specific vars
            # if is_internal_optimizer == False:
            DTR_MAX_DEPTH = int(optimizerParams['dtr_max_depth'][0]) 
            # else:
            #     DTR_MAX_DEPTH = int(optimizerParams['sm_dtr_max_depth'][0]) 

            # error correction (hardcoded for kernel)
            if INIT_SAMPLES < 1:
                INIT_SAMPLES = 1
                msg = "WARNING: a minimum number of 1 initial sample(s) must be used for this kernel. Setting minimum to 1."
                self.updateStatusText(msg)
            if DTR_MAX_DEPTH < 2:
                DTR_MAX_DEPTH = 2
                msg = "WARNING: the lowest max depth is 2. Setting max depth to 2."
                self.updateStatusText(msg)
          
            sm_approx = DecisionTreeRegression(max_depth=DTR_MAX_DEPTH)
            noError, errMsg = sm_approx._check_configuration(INIT_SAMPLES)

        return sm_approx, noError, errMsg
 


    def openSaved(self):
        # AKA import optimizer state


        # TODO
        #opens saved optimizer progress/settings from non-antennaCAT file
        #has more processing here. 
        # NOTE: no longer passing the path through multiple layers

        # 1) open file browser
        # 2) parse file as DF
        # 3) attempt import to optimizer (use try/except)
        # (self.OO.set_import_configuration(import_df))
        # 4) if works fine (might not be right, but it imported), then output message
        # 5) if didn't work, output message via popup to make it harder to ignore

        msg = "Coming Soon! Optimizer Import Checks are Being Finalized"
        wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
        
    
    def setOptimizerFromPC(self):
        # Setting from loaded project
        #called when antennaCAT project is loaded
        optimizerSelection = self.PC.getOptimizerSelection()
        #select the optimizer
        self.selectOptimizerIntegrator(optimizerSelection) 


    def exportOptimizerConfigs(self):
        # Export state
        #try:
        if self.iteration > 0:
            try:
                data = self.OO.get_export_configuration()
                data_df = pd.DataFrame(data)
                with wx.FileDialog(self, "Export optimizer state", wildcard="PKL (*.pkl)|*.pkl",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                    if fileDialog.ShowModal() == wx.ID_CANCEL:
                        return     # user cancelled
                    pathname = fileDialog.GetPath()
                    print(data_df)
                    data_df.to_pickle(pathname)
            except Exception as e:
                print("ERROR: optimizer_integrator.py export error")
                print(e)

        else:
            msg = "WARNING: Cannot export optimizer state before optimizer runs. \n" \
            "The optimizer can be paused and the current state saved at anytime."
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)



####################################################
# Run, pause, stop events
####################################################

    def enableRun(self):
        #run is not enabled until optimizer errors are handled
        self.enableRunBool = True


    def killSimulation(self):
        self.pauseBool = True
        msg = "pausing optimizer..."
        self.updateStatusText(msg)

        self.simRunningBool, noError = self.checkIfSimulationIsRunning()
        if self.simRunningBool == False:
            msg = "no simulation thread to terminate"
            self.updateStatusText(msg)
            return

        msg = "terminating running simulation..."
        self.updateStatusText(msg)
        # kill simulation
        self.SO.terminateRunningProcess()
        msg = "simulation terminated"
        self.updateStatusText(msg)
        self.postSimulationCleanup()

    def pause(self):
        msg = "pause button hit"
        self.updateStatusText(msg)
        self.pauseBool = True

        
    def stop(self): 
        msg = "stop button hit"
        self.updateStatusText(msg)
        self.stopBool = True
        self.stopLooping()


    def stopLooping(self):
        msg = "initiating stop process"
        self.updateStatusText(msg)

    def run(self):
        msg = "run button hit"
        self.updateStatusText(msg)

        if self.enableRunBool == False:
            msg = "running is not enabled until after optimizer is configured"
            self.updateStatusText(msg)
            return
        
        if self.stopBool == True:
            dlg = wx.MessageDialog(None, "Do you want to start a new run?",'Optimizer',wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                # self.stopBool = False
                # self.pauseBool = False
                self.resetVariables()
                msg = "begining new run"
                self.updateStatusText(msg)
                self.stopLooping()
                self.firstRunBool = True

        if self.pauseBool == True:
            self.stopBool = False
            self.pauseBool = False
            msg = "resuming previous run"
            self.updateStatusText(msg)
        
        self.loop()


######################################################
# new run setup
#######################################################

    def firstRun(self):
        msg = "initiating first run setup"
        self.updateStatusText(msg)

        #unpack params into something that can be used by the optimizer
        #try:
        self.F, self.targetMetrics = self.OO.unpackOptimizerParameters(self.optimizerParams, self.processDataAndRunSimulation)
        #except:
            #msg = "ERROR in optimizer_integrater. unable to unpack parameters for the controller"


        
        self.stepCounter = 0
        self.simulationCounter = 0
        self.firstRunBool = False

        self.xNames = []
        # get names of params optimizer is controlling
        for p in self.controllableParams:
            if self.controllableParams[p][4] == False: # only get params that arent being ignored        
                self.xNames.append(p)     

######################################################
# last run cleanup
#######################################################
                
    def postSimulationCleanup(self, includeComment=True):
        if includeComment == True:
            msg = "checking for lock files..."
            self.updateStatusText(msg)
        # remove lock file if it exists
        lockFilepath = self.SO.getLockFile()
        if DEBUG == True:
            self.updateStatusText("checking lockfilePath in optimizer_integrator:")
            self.updateStatusText(str(lockFilepath))
            # print("checking lockfilePath in optimizer_integrator:")
            # print(lockFilepath)
        if os.path.isfile(lockFilepath) == True:
            #print("attempting to remove lockfile")
            self.updateStatusText("attempting to remove lockfile")
            os.remove(lockFilepath)
            if os.path.isfile(lockFilepath) == False:
                self.updateStatusText("lockfile removed")
            
        # reset bools here if unusual behavior is noticed
        # but resetting bools will restart the simulation
        # self.resetVariables()

######################################################
# main looping functions
#######################################################

    def loop(self):
        #check if first loop - setup if needed
        if self.firstRunBool == True:
            self.firstRun()
            msg = "starting optimizer"
            self.updateStatusText(msg)

        #check for stop conditions
        #user
        if self.pauseBool == True:
            msg = "optimizer paused"
            self.updateStatusText(msg)
            return
        if self.stopBool == True:
            msg = "stopping optimizer"
            self.updateStatusText(msg)
            self.postSimulationCleanup()
            return
        #optimizer
        completeBool = self.OO.checkOptimizerComplete()
        if completeBool == True:
            msg = "optimizer converged"
            self.updateStatusText(msg)
            self.stopBool = True
            self.stopLooping() #only event not triggered from UI
            self.updateSolutionValues()
            self.postSimulationCleanup()
            return

        #check if simulation is still running
        # TODO: more specific error recovery from abnormal termination to reset bools
        self.simRunningBool, noError = self.checkIfSimulationIsRunning()
        if noError == False:
            self.postSimulationCleanup(False) #delete lock file
        
        #decide if process and enable step, or pass
        if self.simRunningBool == True:   
            if noError == False:            
                self.SO.terminateRunningProcess() # force kill simulation thread
                self.resetVarsSimError()
                self.simRunningBool, noError = self.checkIfSimulationIsRunning() # check status
            #call SO and check for lock file (or whatever the EMsoftware might have)
            #if the lock file exists, sim is still running and things are fine
            
            ## The code below has been commented out because it always returns true and prevents the optimizers from running
            #  ansys 

            # if no lock file, there was probably an error                              
            # lockFilepath = self.SO.getLockFile()
            # if os.path.isfile(lockFilepath) == False:

                # self.SO.terminateRunningProcess() # force kill simulation thread
                # self.resetVarsSimError()

            wx.CallLater(3000, self.loop) #call 3 seconds later
        else:
            self.postSimulationCleanup(False)
            if self.dataProcessingDone == False:
                self.processDataFromFiles()
                # self.OO.setAllowUpdate(True)
            else:
                # ADDING THE ELSE HAS BEEN AN EDIT TO HELP WITH THE DOUBLE SIM PROBLEM
                self.optimizerStep()
            wx.CallLater(10, self.loop)
      
        
######################################################
# Optimizer step
#######################################################

    def optimizerStep(self): 
        # step through optimizer processing
        self.stepCounter = self.stepCounter + 1
        msg = "optimizer running step " + str(self.stepCounter)
        self.updateStatusText(msg)
        
        self.OO.step()

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        self.OO.callObjective()


#######################################################
# Post processing
#######################################################

    def processDataAndRunSimulation(self, x, numOutVars=2):

        noError = True
        #def processDataAndRunSimulation(self, parent, x):
        #inputs:
        #   parent: the parent class passed through
        #   x:  x vals current params in format [[x1], [x2], [x3]...]

    #try:
        # update script tempate
        self.updateOptimizerTemplate(x)
    #except Exception as e:
        # print("problem with root in optimizer_integrator.py, processDataAndRunSimulation()")
        # print("unable to update optimizer template")
        # print(e)
        noError = False
        #return self.F, noError



        try:
            #run simulation - this starts the simulation and disowns the thread
            self.runSimulation()  
        except Exception as e:
            print("problem with root in optimizer_integrator.py, processDataAndRunSimulation()")
            print("unable to run simulation")
            print(e)
            noError = False
        return self.F, noError

    def processDataFromFiles(self):
        
        #call to the processing class with helper funcs
        #inputs: none, uses default report names
        #output: returns values of parameters to optimizer 

        # self.dataProcessingDone = True # Moved this to later
        F_SHAPE = int(np.prod(np.shape(self.F))) #keep the size of F, but clear it
        
        self.F = np.zeros((F_SHAPE, 1))
        # first run has no data to process
        # return the zeros as a default
        if self.simulationCounter < 1:
            # self.OO.setAllowUpdate(True) #????
            return
        
        msg = "processing simulation data"
        self.updateStatusText(msg)

        # # call data processing funcs
        df = self.getDefaultOptimizerSimulationData()

        #HERE: all vals are now in an array
        #set vals to F(in order)

        try:
            #get num of entries for one category (everything has the same)
            numVals = len(df['s11'][0])


            self.F = []
            ctr = 0 #only works bc categories are grouped together
            
            for tm in self.targetMetrics[0]:
                if tm == "S_11":
                    valArr = float(df['s11'][0][ctr%numVals])
                elif tm == "Gain":
                    valArr = float(df['gain'][0][ctr%numVals])
                elif tm == "BW":
                    valArr = float(df['bw'][0][ctr%numVals])
                elif tm == "Directivity":
                    valArr = float(df['directivity'][0][ctr%numVals])
                elif tm == "Efficiency":
                    valArr = float(df['efficiency'][0][ctr%numVals])
                ctr = ctr +1
                self.F.append([valArr])
        except:
            print("ERROR: file not exported from EM simulation software correctly. attempting to force re-run simulation")
            print("if issue continues, you may need to restart the program.")
            print("A fix to this is in progress!")


        self.dataProcessingDone = True
            
          

    def updateOptimizerTemplate(self, x):
        #inputs: current parameter values x
        #       x vals are in the format [[x1], [x2], [x3]...]
        #outputs: none. saves script to template. uses default paths, etc

        # print("x in optimizer_integrator.updateOptimizerTemplate ")
        # print(x)

        ctr = 0
        lst = [] #array of format [[param, val, unit],[param, val, unit],[param, val, unit]....]
        for p in self.controllableParams:
            if self.controllableParams[p][4] == False: # only get params that arent being ignored             
                paramName = p
                paramVal = float(x[ctr]) #current value from optimizer
                paramUnit = self.controllableParams[p][1] # string unit
                lst.append([paramName, paramVal, paramUnit])
                ctr = ctr + 1

        # update parameters by passing in list of vals to change
        #print("update script template")
        self.updateScriptTemplate(lst, self.simulationCounter)
        self.x = x # for the log file


#######################################################
# Optimizer save funcs & directory management
#######################################################

    def setupOptimizerIntegration(self, optimizerSelection):
        #check for data and recursively create all dirs if not found
        baseDir = self.PC.getOptimizerDirectory()
        self.optimizerDir = os.path.join(baseDir, optimizerSelection)
        self.dataDir = os.path.join(self.optimizerDir, "data")
        if os.path.exists(self.dataDir) == False:
            os.makedirs(self.dataDir)
        fileExt = self.SO.getExpectedScriptFileExtension()
        self.optimizerScriptPath = os.path.join(self.optimizerDir, "optimizer_script"  + str(fileExt))
        # set the reports
        self.SO.useDefaultOptimizerReportSimulationOptions(self.dataDir)  

    def getOptimizerDir(self):
            #base optimizer dir
            return self.optimizerDir
    
    def getDataDir(self):
            #optimizer/data dir
            return self.dataDir
    
#######################################################
# integration with simulation object (SO)
#######################################################

    def updateScriptTemplate(self, lst, stpCtr):
        # print("STEP COUNTER!!!!!")
        # print(stpCtr)

        if stpCtr < 1: 
            # the first step includes design and simulation scripts
            # design could be either instructions to build the CAD model, 
            #   or to open a project.
            # the simulation script could be simulation setup or no setup
            designScript = self.DC.getDesignScript()
            # COMMENTED OUT JUST FOR THE RFID RUN
            simulationScript = self.DC.getSimulationScript() #simulation setup
            # print("STEP CTR 0")
            # print(simulationScript)

            # # change the paramters by list 
            # self.SO.clearParamEditTemplateScript() #clear previous script
            # self.SO.paramEditTemplateGen(lst) #add param change for 1 iteration of changes
            # # add save to param edit script. then don't save after reports (so don't have to clear reports)
            # self.SO.addSaveToParamEditScript()
            
            # # get param edit script
            # paramEditScript = self.SO.getParamEditTemplateScript()
                
            # # report and export do not need to be updated bc they used the same file names
            # # report creations script (simulation, but without the sim setup)
            # reportScript = self.DC.getReportsScript()
            # # get report export script
            # reportExportScript = self.SO.getReportEditTemplateScript()


            # #write all of them out to file to read 
            # with open("designScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(designScript)

            # with open("simulationScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(simulationScript)

            # with open("paramEditScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(paramEditScript)

            # with open("reportScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(reportScript)

            # with open("reportExportScript.txt", "w") as file:
            #     file.writelines(reportExportScript)

            # # time.sleep(25)

            # # combine scripts
            # #use the spacer to see where each script ends - debug only. 
            # script = designScript + simulationScript + paramEditScript + reportScript + reportExportScript

        else:
            #change the design script to be an 'open project' script. (this works for all options, new and imported)
            projectPath = self.SO.getEMSoftwareProjectName()
            # print("project path in optimizer_integrator.py")
            # print(projectPath)
            self.SO.useOpenProjectDesignScript(projectPath) #resets design template object
            designScript = self.DC.getDesignScript()
            # no sim setup
            simulationScript = ['\n'] #must be a list

            if self.saveReportData == True:
                msg = "report data will be saved in the next code update. toggle in updateScriptTemplate in optimizer_integrator call"
                self.updateStatusText(msg)


            # # change the paramters by list 
            # self.SO.clearParamEditTemplateScript() #clear previous script
            # self.SO.paramEditTemplateGen(lst) #add param change for 1 iteration of changes
            # # add save to param edit script. then don't save after reports (so don't have to clear reports)
            # self.SO.addSaveToParamEditScript()
            
            # # get param edit script
            # paramEditScript = self.SO.getParamEditTemplateScript()
                
            # # report and export do not need to be updated bc they used the same file names
            # # report creations script (simulation, but without the sim setup)
            # reportScript = self.DC.getReportsScript()
            # # get report export script
            # reportExportScript = self.SO.getReportEditTemplateScript()


            # #write all of them out to file to read 

            # with open("designScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(designScript)

            # # with open("simulationScript_"+str(stpCtr)+".txt", "w") as file:
            # #     file.writelines(simulationScript)

            # with open("paramEditScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(paramEditScript)

            # with open("reportScript_"+str(stpCtr)+".txt", "w") as file:
            #     file.writelines(reportScript)

            # with open("reportExportScript.txt", "w") as file:
            #     file.writelines(reportExportScript)

            # # time.sleep(25)

            # # combine scripts
            # #use the spacer to see where each script ends - debug only. 
            # script = designScript + paramEditScript + reportScript + reportExportScript


        # change the paramters by list 
        self.SO.clearParamEditTemplateScript() #clear previous script
        self.SO.paramEditTemplateGen(lst) #add param change for 1 iteration of changes
        # add save to param edit script. then don't save after reports (so don't have to clear reports)
        self.SO.addSaveToParamEditScript()
        
        # get param edit script
        paramEditScript = self.SO.getParamEditTemplateScript()
            
        # report and export do not need to be updated bc they used the same file names
        # report creations script (simulation, but without the sim setup)
        reportScript = self.DC.getReportsScript()
        # get report export script
        reportExportScript = self.SO.getReportEditTemplateScript()


        # #write all of them out to file to read the 

        # with open("designScript_"+str(stpCtr)+".txt", "w") as file:
        #     file.writelines(designScript)

        # with open("simulationScript_"+str(stpCtr)+".txt", "w") as file:
        #     file.writelines(simulationScript)

        # with open("paramEditScript_"+str(stpCtr)+".txt", "w") as file:
        #     file.writelines(paramEditScript)

        # with open("reportScript_"+str(stpCtr)+".txt", "w") as file:
        #     file.writelines(reportScript)

        # with open("reportExportScript.txt", "w") as file:
        #     file.writelines(reportExportScript)

        # time.sleep(25)

        # combine scripts
        #use the spacer to see where each script ends - debug only. 
        script = designScript + simulationScript + paramEditScript + reportScript + reportExportScript

        # print("SCRIPT")
        # print(script)

        # export script to file
        self.saveScriptFile(script, self.optimizerScriptPath)
        

    def runSimulation(self):

        self.dataProcessingDone = False
        self.simRunningBool = True
        # self.OO.setAllowUpdate(False)

        self.updateConvergenceData()
        self.saveConvergenceData()
        self.updateLogFiles()

        self.simulationCounter = self.simulationCounter + 1

        # print summary to GUI
        self.formatOptimizerDataForDisplay(self.x, self.xNames)
        self.formatOptimizerDataForDisplay(self.F, self.targetMetrics[0])


        msg = "now running simulation #" + str(self.simulationCounter)
        self.updateStatusText(msg)

        if os.path.isfile(self.optimizerScriptPath) == False:
            print("ERROR: optimizer_integrator.py. optimizer script does not exist")
            print("attempted filepath: ", self.optimizerScriptPath)
            return       
        
        # call the simulation through SO
        self.SO.runWithScriptAndExit(pth=self.optimizerScriptPath)
        #print("run simulation call disabled in optimizer_integrator.py for debug")


    def checkIfSimulationIsRunning(self):
        return self.SO.getSimulationRunningBool()


    def saveScriptFile(self, script, filename):
        fIO.writeOut(filename, script)
        msg = "file exported to " + str(filename)
        self.updateStatusText(msg)


####################################################
# integration with data processing object (DP)
####################################################

    def getDefaultOptimizerSimulationData(self):
        # input: list of target metrics ([gain, s11, bandwidth, etc..])
        # output: dataframe from data processing class
        dataDir = self.dataDir #directory for the saved data
        #dataDir = "C:\\Users\\LCLin\\Desktop\\test2\\output" #for testing format only
        df = self.DP.getDefaultOptimizerSimulationData(dataDir)
        return df


####################################################
# Log files:
# * saveStepToLogFile(): save data out to textfile
####################################################

    def updateLogFiles(self):
        # write out to log
        if self.saveLogBool == True:
            self.saveStepToLogFile(self.simulationCounter, self.xNames, self.x, self.targetMetrics[0], self.F)
        if self.saveOptimizerData == True:
            # write out the x, F metrics 
            #call to GET the data to write out - these are the lists internal to the optimizer
            # TODO
            pass


    def saveStepToLogFile(self, stpCtr, xNames, x, FNames, F, filename="optimizer-log.txt"):
        pathname = os.path.join(self.dataDir, filename)
        #x: parameters from optimizer
        #F: processed data values

        xStr = ' '.join((str(xn) + ",") for xn in xNames)
        fStr = ' '.join((str(fn) + ",") for fn in FNames)
        xVal = ' '.join((str(xv).strip('[]') + ",") for xv in x)
        fVal = ' '.join((str(fv).strip('[]') + ",") for fv in F)

        headerFormat = "step," + str(xStr) + str(fStr) + "\n"   
        line = str(stpCtr) + "," + str(xVal) + str(fVal) + "\n"

        with open(pathname, "a") as f:
            if stpCtr == 1:
                #write header before vars
                f.write(headerFormat)
            f.write(line)
    
######################################################
# optimizer data collection
######################################################

    def updateConvergenceData(self):
        iter, eval = self.OO.get_convergence_data()
        if (eval < self.best_eval) and (eval != 0):
            self.best_eval = eval
        self.iteration = iter

    def saveConvergenceData(self):
        filename = "convergence-log.csv"
        pathname = os.path.join(self.dataDir, filename)
        line = str(self.iteration) + "," + str(self.best_eval) + "\n"
        with open(pathname, "a") as f:
            f.write(line)

    def updateSolutionValues(self):
        self.soln_x_vals = self.OO.get_optimized_soln()
        self.soln_y_vals = self.OO.get_optimized_outs()
######################################################
# optimizer data collection
######################################################

    # def updateConvergenceData(self):
    #     iter, eval = self.OO.get_convergence_data()
    #     if (eval < self.best_eval) and (eval != 0):
    #         self.best_eval = eval
    #     self.iteration = iter

    # def saveConvergenceData(self):
    #     filename = "convergence-log.csv"
    #     pathname = os.path.join(self.dataDir, filename)
    #     line = str(self.iteration) + "," + str(self.best_eval) + "\n"
    #     with open(pathname, "a") as f:
    #         f.write(line)

    # def updateSolutionValues(self):
    #     self.soln_x_vals = self.OO.get_optimized_soln()
    #     self.soln_y_vals = self.OO.get_optimized_outs()