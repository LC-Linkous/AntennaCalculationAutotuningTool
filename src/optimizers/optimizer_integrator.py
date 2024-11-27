##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/opimizers/optimizer_integrator.py'
#   Main class for managing the optimizer hooks
#   Scripts are NOT written or read to file in this class
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu), Jonathan Lundquist
#   Last update: December 29, 2023
##--------------------------------------------------------------------\

import os
import wx
import pandas as pd
import numpy as np


#debug
import project.config.antennaCAT_config as c
DEBUG = c.DEBUG


import helper_func.fileIO_helperFuncs as fIO
# from optimizers.data_interpretation. 
## PSO/SWARM optimizers
from optimizers.PSO_PYTHON.controller_PSO_PYTHON import CONTROLLER_PSO_PYTHON
from optimizers.PSO_BASIC.controller_PSO_BASIC import CONTROLLER_PSO_BASIC
from optimizers.CAT_SWARM.controller_CAT_SWARM import CONTROLLER_CAT_SWARM
from optimizers.SAND_CAT_PYTHON.controller_SAND_CAT import CONTROLLER_SAND_CAT
from optimizers.CHICKEN_SWARM.controller_CHICKEN_SWARM import CONTROLLER_CHICKEN_SWARM
## QUANTUM INSPIRED PSO
from optimizers.PSO_QUANTUM.controller_PSO_QUANTUM import CONTROLLER_PSO_QUANTUM
from optimizers.CAT_SWARM_QUANTUM.controller_CAT_QUANTUM import CONTROLLER_CAT_SWARM_QUANTUM
from optimizers.CHICKEN_SWARM_QUANTUM.controller_CHICKEN_QUANTUM import CONTROLLER_CHICKEN_QUANTUM
#BAYESIAN OPTIMIZERS
from optimizers.BAYESIAN.controller_BAYESIAN import CONTROLLER_BAYESIAN
## MULTI GLODS
from optimizers.MULTI_GLODS.controller_GLODS import CONTROLLER_GLODS
#from optimizers.GLODS_SURROGATE.controller_GLODS_SURROGATE import CONTROLLER_GLODS_SURROGATE
## OTHERS
from optimizers.SWEEP_PYTHON.controller_SWEEP import CONTROLLER_SWEEP


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
        if optimizerSelection == "SELECTION":
           OO = Selection(self.DC, self.PC, self.SO)
        elif optimizerSelection == "RULES":
        #    OO = Rules(self.DC, self.PC, self.SO)
            OO = None
        elif optimizerSelection == "PSO_BASIC":
            OO = CONTROLLER_PSO_BASIC(self)
        elif optimizerSelection == "PSO_PYTHON":
            OO = CONTROLLER_PSO_PYTHON(self)
        elif optimizerSelection == "PSO_QUANTUM":
           OO = CONTROLLER_PSO_QUANTUM(self)
        elif optimizerSelection == "CAT_SWARM":
            OO = CONTROLLER_CAT_SWARM(self)
        elif optimizerSelection == "SAND_CAT_SWARM":
            OO = CONTROLLER_SAND_CAT(self)
        elif optimizerSelection == "CAT_QUANTUM":
            OO = CONTROLLER_CAT_SWARM_QUANTUM(self)
        elif optimizerSelection == "CHICKEN_SWARM":
            OO = CONTROLLER_CHICKEN_SWARM(self)
        elif optimizerSelection == "CHICKEN_QUANTUM":
            OO = CONTROLLER_CHICKEN_QUANTUM(self)
        elif optimizerSelection == "GLODS":
           OO = CONTROLLER_GLODS(self)
        elif optimizerSelection == "BAYESIAN":
            OO = CONTROLLER_BAYESIAN(self)
        elif optimizerSelection == "SWEEP":
           OO = CONTROLLER_SWEEP(self)
        else:
            print("ERROR: non recognized optimizer object: " + str(optimizerSelection))
            print("check selection in optimizer_integrator.py")

        return OO



    def openSaved(self, pth):
        #opens saved optimizer progress/settings from non-antennaCAT file
        #has more processing here. 
        pass
    
    
    def setOptimizerFromPC(self):
        # Setting from loaded project
        #called when antennaCAT project is loaded
        optimizerSelection = self.PC.getOptimizerSelection()
        #select the optimizer
        self.selectOptimizerIntegrator(optimizerSelection) 


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

        #unpack params into something that can be used by multiGLODS
        self.F, self.targetMetrics = self.OO.unpackOptimizerParameters(self.optimizerParams, self.processDataAndRunSimulation)

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
            print("checking lockfilePath in optimizer_integrator:")
            print(lockFilepath)
        if os.path.isfile(lockFilepath) == True:
            print("attempting to remove lockfile")
            os.remove(lockFilepath)
            
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
            msg = "beginning optimizer"
            self.updateStatusText(msg)

        #check for stop conditions
        #user
        if self.pauseBool == True:
            msg = "pausing..."
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

        try:
            # update script tempate
            self.updateOptimizerTemplate(x)
        except Exception as e:
            print("problem with root in optimizer_integrator.py, processDataAndRunSimulation()")
            print("unable to update optimizer template")
            print(e)
            noError = False


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
            print("ERROR: file not exported from EM simulaiton software correctly. attempting to force re-run simulation")
            print("if issue continues. you may need to restart the program.")
            print("A fix to this is in progress!")


        self.dataProcessingDone = True
            
          

    def updateOptimizerTemplate(self, x):
        #inputs: current parameter values x
        #       x vals are in the format [[x1], [x2], [x3]...]
        #outputs: none. saves script to template. uses default paths, etc

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
       
        if stpCtr < 1: 
            # the first step includes design and simulation scripts
            # design could be either instructions to build the CAD model, 
            #   or to open a project.
            # the simulation script could be simulation setup or no setup
            designScript = self.DC.getDesignScript()
            simulationScript = self.DC.getSimulationScript() #simulation setup
        else:
            #change the design script to be an 'open project' script.
            projectPath = self.SO.getEMSoftwareProjectName()
            self.SO.useOpenProjectDesignScript(projectPath) #resets design template object
            designScript = self.DC.getDesignScript()
            # no sim setup
            simulationScript = []

            if self.saveReportData == True:
                msg = "report data will be saved in the next code update. toggle in updateScriptTemplate in optimizer_integrator call"
                self.updateStatusText(msg)

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

        # combine scripts
        #use the spacer to see where each script ends - debug only. 
        script = designScript + simulationScript + paramEditScript + reportScript + reportExportScript

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